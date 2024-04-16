# ./swan/contract/swan_contract_ex.py


from swan.common.constant import *
from swan.common.utils import get_contract_abi

from swan.contract.swan_contract import SwanContract


CLIENT_CONTRACT_ADDRESS="0xe356a758fA1748dfBE71E989c876959665a66ddA"

class SwanContractEx(SwanContract):

    def __init__(self, private_key: str, rpc_url: str):
        """ Initialize swan contract API connection.

        Args:
            private_key: private key for wallet.
            rpc_url: rpc url of swan chain for connection.
        """
        super().__init__(private_key=private_key, rpc_url=rpc_url)
        self.client_contract = self.w3.eth.contract(
            address=CLIENT_CONTRACT_ADDRESS, 
            abi=get_contract_abi(CLIENT_CONTRACT_ABI)
        )

    def submit_payment(self, task_id: str, hardware_id: int, duration: int):
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        max_priority_fee_per_gas = self.w3.to_wei(2, 'gwei')
        max_fee_per_gas = base_fee + max_priority_fee_per_gas
        if max_fee_per_gas < max_priority_fee_per_gas:
            max_fee_per_gas = max_priority_fee_per_gas + base_fee
        tx = self.client_contract.functions.submitPayment(task_id, hardware_id, duration).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            "maxFeePerGas": max_fee_per_gas,
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.to_hex(tx_hash)
    
    def _approve_swan_token(self, amount):
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        max_priority_fee_per_gas = self.w3.to_wei(2, 'gwei')
        max_fee_per_gas = base_fee + max_priority_fee_per_gas
        if max_fee_per_gas < max_priority_fee_per_gas:
            max_fee_per_gas = max_priority_fee_per_gas + base_fee
        tx = self.token_contract.functions.approve(self.client_contract.address, amount).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            "maxFeePerGas": max_fee_per_gas,
            "maxPriorityFeePerGas": max_priority_fee_per_gas,
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.to_hex(tx_hash)
    