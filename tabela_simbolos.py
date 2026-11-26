
class TabelaSimbolos:

    # constroi o dicionário da tabela de símbolos
    def __init__(self):
        self.simbolos = {}

    # verifica se a variável já foi declarada e, caso não tenha sido, adiciona na tabela de símbolos
    def declarar(self, nome, tipo):
        if nome in self.simbolos:
            raise ValueError(
                f"Variável '{nome}' já foi declarada."
            )

        self.simbolos[nome] = tipo

    # verifica a existência de uma variável na tabela de símbolos
    def existe(self, nome):
        return nome in self.simbolos

    # obtém o tipo de uma variável da tabela de símbolos e lança um erro caso a variável não tenha sido declarada
    def obter_tipo(self, nome):
        if not self.existe(nome):
            raise ValueError(
                f"Variável '{nome}' não foi declarada."
            )

        return self.simbolos[nome]