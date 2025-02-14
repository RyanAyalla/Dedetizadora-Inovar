from datetime import datetime        #essa biblioteca lida melhor com dias, horas, minutos e segundos. Não tem suporte grande para meses e anos
import psycopg2
from dateutil.relativedelta import relativedelta #essa biblioteca lida melhor com meses e anos, pois consegue fazer calculos mais sofisticados.
from plyer import notification
import os

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "ryan1234",
    host = "localhost",
    port = "5432"
)
cursor = conn.cursor()

def limpar_tela():
    sistema = os.name
    
    if sistema == 'nt':
        os.system('cls')    

#essa função irá rodar toda vez que o programa abre, então os dados já estarão salvos nas variaveis logo no início.
def Verificar_Servicos_Pendentes ():
    hoje = datetime.now().strftime('%Y-%m-%d')
    hoje_obj = datetime.strptime(hoje, '%Y-%m-%d') #converter a data de hj para um obj
    qnd_ser_pendentes = 0
                                                #lembra sempre de indicar qual abreviação das tabelas são de qual coluna e vice versa
    consulta_servicos_pendentes = ''' SELECT 
    a.id_atendimento, 
    a.id_servico, 
    s.intervalo_servico, 
    a.data_ultimo_atendimento
FROM 
    atendimento a
INNER JOIN 
    servico s
ON 
    a.id_servico = s.id_servico
WHERE 
    a.data_ultimo_atendimento IS NOT NULL AND a.execucao = 'Andamento';
    '''
    cursor.execute(consulta_servicos_pendentes)
    servicos_pendentes = cursor.fetchall()
    
    if servicos_pendentes:
        for servico in servicos_pendentes:
            id_atendimento = servico[0]
            id_servico = servico[1]
            intervalo_servico = servico [2]
            data_ultimo_atendimento = servico [3]
    
            # Convertendo data do último atendimento para um objeto datetime
            data_ultimo_atendimento_obj = datetime.strptime(data_ultimo_atendimento, '%Y-%m-%d')

            # Calculando a data de vencimento do serviço adicionando intervalo de meses
            data_vencimento = data_ultimo_atendimento_obj + relativedelta(month= intervalo_servico)
            
            if data_vencimento <= hoje_obj:    # assim <= verifica se a data já passou ou é hoje. se colocar >= ele vai verificar datas futuras.
                qnd_ser_pendentes += 1      #ele vai sendo incrementado =1 toda vez que o loop chega nele
                
    if qnd_ser_pendentes > 0:
        qnd_ser_pendentes = str(qnd_ser_pendentes) # o plyer só aceita string, então precisa converter para str
        notificar_servico_pendente(qnd_ser_pendentes)
        Pendencias(servicos_pendentes)
        
    return servicos_pendentes #ela precisa ser retornada para que lá no menu_Pendencias, ela seja usada na outra função Pendencias()
         

def notificar_servico_pendente(mensagem):
    notification.notify(
        title=f'Você tem {mensagem} serviços pendentes',
        message=mensagem,
        timeout=5  # O tempo que a notificação fica visível (em segundos)
    )
    
#para não precisar fazer outra consulta no banco de dados, pegamos os dados ja salvos na lista servicos_pendentes. Assim, podemos modifica-los de forma mais otimizada    
def Pendencias(servicos_pendentes):
    
    if servicos_pendentes:
        for servico in servicos_pendentes:
            id_atendimento = servico[0]
            print(f'O Atendimento de número {id_atendimento} está Pendente.\n')
    
    else:
        print('Nenhum Atendimento Pendente')
        
def Concluir_Pendencia():
    while True:
        try:
            escolha_pendencia = input('Digite o ID_Atendimento para Modificar sua Execução.\n')

            if escolha_pendencia.isdigit():
                escolha_pendencia = int(escolha_pendencia)
            
            consulta_pendencia = '''SELECT a.id_atendimento, c.nome, a.execucao
                                    FROM atendimento a JOIN cliente c ON a.id_cliente = c.id_cliente
                                    WHERE a.id_atendimento = %s
            '''
            cursor.execute(consulta_pendencia, (escolha_pendencia,))
            resultado_pendencia = cursor.fetchone()
            
            if resultado_pendencia:
                print(f'O Atendimento {resultado_pendencia[0]} é feito para o Cliente {resultado_pendencia[1]}, onde o Atendimento está em {resultado_pendencia[2]}')
                
                while True: 
                    try:
                        escolha_modificacao = str(input('Deseja Concluir esse Atendimento para não ter Pendências no Futuro? [s - n]')).upper()

                        if escolha_modificacao == 'N':
                            break
                        
                        if escolha_modificacao == 'S':
                            pendencia_update = '''UPDATE Atendimento SET Execucao = %s WHERE ID_Atendimento = %s 
                            '''
                            
                            cursor.execute(pendencia_update, ('Concluido', escolha_pendencia))
                            cursor.connection.commit()
                            
                            print("Atendimento Marcado como 'Concluído'.")
                            input('Aperte Enter para sair...')
                            break
                            
                        else:
                            print("Valor Inválido")
                            break
                        
                    except ValueError:
                        print('Valor Inválido. Digite Novamente')
                break #para sair do primeiro loop quando o bloco de cima for concluído
        
            else:
                print('Não Existe esse Atendimento')
                input('Digite Enter para sair...')
                break
            
        except ValueError:
            print('Valor Inválido. Digite Novamente.')
            
            
            
def Menu_Pendencias(): 
    servicos_pendentes = Verificar_Servicos_Pendentes()
    while True:
        try:
            escolha = input('1. Ver Pendências. \n2. Concluir uma Pendência. \n3. Menu Anterior\n')
        
            if escolha.isdigit():
                escolha = int(escolha)
            
            if escolha == 1:
                Pendencias(servicos_pendentes)
                input('Pressione qualquer Tecla para continuar...')
                
            if escolha == 2:
                Concluir_Pendencia()
                
            if escolha == 3:
                break
        
        except ValueError:
            print("Valor Inválido. Digite Novamente.")
            