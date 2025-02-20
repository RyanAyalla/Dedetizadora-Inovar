import psycopg2

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "ryan1234",
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()


def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def entrar_conta():
    
    while True:
        
        cpf = input('CPF: ')
        senha = input('Senha: ')
        
        cursor.execute('SELECT senha_hash FROM usuarios WHERE CPF = %s', (cpf,))
        senha_hash = cursor.fetchone() 
    
        if senha_hash:   #se ele achar a senha desse cpf, ele vai comparar com a senha digitado no login
            
            cursor.execute("SELECT (senha_hash = crypt(%s, senha_hash)) FROM usuarios WHERE cpf = %s", (senha, cpf))
            senha_correta = cursor.fetchone() # crypt retorna valores booleanos no postegre e em python fetchone retorna uma tupla
            
            if senha_correta and senha_correta[0]:   # o [0] acessa o valor boleano dentro da tupla
                print('Entrando na conta...')
                input('')
                break  #sai de toda a função
            
            else:
                print('CPF ou Senha inválidos.')
    
        if not senha_hash:
            print('CPF ou senha Inválido.')

        