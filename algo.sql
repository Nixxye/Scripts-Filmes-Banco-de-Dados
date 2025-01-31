CREATE TABLE public."BD1_Filmes_Bilheteria"
(
    "Id" bigint NOT NULL,
    "Titulo_Original" character varying,
    "Registro_Sala" bigint,
    "Ano" integer,
    "Publico" bigint,
    "Titulo_pt" character varying,
    "Pais_Obra" character(20),
    PRIMARY KEY ("Id")
)
WITH (
    OIDS = FALSE
);

ALTER TABLE IF EXISTS public."BD1_Filmes_Bilheteria"
    OWNER to postread;