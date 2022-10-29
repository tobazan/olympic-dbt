from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
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

with DAG(dag_id = 'load_raw_data', schedule_interval = "@monthly", default_args = default_args, description = "Loads csv files to raw tables in PG DB") as dag:

    start_task = DummyOperator(task_id='dummy_task')

    generos_raw_create = PostgresOperator(task_id='generos_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.generos_raw (genero_id serial primary key,
                                                                                genero varchar(1));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    generos_raw_populate = PostgresOperator(task_id='generos_raw_populate',
                        sql="""
                            INSERT INTO oly.generos_raw (genero_id, genero) VALUES(1,'M');
                            INSERT INTO oly.generos_raw (genero_id, genero) VALUES(2,'F');
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    deportes_raw_create = PostgresOperator(task_id='deportes_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.deportes_raw (deporte_id serial primary key,
                                                                                deporte varchar(100));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    deportes_raw_populate = PostgresOperator(task_id='deportes_raw_populate',
                        sql="COPY oly.deportes_raw FROM '/tmp/sample_data/deporte.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    equipos_raw_create = PostgresOperator(task_id='equipos_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.equipos_raw (equipo_id serial primary key,
                                                                                equipo varchar(100),
                                                                                sigla varchar(3));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    equipos_raw_populate = PostgresOperator(task_id='equipos_raw_populate',
                        sql="COPY oly.equipos_raw FROM '/tmp/sample_data/paises.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    
    juegos_raw_create = PostgresOperator(task_id='juegos_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.juegos_raw (juego_id serial primary key,
                                                                                nombre_juego varchar(100),
                                                                                annio integer,
                                                                                temporada varchar(100),
                                                                                ciudad varchar(100));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    juegos_raw_populate = PostgresOperator(task_id='juegos_raw_populate',
                        sql="COPY oly.juegos_raw FROM '/tmp/sample_data/juegos.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    deportistas_raw_create  = PostgresOperator(task_id='deportistas_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.deportistas_raw (deportista_id serial primary key,
                                                                                    nombre varchar(100),
                                                                                    genero_id integer REFERENCES oly.generos_raw (genero_id),
                                                                                    edad integer,
                                                                                    altura integer,
                                                                                    peso numeric,
                                                                                    equipo_id integer REFERENCES oly.equipos_raw (equipo_id));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    
    deportistas_raw_populate  = PostgresOperator(task_id='deportistas_raw_populate',
                        sql="""COPY oly.deportistas_raw FROM '/tmp/sample_data/deportista.csv' DELIMITER ',' CSV HEADER;
                                COPY oly.deportistas_raw FROM '/tmp/sample_data/deportista2.csv' DELIMITER ',' CSV HEADER;
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )

    eventos_raw_create  = PostgresOperator(task_id='eventos_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.eventos_raw (evento_id serial primary key,
                                                                                evento varchar(100),
                                                                                deporte_id integer REFERENCES oly.deportes_raw (deporte_id));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    
    eventos_raw_populate  = PostgresOperator(task_id='eventos_raw_populate',
                        sql="COPY oly.eventos_raw FROM '/tmp/sample_data/evento.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    resultados_raw_create  = PostgresOperator(task_id='resultados_raw_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.resultados_raw (resultado_id serial primary key,
                                                                                    medalla varchar(100),
                                                                                    deportista_id integer REFERENCES oly.deportistas_raw (deportista_id),
                                                                                    juego_id integer REFERENCES oly.juegos_raw (juego_id),
                                                                                    evento_id integer REFERENCES oly.eventos_raw (evento_id));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    
    resultados_raw_populate  = PostgresOperator(task_id='resultados_raw_populate',
                        sql="COPY oly.resultados_raw FROM '/tmp/sample_data/resultados.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        ) 

    metabase_paises_create  = PostgresOperator(task_id='metabase_paises_create',
                        sql="""CREATE TABLE IF NOT EXISTS oly.metabase_paises (pais varchar(100),
                                                                            codigo varchar(2));
                        """,
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        )
    
    metabase_paises_populate  = PostgresOperator(task_id='metabase_paises_populate',
                        sql="COPY oly.metabase_paises FROM '/tmp/sample_data/metabase_countries.csv' DELIMITER ',' CSV HEADER;",
                        postgres_conn_id='postgres-default',
                        autocommit=True,
                        database="airflow"
                        ) 

    start_task >> [generos_raw_create, deportes_raw_create, equipos_raw_create, juegos_raw_create]
    generos_raw_create >> generos_raw_populate
    deportes_raw_create >> deportes_raw_populate >> eventos_raw_create >> eventos_raw_populate
    equipos_raw_create >> equipos_raw_populate
    juegos_raw_create >> juegos_raw_populate
    deportistas_raw_create << [generos_raw_populate, equipos_raw_populate]
    deportistas_raw_create >> deportistas_raw_populate
    resultados_raw_create << [juegos_raw_populate, deportistas_raw_populate, eventos_raw_populate]
    resultados_raw_create >> resultados_raw_populate
    resultados_raw_populate >> metabase_paises_create >> metabase_paises_populate