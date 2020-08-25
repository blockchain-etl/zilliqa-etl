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

from zilliqaetl.jobs.export_ds_blocks_job import ExportDsBlocksJob
from zilliqaetl.exporters.zilliqa_item_exporter import ZilliqaItemExporter
from tests.zilliqaetl.helpers import get_zilliqa_api
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

import tests.resources
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_ds_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, resource_group ,provider_type", [
    (123, 125, 'ds_blocks', 'mock'),
    skip_if_slow_tests_disabled([123, 125, 'ds_blocks', 'online']),
])
def test_export_ds_blocks_job(tmpdir, start_block, end_block, resource_group, provider_type):
    job = ExportDsBlocksJob(
        start_block=start_block,
        end_block=end_block,
        zilliqa_api=ThreadLocalProxy(
            lambda: get_zilliqa_api(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file))),
        max_workers=5,
        item_exporter=ZilliqaItemExporter(str(tmpdir)),
    )
    job.run()

    all_files = ['ds_blocks.json']

    for file in all_files:
        print(read_file(str(tmpdir.join(file))))
        compare_lines_ignore_order(
            read_resource(resource_group, f'expected_{file}'), read_file(str(tmpdir.join(file)))
        )
