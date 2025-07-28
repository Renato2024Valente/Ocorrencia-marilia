CREATE DATABASE IF NOT EXISTS ocorrencias;
USE ocorrencias;
CREATE TABLE IF NOT EXISTS registros (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nomeAluno VARCHAR(255),
  serie VARCHAR(50),
  professor VARCHAR(255),
  assinatura VARCHAR(255),
  descricao TEXT,
  ocorrencias TEXT,
  dataHora DATETIME DEFAULT CURRENT_TIMESTAMP
);