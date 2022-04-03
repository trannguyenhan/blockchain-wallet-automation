from terra_sdk.client.lcd import LCDClient
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.market import MsgSwap
from terra_sdk.client.lcd.api.tx import CreateTxOptions
import sys

import requests

class Terra:
    COEFF = 1000000
    TOKEN = "harbor flat drink elder ranch age unaware gas example able hockey sustain tomato novel tray critic later extend parrot manual quality snack banner concert"
    
    # host 
    CHAIN_ID = "bombay-12"
    URL = "https://bombay-lcd.terra.dev"

    def __init__(self):
        # terra client
        try:
            self.terra = LCDClient(
                chain_id=self.CHAIN_ID, 
                url=self.URL
            )
        except: 
            # if cannot connect to host (mainnet or testnet) terra
            # print and exit
            print("Cannot connect " + self.CHAIN_ID)
            sys.exit(5)

        # login with token
        self._login(self.TOKEN)
        self.fetch_balance()

    def _login(self, token):
        # login with token
        self.mk = MnemonicKey(mnemonic=token)
        self.acc_address = self.mk.acc_address
        

    # function send coin from master account to send_to 
    def send_coin(self, coin, send_to, value): 
        vcoin = str(int(value * self.COEFF)) + "u" + coin
        print("sending {}{} to ({})".format(value, coin, send_to))
        
        msg = MsgSend(
            self.acc_address,
            send_to,
            vcoin
        )

        wallet = self.terra.wallet(self.mk)
        tx = wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[msg],
                memo="transaction"
            )
        )

        result = self.terra.tx.broadcast(tx)
        print("Transaction hash: {}\nAccess to https://finder.terra.money/ check your transaction".format(result.txhash))
        return result

    # function fetch balane
    def fetch_balance(self):
        # fetch wallet
        wallet = self.terra.bank.balance(self.acc_address)
        self.balance = wallet[0]

    # check rate luna/ ust
    def check_rate(self):
        rate = self.terra.market.swap_rate('1000000uluna', 'uusd')
        print("now rate (luna / ust): {}".format(rate / 1000000)) # print rate console

        # check historical rate
        rate_list = requests.get('https://fcd.terra.dev/v1/market/price?denom=uusd&interval=1h').json()
        print("\nHistorical rate:")
        print(rate_list)
        return rate

    # swap coin
    # base swap
    def swap_2_coin(self, valuein, coin_source, coin_dest):
        vcoin_source = str(int(valuein * self.COEFF)) + "u" + coin_source
        vcoin_dest = "u" + coin_dest
        print("Swap coin ({}) to ({})".format(coin_source, coin_dest))

        msg = MsgSwap(
            self.acc_address,
            vcoin_source,
            vcoin_dest
        )
        
        wallet = self.terra.wallet(self.mk)
        tx = wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[msg],
                memo="Algotrading",
            )
        )

        result = self.terra.tx.broadcast(tx)
        print("Transaction hash: {}\nAccess to https://finder.terra.money/ check your transaction".format(result.txhash))
        return result

    def swap_2_luna(self, valuein, coin="usd"):
        self.swap_2_coin(valuein, coin, 'luna')

    def swap_2_ust(self, valuein, coin="luna"):
        self.swap_2_coin(valuein, coin, 'usd')

acc = Terra()
acc.check_rate()
# acc.send_coin('luna', 'terra1t2rcdcyh3nd2vjaerrk0ct4gkj4qu8f4jpm4hn', 0.3)
# acc.swap_2_ust(1, 'luna')
# acc.swap_2_luna(100, 'usd')
