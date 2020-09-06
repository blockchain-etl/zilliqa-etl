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

from zilliqaetl.utils.zilliqa_utils import to_int, iso_datetime_string, encode_bench32_pub_key


def map_tx_block(raw_block):
    header = raw_block.get('header')
    body = raw_block.get('body')
    block = {
        'type': 'tx_block',
        'number': to_int(header.get('BlockNum')),
        'ds_block_number': to_int(header.get('DSBlockNum')),
        'timestamp': iso_datetime_string(header.get('Timestamp')),
        'version': header.get('Version'),
        'gas_limit': to_int(header.get('GasLimit')),
        'gas_used': to_int(header.get('GasUsed')),
        'mb_info_hash': header.get('MbInfoHash'),
        'tx_leader_pub_key': header.get('MinerPubKey'),
        'tx_leader_address': encode_bench32_pub_key(header.get('MinerPubKey')),
        'num_micro_blocks': to_int(header.get('NumMicroBlocks')),
        'num_transactions': to_int(header.get('NumTxns')),
        'prev_block_hash': header.get('PrevBlockHash'),
        'rewards': to_int(header.get('Rewards')),
        'state_delta_hash': header.get('StateDeltaHash'),
        'state_root_hash': header.get('StateRootHash'),
        'header_signature': body.get('HeaderSign')
    }

    return block
