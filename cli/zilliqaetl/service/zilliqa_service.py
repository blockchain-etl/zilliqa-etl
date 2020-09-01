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
            print(f'Error getting transactions for tx_block#{block_number} caused by "{e}"')
            return []
