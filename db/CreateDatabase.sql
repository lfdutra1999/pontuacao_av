"DB_HOST": "15.228.232.102",
"DB_HOST": "127.0.0.1",

create database rpmesports CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE rpmesports;
drop tables temporadas, equipes, piloto, piloto_informacoes, piloto_equipe_temporada, grids, etapas, grid_pontos, pontuacao, baterias;

CREATE TABLE temporadas (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nome)
);

CREATE TABLE equipes (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(128) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nome)
);

CREATE TABLE piloto (
    uuid BINARY(16) PRIMARY KEY,
    username VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(64),
    isAdmin INT(1)
);

CREATE TABLE piloto_informacoes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    piloto_uuid BINARY(16),
    nome VARCHAR(32) NOT NULL,
    sobrenome VARCHAR(128) NOT NULL,
    nickname VARCHAR(128) NOT NULL,
    steamid VARCHAR(32) NOT NULL,
    whatsapp VARCHAR(11) NOT NULL,
    chavepix VARCHAR(256) NOT NULL,
    cidade VARCHAR(128),
    estado VARCHAR(2),
    controlador VARCHAR(128),
    linkcanal VARCHAR(128),
    foto varchar(128),
    FOREIGN KEY (piloto_uuid) REFERENCES piloto(uuid)
);


CREATE TABLE piloto_equipe_temporada (
    id INT NOT NULL AUTO_INCREMENT,
    piloto_id INT NOT NULL,
    equipe_id INT NOT NULL,
    temporada_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (piloto_id) REFERENCES piloto(id),
    FOREIGN KEY (equipe_id) REFERENCES equipes(id),
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
);


CREATE TABLE grids (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(64) NOT NULL,
    simulador VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nome)
);

CREATE TABLE etapas (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(64) NOT NULL,
    grid_id INT NOT NULL,
    temporada_id INT NOT NULL,
    multiplicador FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (grid_id) REFERENCES grids(id),
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id),
    UNIQUE (nome)
);

CREATE TABLE grid_pontos (
    id INT NOT NULL AUTO_INCREMENT,
    grid_id INT NOT NULL,
    posicao INT NOT NULL,
    pontos FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (grid_id) REFERENCES grids(id)
);

CREATE TABLE baterias (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(64) NOT NULL,
    etapa_id INT NOT NULL,
    multiplicador FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (etapa_id) REFERENCES etapas(id),
    UNIQUE (nome)
);

CREATE TABLE pontuacao (
    id INT NOT NULL AUTO_INCREMENT,
    bateria_id INT NOT NULL,
    posicao INT NOT NULL,
    piloto_id INT NOT NULL,
    pontos FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (bateria_id) REFERENCES baterias(id),
    FOREIGN KEY (piloto_id) REFERENCES pilotos(id)
);