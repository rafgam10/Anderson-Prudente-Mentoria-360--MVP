CREATE DATABASE IF NOT EXISTS mentoria360_mvp;
USE mentoria360_mvp;

-- ==============================
-- Tabela de administradores
-- ==============================
CREATE TABLE IF NOT EXISTS administradores (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    nomeAdmin VARCHAR(255) NOT NULL,
    emailAdmin VARCHAR(255) NOT NULL,
    senhaAdmin VARCHAR(255) NOT NULL
);

-- ==============================
-- Tabela de alunos
-- ==============================
CREATE TABLE IF NOT EXISTS alunos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomeAluno VARCHAR(255) NOT NULL,
    emailAluno VARCHAR(255) NOT NULL,
    senhaAluno VARCHAR(255) NOT NULL,
    CPFAluno VARCHAR(255) NOT NULL
);

-- ==============================
-- Tabela de produtos
-- ==============================
CREATE TABLE IF NOT EXISTS produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomeProduto VARCHAR(100) NOT NULL
);

-- ==============================
-- Relacionamento Aluno x Produto (M:N)
-- ==============================
CREATE TABLE IF NOT EXISTS usuarios_produtos (
    usuario_id INT NOT NULL,
    produto_id INT NOT NULL,
    PRIMARY KEY (usuario_id, produto_id),
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES alunos(id) ON DELETE CASCADE,
    CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

-- ==============================
-- Tabela de palestras e eventos
-- ==============================
CREATE TABLE IF NOT EXISTS palestras_eventos (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nomeEvento VARCHAR(255) NOT NULL,
	dataInicial DATE NOT NULL,
	horaInicial TIME  NOT NULL,
	dataFinal DATE NOT NULL,
	horaFinal TIME NOT NULL,
	nomePalestrante VARCHAR(150) NOT NULL 
);

-- ==============================
-- Tabela de fases
-- ==============================
CREATE TABLE IF NOT EXISTS fases (
    id_fase INT PRIMARY KEY AUTO_INCREMENT,
    nome_fase VARCHAR(100) NOT NULL
);

-- ==============================
-- Tabela de atividades
-- ==============================
CREATE TABLE IF NOT EXISTS atividades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_atividade VARCHAR(200) NOT NULL,
    descricao TEXT,
    data DATE NOT NULL,
    hora TIME NOt NULL,
    plataforma VARCHAR(50) NOT NULL,
    fase_id INT NOT NULL,
    FOREIGN KEY (fase_id) REFERENCES fases(id_fase)
);

-- ==============================
-- Inserts iniciais
-- ==============================
INSERT INTO produtos (nomeProduto) VALUES 
('MPS'),
('DOP');

INSERT INTO fases (nome_fase) VALUES 
('Fase 1'), 
('Fase 2'), 
('Fase 3'),
('Fase 4'),
('Fase 5');

INSERT INTO administradores (nomeAdmin, emailAdmin, senhaAdmin) VALUES
('Rafael Timóteo', 'rafael@gmail.com', 'gamer');


-- ==============================
-- Inserindo Palestras e Eventos
-- ==============================
INSERT INTO palestras_eventos (nomeEvento, dataInicial, horaInicial, dataFinal, horaFinal, nomePalestrante)
VALUES
('Inovação na Indústria 4.0', '2025-10-20', '09:00:00', '2025-10-20', '11:00:00', 'Dra. Ana Silva'),
('Gestão Ágil de Projetos', '2025-10-22', '14:00:00', '2025-10-22', '16:30:00', 'Carlos Pereira'),
('Introdução ao Machine Learning', '2025-11-05', '10:00:00', '2025-11-05', '12:00:00', 'Prof. João Mendes');


-- ==============================
-- Inserindo Atividades
-- ==============================
INSERT INTO atividades (nome_atividade, descricao, data, hora, plataforma, fase_id)
VALUES
('Atividade 1', 'Introdução à Plataforma MPS', '2025-10-10', '09:00:00', 'MPS', 1),
('Atividade 2', 'Primeiros exercícios práticos', '2025-10-11', '14:00:00', 'MPS', 1),
('Atividade 1', 'Planejamento de Sprint', '2025-10-12', '09:00:00', 'DOP', 2),
('Atividade 2', 'Revisão de Requisitos', '2025-10-13', '11:00:00', 'DOP', 2),
('Atividade 3', 'Testes Automatizados', '2025-10-15', '15:30:00', 'MPS', 3),
('Atividade 4', 'Deploy em Produção', '2025-10-16', '16:00:00', 'DOP', 3);


