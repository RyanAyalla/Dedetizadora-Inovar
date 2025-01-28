import re

def validar_cpf(CPF):
    CPF = re.sub(r'\D','', CPF) #a função re remove os caracteres especificados. r'\D' diz que \ vai ser tratado como texto literal, o \D é um metacaractere
    
    return len(CPF) == 11  
    
def validar_cnpj(CNPJ):
    CNPJ = re.sub(r'\D', '', CNPJ)
    
    return len(CNPJ) == 14

def validar_telefone(Telefone):
    Telefone = str(Telefone)  #Garante que a entrada de qualquer dado, seja convertido para string
    Telefone = re.sub(r'\D','',Telefone)    #remove os caracteres não númericos
    
    return len(Telefone) == 11

def validar_email(email):
    
    # Expressão regular para validar o formato do email
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'   #o r é usado aqui para ele interpretar o \ como caractere literal na expressão regular
    
    # Verifica se o comprimento é <= 100 caracteres e se o formato está correto
    if len(email) > 100:
        return False
    elif re.match(padrao_email, email):  #re.match verifica se o email está de acordo com a expressão regular inserida na variavel padrao_email
        return True
    else:
        return False
        
def validar_preco(preco):
    # Converte o valor para string para separar a parte inteira e a decimal
    preco_str = str(preco)
    
    # Separa a parte inteira e decimal com base no ponto
    if '.' in preco_str:
        partes = preco_str.split(".")
        
        # Verifica se a parte inteira tem no máximo 10 dígitos
        if len(partes[0]) > 10:
            print("Erro: A parte inteira do preço deve ter no máximo 10 dígitos.")
            return False
        
        # Verifica se a parte decimal tem no máximo 2 dígitos
        if len(partes[1]) > 2:
            print("Erro: A parte decimal do preço deve ter no máximo 2 dígitos.")
            return False
        
    else:
        # Se não houver ponto, o preço é inteiro, então verifica apenas a parte inteira
        if len(preco_str) > 10:
            print("Erro: O preço inteiro deve ter no máximo 10 dígitos.")
            return False

    return True



