CREATE DATABASE IF NOT EXISTS livraria
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE livraria;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS itens_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

INSERT INTO produtos (nome, descricao, preco, estoque) VALUES
('Dom Casmurro', 'Romance clássico de Machado de Assis.', 39.90, 25),
('O Pequeno Príncipe', 'Conto filosófico de Antoine de Saint-Exupéry.', 29.90, 40),
('1984', 'Distopia de George Orwell.', 44.90, 18),
('A Revolução dos Bichos', 'Alegoria política de George Orwell.', 32.50, 30),
('Cem Anos de Solidão', 'Obra-prima de Gabriel García Márquez.', 54.90, 15),
('O Hobbit', 'Aventura de J.R.R. Tolkien.', 49.90, 22),
('Harry Potter e a Pedra Filosofal', 'Primeiro livro da saga de J.K. Rowling.', 42.00, 35),
('O Senhor dos Anéis: A Sociedade do Anel', 'Fantasia épica de J.R.R. Tolkien.', 59.90, 12),
('Orgulho e Preconceito', 'Romance de Jane Austen.', 36.90, 20),
('Crime e Castigo', 'Romance psicológico de Dostoiévski.', 47.50, 10),
('A Metamorfose', 'Conto de Franz Kafka.', 24.90, 28),
('Memórias Póstumas de Brás Cubas', 'Romance de Machado de Assis.', 38.00, 16);
