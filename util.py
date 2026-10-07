class Token: #classe que representará um token do código, com tipo, valor e linha em que está
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, linha={self.linha})" #representação do token quando houver print


PALAVRAS_RESERVADAS = { #dicionário de palavras reservadas
    "program": "PROGRAM",
    "int": "INT",
    "bool": "BOOL",
    "if": "IF",
    "else": "ELSE",
    "read": "READ",
    "write": "WRITE",
    "true": "TRUE",
    "false": "FALSE"
}


OPERADORES = { #operadores da linguagem
    "+": "MAIS",
    "-": "MENOS",
    "*": "MULTIPLICACAO",
    "/": "DIVISAO",
    "<": "MENOR",
    "<=": "MENOR_IGUAL",
    ">": "MAIOR",
    ">=": "MAIOR_IGUAL",
    "==": "IGUAL",
    "!=": "DIFERENTE",
    "&&": "E",
    "||": "OU",
    "!": "NAO",
    "=": "ATRIBUICAO"
}


DELIMITADORES = { #delimitadores de operações e blocos
    "(": "ABRE_PARENTESES",
    ")": "FECHA_PARENTESES",
    "{": "ABRE_CHAVES",
    "}": "FECHA_CHAVES",
    ";": "PONTO_VIRGULA",
    ",": "VIRGULA"
}