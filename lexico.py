from util import Token, PALAVRAS_RESERVADAS, OPERADORES, DELIMITADORES, ErroLexico

#função geral de análise léxica
def analisar(codigo):
    tokens = [] #cria lista de tokens

    posicao = 0
    linha = 1

    while posicao < len(codigo):
        caractere = codigo[posicao]

        #espaços, tabulações e quebras de linha
        if caractere in " \t\n":
            posicao, linha = analisar_espaco(codigo, posicao, linha)
            continue

        #identificadores e palavras reservadas
        if caractere.isalpha():
            token, posicao = analisar_identificador_reservada(codigo, posicao, linha)
            tokens.append(token)
            continue

        #números
        if caractere.isdigit():
            token, posicao = analisar_numero(codigo, posicao, linha)
            tokens.append(token)
            continue

        #delimitadores
        if caractere in DELIMITADORES:
            token, posicao = analisar_delimitador(codigo, posicao, linha)
            tokens.append(token)
            continue

        #operadores
        if caractere in OPERADORES or codigo[posicao:posicao + 2] in OPERADORES:
            token, posicao = analisar_operador(codigo, posicao, linha)
            tokens.append(token)
            continue

        #caso o caractere não pertença a nenhuma condição anterior, sobe um erro léxico
        raise ErroLexico(f"Caractere inválido '{caractere}' na linha {linha}")

    return tokens

#função para analisar espaços ou quebra de linha
def analisar_espaco(codigo, posicao, linha):
    caractere = codigo[posicao]

    if caractere in " \t": #verifica se o caractere é espaço
        return posicao + 1, linha

    if caractere == "\n": #verifica se o caractere é quebra de linha
        return posicao + 1, linha + 1

    return posicao, linha

#função para analisar identificadores ou palavras reservadas
def analisar_identificador_reservada(codigo, posicao, linha): 
    inicio = posicao

    while posicao < len(codigo) and (
        codigo[posicao].isalnum() or codigo[posicao] == "_" #função isalnum() verifica se o caractere é alfanumérico
    ):
        posicao += 1

    palavra = codigo[inicio:posicao]

    if palavra in PALAVRAS_RESERVADAS:
        tipo = PALAVRAS_RESERVADAS[palavra]
    else:
        tipo = "IDENTIFICADOR"

    token = Token(tipo, palavra, linha)

    return token, posicao

#função para analisar números
def analisar_numero(codigo, posicao, linha):
    inicio = posicao

    while posicao < len(codigo) and codigo[posicao].isdigit(): #verifica se é dígito
        posicao += 1

    numero = codigo[inicio:posicao]

    token = Token("NUMERO", numero, linha)

    return token, posicao

#função para analisar delimitadores
def analisar_delimitador(codigo, posicao, linha):
    caractere = codigo[posicao]

    tipo = DELIMITADORES[caractere]

    token = Token(tipo, caractere, linha)

    return token, posicao + 1

#função para analisar operadores
def analisar_operador(codigo, posicao, linha):
    operador = codigo[posicao]

    if posicao + 1 < len(codigo):
        proximo = codigo[posicao + 1]
        operador_duplo = operador + proximo

        if operador_duplo in OPERADORES:
            operador = operador_duplo

    tipo = OPERADORES[operador]

    token = Token(tipo, operador, linha)

    return token, posicao + len(operador)