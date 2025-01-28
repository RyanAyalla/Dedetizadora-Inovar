from Cadastro_Cliente import menu_cliente
from Cadastro_Funcionario import menu_funcionarios
from Cadastro_Produto import menu_produto
from Cadastro_Servico import menu_servico

import os

def limpar_tela():
    sistema = os.name
    
    if sistema == 'nt':  # os.name retorna 'nt' que faz a verificação da tela 
        os.system('cls')    #A função os.system('cls') chama o comando cls para limpar a tela.

while True:
    limpar_tela()
    try:
        escolha = input('1. Clientes \n2. Produto \n3. Serviços \n4. Funcionários \n5.Fechar o Programa \n')
        
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
            input('Pressione Enter para fechar o Programa...')
            exit()
            
    except ValueError:
        print('Valor Inválido. Tente novamente')
        