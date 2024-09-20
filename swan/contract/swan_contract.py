# ./swan/contract/swan_contract.py
import os
from functools import cached_property
from typing import Dict
import logging

from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware

from swan.common.constant import *
from swan.common.exception import SwanEnvironmentValueException
from swan.common.utils import get_contract_abi
from swan.object import PaymentResult


class SwanContract():

    def __init__(self, private_key: str, contract_info: dict):
        """ Initialize swan contract API connection.

        Args:
            private_key: private key for wallet.
            rpc_url: rpc url of swan chain for connection.
        """
        self.rpc_url = contract_info["rpc_url"]
        self.swan_token_contract_addr = contract_info["swan_token_contract_address"]
        self.payment_contract_addr = contract_info["payment_contract_address"]
        self.client_contract_addr = contract_info["client_contract_address"]

        self.account = None
        if private_key:
            self.account = Account.from_key(private_key)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.client_contract = self.w3.eth.contract(
            self.client_contract_addr,
            abi=get_contract_abi(CLIENT_CONTRACT_ABI)
        )

        self.payment_contract = self.w3.eth.contract(
            self.payment_contract_addr, 
            abi=get_contract_abi(PAYMENT_CONTRACT_ABI)
        )

        self.token_contract = self.w3.eth.contract(
            self.swan_token_contract_addr, 
            abi=get_contract_abi(SWAN_TOKEN_ABI)
        )

    @cached_property
    def max_priority_fee_percentage(self) -> float:
        return float(os.getenv("SWAN_SDK_PRIORITY_FEE_PERCENTAGE", 0.2))

    @cached_property
    def priority_fee_cap(self) -> float:
        return float(os.getenv("SWAN_SDK_MAX_PRIORITY_FEE_GWEI", 0.001))

    def _get_fee_per_gas(self) -> Dict[str, int]:
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']

        if not (0 <= self.max_priority_fee_percentage <= 1):
            raise SwanEnvironmentValueException(
                f"Priority fee percentage should be between 0 and 1: {self.max_priority_fee_percentage=}"
            )

        # Calculate 10% of the base fee
        priority_fee_percentage = int(base_fee * self.max_priority_fee_percentage)

        # Cap the priority fee at 0.001 gwei
        max_priority_fee_cap = Web3.to_wei(self.priority_fee_cap, "gwei")

        # Use the lower value between the percentage and the cap
        max_priority_fee_per_gas = min(priority_fee_percentage, max_priority_fee_cap)

        max_fee_per_gas = max(base_fee, self.w3.eth.gas_price) + max_priority_fee_per_gas

        return {
            "maxFeePerGas": max_fee_per_gas,
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
        }

    def get_public_wallet_address(self, private_key: str):
        """Get public wallet address from private key.

        Args:
            private_key: private key for wallet.

        Returns:
            str public wallet address.
        """
        try:
            account = Account.from_key(private_key)
            return account.address
        except:
            return None

    def hardware_info(self, hardware_id: int):
        """Retrieve hardware information from payment contract.

        Args:
            hardware_id: integer id of hardware, can be retrieve through Swan API.

        Returms:
            tuple[] hardware information, [name: str, price/hr: int, avaliability: bool]
            e.g. ['C1ae.medium', 1000000000000000000, True]
            see more detial in ./swan/contract/abi/paymentContract.json
        """
        # hardware_info = self.payment_contract.functions.hardwareInfo(hardware_id).call()
        hardware_info = self.client_contract.functions.hardwareInfo(hardware_id).call()
        return hardware_info
    
    def estimate_payment(self, hardware_id: int, duration: int):
        """Estimate required funds for lock_renvenue() function.

        Args:
            hardware_id: integer id of hardware, can be retrieve through Swan API.
            duration: duration in hours for space runtime.
        
        Returns:
            int estimated price in wei (18 decimal, 1e-18 swan).
            e.g. (price = 1000 wei, duration = 1 hr) -> 1000 wei
        """
        price = self.hardware_info(hardware_id)[1]
        return price * duration

    def get_allowance(self):
        """Get allowance of swan token for payment contract.

        Returns:
            int allowance in wei.
        """
        return self.token_contract.functions.allowance(
            self.account.address, 
            self.client_contract.address
        ).call()
    

    def submit_payment(
            self, 
            task_uuid: str, 
            hardware_id: int, 
            duration: int
        ) -> PaymentResult:
        """
        Submit payment for a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            hardware_id: id of cp/hardware configuration set
            duration: duration of service runtime (seconds).

        Returns:
            tx_hash
        """
        
        # first approve payment
        amount = int(self.estimate_payment(
            hardware_id=hardware_id, 
            duration=duration/3600  # duration in estimate_
        ))

        tx_hash_approve = None
        
        if self.get_allowance() < amount:
            logging.info(f"Approving payment for {amount} wei")
            tx_hash_approve = self.approve_payment(amount)
        else:
            logging.info(f"Allowance is enough for {amount} wei")

        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.client_contract.functions.submitPayment(
            task_uuid, 
            hardware_id, 
            duration
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            **self._get_fee_per_gas(),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        tx_hash = self.w3.to_hex(tx_hash)

        return PaymentResult(
            tx_hash_approve=tx_hash_approve,
            tx_hash=tx_hash, 
            amount=self.from_wei(amount)
        )
    

    def renew_payment(
            self, 
            task_uuid: str, 
            hardware_id: int, 
            duration: int
        ) -> PaymentResult:
        """
        Submit payment for task renewal

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            hardware_id: id of cp/hardware configuration set
            duration: duration of service runtime (seconds).

        Returns:
            tx_hash
        """
        
        # first approve payment
        amount = int(self.estimate_payment(
            hardware_id=hardware_id, 
            duration=duration/3600  # duration in estimate_
        ))

        tx_hash_approve = None
        if self.get_allowance() < amount:
            logging.info(f"Approving payment for {amount} wei")
            tx_hash_approve = self.approve_payment(amount)
        else:
            logging.info(f"Allowance is enough for {amount} wei")

        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.client_contract.functions.renewPayment(
            task_uuid, 
            hardware_id, 
            duration
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            **self._get_fee_per_gas(),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        tx_hash = self.w3.to_hex(tx_hash)
    
        return PaymentResult(
            tx_hash_approve=tx_hash_approve,
            tx_hash=tx_hash, 
            amount=self.from_wei(amount)
        )
    
    
    def approve_payment(self, amount):
        """
        called in submit_payment

        Args:
            amount: amount in wei
        """
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.token_contract.functions.approve(
            self.client_contract.address,
            amount
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            **self._get_fee_per_gas(),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.to_hex(tx_hash)
    

    def lock_revenue(self, task_id: str, hardware_id: int, duration: int):
        """
        deprecated
        """
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.payment_contract.functions.lockRevenue(
            task_id, 
            hardware_id, 
            duration
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            **self._get_fee_per_gas(),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.to_hex(tx_hash)
    
    def _approve_swan_token(self, amount):
        """
        deprecated
        """
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.token_contract.functions.approve(
            self.payment_contract.address, 
            amount
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            **self._get_fee_per_gas(),
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.to_hex(tx_hash)
    
    def _get_swan_balance(self, address=None):
        """Retrieve swan token balance of any wallet from Swan token contract.

        Args:
            address: wallet address to check balance. If None, retrieve own token balance.

        Returns:
            int Swan token balance in wei (18 decimal, 1e-18 swan).
        """
        if not address:
            address = self.account.address
        return self.token_contract.functions.balanceOf(address).call()
    
    def _wei_to_swan(self, value: int, decimal: int = 18):
        """Convert wei to swan.

        Args:
            value: integer value in wei.
            decimal: number of decimal digit if swan token (defaut 18)
        
        Return:
            float converted value with correct decimal (default swan, 18 decimal).
        """
        if value == 0: 
            return 0
        return self.w3.from_wei(value, 'ether')
    
    def to_wei(self, value: float):
        return int(self.w3.to_wei(value, 'ether'))
    
    def from_wei(self, value: float):
        return float(self.w3.from_wei(value, 'ether'))
    
    def _get_swan_gas(self):
        """Get current gas on Swan chain

        Returns:
            int current gas price in wei.
        """
        return self.w3.eth.gas_price