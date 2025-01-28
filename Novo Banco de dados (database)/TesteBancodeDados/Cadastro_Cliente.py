import sqlite3
import pandas as pd
import os
from Validacoes import validar_telefone, validar_email, validar_cnpj, validar_cpf

# O arquivo do banco precisa ser consultado com o final '.db'
caminho_do_banco = r'C:\Users\Dev\Novo Banco de dados (database)\Dedetizadora Inovar.db'  # Podemos usar duas \\ invertidas aqui ou o r (string raw) para o Python não tratar a \ como prefixo de escape

# Conexão com o banco de dados
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()

def Dados_Cliente():

    while True:
        Nome = str(input('Nome do Cliente (Máximo de 100 caracteres): '))
        if len(Nome) > 100:
            print('Muitos caracteres, diminua o nome')
        else:
            if len(Nome) <= 100:
                break

    while True:
        Endereco = str(input('Endereço do Cliente (Máximo de 100 caracteres): '))
        if len(Endereco) > 100:
            print('Muitos caracteres, diminua o Endereço')
        else:
            if len(Endereco) <= 100:
                break

    while True:
        Telefone = input('Telefone do Cliente (Ex: (XX) XXXXX-XXXX): ')
        if validar_telefone(Telefone):
            break
        else:
            print('O número deve conter 11 dígitos numéricos.')

    while True:
        email = input('E-mail do Cliente (Máximo de 100 caracteres): ')
        if validar_email(email):
            break
        else:
            print("E-mail inválido! Verifique o formato e o tamanho (máximo 100 caracteres).")

    while True:
        CPF_CNPJ = input('CPF/CNPJ: ')
        if validar_cpf(CPF_CNPJ):  # Não se coloca == 11 aqui por exemplo, pois o que retorna é True ou False
            break
        else:
            if validar_cnpj(CPF_CNPJ):
                break
            else:
                print('CPF ou CNPJ incorretos, digite novamente.')

    # Inserindo os dados nas colunas da tabela
    consulta = '''INSERT INTO Cliente (Nome, CPF_CNPJ, Endereco, Telefone, Email)
                  VALUES (?, ?, ?, ?, ?)'''

    # As variáveis substituem os ? (placeholders) na consulta SQL
    cursor.execute(consulta, (Nome, CPF_CNPJ, Endereco, Telefone, email))
    conexao.commit()
    print("Cadastro de Cliente realizado com sucesso!")
    
    input('Pressione Enter para sair...\n')
    
    
    
    

def mostrar_dados_cliente():
    while True:
        try:
            opcao = input('1.Buscar todos os Clientes. \n2.Buscar um Cliente em específico.\n3.Exportar os dados para o Excel.\n')

            if opcao not in ['1', '2', '3']:
                raise ValueError()  
            
            break  
    
        except ValueError:  
            resposta = input('Valor inválido. Deseja tentar novamente? [s - n]\n').upper()
            
            if resposta != 'S':
                break  # Sai do loop se o usuário não quiser tentar novamente

    if opcao == '1':  
        consulta = 'SELECT * FROM Cliente'
        cursor.execute(consulta)
        dados = cursor.fetchall()  
        
        if dados:
            print("Dados dos Clientes")
            for linha in dados:
                print(f'ID_Cliente: {linha[0]}, CPF/CNPJ: {linha[1]}, Endereço: {linha[2]}, Telefone: {linha[3]}, Email: {linha[4]}')
        else:
            print('Nenhum dado encontrado na Tabela Clientes')

    if opcao == '2':  
        while True:
            try:
                numero_produto = int(input('Número do Cliente (ID): \n'))
                consulta = 'SELECT * FROM Cliente WHERE ID_Cliente = ?'
                cursor.execute(consulta, (numero_produto,))  # #o segundo parametro fica assim e com a virgula para o python interpretalo como uma tupla. Ele precisa ser uma tupla.
                dados = cursor.fetchone()  # Recupera um Cliente em específico
                
                if dados:  #aqui usamos dados ao inves de linha, pois é um dados de uma liha, não varias linhas com varios dados como lá em cima
                    print(f'ID_Cliente: {dados[0]}, CPF/CNPJ: {dados[1]}, Endereço: {dados[2]}, Telefone: {dados[3]}, Email: {dados[4]}')
                    break 

                else:
                    raise ValueError()  # Se não encontrar o cliente, gera um erro
            
            except ValueError as e: 
                
                resposta = input('Valor inválido ou o Cliente não existe. Deseja tentar novamente? [s - n]\n').upper()
                if resposta != 'S':
                    break  
        
    if opcao == '3':
        # Consulta para buscar todos os clientes
        consulta = 'SELECT * FROM Cliente'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Retorna todos os dados como uma lista de listas
        
        if dados:
            # Chama a função para exportar os dados para um arquivo Excel
            exportar_dados_para_excel(dados, 'Dados_Clientes.xlsx')
        else:
            print('Nenhum dado encontrado na Tabela Clientes')
        
    input('Pressione Enter para sair...\n')


