from util import ErroSintatico

#biblioteca que permite criar classes com menos código
from dataclasses import dataclass, field

## DECLARAÇÃO DAS CLASSES QUE SERÃO OS NÓS DA AST

#o programa a ser analisado
@dataclass
class Programa:
    nome: str
    declaracoes: list
    comandos: list


#declaração de variáveis
@dataclass
class Declaracao:
    tipo: str
    identificadores: list
    linhas: list = field(default_factory=list)  # linha de cada identificador (análise semântica)


#atribuições
@dataclass
class Atribuicao:
    identificador: str
    expressao: object
    linha: int = 0

#read
@dataclass
class Leitura:
    identificadores: list
    linhas: list = field(default_factory=list)
    linha: int = 0

#write
@dataclass
class Escrita:
    expressoes: list
    linha: int = 0

#bloco de comandos
@dataclass
class Bloco:
    comandos: list

#if/else
@dataclass
class Condicional:
    condicao: object
    bloco_entao: Bloco
    bloco_senao: Bloco | None
    linha: int = 0


#operações com 2 operandos
@dataclass
class Binario:
    operador: str
    esquerda: object
    direita: object
    linha: int = 0

#operações com 1 operando
@dataclass
class Unario:
    operador: str
    operando: object
    linha: int = 0

#identificadores/variáveis
@dataclass
class Identificador:
    nome: str
    linha: int = 0

#números
@dataclass
class Numero:
    valor: int
    linha: int = 0

