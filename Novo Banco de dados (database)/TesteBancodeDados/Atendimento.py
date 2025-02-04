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
        try:
            escolha_atendimento = int(input('1. Novo Atendimento \n2. Exportar dados para o Excel \n3. Menu Anterior \n'))
                
            if escolha_atendimento == 1:
                Registrar_Atendimento()
                
            elif escolha_atendimento == 2:
                Exportar_Dados_Excel()
            
            elif escolha_atendimento == 3:
                return
            
            else:
                print('Opção Inválida')
                
        except ValueError:
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
            
    # Inserir o atendimento com a data atual
    data_atendimento = datetime.now().strftime('%Y-%m-%d')
    
    inserir_dados_atendimento = ''' INSERT INTO Atendimento (ID_Cliente, ID_Servico, Data, ID_Funcionario, Valor_Total) 
                                    VALUES (?, ?, ?, ?, ?)
    
    '''
    cursor.execute(inserir_dados_atendimento, (id_cliente, id_servico, data_atendimento, id_funcionario, preco_atendimento))
    conexao.commit()
    
    
def Exportar_Dados_Excel():
    
    while True:
        #consultar todos os dados da tabela Atendimento
        consulta = 'SELECT * FROM Atendimento'
        cursor.execute(consulta)
        dados = cursor.fetchall() #retorna todos os dados se tiver
        
        if dados:
            
            caminho_diretorio = r'C:\Users\Dev\Novo Banco de dados (database)\TesteBancodeDados\Planilhas'
            
            if not os.path.exists(caminho_diretorio):  #função que verifica se algo existe 
                os.makedirs(caminho_diretorio)  # Cria o diretório se ele não existir
            
            caminho_completo = os.path.join(caminho_diretorio, 'Dados_Atendimento.xlsx')

            if isinstance(dados, list): #transforma os dados em lista
                df = pd.DataFrame(dados, columns= ['ID_Atendimento', 'Cliente', 'Serviço', 'Data', 'Funcionário', 'Valor Total do Serviço'])
                
            else:
                df = pd.DataFrame([dados], columns= ['ID_Atendimento', 'Cliente', 'Serviço', 'Data', 'Funcionário', 'Valor Total do Serviço'])
            
            df.to_excel(caminho_completo, index=False)
            print(f'Dados exportados para {caminho_completo}')
            break
        else:
            print('Não há dados registrados.')
            break