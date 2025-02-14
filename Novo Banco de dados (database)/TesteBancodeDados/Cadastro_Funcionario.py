import psycopg2
import pandas as pd
import os
from Validacoes import validar_telefone, validar_email

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "ryan1234",
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()

def Dados_Funcionario():
    # Função para cadastrar um novo funcionário

    while True:
        Nome = str(input('Nome do Funcionário (Máximo de 100 caracteres): '))
        if len(Nome) > 100:
            print('Muitos caracteres, diminua o nome')
        else:
            if len(Nome) <= 100:
                break

    while True:
        Cargo = str(input('Cargo do Funcionário (Máximo de 100 caracteres): '))
        if len(Cargo) > 100:
            print('Muitos caracteres, diminua o cargo')
        else:
            if len(Cargo) <= 100:
                break

    while True:
        Telefone = input('Telefone do Funcionário (Ex: (XX) XXXXX-XXXX): ')
        if validar_telefone(Telefone):
            break
        else:
            print('O número deve conter 11 dígitos numéricos.')

    while True:
        email = input('E-mail do Funcionário (Máximo de 100 caracteres): ')
        if validar_email(email):
            break
        else:
            print("E-mail inválido! Verifique o formato e o tamanho (máximo 100 caracteres).")

    # Inserindo os dados nas colunas da tabela
    consulta = '''INSERT INTO funcionarios (nome, cargo, telefone, email)
                  VALUES (%s, %s, %s, %s)'''

    # As variáveis substituem os ? (placeholders) na consulta SQL
    cursor.execute(consulta, (Nome, Cargo, Telefone, email))
    cursor.connection.commit()
    
    
def mostrar_dados_funcionarios():
    while True:
        try:
            opcao = input('1.Buscar todos os Funcionários. \n2.Buscar um Funcionário em específico. \n3.Exportar dados para o Excel \n')

            if opcao not in ['1', '2', '3']:
                raise ValueError()  
            
            break  
    
        except ValueError:  
            resposta = input('Valor inválido. Deseja tentar novamente? [s - n]\n').upper()
            
            if resposta != 'S':
                break

    if opcao == '1':  
        consulta = 'SELECT * FROM funcionarios'
        cursor.execute(consulta)
        dados = cursor.fetchall()  
        
        if dados:
            print("Dados dos Funcionarios")
            for linha in dados:
                print(f'ID_Funcionario: {linha[0]}, Nome: {linha[1]}, Cargo: {linha[2]}, Telefone: {linha[3]}, Email: {linha[4]}')
        else:
            print('Nenhum dado encontrado na Tabela de Funcionários')

    if opcao == '2':  
        while True:
            try:
                numero_produto = int(input('Número do Funcionario (ID): \n'))
                consulta = 'SELECT * FROM Funcionarios WHERE ID_Funcionario = %s'
                cursor.execute(consulta, (numero_produto,))  # #o segundo parametro fica assim e com a virgula para o python interpretalo como uma tupla. Ele precisa ser uma tupla.
                dados = cursor.fetchone()  # Recupera um Funcionario em específico
                
                if dados:  #aqui usamos dados ao inves de linha, pois é um dados de uma liha, não varias linhas com varios dados como lá em cima
                    print(f'ID_Funcionario: {dados[0]}, Nome: {dados[1]}, Cargo: {dados[2]}, Telefone: {dados[3]}, Email: {dados[4]}')
                    break 

                else:
                    raise ValueError()
            
            except ValueError: 
                
                resposta = input('Valor inválido ou o Funcionário não existe. Deseja tentar novamente? [s - n]\n').upper()
                if resposta != 'S':
                    break  
    if opcao == '3':
    # Consulta para buscar todos os clientes
        consulta = 'SELECT * FROM funcionarios'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Retorna todos os dados como uma lista de listas
        
        if dados:
            # Chama a função para exportar os dados para um arquivo Excel
            exportar_dados_para_excel(dados, 'Dados_Funcionários.xlsx')
        else:
            print('Nenhum dado encontrado na Tabela Funcionários')
        
    input('Pressione Enter para sair...\n')

def apagar_dados_funcionarios():
    while True:
        try:
            apagar = int(input('Digite o ID do Funcionario que deseja apagar: '))

            # Primeiro, usamos o COUNT(*) para verificar se o Funcionário existe, se sim, ele irá retornar 1, se não, irá retornar 0. O dado vai para a variavel 'resultado'
            consulta_verificar = 'SELECT COUNT(*) FROM funcionarios WHERE id_funcionario = %s'
            cursor.execute(consulta_verificar, (apagar,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:  # Se o Funcionario existe, o resultado será maior que 0
                consulta = 'DELETE FROM funcionarios WHERE id_funcionario = %s'
                cursor.execute(consulta, (apagar,))
                cursor.connection.commit()  # Confirma a mudança na tabela, pois iremos modificar ela
                print(f'Funcionário apagado.')
                break 
            else:
                print('Funcionário não encontrado')
                break

        except ValueError:
            print("Por favor, insira um número válido para o ID do Funcionário.")
            
            
def menu_funcionarios():
    while True:
        try:
            escolha_funcionario = input('1. Cadastro de Funcionário \n2. Pesquisar Funcionários \n3. Excluir dados de Funcionários \n4. Voltar ao Menu Anterior\n')
        
            if escolha_funcionario.isdigit():
                escolha_funcionario = int(escolha_funcionario)
            
            if escolha_funcionario == 1:
                Dados_Funcionario()
            
            elif escolha_funcionario == 2:
                mostrar_dados_funcionarios()
        
            elif escolha_funcionario == 3:
                apagar_dados_funcionarios()
        
            elif escolha_funcionario == 4:
                return                              #return sozinho retorna none. Tem uma difereça dele para o break. Mas ele interrompe todo o fluxo
        
            else:
                print('Opção inválida')

        except ValueError:
            ('Valor inválido. Tente Novamente.')
    
        
def exportar_dados_para_excel(dados, nome_arquivo):
    
    # Exemplo de caminho absoluto
    caminho_diretorio = r'C:\Users\Dev\Novo Banco de dados (database)\TesteBancodeDados\Planilhas'  # o arquivo tem que ser salvo onde ele tenha a permissão de modificar os arquivos, se não será negado na hora de salvar
    
    if not os.path.exists(caminho_diretorio):  #função que verifica se algo existe 
        os.makedirs(caminho_diretorio)  # Cria o diretório se ele não existir
    
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo) #essa variavel caminho_completo precisa ser definida antesda linha df.to_excel() para que o caminho seja definido antes de usar 
    
    
    # insinstance verifica se o primeiro parametro é uma lista (varios clientes) ou se não for é uma tupla (um cliente). isso é feito através do fetchall e o fetchone
    if isinstance(dados, list):  # se for uma lista, as colunas serão essas.
        df = pd.DataFrame(dados, columns=['ID_Funcionários', 'Nome', 'Cargo', 'Telefone', 'Email'])   #df é o nome da variavel. DataFrame é a função que que organiza os dados em linhas e colunas
        #o segundo parametro é as colunas e os dados serão as linhas
    
    else:
        df = pd.DataFrame([dados], columns=['ID_Funcionários', 'Nome', 'Cargo', 'Telefone', 'Email'])
    
    # Exporta os dados para o arquivo Excel sem salvar o índice
    # O parâmetro index=False impede que a coluna de índice seja salva no arquivo
    df.to_excel(caminho_completo, index=False)
    print(f"Dados exportados para '{caminho_completo}'")