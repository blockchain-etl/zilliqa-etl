from __future__ import print_function

import os
import logging
from datetime import timedelta
from tempfile import TemporaryDirectory
from pathlib import Path

from airflow import DAG, configuration
from airflow.operators import python_operator

from zilliqaetl_airflow.gcs_utils import upload_to_gcs


def build_export_dag(
        dag_id,
        provider_uris,
        output_bucket,
        export_start_date,
        export_end_date=None,
        notification_emails=None,
        export_schedule_interval='0 0 * * *',
        export_max_workers=5,
        export_max_active_runs=None,
        gzip=False,
):
    """Build Export DAG"""
    default_dag_args = {
        "depends_on_past": False,
        "start_date": export_start_date,
        "end_date": export_end_date,
        "email_on_failure": True,
        "email_on_retry": True,
        "retries": 5,
        "retry_delay": timedelta(minutes=5)
    }

    if notification_emails and len(notification_emails) > 0:
        default_dag_args['email'] = [email.strip() for email in notification_emails.split(',')]

    if export_max_active_runs is None:
        export_max_active_runs = configuration.conf.getint('core', 'max_active_runs_per_dag')

    dag = DAG(
        dag_id,
        schedule_interval=export_schedule_interval,
        default_args=default_dag_args,
        max_active_runs=export_max_active_runs
    )

    from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
    cloud_storage_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id="google_cloud_default")

    def import_zilliqaetl():
        from zilliqaetl.cli import (
            get_ds_block_range_for_date,
            get_tx_block_range_for_date,
            export_ds_blocks,
            export_tx_blocks,
        )
        globals()['get_ds_block_range_for_date'] = get_ds_block_range_for_date
        globals()['get_tx_block_range_for_date'] = get_tx_block_range_for_date
        globals()['export_ds_blocks'] = export_ds_blocks
        globals()['export_tx_blocks'] = export_tx_blocks

    # Export
    def export_path(directory, date):
        return "export/{directory}/block_date={block_date}/".format(
            directory=directory, block_date=date.strftime("%Y-%m-%d")
        )

    def copy_to_export_path(file_path, export_path, upload_empty_if_not_exist=True):
        logging.info('Calling copy_to_export_path({}, {})'.format(file_path, export_path))
        filename = os.path.basename(file_path)
        if gzip:
            filename = Path(file_path).stem + '.gz'

        if not os.path.exists(file_path):
            if upload_empty_if_not_exist:
                open(file_path, mode='a').close()
            else:
                raise ValueError('File {} does not exist'.format(file_path))

        upload_to_gcs(
            gcs_hook=cloud_storage_hook,
            bucket=output_bucket,
            object=export_path + filename,
            filename=file_path,
            gzip=gzip)

    def get_ds_block_range(tempdir, date, provider_uri):
        logging.info('Calling get_ds_block_range_for_date({}, {}, ...)'.format(provider_uri, date))
        get_ds_block_range_for_date.callback(
            provider_uri=provider_uri, date=date, output=os.path.join(tempdir, "ds_block_range.txt")
        )

        with open(os.path.join(tempdir, "ds_block_range.txt")) as block_range_file:
            block_range = block_range_file.read()
            start_block, end_block = block_range.split(",")

        return int(start_block), int(end_block)

    def get_tx_block_range(tempdir, date, provider_uri):
        logging.info('Calling get_tx_block_range_for_date({}, {}, ...)'.format(provider_uri, date))
        get_tx_block_range_for_date.callback(
            provider_uri=provider_uri, date=date, output=os.path.join(tempdir, "tx_block_range.txt")
        )

        with open(os.path.join(tempdir, "tx_block_range.txt")) as block_range_file:
            block_range = block_range_file.read()
            start_block, end_block = block_range.split(",")

        return int(start_block), int(end_block)

    def export_ds_blocks_command(execution_date, provider_uri, **kwargs):
        import_zilliqaetl()
        with TemporaryDirectory() as tempdir:
            start_block, end_block = get_ds_block_range(tempdir, execution_date, provider_uri)

            logging.info('Calling export_ds_blocks({}, {}, {}, {}, {})'.format(
                start_block, end_block, provider_uri, export_max_workers, tempdir))

            export_ds_blocks.callback(
                start_block=start_block,
                end_block=end_block,
                provider_uri=provider_uri,
                max_workers=export_max_workers,
                output_dir=tempdir,
                output_format='json'
            )

            copy_to_export_path(
                os.path.join(tempdir, "ds_block_range.txt"), export_path("ds_block_range", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "ds_blocks.json"), export_path("ds_blocks", execution_date)
            )

    def export_tx_blocks_command(execution_date, provider_uri, **kwargs):
        import_zilliqaetl()
        with TemporaryDirectory() as tempdir:
            start_block, end_block = get_tx_block_range(tempdir, execution_date, provider_uri)

            logging.info('Calling export_tx_blocks({}, {}, {}, {}, {})'.format(
                start_block, end_block, provider_uri, export_max_workers, tempdir))

            export_tx_blocks.callback(
                start_block=start_block,
                end_block=end_block,
                provider_uri=provider_uri,
                max_workers=export_max_workers,
                output_dir=tempdir,
                output_format='json'
            )

            copy_to_export_path(
                os.path.join(tempdir, "tx_block_range.txt"), export_path("tx_block_range", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "tx_blocks.json"), export_path("tx_blocks", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "transactions.json"), export_path("transactions", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "transitions.json"), export_path("transitions", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "event_logs.json"), export_path("event_logs", execution_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "exceptions.json"), export_path("exceptions", execution_date)
            )

    def add_export_task(toggle, task_id, python_callable, dependencies=None):
        if toggle:
            operator = python_operator.PythonOperator(
                task_id=task_id,
                python_callable=python_callable,
                provide_context=True,
                execution_timeout=timedelta(hours=48),
                dag=dag,
            )
            if dependencies is not None and len(dependencies) > 0:
                for dependency in dependencies:
                    if dependency is not None:
                        dependency >> operator
            return operator
        else:
            return None

    # Operators

    add_export_task(
        True,
        "export_ds_blocks",
        add_provider_uri_fallback_loop(export_ds_blocks_command, provider_uris),
    )

    add_export_task(
        True,
        "export_tx_blocks",
        add_provider_uri_fallback_loop(export_tx_blocks_command, provider_uris)
    )

    return dag


def add_provider_uri_fallback_loop(python_callable, provider_uris):
    """Tries each provider uri in provider_uris until the command succeeds"""
    def python_callable_with_fallback(**kwargs):
        for index, provider_uri in enumerate(provider_uris):
            kwargs['provider_uri'] = provider_uri
            try:
                python_callable(**kwargs)
                break
            except Exception as e:
                if index < (len(provider_uris) - 1):
                    logging.exception('An exception occurred. Trying another uri')
                else:
                    raise e

    return python_callable_with_fallback
