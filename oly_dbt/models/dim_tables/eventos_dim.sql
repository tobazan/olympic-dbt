with deportes as (

    select
        deporte_id,
        deporte
    from airflow.oly.deportes_raw

),

eventos_dim as (

    select
        evento_id,
        evento,
        deporte_id,
        d.deporte

    from airflow.oly.eventos_raw

    left join deportes d using (deporte_id)

)

select * from eventos_dim