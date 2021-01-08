from __future__ import print_function

import logging

from zilliqaetl_airflow.build_load_dag import build_load_dag
from zilliqaetl_airflow.variables import read_load_dag_vars

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# airflow DAG
DAG = build_load_dag(
    dag_id='zilliqa_load_dag',
    chain='zilliqa',
    **read_load_dag_vars(
        var_prefix='zilliqa_',
        load_schedule_interval='0 2 * * *'
    )
)
