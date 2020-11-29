# MIT License
#
# Copyright (c) 2020 Worawat Wijarn worawat.wijarn@gmail.com
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

import click

from zilliqaetl.cli.rate_limiting_proxy import RateLimitingProxy
from zilliqaetl.jobs.export_tx_blocks_job import ExportTxBlocksJob

from zilliqaetl.exporters.zilliqa_item_exporter import ZilliqaItemExporter
from blockchainetl_common.logging_utils import logging_basic_config
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy
from pyzil.zilliqa.api import ZilliqaAPI

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-p', '--provider-uri', default='https://api.zilliqa.com', show_default=True, type=str,
              help='The URI of the remote Zilliqa node.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
@click.option('-o', '--output-dir', default=None, type=str, help='The output directory for block data.')
@click.option('-f', '--output-format', default='json', show_default=True, type=click.Choice(['json']),
              help='The output format.')
@click.option('-r', '--rate-limit', default=None, show_default=True, type=int,
              help='Maximum requests per second for provider in case it has rate limiting')
def export_tx_blocks(start_block, end_block, provider_uri, max_workers, output_dir, output_format, rate_limit=None):
    """Exports tx blocks."""

    zilliqa_api = ThreadLocalProxy(lambda: ZilliqaAPI(provider_uri))
    if rate_limit is not None and rate_limit > 0:
        zilliqa_api = RateLimitingProxy(zilliqa_api, max_per_second=rate_limit)
    job = ExportTxBlocksJob(
        start_block=start_block,
        end_block=end_block,
        zilliqa_api=zilliqa_api,
        max_workers=max_workers,
        item_exporter=ZilliqaItemExporter(output_dir, output_format=output_format),
    )
    job.run()
