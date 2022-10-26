with generos as (

    select
        genero_id,
        genero
    from airflow.public.generos_raw

),

equipos as (

    select
        equipo_id,
        equipo,
        sigla
    from airflow.public.equipos_raw

),

deportistas_dim as (

    select
        deportista_id,
        nombre,
        genero_id,
        g.genero,
        edad,
        altura,
        peso,
        equipo_id,
        e.equipo,
        e.sigla

    from airflow.public.deportistas_raw

    left join generos g using (genero_id)
    left join equipos e using (equipo_id)

)

select * from deportistas_dim