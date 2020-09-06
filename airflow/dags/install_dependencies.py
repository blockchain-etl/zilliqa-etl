"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

from airflow.operators.python_operator import PythonOperator

default_args = {
    'start_date': '2020-01-01',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'install_dependencies',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False,
    dagrun_timeout=timedelta(minutes=60))

# pyzil package requires fastecdsa which requires python-dev and libgmp3-dev
# https://github.com/AntonKueltz/fastecdsa/issues/29
t1 = BashOperator(
    task_id='apt_install',
    bash_command='sudo apt update && sudo apt -y install python-dev libgmp3-dev && sudo pip3 install zilliqa-etl==1.0.2',
    dag=dag,
    depends_on_past=False)


def test_pyzil(**kwargs):
    from pyzil.account import Account
    acc = Account(public_key='039fbf7df13d0b6798fa16a79daabb97d4424062d2f8bd4e9a7c7851e732a25e1d')
    print(acc.bech32_address)


t2 = operator = PythonOperator(
    task_id='test_pyzil',
    python_callable=test_pyzil,
    provide_context=True,
    execution_timeout=timedelta(hours=48),
    dag=dag,
)

t1 >> t2