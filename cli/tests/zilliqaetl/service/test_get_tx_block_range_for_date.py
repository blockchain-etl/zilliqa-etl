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

import pytest
from dateutil.parser import parse

from blockchainetl_common.graph.graph_operations import OutOfBoundsError
from tests.zilliqaetl.helpers import get_zilliqa_api
from tests.helpers import skip_if_slow_tests_disabled
from zilliqaetl.service.block_range_service import BlockRangeService
from zilliqaetl.service.tx_block_timestamp_graph import TxBlockTimestampGraph


@pytest.mark.parametrize("date,expected_start_block,expected_end_block", [
    skip_if_slow_tests_disabled(['2019-06-18', 0, 142160]),
    skip_if_slow_tests_disabled(['2020-08-01', 700286, 702099]),
])
def test_get_tx_block_range_for_date(date, expected_start_block, expected_end_block):
    block_range_service = get_tx_block_range_service()
    parsed_date = parse(date)
    blocks = block_range_service.get_block_range_for_date(parsed_date)
    assert (expected_start_block, expected_end_block) == blocks


@pytest.mark.parametrize("date", [
    skip_if_slow_tests_disabled(['2019-06-01'])
])
def test_get_tx_block_range_for_date_fail(date):
    block_range_service = get_tx_block_range_service()
    parsed_date = parse(date)
    with pytest.raises(OutOfBoundsError):
        block_range_service.get_block_range_for_date(parsed_date)


def get_tx_block_range_service():
    block_timestamp_graph = TxBlockTimestampGraph(get_zilliqa_api("online"))
    return BlockRangeService(block_timestamp_graph)
