create database rpmesports CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE rpmesports;

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