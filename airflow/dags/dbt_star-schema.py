from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 9, 1),
    "end_date": datetime(2022, 10, 10),
    'retries': 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": True
}

with DAG(dag_id = 'dbt_star-schema', schedule_interval = "@monthly", default_args = default_args, description = "Validates expectations and creates DIM and FACT tables") as dag:

    start_sensor = ExternalTaskSensor(task_id='start_sensor',
                poke_interval=30,
                timeout=60*10,
                retries=1,
                external_dag_id='load_raw_data'
    )

    test_raw_tables = BashOperator(task_id='test_raw_tables',
        bash_command='cd /opt/dbt/oly_dbt && dbt test'
    )

    deportistas_dim = BashOperator(task_id='deportistas_dim',
        bash_command='cd /opt/dbt/oly_dbt && dbt run --select +deportistas_dim'
    )

    eventos_dim = BashOperator(task_id='eventos_dim',
        bash_command='cd /opt/dbt/oly_dbt && dbt run --select +eventos_dim'
    )

    resultados_fact = BashOperator(task_id='resultados_fact',
        bash_command='cd /opt/dbt/oly_dbt && dbt run --select +resultados_fact'
    )

    start_sensor >> test_raw_tables >> [deportistas_dim, eventos_dim]
    [deportistas_dim, eventos_dim] >> resultados_fact