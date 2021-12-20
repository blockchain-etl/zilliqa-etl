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

from zilliqaetl.cli.export_ds_blocks import export_ds_blocks
from zilliqaetl.cli.export_tx_blocks import export_tx_blocks
from zilliqaetl.cli.get_ds_block_range_for_date import get_ds_block_range_for_date
from zilliqaetl.cli.get_tx_block_range_for_date import get_tx_block_range_for_date


@click.group()
@click.version_option(version='1.0.8')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_ds_blocks, "export_ds_blocks")
cli.add_command(export_tx_blocks, "export_tx_blocks")

# utils
cli.add_command(get_ds_block_range_for_date, "get_ds_block_range_for_date")
cli.add_command(get_tx_block_range_for_date, "get_tx_block_range_for_date")
