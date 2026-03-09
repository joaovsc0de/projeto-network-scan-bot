use rede;

CREATE DATABASE rede;

CREATE TABLE dispositivos (

    id INT AUTO_INCREMENT PRIMARY KEY,

    ip VARCHAR(45),
    mac VARCHAR(50) UNIQUE,
    fabricante VARCHAR(100),

    conectado BOOLEAN DEFAULT FALSE,

    primeiro_scan DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_scan DATETIME
);