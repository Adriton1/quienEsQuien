\c quienesquien;

\echo 'LOADING DATABASE'

CREATE TABLE IF NOT EXISTS pruebasUsuarios(
    username text,
    tiempo real[][][]
);

CREATE TABLE IF NOT EXISTS preprocesadorecogida(
    username text,
    tiempos real[][][],
    H1 real[],
    H2 real[], 
    HP real[],
    PH real[],
    PP real[],
    HH real[],
    codigo_usuario integer
);


CREATE TABLE IF NOT EXISTS preprocesadoprediccion(
    username text,
    tiempos real[][][],
    H1 real[],
    H2 real[], 
    HP real[],
    PH real[],
    PP real[],
    HH real[],
    result real[],
    codigo_usuario integer

);
