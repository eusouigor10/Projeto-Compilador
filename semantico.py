from sintatico import (
    Programa,
    Declaracao,
    Atribuicao,
    Leitura,
    Escrita,
    Bloco,
    Condicional,
    Binario,
    Unario,
    Identificador,
    Numero,
    Booleano,
)
from tabela_simbolos import TabelaSimbolos


# "Tipo" especial devolvido quando uma expressão já tem erro.
# Serve para não gerar erros em cascata: o erro é reportado uma única vez,
# no ponto onde aconteceu, e quem está acima apenas repassa ERRO adiante.
ERRO = "erro"

# Regras de tipos dos operadores da MiniC
OPERADORES_ARITMETICOS = ["+", "-", "*", "/"]     # int, int -> int
OPERADORES_RELACIONAIS = ["<", "<=", ">", ">="]   # int, int -> bool
OPERADORES_IGUALDADE = ["==", "!="]               # mesmo tipo -> bool
OPERADORES_LOGICOS = ["&&", "||"]                 # bool, bool -> bool


class AnalisadorSemantico:
    """Percorre a AST gerada pelo parser verificando declarações e tipos.

    Os erros não interrompem a análise: todos são acumulados em self.erros,
    para que o programador veja todos os problemas de uma vez.
    """

    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.erros = []

    def erro(self, mensagem, linha=0):
        if linha:
            self.erros.append(f"Erro semântico na linha {linha}: {mensagem}")
        else:
            self.erros.append(f"Erro semântico: {mensagem}")

    # Ponto de entrada: recebe o nó Programa e devolve a lista de erros
    def analisar(self, programa: Programa):
        for declaracao in programa.declaracoes:
            self.verificar_declaracao(declaracao)

        for comando in programa.comandos:
            self.verificar_comando(comando)

        return self.erros

    # ------------------------------------------------------------------
    # DECLARAÇÕES
    # ------------------------------------------------------------------

    # <declaração> ::= <tipo> <lista_identificadores> ;
    # Cada identificador é inserido na tabela de símbolos com o seu tipo.
    # A tabela lança ValueError se a variável já tiver sido declarada.
    def verificar_declaracao(self, declaracao: Declaracao):
        for indice, nome in enumerate(declaracao.identificadores):
            linha = self._linha_da_lista(declaracao.linhas, indice)
            try:
                self.tabela.declarar(nome, declaracao.tipo)
            except ValueError:
                tipo_anterior = self.tabela.obter_tipo(nome)
                self.erro(
                    f"declaração duplicada da variável '{nome}' "
                    f"(já declarada anteriormente como '{tipo_anterior}').",
                    linha,
                )

    # ------------------------------------------------------------------
    # COMANDOS
    # ------------------------------------------------------------------

    def verificar_comando(self, comando):
        if isinstance(comando, Atribuicao):
            self.verificar_atribuicao(comando)
        elif isinstance(comando, Leitura):
            self.verificar_leitura(comando)
        elif isinstance(comando, Escrita):
            self.verificar_escrita(comando)
        elif isinstance(comando, Condicional):
            self.verificar_condicional(comando)
        elif isinstance(comando, Bloco):
            self.verificar_bloco(comando)

    # <atribuição> ::= <identificador> = <expressão> ;
    # A variável precisa existir e o tipo da expressão precisa ser igual ao dela.
    def verificar_atribuicao(self, atribuicao: Atribuicao):
        variavel_existe = self.tabela.existe(atribuicao.identificador)
        if not variavel_existe:
            self.erro(
                f"variável '{atribuicao.identificador}' não foi declarada.",
                atribuicao.linha,
            )

        # A expressão é sempre verificada, mesmo se a variável não existir,
        # para que erros dentro dela também sejam reportados.
        tipo_expressao = self.tipo_expressao(atribuicao.expressao)

        if not variavel_existe:
            return

        tipo_variavel = self.tabela.obter_tipo(atribuicao.identificador)

        if tipo_expressao != ERRO and tipo_expressao != tipo_variavel:
            self.erro(
                f"tipos incompatíveis na atribuição: a variável "
                f"'{atribuicao.identificador}' é do tipo '{tipo_variavel}', "
                f"mas recebeu uma expressão do tipo '{tipo_expressao}'.",
                atribuicao.linha,
            )

    # <leitura> ::= read ( <lista_identificadores> ) ;
    # O read armazena valores em variáveis, então cada identificador precisa
    # estar declarado (int ou bool). Repetir a mesma variável no mesmo read
    # também é sinalizado, pois o primeiro valor lido seria descartado.
    
    def verificar_leitura(self, leitura: Leitura):
        for indice, nome in enumerate(leitura.identificadores):
            linha = self._linha_da_lista(
                leitura.linhas, indice, leitura.linha
            )

            if not self.tabela.existe(nome):
                self.erro(
                    f"variável '{nome}' utilizada no comando read "
                    f"não foi declarada.",
                    linha,
                )

    # <escrita> ::= write ( <lista_expressoes> ) ;
    # Cada expressão precisa ser válida (variáveis declaradas e tipos corretos).
    # Podem ser escritos valores int ou bool.
    def verificar_escrita(self, escrita: Escrita):
        for expressao in escrita.expressoes:
            self.tipo_expressao(expressao)

    # <condicional> ::= if ( <expressão> ) <bloco> [ else <bloco> ]
    # A condição precisa ser do tipo bool.
    def verificar_condicional(self, condicional: Condicional):
        tipo_condicao = self.tipo_expressao(condicional.condicao)

        if tipo_condicao != ERRO and tipo_condicao != "bool":
            self.erro(
                f"a condição do comando if deve ser do tipo 'bool', "
                f"mas é do tipo '{tipo_condicao}'.",
                condicional.linha,
            )

        self.verificar_bloco(condicional.bloco_entao)
        if condicional.bloco_senao is not None:
            self.verificar_bloco(condicional.bloco_senao)

    # <bloco> ::= { { <comando> } }
    def verificar_bloco(self, bloco: Bloco):
        for comando in bloco.comandos:
            self.verificar_comando(comando)

    # ------------------------------------------------------------------
    # EXPRESSÕES: cada método devolve o TIPO da expressão ("int", "bool" ou ERRO)
    # ------------------------------------------------------------------

    def tipo_expressao(self, expressao):
        if isinstance(expressao, Numero):
            return "int"

        if isinstance(expressao, Booleano):
            return "bool"

        if isinstance(expressao, Identificador):
            return self.tipo_identificador(expressao)

        if isinstance(expressao, Unario):
            return self.tipo_unario(expressao)

        if isinstance(expressao, Binario):
            return self.tipo_binario(expressao)

        self.erro(f"expressão desconhecida: {expressao}.")
        return ERRO

    def tipo_identificador(self, identificador: Identificador):
        if not self.tabela.existe(identificador.nome):
            self.erro(
                f"variável '{identificador.nome}' não foi declarada.",
                identificador.linha,
            )
            return ERRO

        return self.tabela.obter_tipo(identificador.nome)

    # ! <fator>  -> exige bool, resulta em bool
    # - <fator>  -> exige int,  resulta em int
    def tipo_unario(self, unario: Unario):
        tipo_operando = self.tipo_expressao(unario.operando)
        tipo_esperado = "bool" if unario.operador == "!" else "int"

        if tipo_operando == ERRO:
            return ERRO

        if tipo_operando != tipo_esperado:
            self.erro(
                f"o operador '{unario.operador}' exige um operando do tipo "
                f"'{tipo_esperado}', mas recebeu '{tipo_operando}'.",
                unario.linha,
            )
            return ERRO

        return tipo_esperado

    def tipo_binario(self, binario: Binario):
        tipo_esquerda = self.tipo_expressao(binario.esquerda)
        tipo_direita = self.tipo_expressao(binario.direita)
        operador = binario.operador

        # Algum dos lados já tem erro (e ele já foi reportado)
        if tipo_esquerda == ERRO or tipo_direita == ERRO:
            return ERRO

        if operador in OPERADORES_ARITMETICOS:
            categoria, exigido, resultado = "aritmético", "int", "int"
        elif operador in OPERADORES_RELACIONAIS:
            categoria, exigido, resultado = "relacional", "int", "bool"
        elif operador in OPERADORES_LOGICOS:
            categoria, exigido, resultado = "lógico", "bool", "bool"
        elif operador in OPERADORES_IGUALDADE:
            # == e != aceitam int com int ou bool com bool
            if tipo_esquerda == tipo_direita:
                return "bool"
            self.erro(
                f"o operador relacional '{operador}' exige operandos do "
                f"mesmo tipo, mas recebeu '{tipo_esquerda}' e '{tipo_direita}'.",
                binario.linha,
            )
            return ERRO
        else:
            self.erro(f"operador desconhecido '{operador}'.", binario.linha)
            return ERRO

        if tipo_esquerda == exigido and tipo_direita == exigido:
            return resultado

        self.erro(
            f"o operador {categoria} '{operador}' exige operandos do tipo "
            f"'{exigido}', mas recebeu '{tipo_esquerda}' e '{tipo_direita}'.",
            binario.linha,
        )
        return ERRO

    # ------------------------------------------------------------------

    @staticmethod
    def _linha_da_lista(linhas, indice, padrao=0):
        if linhas and indice < len(linhas):
            return linhas[indice]
        return padrao
