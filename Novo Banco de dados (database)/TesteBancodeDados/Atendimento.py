import sqlite3
import os
import pandas as pd
from datetime import datetime
from Validacoes import validar_preco


caminho_do_banco = r'C:\Users\Dev\Novo Banco de dados (database)\Dedetizadora Inovar.db'  # Podemos usar duas \\ invertidas aqui ou o r (string raw) para o Python não tratar a \ como prefixo de escape
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()


def Menu_Atendimento():
    while True:
        escolha_atendimento = input('1. Novo Atendimento \n2. Atendimentos em Execução \n3. Atendimentos Concluídos \n4. Menu Anterior \n')
        
        if escolha_atendimento.isdigit():  # Verifica se a entrada é numérica
            escolha_atendimento = int(escolha_atendimento)
            
            if escolha_atendimento == 1:
                Registrar_Atendimento()
                
            elif escolha_atendimento == 2:
                print("Atendimentos em Execução.")
            
            elif escolha_atendimento == 3:
                print("Atendimentos Concluídos")
            
            elif escolha_atendimento == 4:
                Exportar_Dados_Excel()
            
            else:
                print('Opção Inválida')
        else:
            print('Valor Inválido, tente novamente.')
                
                

def Registrar_Atendimento():
    
    #qual serviço será prestado
    while True:
        try:
            id_servico = int(input('Digite o ID do Serviço prestado: '))
            consulta_servico = 'SELECT * FROM Servico WHERE ID_Servico = ?'
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
            consulta_servico = 'SELECT * FROM Funcionarios WHERE ID_Funcionario = ?'
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
            consulta_servico = 'SELECT * FROM Cliente WHERE ID_Cliente = ?'
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
    
    inserir_dados_atendimento = ''' INSERT INTO Atendimento (ID_Cliente, ID_Servico, Data, ID_Funcionario, Valor_Total, Execucao) 
                                    VALUES (?, ?, ?, ?, ?, ?)
    
    '''
    cursor.execute(inserir_dados_atendimento, (id_cliente, id_servico, data_atendimento, id_funcionario, preco_atendimento, Execucao))
    conexao.commit()
    
    
    
    #AQUI VAMOS VERIFICAR SE O SERVIÇO TEM INTERVALO, SE ELE TIVER, IRA ADICIONAR A DATA ATUAL NA COLUNA (DATA_ULTIMO_ATENDIMENTO NO SQL)
    cursor.execute('SELECT Intervalo_Servico FROM Servico WHERE ID_Servico = ?', (id_servico,))
    consulta_intervalo = cursor.fetchone()
    
    #se tiver um intervalo, um UPDATE na coluna Data_Ultimo_Atendimento é feito, para que assim futuramente, a verificação com ela seja feita.
    if consulta_intervalo and consulta_intervalo[0]: #consulta_intervalo[0] verifica se o valor do primeiro item da tupla retornada não é "false" (nulo, zero, etc.). 
        consulta_data_atendimento = '''UPDATE Atendimento SET Data_Ultimo_Atendimento = ? WHERE ID_Servico = ?
        '''
        cursor.execute(consulta_data_atendimento, (data_atendimento, id_servico))
        conexao.commit()
        
    conexao.close()
    
def Exportar_Dados_Excel():
    
    while True:
        
        consulta = 'SELECT * FROM Atendimento'
        cursor.execute(consulta)
        dados = cursor.fetchall() 
        
        if dados:
            caminho_diretorio = r'C:\Users\Dev\Novo Banco de dados (database)\TesteBancodeDados\Planilhas'
            
            if not os.path.exists(caminho_diretorio):  
                os.makedirs(caminho_diretorio)  
            
            caminho_completo = os.path.join(caminho_diretorio, 'Dados_Atendimento.xlsx')

            # Verificar o número de colunas no resultado
            cursor.execute('PRAGMA table_info(Atendimento);')  # Isso retorna as colunas da tabela Atendimento
            colunas_db = cursor.fetchall()  # Recebe os detalhes das colunas
            colunas = [col[1] for col in colunas_db]  #col[1] retorna o nome das coluna.
                                                      #PRAGMA(comando do SQLite), tras informações de cada coluna, 0 é o  numero dela, 2 o nome, 3 tipo, 4 se é null ou nao e 4 se é PK ou nao
            
            df = pd.DataFrame(dados, columns=colunas)
            
            df.to_excel(caminho_completo, index=False)
            print(f'Dados exportados para {caminho_completo}')
            break
        else:
            print('Não há dados registrados.')
            break
    conexao.close()