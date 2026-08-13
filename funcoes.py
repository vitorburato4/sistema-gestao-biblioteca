import pandas as pd
from datetime import datetime

def cadastrar_livro(cursor, conexao):
    print("\n>> Iniciando cadastro de livro...")
    try:
        titulo = input("Digite o título do livro: ")
        autor = input("Digite o autor: ")
        ano = input("Digite o ano de publicação: ")
        
        if titulo == "" or autor == "":
            print(">> Erro: O título e o autor não podem ficar em branco!")
            return 

        cursor.execute("INSERT INTO livros (titulo, autor, ano, status) VALUES (?, ?, ?, 'Disponível')", (titulo, autor, ano))
        conexao.commit()
        print(f"\n>> Sucesso! O livro '{titulo}' foi salvo.")
    except Exception as erro:
        print(f"\n>> Ops! Algo correu mal no banco de dados: {erro}")

def listar_livros(cursor):
    print("\n>> Listando acervo...")
    try:
        cursor.execute("SELECT * FROM livros")
        livros_db = cursor.fetchall()
        if len(livros_db) == 0:
            print("O acervo ainda está vazio no banco de dados.")
        else:
            for livro in livros_db:
                print(f"- ID {livro[0]}: {livro[1]} (Autor: {livro[2]} | Ano: {livro[3]}) -> Status: [{livro[4]}]")
    except Exception as erro:
        print(f"\n>> Erro ao procurar dados: {erro}")

def buscar_livro(cursor):
    print("\n>> Procurando livro...")
    try:
        termo_busca = input("Digite o título do livro: ")
        cursor.execute("SELECT * FROM livros WHERE titulo LIKE ?", ('%' + termo_busca + '%',))
        resultados = cursor.fetchall()
        
        if len(resultados) == 0:
            print("Nenhum livro encontrado com esse título.")
        else:
            for livro in resultados:
                print(f"- ENCONTRADO: ID {livro[0]} | {livro[1]} (Autor: {livro[2]}) -> Status: [{livro[4]}]")
    except Exception as erro:
        print(f"\n>> Erro ao procurar: {erro}")

def cadastrar_usuario(cursor, conexao):
    print("\n>> Iniciando cadastro de utilizador...")
    try:
        nome = input("Digite o nome do utilizador: ")
        telefone = input("Digite o telefone: ")
        
        if nome == "":
            print(">> Erro: O nome não pode ficar em branco!")
            return
            
        cursor.execute("INSERT INTO usuarios (nome, telefone) VALUES (?, ?)", (nome, telefone))
        conexao.commit()
        print(f"\n>> Sucesso! O utilizador '{nome}' foi cadastrado.")
    except Exception as erro:
        print(f"\n>> Erro no registo: {erro}")

def listar_usuarios(cursor):
    print("\n>> Listando utilizadores...")
    try:
        cursor.execute("SELECT * FROM usuarios")
        usuarios_db = cursor.fetchall()
        if len(usuarios_db) == 0:
            print("Nenhum utilizador cadastrado.")
        else:
            for user in usuarios_db:
                print(f"- ID {user[0]}: Nome: {user[1]} | Tel: {user[2]}")
    except Exception as erro:
        print(f"\n>> Erro na listagem: {erro}")

def realizar_emprestimo(cursor, conexao):
    print("\n>> Realizando Empréstimo...")
    try:
        nome_busca = input("Digite o nome do utilizador: ")
        titulo_busca = input("Digite o título do livro: ")
        
        cursor.execute("SELECT nome FROM usuarios WHERE nome LIKE ?", ('%' + nome_busca + '%',))
        user_db = cursor.fetchone() 
        
        cursor.execute("SELECT titulo FROM livros WHERE titulo LIKE ? AND status = 'Disponível'", ('%' + titulo_busca + '%',))
        livro_db = cursor.fetchone()
        
        if user_db != None and livro_db != None:
            nome_encontrado = user_db[0]
            titulo_encontrado = livro_db[0]
            data_agora = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            cursor.execute("INSERT INTO emprestimos (nome_usuario, titulo_livro, data_emprestimo) VALUES (?, ?, ?)", (nome_encontrado, titulo_encontrado, data_agora))
            cursor.execute("UPDATE livros SET status = 'Emprestado' WHERE titulo = ?", (titulo_encontrado,))
            conexao.commit()
            print(f"\n>> Sucesso! O livro '{titulo_encontrado}' foi emprestado para '{nome_encontrado}' em {data_agora}.")
        else:
            print("\n>> Erro: Utilizador não encontrado ou Livro já está emprestado/não existe.")
    except Exception as erro:
        print(f"\n>> Erro na transação: {erro}")

def listar_emprestimos(cursor):
    print("\n>> Listando Empréstimos Ativos...")
    try:
        cursor.execute("SELECT * FROM emprestimos")
        emprestimos_db = cursor.fetchall()
        if len(emprestimos_db) == 0:
            print("Nenhum livro está emprestado no momento.")
        else:
            for emp in emprestimos_db:
                print(f"- Empréstimo ID {emp[0]}: '{emp[2]}' com '{emp[1]}' (Retirado em: {emp[3]})")
    except Exception as erro:
        print(f"\n>> Erro: {erro}")

def devolver_livro(cursor, conexao):
    print("\n>> Realizando Devolução...")
    try:
        titulo_devolucao = input("Digite o título do livro que está a ser devolvido: ")
        cursor.execute("SELECT * FROM emprestimos WHERE titulo_livro LIKE ?", ('%' + titulo_devolucao + '%',))
        emp_db = cursor.fetchone()
        
        if emp_db != None:
            cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emp_db[0],))
            cursor.execute("UPDATE livros SET status = 'Disponível' WHERE titulo = ?", (emp_db[2],))
            conexao.commit()
            print(f"\n>> Sucesso! O livro '{emp_db[2]}' foi devolvido ao acervo e removido dos empréstimos ativos.")
        else:
            print("\n>> Erro: Este livro não consta na nossa lista de empréstimos ativos.")
    except Exception as erro:
        print(f"\n>> Erro na devolução: {erro}")

def exportar_excel(conexao):
    print("\n>> Gerando relatório formatado no Excel...")
    try:
        df_livros = pd.read_sql("SELECT * FROM livros", conexao)
        df_usuarios = pd.read_sql("SELECT * FROM usuarios", conexao)
        df_emprestimos = pd.read_sql("SELECT * FROM emprestimos", conexao)
        
       
        with pd.ExcelWriter('relatorio_biblioteca.xlsx', engine='xlsxwriter') as relatorio:
            df_livros.to_excel(relatorio, sheet_name='Livros', index=False)
            df_usuarios.to_excel(relatorio, sheet_name='Usuarios', index=False)
            df_emprestimos.to_excel(relatorio, sheet_name='Emprestimos', index=False)
            workbook = relatorio.book
            
            
            for sheet_name in ['Livros', 'Usuarios', 'Emprestimos']:
                worksheet = relatorio.sheets[sheet_name]
                worksheet.set_column('A:Z', 22)
            
            
        print(">> Sucesso! O arquivo 'relatorio_biblioteca.xlsx' foi salvo e formatado na sua pasta.")
    except Exception as e:
        print(f">> Erro ao gerar Excel. Detalhe: {e}")
       