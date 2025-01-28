import sqlite3
import pandas as pd
import os
from Validacoes import validar_preco

# O arquivo do banco precisa ser consultado com o final '.db'
caminho_do_banco = r'C:\Users\Dev\Novo Banco de dados (database)\Dedetizadora Inovar.db'
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()

def Dados_Servico():
    # Função para cadastrar um novo serviço

    while True:
        Tipo = str(input('Tipo de Serviço (Máximo 100 caracteres): '))
        if len(Tipo) > 100:
            print('Muitos caracteres, diminua o texto')
        else:
            if len(Tipo) <= 100:
                break

    while True:
        Descricao = str(input('Descrição do Serviço (Máximo 500 caracteres): '))
        if len(Descricao) > 500:
            print('Ultrapassado os 500 caracteres.')
        else:
            if len(Descricao) <= 500:
                break

    while True:
        try:
            preco = float(input('Preço do serviço (formato: 10.99): '))
            # Verificar se o preço é maior que 0
            if preco < 0:
                print('O preço deve ser maior que 0.')
            else:
                # Validar o preço com a função
                if validar_preco(preco):
                    break  # Sai do loop quando o preço está válido
        except ValueError:
            print('Valor inválido. Digite um valor válido para o preço.')

    # Inserindo os dados nas colunas da tabela
    consulta = '''INSERT INTO Servico (Tipo, Descricao, Preco)
                  VALUES (?, ?, ?)'''

    # As variáveis substituem os ? (placeholders) na consulta SQL
    cursor.execute(consulta, (Tipo, Descricao, preco))
    conexao.commit()
    
    
def mostrar_dados_servico():
    while True:
        try:
            opcao = input('1. Ver todos os Serviços \n2. Serviço em específico \n3. Exportar dados para o Excel \n')

            if opcao not in ['1', '2', '3']:
                raise ValueError()  
            
            break  
    
        except ValueError:  
            resposta = input('Valor inválido. Deseja tentar novamente? [s - n]\n').upper()
            
            if resposta != 'S':
                break  # Sai do loop se o usuário não quiser tentar novamente

    if opcao == '1':  # Exibir todos os servicos
        consulta = 'SELECT * FROM Servico'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Recupera todos os serviços
        
        if dados:
            print("Dados de Serviços")
            for linha in dados:
                print(f'ID_Servico: {linha[0]}, Tipo: {linha[1]}, Descrição: {linha[2]}, Preço: {linha[3]}')
        else:
            print('Nenhum dado encontrado na Tabela Serviço')

    if opcao == '2':  # Exibir um serviço específico
        while True:
            try:
                numero_produto = int(input('Número do Serviço (ID): \n'))
                consulta = 'SELECT * FROM Servico WHERE ID_Servico = ?'
                cursor.execute(consulta, (numero_produto,))  #o segundo parametro fica assim e com a virgula para o python interpretalo como uma tupla. Ele precisa ser uma tupla.
                dados = cursor.fetchone()  # Recupera um serviço específico
                
                if dados:  
                    print(f'ID_Servico: {dados[0]}, Tipo: {dados[1]}, Descrição: {dados[2]}, Preço: {dados[3]}')
                    break 

                else:
                    raise ValueError()  # Se não encontrar o serviço, gera um erro
            
            except ValueError: 
                resposta = input('Valor inválido ou o Serviço não existe. Deseja tentar novamente? [s - n]\n').upper()
                if resposta != 'S':
                    break  
    if opcao == '3':
        # Consulta para buscar todos os clientes
        consulta = 'SELECT * FROM Servico'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Retorna todos os dados como uma lista de listas
        
        if dados:
            # Chama a função para exportar os dados para um arquivo Excel
            exportar_dados_para_excel(dados, 'Dados_Serviço.xlsx')
        else:
            print('Nenhum dado encontrado na Tabela Serviços')
        
    input('Pressione Enter para sair...\n')
    
def apagar_dados_servico():
    while True:
        try:
            apagar = int(input('Digite o ID do Serviço que deseja apagar: '))

            # Primeiro, usamos o COUNT(*) para verificar se o Serviço existe, se sim, ele irá retornar 1, se não, irá retornar 0. O dado vai para a variavel 'resultado'
            consulta_verificar = 'SELECT COUNT(*) FROM Servico WHERE ID_Servico = ?'
            cursor.execute(consulta_verificar, (apagar,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:  # Se o Serviço existe, o resultado será maior que 0
                consulta = 'DELETE FROM Servico WHERE ID_Servico = ?'
                cursor.execute(consulta, (apagar,))
                conexao.commit()  # Confirma a mudança na tabela, pois iremos modificar ela
                print('Serviço apagado.')
                break 
            else:
                print('Serviço não encontrado')
                break

        except ValueError:
            print("Por favor, insira um número válido para o ID do Serviço.")
        
        
def menu_servico():
    while True:
        try:
            escolha_servico = input('1. Cadastro de Serviços \n2. Pesquisar Serviços \n3. Excluir dados de Serviços \n4. Voltar ao Menu Anterior\n')
        
            if escolha_servico.isdigit():
                escolha_servico = int(escolha_servico)
            
            if escolha_servico == 1:
                Dados_Servico()
            
            elif escolha_servico == 2:
                mostrar_dados_servico()
        
            elif escolha_servico == 3:
                apagar_dados_servico()
        
            elif escolha_servico == 4:
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
    
    caminho_completo = os.path.join(caminho_diretorio, nome_arquivo)
    
    if isinstance(dados, list):  # se for uma lista, as colunas serão essas.
        df = pd.DataFrame(dados, columns=['ID_Serviço', 'Tipo', 'Descrição', 'Preço'])   #df é o nome da variavel. DataFrame é a função que que organiza os dados em linhas e colunas
        #o segundo parametro é as colunas e os dados serão as linhas
    
    else:
        
        df = pd.DataFrame([dados], columns=['ID_Serviço', 'Nome', 'Descrição', 'Preço'])
    
    # Exporta os dados para o arquivo Excel sem salvar o índice
    # O parâmetro index=False impede que a coluna de índice seja salva no arquivo
    df.to_excel(caminho_completo, index=False)
    print(f"Dados exportados para '{caminho_completo}'")
    