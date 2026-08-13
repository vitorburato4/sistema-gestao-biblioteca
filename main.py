import sqlite3
from funcoes import *

conexao = sqlite3.connect('biblioteca.db')
cursor = conexao.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, autor TEXT, ano TEXT, status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, telefone TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS emprestimos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT, titulo_livro TEXT, data_emprestimo TEXT)''')
conexao.commit()

while True:
    print("\n" + "="*30)
    print("      SISTEMA DE BIBLIOTECA      ")
    print("="*30)
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Buscar livro")
    print("4 - Cadastrar utilizador")
    print("5 - Listar utilizadores")
    print("6 - Realizar empréstimo")
    print("7 - Listar empréstimos")
    print("8 - Devolver livro")
    print("9 - Exportar para Excel")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ")
    
    match opcao:

        case "1": cadastrar_livro(cursor, conexao)
        case "2": listar_livros(cursor)
        case "3": buscar_livro(cursor)
        case "4": cadastrar_usuario(cursor, conexao)
        case "5": listar_usuarios(cursor)
        case "6": realizar_emprestimo(cursor, conexao)
        case "7": listar_emprestimos(cursor)
        case "8": devolver_livro(cursor, conexao)
        case "9": exportar_excel(conexao)
        case "0":
            print("\n>> A encerrar o sistema. Volte sempre!")
            conexao.close() 
            break 
        case _:
            print("\n>> Opção inválida! Digite um número do menu.")