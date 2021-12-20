# MIT License
#
# Copyright (c) 2020 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from pyzil.zilliqa.api import APIError

TXN_HASH_NOT_PRESENT = "Txn Hash not Present"
TX_BLOCK_NO_TRANSACTIONS = "TxBlock has no transactions"
FAILED_TO_GET_MICROBLOCK = "Failed to get Microblock"


class ZilliqaService(object):
    def __init__(self, zilliqa_api):
        self.zilliqa_api = zilliqa_api

    def get_ds_block(self, block_number):
        return self.zilliqa_api.GetDsBlock(str(block_number))

    def get_genesis_ds_block(self):
        return self.get_ds_block(0)

    def get_latest_ds_block(self):
        return self.zilliqa_api.GetLatestDsBlock()

    def get_tx_block(self, block_number):
        return self.zilliqa_api.GetTxBlock(str(block_number))

    def get_genesis_tx_block(self):
        return self.get_tx_block(0)

    def get_latest_tx_block(self):
        return self.zilliqa_api.GetLatestTxBlock()

    def get_transactions(self, block_number):
        try:
            return self.zilliqa_api.GetTxnBodiesForTxBlock(str(block_number))
        except APIError as e:
            if str(e) in (TXN_HASH_NOT_PRESENT, FAILED_TO_GET_MICROBLOCK):
                return self.get_validated_transactions(block_number)
            if str(e) == TX_BLOCK_NO_TRANSACTIONS:
                return []
            raise e

    def get_validated_transactions(self, block_number):
        for group in self.zilliqa_api.GetTransactionsForTxBlock(str(block_number)):
            if isinstance(group, list):
                for txn_hash in group:
                    try:
                        yield self.get_transaction_by_hash(txn_hash)
                    except APIError as e:
                        if str(e) not in (TXN_HASH_NOT_PRESENT, FAILED_TO_GET_MICROBLOCK):
                            raise e

    def get_transaction_by_hash(self, txn_hash):
        return self.zilliqa_api.GetTransaction(txn_hash)
