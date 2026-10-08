    # sintatico.py
from util import ErroSintatico

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def token_atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def consumir(self, tipo_esperado):
        token = self.token_atual()
        if token is None:
            raise ErroSintatico(f"Erro sintático: Fim inesperado do arquivo. Esperado '{tipo_esperado}'.")
        if token.tipo == tipo_esperado:
            self.posicao += 1
            return token
        raise ErroSintatico(
            f"Erro sintático na linha {token.linha}: Esperado '{tipo_esperado}', mas encontrado '{token.valor}' ({token.tipo})"
        )

    def analisar(self):
        self.programa()
        if self.token_atual() is not None:
            token = self.token_atual()
            raise ErroSintatico(f"Erro sintático na linha {token.linha}: Código extra inesperado após o fim do programa.")
        return True

    # <programa> ::= program <identificador> { { <declaração> } { <comando> } }
    def programa(self):
        self.consumir("PROGRAM")
        self.consumir("IDENTIFICADOR")
        self.consumir("ABRE_CHAVES")

        # { <declaração> }
        while self.token_atual() and self.token_atual().tipo in ["INT", "BOOL"]:
            self.declaracao()

        # { <comando> }
        while self.token_atual() and self.token_atual().tipo != "FECHA_CHAVES":
            self.comando()

        self.consumir("FECHA_CHAVES")

    # <declaração> ::= <tipo> <lista_identificadores> ;
    def declaracao(self):
        tipo_token = self.token_atual()
        if tipo_token and tipo_token.tipo in ["INT", "BOOL"]:
            self.consumir(tipo_token.tipo)
        else:
            raise ErroSintatico(f"Erro sintático na linha {tipo_token.linha}: Tipo esperado ('int' ou 'bool').")

        self.lista_identificadores()
        self.consumir("PONTO_VIRGULA")

    # <lista_identificadores> ::= <identificador> { , <identificador> }
    def lista_identificadores(self):
        self.consumir("IDENTIFICADOR")
        while self.token_atual() and self.token_atual().tipo == "VIRGULA":
            self.consumir("VIRGULA")
            self.consumir("IDENTIFICADOR")

    # <comando> ::= <atribuição> | <leitura> | <escrita> | <condicional> | <bloco>
    def comando(self):
        tok = self.token_atual()
        if tok is None:
            raise ErroSintatico("Fim inesperado de arquivo ao processar comandos.")

        if tok.tipo == "IDENTIFICADOR":
            self.atribuicao()
        elif tok.tipo == "READ":
            self.leitura()
        elif tok.tipo == "WRITE":
            self.escrita()
        elif tok.tipo == "IF":
            self.condicional()
        elif tok.tipo == "ABRE_CHAVES":
            self.bloco()
        else:
            raise ErroSintatico(f"Erro sintático na linha {tok.linha}: Comando inválido '{tok.valor}'.")

    # <atribuição> ::= <identificador> = <expressão> ;
    def atribuicao(self):
        self.consumir("IDENTIFICADOR")
        self.consumir("ATRIBUICAO")
        self.expressao()
        self.consumir("PONTO_VIRGULA")

    # <leitura> ::= read ( <lista_identificadores> ) ;
    def leitura(self):
        self.consumir("READ")
        self.consumir("ABRE_PARENTESES")
        self.lista_identificadores()
        self.consumir("FECHA_PARENTESES")
        self.consumir("PONTO_VIRGULA")

    # <escrita> ::= write ( <lista_expressoes> ) ;
    def escrita(self):
        self.consumir("WRITE")
        self.consumir("ABRE_PARENTESES")
        self.lista_expressoes()
        self.consumir("FECHA_PARENTESES")
        self.consumir("PONTO_VIRGULA")

    # <condicional> ::= if ( <expressão> ) <bloco> [ else <bloco> ]
    def condicional(self):
        self.consumir("IF")
        self.consumir("ABRE_PARENTESES")
        self.expressao()
        self.consumir("FECHA_PARENTESES")
        self.bloco()

        if self.token_atual() and self.token_atual().tipo == "ELSE":
            self.consumir("ELSE")
            self.bloco()

    # <bloco> ::= { { <comando> } }
    def bloco(self):
        self.consumir("ABRE_CHAVES")
        while self.token_atual() and self.token_atual().tipo != "FECHA_CHAVES":
            self.comando()
        self.consumir("FECHA_CHAVES")

    # <lista_expressoes> ::= <expressão> { , <expressão> }
    def lista_expressoes(self):
        self.expressao()
        while self.token_atual() and self.token_atual().tipo == "VIRGULA":
            self.consumir("VIRGULA")
            self.expressao()

    # <expressão> ::= <expressão_logica>
    def expressao(self):
        self.expressao_logica()

    # <expressão_logica> ::= <expressão_and> { || <expressão_and> }
    def expressao_logica(self):
        self.expressao_and()
        while self.token_atual() and self.token_atual().tipo == "OU":
            self.consumir("OU")
            self.expressao_and()

    # <expressão_and> ::= <expressão_relacional> { && <expressão_relacional> }
    def expressao_and(self):
        self.expressao_relacional()
        while self.token_atual() and self.token_atual().tipo == "E":
            self.consumir("E")
            self.expressao_relacional()

    # <expressão_relacional> ::= <expressão_aritmética> [ <operador_relacional> <expressão_aritmética> ]
    def expressao_relacional(self):
        self.expressao_aritmetica()
        operadores_relacionais = ["MENOR", "MENOR_IGUAL", "MAIOR", "MAIOR_IGUAL", "IGUAL", "DIFERENTE"]
        if self.token_atual() and self.token_atual().tipo in operadores_relacionais:
            self.consumir(self.token_atual().tipo)
            self.expressao_aritmetica()

    # <expressão_aritmética> ::= <termo> { (+ | -) <termo> }
    def expressao_aritmetica(self):
        self.termo()
        while self.token_atual() and self.token_atual().tipo in ["MAIS", "MENOS"]:
            self.consumir(self.token_atual().tipo)
            self.termo()

    # <termo> ::= <fator> { (* | /) <fator> }
    def termo(self):
        self.fator()
        while self.token_atual() and self.token_atual().tipo in ["MULTIPLICACAO", "DIVISAO"]:
            self.consumir(self.token_atual().tipo)
            self.fator()

    # <fator> ::= <identificador> | <número> | true | false | ( <expressão> ) | ! <fator> | - <fator>
    def fator(self):
        tok = self.token_atual()
        if tok is None:
            raise ErroSintatico("Erro sintático: Expressão incompleta no fim do arquivo.")

        if tok.tipo == "IDENTIFICADOR":
            self.consumir("IDENTIFICADOR")
        elif tok.tipo == "NUMERO":
            self.consumir("NUMERO")
        elif tok.tipo in ["TRUE", "FALSE"]:
            self.consumir(tok.tipo)
        elif tok.tipo == "ABRE_PARENTESES":
            self.consumir("ABRE_PARENTESES")
            self.expressao()
            self.consumir("FECHA_PARENTESES")
        elif tok.tipo in ["NAO", "MENOS"]:
            self.consumir(tok.tipo)
            self.fator()
        else:
            raise ErroSintatico(f"Erro sintático na linha {tok.linha}: Fator de expressão inválido '{tok.valor}'.")