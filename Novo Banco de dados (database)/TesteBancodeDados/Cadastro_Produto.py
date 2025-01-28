import sqlite3
import pandas as pd
import os
from Validacoes import validar_preco

# O arquivo do banco precisa ser consultado com o final '.db'
caminho_do_banco = r'C:\Users\Dev\Novo Banco de dados (database)\Dedetizadora Inovar.db'  # Podemos usar duas \\ invertidas aqui ou o r (string raw) para o Python não tratar a \ como prefixo de escape
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()

def Dados_Produto():
    # Função para cadastrar um novo produto

    while True:
        Nome = str(input('Nome do Produto (Máximo de 50 caracteres): '))
        if len(Nome) > 50:
            print('Muitos caracteres, diminua o nome')
        else:
            if len(Nome) <= 50:
                break

    while True:
        Descricao = str(input('Descrição do Produto (Máximo de 500 caracteres): '))
        if len(Descricao) > 500:
            print('Ultrapassado os 500 caracteres.')
        else:
            if len(Descricao) <= 500:
                break

    while True:
        try:
            preco = float(input('Preço do produto (formato: 10.99): '))
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
    consulta = '''INSERT INTO Produto (Nome, Descricao, Preco)
                  VALUES (?, ?, ?)'''

    # As variáveis substituem os ? (placeholders) na consulta SQL
    cursor.execute(consulta, (Nome, Descricao, preco))

    # Para confirmar as alterações no banco de dados
    conexao.commit()

    # Mensagem de sucesso
    print("Cadastro de produto realizado com sucesso!")

# Não feche a conexão e o cursor aqui, pois você pode querer usá-los em outro momento.
# Deixe a conexão aberta para o uso posterior, fechando-a no final do programa principal.
# conexao.close()


def mostrar_dados_produto():
    while True:
        try:
            opcao = input('1. Ver todos os Produtos \n2. Um produto em específico\n3. Exportar os dados para o Excel\n')

            if opcao not in ['1', '2', '3']:
                raise ValueError()  
            
            break  
    
        except ValueError:  
            resposta = input('Valor inválido. Deseja tentar novamente? [s - n]\n').upper()
            
            if resposta != 'S':
                break  # Sai do loop se o usuário não quiser tentar novamente

    if opcao == '1':  # Exibir todos os produtos
        consulta = 'SELECT * FROM Produto'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Recupera todos os produtos
        
        if dados:
            print("Dados dos Produtos")
            for linha in dados:
                print(f'ID_Produto: {linha[0]}, Nome: {linha[1]}, Descrição: {linha[2]}, Preço: {linha[3]}, Quantidade_Estoque: {linha[4]}')
        else:
            print('Nenhum dado encontrado na Tabela Produtos')

    if opcao == '2':  # Exibir um produto específico
        while True:
            try:
                numero_produto = int(input('Número do Produto (ID): \n'))
                consulta = 'SELECT * FROM Produto WHERE ID_Produto = ?'
                cursor.execute(consulta, (numero_produto,))  # #o segundo parametro fica assim e com a virgula para o python interpretalo como uma tupla. Ele precisa ser uma tupla.
                dados = cursor.fetchone()  # Recupera um produto específico
                
                if dados:  
                    print(f'ID_Produto: {dados[0]}, Nome: {dados[1]}, Descrição: {dados[2]}, Preço: {dados[3]}, Quantidade_Estoque: {dados[4]}')
                    break 

                else:
                    raise ValueError()  # Se não encontrar o produto, gera um erro
            
            except ValueError: 
                resposta = input('Valor inválido ou o Produto não existe. Deseja tentar novamente? [s - n]\n').upper()
                if resposta != 'S':
                    break  
    if opcao == '3':
        # Consulta para buscar todos os clientes
        consulta = 'SELECT * FROM Produto'
        cursor.execute(consulta)
        dados = cursor.fetchall()  # Retorna todos os dados como uma lista de listas
        
        if dados:
            # Chama a função para exportar os dados para um arquivo Excel
            exportar_dados_para_excel(dados, 'Dados_Produto.xlsx')
        else:
            print('Nenhum dado encontrado na Tabela Produtos')
        
    input('Pressione Enter para sair...\n')
    
def apagar_dados_produto():
    while True:
        try:
            apagar = int(input('Digite o ID do Produto que deseja apagar: '))

            # Primeiro, usamos o COUNT(*) para verificar se o Produto existe, se sim, ele irá retornar 1, se não, irá retornar 0. O dado vai para a variavel 'resultado'
            consulta_verificar = 'SELECT COUNT(*) FROM Produto WHERE ID_Produto = ?'
            cursor.execute(consulta_verificar, (apagar,))
            resultado = cursor.fetchone()

            if resultado[0] > 0:  # Se o produto existe, o resultado será maior que 0
                consulta = 'DELETE FROM Produto WHERE ID_Produto = ?'
                cursor.execute(consulta, (apagar,))
                conexao.commit()  # Confirma a mudança na tabela, pois iremos modificar ela
                print(f'Produto apagado.')
                break 
            else:
                print('Produto não encontrado')
                break

        except ValueError:
            print("Por favor, insira um número válido para o ID do Produto.")


def menu_produto():
    while True:
        try:
            escolha_produto = input('1. Cadastro de Produto \n2. Pesquisar Produtos \n3. Excluir dados de Produtos \n4. Voltar ao Menu Anterior\n')
        
            if escolha_produto.isdigit():
                escolha_produto = int(escolha_produto)
            
            if escolha_produto == 1:
                Dados_Produto()
            
            elif escolha_produto == 2:
                mostrar_dados_produto()
        
            elif escolha_produto == 3:
                apagar_dados_produto()
        
            elif escolha_produto == 4:
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
    
    
    # insinstance verifica se o primeiro parametro é uma lista (varios produtos) ou se não for é uma tupla (um produto). isso é feito através do fetchall e o fetchone
    if isinstance(dados, list):  # se for uma lista, as colunas serão essas.
        df = pd.DataFrame(dados, columns=['ID_Produto', 'Nome', 'Descrição', 'Preço', 'Quantidade'])   #df é o nome da variavel. DataFrame é a função que que organiza os dados em linhas e colunas
        #o segundo parametro é as colunas e os dados serão as linhas
    
    else:
        # Se for uma tupla (um único cliente), coloca a tupla dentro de uma lista
        # [dados] aqui dentro, transforma a tupla em lista, pois o pandas precisa de uma lista de listas ex:
         # Isso transforma:
        # dados = (1, '123456789', 'Rua A', '12345678', 'cliente1@email.com')
        # Em uma lista com uma linha:
        # [ (1, '123456789', 'Rua A', '12345678', 'cliente1@email.com') ]
        df = pd.DataFrame([dados], columns=['ID_Produto', 'Nome', 'Descrição', 'Preço', 'Quantidade'])
    
    # Exporta os dados para o arquivo Excel sem salvar o índice
    # O parâmetro index=False impede que a coluna de índice seja salva no arquivo
    df.to_excel(caminho_completo, index=False)
    print(f"Dados exportados para '{caminho_completo}'")
    