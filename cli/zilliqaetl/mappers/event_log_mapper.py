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

from zilliqaetl.utils.zilliqa_utils import to_int, json_dumps, iso_datetime_string, encode_bench32_address


def map_event_logs(tx_block, txn):
    receipt = txn.get('receipt')
    if receipt and receipt.get('event_logs'):
        for index, event_log in enumerate(receipt.get('event_logs')):
            yield {
                'type': 'event_log',
                'block_number': tx_block.get('number'),
                'block_timestamp': tx_block.get('timestamp'),
                'transaction_id': txn.get('ID'),
                'index': index,
                'address': encode_bench32_address(event_log.get('address')),
                'event_name': event_log.get('_eventname'),
                'params': [json_dumps(param) for param in event_log.get('params')]
            }
