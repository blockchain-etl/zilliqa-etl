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
from pyzil.account import Account

from zilliqaetl.utils.zilliqa_utils import to_int, iso_datetime_string, encode_bench32_pub_key, encode_bench32_address


def map_transaction(tx_block, txn):
    block = {
        'type': 'transaction',
        'id': txn.get('ID'),
        'block_number': tx_block.get('number'),
        'block_timestamp': tx_block.get('timestamp'),
        'amount': to_int(txn.get('amount')),
        'code': txn.get('code'),
        'data': txn.get('data'),
        'gas_limit': to_int(txn.get('gasLimit')),
        'gas_price': to_int(txn.get('gasPrice')),
        'nonce': to_int(txn.get('nonce')),
        'sender_pub_key': txn.get('senderPubKey'),
        'sender': encode_bench32_pub_key(txn.get('senderPubKey')),
        'signature': txn.get('signature'),
        'to_addr': encode_bench32_address(txn.get('toAddr')),
        'version': to_int(txn.get('version')),
        **map_receipt(txn)
    }

    return block


def map_receipt(txn):
    receipt = txn.get('receipt')
    if receipt is None:
        return None

    return {
        'accepted': receipt.get('accepted'),
        'success': receipt.get('success'),
        'cumulative_gas': to_int(receipt.get('cumulative_gas')),
        'epoch_num': to_int(receipt.get('epoch_num')),
    }