#true/false
@dataclass
class Booleano:
    valor: bool
    linha: int = 0

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
        arvore = self.programa()
        if self.token_atual() is not None:
            token = self.token_atual()
            raise ErroSintatico(f"Erro sintático na linha {token.linha}: Código extra inesperado após o fim do programa.")
        return arvore

    # <programa> ::= program <identificador> { { <declaração> } { <comando> } }
    def programa(self):
        self.consumir("PROGRAM")
        nome = self.consumir("IDENTIFICADOR").valor
        self.consumir("ABRE_CHAVES")

        #lista para guardar as declarações
        declaracoes = []

        # { <declaração> }
        while self.token_atual() and self.token_atual().tipo in ["INT", "BOOL"]:
            declaracoes.append(self.declaracao())

        #lista para guardar os comandos
        comandos = []

        # { <comando> }
        while self.token_atual() and self.token_atual().tipo != "FECHA_CHAVES":
            comandos.append(self.comando())

        self.consumir("FECHA_CHAVES")

        #retorna o nó do programa
        return Programa(nome, declaracoes, comandos)


    
    # <declaração> ::= <tipo> <lista_identificadores> ;
    def declaracao(self):
        tipo_token = self.token_atual()

        if tipo_token and tipo_token.tipo in ["INT", "BOOL"]:
            self.consumir(tipo_token.tipo)
        else:
            raise ErroSintatico(
                f"Erro sintático na linha {tipo_token.linha}: "
                "Tipo esperado ('int' ou 'bool')."
            )

        tokens_ids = self.lista_tokens_identificadores()
        self.consumir("PONTO_VIRGULA")

        #retorna o nó da declaração (com a linha de cada identificador)
        return Declaracao(
            tipo_token.valor,
            [t.valor for t in tokens_ids],
            [t.linha for t in tokens_ids],
        )


    
    # <lista_identificadores> ::= <identificador> { , <identificador> }
    def lista_identificadores(self):
        return [t.valor for t in self.lista_tokens_identificadores()]

    #mesma lista, mas devolvendo os tokens (para guardar a linha de cada identificador)
    def lista_tokens_identificadores(self):
        tokens_ids = [self.consumir("IDENTIFICADOR")]

        while self.token_atual() and self.token_atual().tipo == "VIRGULA":
            self.consumir("VIRGULA")
            tokens_ids.append(self.consumir("IDENTIFICADOR"))

        return tokens_ids


    
    def comando(self):
        tok = self.token_atual()

        if tok is None:
            raise ErroSintatico(
                "Fim inesperado de arquivo ao processar comandos."
            )

        if tok.tipo == "IDENTIFICADOR":
            return self.atribuicao()
        elif tok.tipo == "READ":
            return self.leitura()
        elif tok.tipo == "WRITE":
            return self.escrita()
        elif tok.tipo == "IF":
            return self.condicional()
        elif tok.tipo == "ABRE_CHAVES":
            return self.bloco()
        else:
            raise ErroSintatico(
                f"Erro sintático na linha {tok.linha}: "
                f"Comando inválido '{tok.valor}'."
            )

    
    # <atribuição> ::= <identificador> = <expressão> ;
    def atribuicao(self):
        tok = self.consumir("IDENTIFICADOR")
        self.consumir("ATRIBUICAO")
        expressao = self.expressao()
        self.consumir("PONTO_VIRGULA")

        return Atribuicao(
            tok.valor,
            expressao,
            tok.linha
        )

    
    # <leitura> ::= read ( <lista_identificadores> ) ;
    def leitura(self):
        tok = self.consumir("READ")
        self.consumir("ABRE_PARENTESES")

        tokens_ids = self.lista_tokens_identificadores()

        self.consumir("FECHA_PARENTESES")
        self.consumir("PONTO_VIRGULA")

        return Leitura(
            [t.valor for t in tokens_ids],
            [t.linha for t in tokens_ids],
            tok.linha
        )

    
    # <escrita> ::= write ( <lista_expressoes> ) ;
    def escrita(self):
        tok = self.consumir("WRITE")
        self.consumir("ABRE_PARENTESES")

        expressoes = self.lista_expressoes()

        self.consumir("FECHA_PARENTESES")
        self.consumir("PONTO_VIRGULA")

        return Escrita(expressoes, tok.linha)

    def condicional(self):
        tok_if = self.consumir("IF")
        self.consumir("ABRE_PARENTESES")

        condicao = self.expressao()

        self.consumir("FECHA_PARENTESES")
        bloco_entao = self.bloco()

        bloco_senao = None

        if self.token_atual() and self.token_atual().tipo == "ELSE":
            self.consumir("ELSE")
            bloco_senao = self.bloco()

        return Condicional(condicao, bloco_entao, bloco_senao, tok_if.linha)

    def bloco(self):
        self.consumir("ABRE_CHAVES")

        comandos = []
        while self.token_atual() and self.token_atual().tipo != "FECHA_CHAVES":
            comandos.append(self.comando())

        self.consumir("FECHA_CHAVES")

        return Bloco(comandos)

    
    # <lista_expressoes> ::= <expressão> { , <expressão> }
    def lista_expressoes(self):
        expressoes = [self.expressao()]

        while self.token_atual() and self.token_atual().tipo == "VIRGULA":
            self.consumir("VIRGULA")
            expressoes.append(self.expressao())

        return expressoes
    
    def expressao(self):
        return self.expressao_logica()


    def expressao_logica(self):
        esquerda = self.expressao_and()

        while self.token_atual() and self.token_atual().tipo == "OU":
            tok_op = self.consumir("OU")
            direita = self.expressao_and()
            esquerda = Binario(tok_op.valor, esquerda, direita, tok_op.linha)

        return esquerda


    def expressao_and(self):
        esquerda = self.expressao_relacional()

        while self.token_atual() and self.token_atual().tipo == "E":
            tok_op = self.consumir("E")
            direita = self.expressao_relacional()
            esquerda = Binario(tok_op.valor, esquerda, direita, tok_op.linha)

        return esquerda


    def expressao_relacional(self):
        esquerda = self.expressao_aritmetica()

        operadores_relacionais = [
            "MENOR", "MENOR_IGUAL", "MAIOR",
            "MAIOR_IGUAL", "IGUAL", "DIFERENTE"
        ]

        if (
            self.token_atual()
            and self.token_atual().tipo in operadores_relacionais
        ):
            tok_op = self.consumir(self.token_atual().tipo)
            direita = self.expressao_aritmetica()
            esquerda = Binario(tok_op.valor, esquerda, direita, tok_op.linha)

        return esquerda

    
    # <expressão_aritmética> ::= <termo> { (+ | -) <termo> }
    def expressao_aritmetica(self):
        esquerda = self.termo()

        while self.token_atual() and self.token_atual().tipo in ["MAIS", "MENOS"]:
            tok_op = self.consumir(self.token_atual().tipo)
            direita = self.termo()
            esquerda = Binario(tok_op.valor, esquerda, direita, tok_op.linha)

        return esquerda

    
    # <termo> ::= <fator> { (* | /) <fator> }
    def termo(self):
        esquerda = self.fator()

        while self.token_atual() and self.token_atual().tipo in ["MULTIPLICACAO", "DIVISAO"]:
            tok_op = self.consumir(self.token_atual().tipo)
            direita = self.fator()
            esquerda = Binario(tok_op.valor, esquerda, direita, tok_op.linha)

        return esquerda

    
    # <fator> ::= <identificador> | <número> | true | false
    #          | ( <expressão> ) | ! <fator> | - <fator>
    def fator(self):
        tok = self.token_atual()

        if tok is None:
            raise ErroSintatico(
                "Erro sintático: Expressão incompleta no fim do arquivo."
            )

        if tok.tipo == "IDENTIFICADOR":
            self.consumir("IDENTIFICADOR")
            return Identificador(tok.valor, tok.linha)

        elif tok.tipo == "NUMERO":
            self.consumir("NUMERO")
            return Numero(int(tok.valor), tok.linha)

        elif tok.tipo in ["TRUE", "FALSE"]:
            self.consumir(tok.tipo)
            return Booleano(tok.tipo == "TRUE", tok.linha)

        elif tok.tipo == "ABRE_PARENTESES":
            self.consumir("ABRE_PARENTESES")
            expressao = self.expressao()
            self.consumir("FECHA_PARENTESES")
            return expressao

        elif tok.tipo in ["NAO", "MENOS"]:
            operador = self.consumir(tok.tipo).valor
            operando = self.fator()
            return Unario(operador, operando, tok.linha)

        else:
            raise ErroSintatico(
                f"Erro sintático na linha {tok.linha}: "
                f"Fator de expressão inválido '{tok.valor}'."
            )