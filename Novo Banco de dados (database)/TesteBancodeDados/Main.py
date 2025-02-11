from Cadastro_Cliente import menu_cliente
from Cadastro_Funcionario import menu_funcionarios
from Cadastro_Produto import menu_produto
from Cadastro_Servico import menu_servico
from Atendimento import Menu_Atendimento
from pendencias import Menu_Pendencias, Verificar_Servicos_Pendentes
import schedule                                     #essa função determina um tempo que outra função pode ser executada automaticamente
import os

def limpar_tela():
    sistema = os.name
    
    if sistema == 'nt':  # os.name retorna 'nt' que faz a verificação da tela 
        os.system('cls')    #A função os.system('cls') chama o comando cls para limpar a tela.

schedule.every(1).hours.do(Verificar_Servicos_Pendentes)  #a função é verificada a cada 1 hora, essa aqui faz o agendamento
schedule.run_pending()                                      #já essa função, faz o agendamento ser executado

while True:
    limpar_tela()
    try:
        escolha = input('1. Clientes \n2. Produto \n3. Serviços \n4. Funcionários \n5. Registrar Atendimento \n6. Pendências \n7. Fechar o Programa\n')
        
        if escolha.isdigit():   #verifica se a entrada é um número, se for, transforma a variavel em inteiro
            escolha = int(escolha)
            
        if escolha == 1:
            menu_cliente()
            
        elif escolha == 2:
            menu_produto()
        
        elif escolha == 3:
            menu_servico()
            
        elif escolha == 4:
            menu_funcionarios()
            
        elif escolha == 5:
            Menu_Atendimento()
            
        elif escolha == 6:
            Menu_Pendencias()
            
        elif escolha == 7:
            input('Pressione Enter para fechar o Programa...')
            exit()
                 
    except ValueError:
        print('Valor Inválido. Tente novamente')
        