CREATE DATABASE IF NOT EXISTS mentoria360_mvp;
USE mentoria360_mvp;

CREATE TABLE IF NOT EXISTS administradores(
    id INT PRIMARY KEY AUTO_INCREMENT, 
    nomeAdmin VARCHAR(255) NOT NULL,
    emailAdmin VARCHAR(255) NOT NULL,
    senhaAdmin VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS alunos(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomeAluno VARCHAR(255) NOT NULL,
    emailAluno VARCHAR(255) NOT NULL,
    senhaAluno VARCHAR(255) NOT NULL,
    CPFAluno VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomeProduto VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios_produtos(
    usuario_id INT NOT NULL,
    produto_id INT NOT NULL,
    PRIMARY KEY (usuario_id, produto_id),
    FOREIGN KEY (usuario_id) REFERENCES alunos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS palestras_eventos (
	id int AUTO_INCREMENT PRIMARY KEY,
	nomeEvento VARCHAR(255) not null,
	dataInicial DATE NOT NULL,
	dataFinal DATE NOT NULL,
	nomePalestrate VARCHAR(150) NOT NULL 
);


INSERT INTO produtos (nomeProduto) VALUES 
('MPS'),
('DOP');


