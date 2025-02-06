from datetime import datetime        #essa biblioteca lida melhor com dias, horas, minutos e segundos. Não tem suporte grande para meses e anos
import sqlite3
from dateutil.relativedelta import relativedelta #essa biblioteca lida melhor com meses e anos, pois consegue fazer calculos mais sofisticados.
from plyer import notification

caminho_do_banco = r'C:\Users\Dev\Novo Banco de dados (database)\Dedetizadora Inovar.db'
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()

def Verificar_Servicos_Pendentes ():
    hoje = datetime.now().strftime('%Y-%m-%d')
    hoje_obj = datetime.strptime(hoje, '%Y-%m-%d') #converter a data de hj para um obj
    qnd_ser_pendentes = 0
                                                #lembra sempre de indicar qual abreviação das tabelas são de qual coluna e vice versa
    consulta_servicos_pendentes = ''' SELECT 
    a.ID_Atendimento, 
    a.ID_Servico, 
    s.Intervalo_Servico, 
    a.Data_Ultimo_Atendimento
FROM 
    Atendimento a
INNER JOIN 
    Servico s
ON 
    a.ID_Servico = s.ID_Servico
WHERE 
    a.Data_Ultimo_Atendimento IS NOT NULL AND a.Execucao = 'Andamento';
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
            
            if data_vencimento >= hoje_obj:    # assim <= verifica se a data já passou ou é hoje. se colocar >= ele vai verificar datas futuras.
                qnd_ser_pendentes += 1      #ele vai sendo incrementado =1 toda vez que o loop chega nele
                
    if qnd_ser_pendentes > 0:
        qnd_ser_pendentes = str(qnd_ser_pendentes) # o plyer só aceita string, então precisa converter para str
        notificar_servico_pendente(qnd_ser_pendentes)
         

def notificar_servico_pendente(mensagem):
    notification.notify(
        title=f'Você tem {mensagem} serviços pendentes',
        message=mensagem,
        timeout=5  # O tempo que a notificação fica visível (em segundos)
    )
    
def Notificacoes_Pendencias():
    print('')
    