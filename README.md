Sistema de Gestão de Biblioteca (CRUD com Python e SQL)

Descrição:

Este projeto é um sistema completo de gestão de biblioteca desenvolvido em Python. A aplicação atua como um pipeline de dados e realiza operações CRUD (Create, Read, Update, Delete) completas, com armazenamento persistente em base de dados relacional e capacidade de gerar relatórios automáticos.

Habilidades e Tecnologias Aplicadas:

Integração Python e Banco de Dados (SQL): Uso nativo da biblioteca sqlite3 para criação e manipulação de tabelas, garantindo a rastreabilidade e segurança dos dados.
Análise e Relatórios (Pandas): Implementação de exportação automatizada do banco de dados para ficheiros Excel (.xlsx), facilitando a leitura gerencial dos acervos e empréstimos.
Arquitetura Modular (Engenharia de Software): Separação de responsabilidades com o código dividido em módulos (main.py para o motor do sistema e funcoes.py para a lógica de negócio), garantindo um código limpo e de fácil manutenção.
Tratamento de Exceções: Uso de blocos try/except para proteger a aplicação contra entradas inválidas e garantir a estabilidade do sistema.
Lógica de Relacionamentos: Cruzamento avançado de dados utilizando comandos SQL (UPDATE, DELETE, JOIN lógico) para gerir a disponibilidade dos livros e o histórico de retiradas através da biblioteca datetime.

Como Funciona o Sistema:

Módulo de Livros e Utilizadores: Permite o registo e a listagem do acervo e dos clientes.
Módulo de Empréstimos (Relacionamento): O sistema conecta um utilizador a um livro, regista o momento exato do empréstimo e atualiza automaticamente o status do livro para "Emprestado".
Módulo de Devolução: Remove o registo ativo e liberta o livro de volta para o acervo (Status: "Disponível").
Módulo Gerencial: Um único comando exporta todas as tabelas do SQL para um ficheiro Excel formatado.
