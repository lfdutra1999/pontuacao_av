USE rpmesports;
drop table piloto_informacoes, piloto, equipe, temporada, piloto_equipe_temporada, grid, categoria, classe, carro, categoria_carros;
CREATE TABLE piloto (
    uuid BINARY(16) PRIMARY KEY,
    username VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(64),
    isAdmin INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

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
    foto varchar(255),
    FOREIGN KEY (piloto_uuid) REFERENCES piloto(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE equipe (
    uuid BINARY(16) PRIMARY KEY,
    nome VARCHAR(128) NOT NULL,
    foto varchar(255),
    UNIQUE (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE temporada (
    uuid BINARY(16) PRIMARY KEY,
    nome VARCHAR(128) NOT NULL,
    dtInicio DATE NOT NULL,
    dtFim DATE NOT NULL,
    UNIQUE (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE piloto_equipe_categoria (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    categoria_uuid BINARY(16),
    equipe_uuid BINARY(16),
    piloto_uuid BINARY(16),
    FOREIGN KEY (categoria_uuid) REFERENCES categoria(uuid),
    FOREIGN KEY (equipe_uuid) REFERENCES equipe(uuid),
    FOREIGN KEY (piloto_uuid) REFERENCES piloto(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE grid (
    uuid BINARY(16) PRIMARY KEY,
    temporada_uuid BINARY(16),
    nome VARCHAR(64) UNIQUE,
    simulador VARCHAR(16) NOT NULL,
    dia_da_semana VARCHAR(32) NOT NULL,
    link_onboard VARCHAR(255) NOT NULL,
    imagem VARCHAR(255),
    FOREIGN KEY (temporada_uuid) REFERENCES temporada(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE categoria (
    uuid BINARY(16) PRIMARY KEY,
    grid_uuid BINARY(16),
    nome VARCHAR(64),
    horario VARCHAR(5) NOT NULL,
    FOREIGN KEY (grid_uuid) REFERENCES grid(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE classe (
    uuid BINARY(16) PRIMARY KEY,
    nome VARCHAR(64) UNIQUE,
    imagem VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE carro (
    uuid BINARY(16) PRIMARY KEY,
    classe_uuid BINARY(16),
    nome VARCHAR(64),
    imagem VARCHAR(255),
    FOREIGN KEY (classe_uuid) REFERENCES classe(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE categoria_carros (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    categoria_uuid BINARY(16),
    classe_uuid BINARY(16),
    carro_uuid BINARY(16),
    FOREIGN KEY (categoria_uuid) REFERENCES grid(uuid),
    FOREIGN KEY (classe_uuid) REFERENCES classe(uuid),
    FOREIGN KEY (carro_uuid) REFERENCES carro(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE pista (
    uuid BINARY(16) PRIMARY KEY,
    nome VARCHAR(64),
    pais VARCHAR(64),
    imagem VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;

CREATE TABLE etapa (
    uuid BINARY(16) PRIMARY KEY,
    categoria_uuid BINARY(16),
    pista_uuid BINARY(16),
    nome VARCHAR(64),
    periodo INT,
    FOREIGN KEY (categoria_uuid) REFERENCES categoria(uuid),
    FOREIGN KEY (pista_uuid) REFERENCES pista(uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_ci;
