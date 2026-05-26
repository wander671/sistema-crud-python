# IMPORTAÇÕES
import tkinter as tk # importando a biblioteca Tkinter para criar a interface gráfica
from tkinter import ttk # importando o módulo ttk para usar widgets mais avançados
from tkinter import messagebox # importando o módulo messagebox para exibir mensagens de alerta
import sqlite3 # importando a biblioteca sqlite3 para trabalhar com banco de dados SQLite

# BANCO DE DADOS
conn = sqlite3.connect("cadastro.db") # Conecta ao banco de dados (ou cria se não existir)
cursor = conn.cursor() # Cria um cursor para executar comandos SQL
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    email TEXT NOT NULL
)""") # Cria a tabela "usuarios" se ela não existir
conn.commit() # Salva as alterações no banco de dados

# CRIAR JANELA PRINCIPAL
janela = tk.Tk()# Cria a janela principal da aplicação 
janela.title("cadastro de usuários") # Define o título da janela
janela.geometry("400x300") # Define o tamanho da janela
janela.config(bg="#f0f0f0") # Define a cor de fundo da janela

# CAMPOS:NOME
label_nome = tk.Label(janela, text="Nome:", bg="#f0f0f0") # Cria um rótulo para o campo "nome"
label_nome.pack(pady=5) # Adiciona o rótulo á janela com um espaçamento vertical de 5 pixels

entry_nome = tk.Entry(janela) # Cria um campo de entrada para o nome
entry_nome.pack(pady=5) # Adiciona o campo de entrada á janela com um espaçamento vertical de 5 pixels

# CAMPOS: IDADE
label_idade = tk.Label(janela, text="Idade:", bg="#f0f0f0") # Cria um rótulo para o campo idade
label_idade.pack(pady=5) # Adiciona o rótulo á janela com um espaçamento vertical de 5 pixels

entry_idade = tk.Entry(janela) # Cria um campo de entrada para a idade
entry_idade.pack(pady=5) # Adiciona o campo de entrada á janela com um espaçamento vertical de 5 pixels

# CAMPOS: EMAIL
label_email = tk.Label(janela, text="Email:", bg="#f0f0f0") # Cria um rótulo para o campo email
label_email.pack(pady=5) # Adiciona o rótulo á janela com um espaçamento vertical de 5 pixels

entry_email = tk.Entry(janela) # Cria um campo de entrada para o email
entry_email.pack(pady=5) # Adiciona o campo de entrada á janela com um espaçamento vertical de 5 pixels

# TABELA VISUAL ( Essa parte mostra os usuários cadastrados )
tabela = ttk. Treeview(janela, columns=("id", "nome", "idade", "email"), show="headings") # Cria uma tabela para exibir os usuários cadastrados

tabela.heading("id", text="ID") # Define o título da coluna "id" na tabela
tabela.heading("nome", text="Nome")# Define o título da coluna "nome" na tabela
tabela.heading("idade", text="Idade") # Define o título da coluna "idade" na tabela
tabela.heading("email", text="Email") # Define o título da coluna "email" na tabela

tabela.pack(pady=10) # Adiciona a tabela á janela com um espaçamento vertical de 10 pixels

# FUNÇÂO LISTAR USUÁRIOS
def listar_usuarios():

    # LIMPAR TABELA
    for item in tabela.get_children(): # Itera sobre os itens da tabela
        tabela.delete(item) # Limpa a tabela antes de listar os usuários
    
    # BUSCAR DADOS
    cursor.execute("SELECT * FROM usuarios") # Executa uma consulta SQL para selecionar todos os usuários
    usuarios = cursor.fetchall() # Armazena os resultados da consulta em uma variável

    # INSERIR NA TABELA
    for usuario in usuarios: # Itera sobre os usuários obtidos do banco de dados
        tabela.insert("", "end", values=usuario) # Insere cada usuário na tela

# FUNÇÂO CADASTRAR USUÁRIO  
def cadastrar():
    nome = entry_nome.get() # Obtém o valor do campo de entrada "nome"
    idade = entry_idade.get() # Obtém o valor do campo de entrada "idade"
    email = entry_email.get() # Obtém o valor do campo de entrada "email"

    if nome and idade and email: # Verifica se todos os campos foram preenchidos

        cursor.execute("""INSERT INTO usuarios (nome, idade, email) VALUES (?, ?, ?)""", (nome, idade, email)) # Insere um novo usuário no banco de dados

        conn.commit() # Salva as alteraçôes no banco de dados

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!") # Exibe uma mensagem de sucesso

        limpar_campos() # Limpar os campos de entrada

        listar_usuarios() # Atualiza a tabela com os usuários cadastrados

# FUNÇÂO LIMPAR CAMPOS
def limpar_campos():
    entry_nome.delete(0, tk.END) # Limpa o campo de entrada "nome"
    entry_idade.delete(0, tk.END) # Limpa o campo de entrada "idade"
    entry_email.delete(0, tk.END) # Limpa o campo de entrada "email"

# SELECIONAR ITEM (QUANDO O USUÁRIO CLICA EM UM ITEM DA TABELA)
def selecionar_usuario(event):

    item = tabela.selection() # Obtém o item selecionado na tabela
    if item: # Verificar se um item foi selecionado
        dados = tabela.item(item[0], "values") # Obtém os dados do item selecionado
        
        entry_nome.delete(0, tk.END) # Limpa o campo de entrada "nome"
        entry_nome.insert(0, dados [1]) # Insere o nome do usuário selecionado no campo de entrada "nome"

        entry_idade.delete(0, tk.END) # Limpa o campo de entrada "idade"
        entry_idade.insert(0, dados [2]) # Insere a idade do usuário selecionado no campo de entrada "idade"

        entry_email.delete(0, tk.END) # Limpa o campo de entrada "email"
        entry_email.insert(0, dados [3]) # Insere o email do usuário selecionado no campo de entrada "email"

tabela.bind("<ButtonRelease-1>", selecionar_usuario) # Associa o evento de clique na tabela à função selecionar_usuario

# ATUALIZAR USUÁRIO
def atualizar():

    item = tabela.selection() # Obtém o item selecionado na tabela
    if not item: # Verifica se nenhum item foi selecionado
        messagebox.showerror("Erro", "Selecione um usuário para atualizar!") # Exibe uma mensagem de erro
        return
    
    id_usuario = tabela.item(item[0], "values")[0]  # Obtém o ID do usuário selecionado
    nome = entry_nome.get() # Obtém o valor do campo de entrada "nome"
    idade = entry_idade.get() # Obtém o valor do campo de entrada "idade"
    email = entry_email.get() # Obtém o valor do campo de entrada "email"

    cursor.execute("""UPDATE usuarios SET nome = ?, idade = ?, email = ? WHERE id = ?""", (nome, idade, email, id_usuario)) # Atualiza os dados do usuário no banco de dados

    conn.commit() # Salva as alterações no banco de dados

    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!") # Exibe uma mensagem de secesso

    listar_usuarios() # Atualiza a tabela com os usuários cadastrados

    limpar_campos() # Limpa os campos de entrada

# DELETAR USUÁRIO
def deletar():

    item = tabela.selection() # Obtém o item selecionado na tabela
    if not item: # Verifica se nenhum item foi selecionado
        messagebox.showerror("Erro", "Selecione um usuário para deletar!") # Exibe uma mensagem de erro
        return
    
    id_usuario = tabela.item(item[0], "values")[0] # Obtém o ID do usuário selecionado

    cursor.execute("""DELETE FROM usuarios WHERE id = ?""", (id_usuario,)) # Deleta o usuário do banco de dados


    conn.commit() # Salva as alterações no banco de dados

    messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!") # Exibe uma mensagem de sucesso

    listar_usuarios() # Atualiza a tabela com os usuários cadastrados

    limpar_campos() # Limpa os campos de entrada

# BOTÕES
frame_botoes = tk.Frame(janela, bg="#f0f0f0") # Cria um frame para os botões
frame_botoes.pack(pady=10) # Adiciona o frame à janela com um espaçamento vertical de 10 pixels

btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar) # Cria um botão para cadastrar usuários
btn_cadastrar.pack(side=tk.LEFT, padx=5) # Adiciona o botão ao frame com um espaçamento horizontal de 5 pixels

btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar) # Cria um botão para atualizar usuarios
btn_atualizar.pack(side=tk.LEFT, padx=5) # Adiciona o botão ao frame com um espaçamento horizontal de 5 pixels

btn_deletar = tk.Button(frame_botoes, text="Deletar", command=deletar) # Cria um botão para deletar usuarios
btn_deletar.pack(side=tk.LEFT, padx=5) # Adiciona o botão ao frame com um espaçamento horizontal de 5 pixels

# INICIAR LISTAR

listar_usuarios() # Chama a função listar_usuarios para exibir os usuários cadastrados na tabela

# LOOP PRINCIPAL
janela.mainloop() # Inicia o loop principal da aplicação para exibir a janela e aguardar interações do usuário
