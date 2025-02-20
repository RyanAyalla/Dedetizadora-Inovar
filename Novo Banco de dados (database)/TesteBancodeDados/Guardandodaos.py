import tkinter as tk
from tkinter import messagebox
import bcrypt


def validar_cpf(cpf):
    """Valida se o CPF tem 11 dígitos."""
    return len(cpf) == 11 and cpf.isdigit()

def validar_senha(senha):
    """Valida se a senha tem pelo menos 6 caracteres."""
    return len(senha) >= 6

def criar_conta(cpf, senha):
    """Cria uma conta com CPF e senha válidos."""
    if not validar_cpf(cpf):
        return "CPF inválido! Deve ter exatamente 11 dígitos."
    
    if not validar_senha(senha):
        return "Senha inválida! Deve ter pelo menos 6 caracteres."
    
    # Gera o hash da senha
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    # Simula o cadastro no banco de dados
    print(f"Usuário cadastrado com CPF: {cpf} e Senha Hash: {senha_hash.decode('utf-8')}")
    return "Cadastro realizado com sucesso!"
# Função chamada quando o botão "Cadastrar" é clicado
def cadastrar():
    cpf = entry_cpf.get()
    senha = entry_senha.get()
    
    resultado = criar_conta(cpf, senha)
    messagebox.showinfo("Resultado", resultado)

# Configuração da janela
janela = tk.Tk()
janela.title("Cadastro de Usuário")

# Campos de entrada
label_cpf = tk.Label(janela, text="CPF:")
label_cpf.grid(row=0, column=0, padx=10, pady=10)
entry_cpf = tk.Entry(janela)
entry_cpf.grid(row=0, column=1, padx=10, pady=10)

label_senha = tk.Label(janela, text="Senha:")
label_senha.grid(row=1, column=0, padx=10, pady=10)
entry_senha = tk.Entry(janela, show="*")  # Oculta a senha
entry_senha.grid(row=1, column=1, padx=10, pady=10)

# Botão de cadastro
botao_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar)
botao_cadastrar.grid(row=2, column=0, columnspan=2, pady=10)

# Inicia a interface
janela.mainloop()