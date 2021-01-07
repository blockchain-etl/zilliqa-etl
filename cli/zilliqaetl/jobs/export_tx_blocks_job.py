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

from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range

from zilliqaetl.jobs.retriable_exceptions import RETRY_EXCEPTIONS
from zilliqaetl.mappers.event_log_mapper import map_event_logs
from zilliqaetl.mappers.exception_mapper import map_exceptions
from zilliqaetl.mappers.transaction_mapper import map_transaction
from zilliqaetl.mappers.transition_mapper import map_transitions
from zilliqaetl.mappers.tx_block_mapper import map_tx_block
from zilliqaetl.service.zilliqa_service import ZilliqaService


# Exports tx blocks
class ExportTxBlocksJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            zilliqa_api,
            max_workers,
            item_exporter,
            export_transactions=True,
            export_event_logs=True,
            export_exceptions=True,
            export_transitions=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(1, max_workers, retry_exceptions=RETRY_EXCEPTIONS)
        self.item_exporter = item_exporter

        self.zilliqa_service = ZilliqaService(zilliqa_api)

        self.export_transactions = export_transactions
        self.export_event_logs = export_event_logs
        self.export_exceptions = export_exceptions
        self.export_transitions = export_transitions

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        items = []
        for number in block_number_batch:
            tx_block = map_tx_block(self.zilliqa_service.get_tx_block(number))

            txns = list(self.zilliqa_service.get_transactions(number)) if tx_block.get('num_transactions') > 0 else []
            if self._should_export_transactions():
                for txn in txns:
                    items.append(map_transaction(tx_block, txn))
                    if self._should_export_event_logs(txn):
                        items.extend(map_event_logs(tx_block, txn))
                    if self._should_export_exceptions(txn):
                        items.extend(map_exceptions(tx_block, txn))
                    if self._should_export_transitions(txn):
                        items.extend(map_transitions(tx_block, txn))
            tx_block['num_present_transactions'] = len(txns)
            items.append(tx_block)

        for item in items:
            self.item_exporter.export_item(item)

    def _should_export_transactions(self):
        return self.export_transactions

    def _should_export_event_logs(self, txn):
        return self.export_event_logs and txn.get('receipt')

    def _should_export_exceptions(self, txn):
        return self.export_exceptions and txn.get('receipt')

    def _should_export_transitions(self, txn):
        return self.export_transitions and txn.get('receipt')

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
