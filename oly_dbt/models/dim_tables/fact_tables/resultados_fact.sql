with deportistas_dim as (

    select *
    from airflow.public.deportistas_dim

),
eventos_dim as (

    select 
        evento_id,
        evento,
        deporte
    from airflow.public.eventos_dim

),
juegos as (

    select *
    from airflow.public.juegos_raw

),

resultados_fact as (

    select
        resultado_id,
        medalla,
        deportista_id,
        de.nombre,
        de.genero,
        de.edad,
        de.altura,
        de.peso,
        de.equipo,
        de.sigla,
        juego_id,
        ju.nombre_juego,
        ju.annio,
        ju.temporada,
        ju.ciudad,
        evento_id,
        ev.evento,
        ev.deporte

    from airflow.public.resultados_raw

    left join deportistas_dim de using (deportista_id)
    left join eventos_dim ev using (evento_id)
    left join juegos ju using (juego_id)

)

select * from resultados_fact