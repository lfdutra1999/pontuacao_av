USE rpmesports;
drop tables temporadas, equipes, pilotos, piloto_equipe_temporada, grids, etapas, grid_pontos, pontuacao, baterias;

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

CREATE TABLE pilotos (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(128) NOT NULL,
    steam_id VARCHAR(128),
    PRIMARY KEY (id),
    UNIQUE (nome),
    UNIQUE (steam_id)
);

CREATE TABLE piloto_equipe_temporada (
    id INT NOT NULL AUTO_INCREMENT,
    piloto_id INT NOT NULL,
    equipe_id INT NOT NULL,
    temporada_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (piloto_id) REFERENCES pilotos(id),
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