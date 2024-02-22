# ./swan/contract/swan_contract.py

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

from swan.common.constant import *
from swan.common.utils import get_contract_abi

class SwanContract():

    def __init__(self, private_key: str, rpc_url: str):
        """ Initialize swan contract API connection.

        Args:
            private_key: private key for wallet.
            rpc_url: rpc url of swan chain for connection.
        """
        self.account = Account.from_key(private_key)
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.payment_contract = self.w3.eth.contract("0xF0F98f476b1a5c1c6EA97eEb23d8796F553246d9", abi=get_contract_abi(PAYMENT_CONTRACT_ABI))
        self.token_contract = self.w3.eth.contract("0x91B25A65b295F0405552A4bbB77879ab5e38166c", abi=get_contract_abi(SWAN_TOKEN_ABI))

    def hardware_info(self, hardware_id: int):
        """Retrieve hardware information from payment contract.

        Args:
            hardware_id: integer id of hardware, can be retrieve through Swan API.

        Returms:
            tuple[] hardware information, [name: str, price/hr: int, avaliability: bool]
            e.g. ['C1ae.medium', 1000000000000000000, True]
            see more detial in ./swan/contract/abi/paymentContract.json
        """
        hardware_info = self.payment_contract.functions.hardwareInfo(hardware_id).call()
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

    def lock_revenue(self, space_id: str, hardware_id: int, duration: int):
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.payment_contract.functions.lockRevenue(space_id, hardware_id, duration).build_transaction({
            'from': self.account.address,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.toHex(tx_hash)
    
    def _approve_swan_token(self, amount):
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = self.token_contract.functions.approve(self.payment_contract.address, amount).build_transaction({
            'from': self.account.address,
            'nonce': nonce
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=CONTRACT_TIMEOUT)
        return self.w3.toHex(tx_hash)
    
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
        return value ** -(decimal)
    
    def _get_swan_gas(self):
        """Get current gas on Swan chain

        Returns:
            int current gas price in wei.
        """
        return self.w3.eth.gas_price