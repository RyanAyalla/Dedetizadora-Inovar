import psycopg2
import os
import pandas as pd
from datetime import datetime
from Validacoes import validar_preco


conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "ryan1234",
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()

def Menu_Atendimento():
    while True:
        escolha_atendimento = input('1. Novo Atendimento \n2. Exportar Dados para o Excel \n3. Menu Anterior \n')
        
        if escolha_atendimento.isdigit():  # Verifica se a entrada é numérica
            escolha_atendimento = int(escolha_atendimento)
            
            if escolha_atendimento == 1:
                Registrar_Atendimento()
                
            elif escolha_atendimento == 2:
                Exportar_Dados_Excel()
            
            elif escolha_atendimento == 3:
                return
            
            else:
                print('Opção Inválida')
        else:
            print('Valor Inválido, tente novamente.')
                
                

def Registrar_Atendimento():
    
    #qual serviço será prestado
    while True:
        try:
            id_servico = int(input('Digite o ID do Serviço prestado: '))
            consulta_servico = 'SELECT * FROM servico WHERE id_servico = %s'
            cursor.execute(consulta_servico, (id_servico,))
            servico = cursor.fetchone()
            if servico:
                break
            else:
                print("Serviço não encontrado.")
        except ValueError:
            print("ID inválido. Tente novamente.")
    
    #qual funcionário fará o serviço
    while True:
        try:
            id_funcionario = int(input('Digite o ID do Funcionário que prestará o serviço: '))
            consulta_servico = 'SELECT * FROM funcionarios WHERE id_funcionario = %s'
            cursor.execute(consulta_servico, (id_funcionario,))
            funcionario = cursor.fetchone()
            if funcionario:
                break
            else:
                print("Funcionário não encontrado.")
        except ValueError:
            print("ID inválido. Tente novamente.")
            
            
    #o serviço será prestado para qual cliente?
    while True:
        try:
            id_cliente = int(input('Digite o ID do Cliente onde o serviço será prestado: '))
            consulta_servico = 'SELECT * FROM cliente WHERE id_cliente = %s'
            cursor.execute(consulta_servico, (id_cliente,))
            cliente = cursor.fetchone()
            if cliente:
                break
            else:
                print("Cliente não encontrado.")
        except ValueError:
            print("ID inválido. Tente novamente.")
            
    while True:
        try:
            preco_atendimento = float(input('Preço Total(formato: 10.99): '))
            # Verificar se o preço é maior que 0
            if preco_atendimento < 0:
                print('O preço deve ser maior que 0.')
            else:
                if validar_preco(preco_atendimento):
                    break  
        except ValueError:
            print('Valor inválido. Digite um valor válido para o preço.')
    
    Execucao = 'Andamento'        
    # Inserir o atendimento com a data atual
    data_atendimento = datetime.now().strftime('%Y-%m-%d')
    
    inserir_dados_atendimento = ''' INSERT INTO atendimento (id_cliente, id_servico, data, id_funcionario, valor_total, execucao) 
                                    VALUES (%s, %s, %s, %s, %s, %s)
    
    '''
    cursor.execute(inserir_dados_atendimento, (id_cliente, id_servico, data_atendimento, id_funcionario, preco_atendimento, Execucao))
    cursor.connection.commit()
    
    
    
    #AQUI VAMOS VERIFICAR SE O SERVIÇO TEM INTERVALO, SE ELE TIVER, IRA ADICIONAR A DATA ATUAL NA COLUNA (DATA_ULTIMO_ATENDIMENTO NO SQL)
    cursor.execute('SELECT intervalo_servico FROM servico WHERE id_servico = %s', (id_servico,))
    consulta_intervalo = cursor.fetchone()
    
    #se tiver um intervalo, um UPDATE na coluna Data_Ultimo_Atendimento é feito, para que assim futuramente, a verificação com ela seja feita.
    if consulta_intervalo and consulta_intervalo[0]: #consulta_intervalo[0] verifica se o valor do primeiro item da tupla retornada não é "false" (nulo, zero, etc.). 
        consulta_data_atendimento = '''UPDATE atendimento SET data_ultimo_atendimento = %s WHERE id_servico = %s
        '''
        cursor.execute(consulta_data_atendimento, (data_atendimento, id_servico))
        cursor.connection.commit()
        
    
def Exportar_Dados_Excel():
    
    while True:
        
        consulta = 'SELECT * FROM atendimento'
        cursor.execute(consulta)
        dados = cursor.fetchall() 
        
        if dados:
            caminho_diretorio = r'C:\Users\Dev\Novo Banco de dados (database)\TesteBancodeDados\Planilhas'
            
            if not os.path.exists(caminho_diretorio):  
                os.makedirs(caminho_diretorio)  
            
            caminho_completo = os.path.join(caminho_diretorio, 'Dados_Atendimento.xlsx')

            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'atendimento';")
            colunas_db = cursor.fetchall()
            colunas = [col[0] for col in colunas_db]  # [0] retorna o nome das colunas
            df = pd.DataFrame(dados, columns=colunas)
            
            df.to_excel(caminho_completo, index=False)
            print(f'Dados exportados para {caminho_completo}')
            break
        else:
            print('Não há dados registrados.')
            break
    cursor.connection.close()