def apagar_dados_cliente():
    while True:
        try:
            apagar = int(input('Digite o ID do Cliente que deseja apagar: '))

            # Primeiro, usamos o COUNT(*) para verificar se o Cliente existe, se sim, ele irá retornar 1, se não, irá retornar 0. O dado vai para a variavel 'resultado'
            consulta_verificar = 'SELECT COUNT(*) FROM Cliente WHERE ID_Cliente = ?'
            cursor.execute(consulta_verificar, (apagar,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:  # Se o Cliente existe, o resultado será maior que 0
                consulta = 'DELETE FROM Cliente WHERE ID_Cliente = ?'
                cursor.execute(consulta, (apagar,))
                conexao.commit()  # Confirma a mudança na tabela, pois iremos modificar ela
                print(f'Cliente apagado.')
                break 
            else:
                print('Cliente não encontrado')
                break

        except ValueError:
            print("Por favor, insira um número válido para o ID do Cliente.")
            
    input('Pressione Enter para sair...')
        
        
def menu_cliente():
    while True:
        try:
            escolha_cliente = input('1. Cadastro de Clientes \n2. Pesquisar Clientes \n3. Excluir dados de Clientes \n4. Voltar ao Menu Anterior\n')
        
            if escolha_cliente.isdigit():
                escolha_cliente = int(escolha_cliente)
            
            if escolha_cliente == 1:
                Dados_Cliente()
            
            elif escolha_cliente == 2:
                mostrar_dados_cliente()
        
            elif escolha_cliente == 3:
                apagar_dados_cliente()
        
            elif escolha_cliente == 4:
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
    
    # Adiciona o nome do arquivo ao caminho do diretório SUUUUUUUPER IMPORTANTE ESSE AQUI, PARA SALVAR NA PASTA CORRETA COM OS DADOS, O CAMINHO E A VARIAVEL CAMINHO_COMPLETO QUE VAI REPRESENTAR ELES.
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo) #essa variavel caminho_completo precisa ser definida antesda linha df.to_excel() para que o caminho seja definido antes de usar 
    
    
    # insinstance verifica se o primeiro parametro é uma lista (varios clientes) ou se não for é uma tupla (um cliente). isso é feito através do fetchall e o fetchone
    if isinstance(dados, list):  # se for uma lista, as colunas serão essas.
        df = pd.DataFrame(dados, columns=['ID_Cliente', 'Nome', 'CPF_CNPJ', 'Endereco', 'Telefone', 'Email'])   #df é o nome da variavel. DataFrame é a função que que organiza os dados em linhas e colunas
        #o segundo parametro é as colunas e os dados serão as linhas
    
    else:
        # Se for uma tupla (um único cliente), coloca a tupla dentro de uma lista
        # [dados] aqui dentro, transforma a tupla em lista, pois o pandas precisa de uma lista de listas ex:
         # Isso transforma:
        # dados = (1, '123456789', 'Rua A', '12345678', 'cliente1@email.com')
        # Em uma lista com uma linha:
        # [ (1, '123456789', 'Rua A', '12345678', 'cliente1@email.com') ]
        df = pd.DataFrame([dados], columns=['ID_Cliente', 'Nome', 'CPF_CNPJ', 'Endereco', 'Telefone', 'Email'])
    
    # Exporta os dados para o arquivo Excel sem salvar o índice
    # O parâmetro index=False impede que a coluna de índice seja salva no arquivo
    df.to_excel(caminho_completo, index=False)
    print(f"Dados exportados para '{caminho_completo}'")
    