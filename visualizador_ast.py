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


def _descricao(no):
    """Retorna o texto que identifica um nó da AST."""
    if isinstance(no, Programa):
        return f"Programa: {no.nome}"
    if isinstance(no, Declaracao):
        return f"Declaração: {no.tipo}"
    if isinstance(no, Atribuicao):
        return f"Atribuição: {no.identificador}"
    if isinstance(no, Leitura):
        return "Leitura"
    if isinstance(no, Escrita):
        return "Escrita"
    if isinstance(no, Bloco):
        return "Bloco"
    if isinstance(no, Condicional):
        return "Condicional (if/else)" if no.bloco_senao is not None else "Condicional (if)"
    if isinstance(no, Binario):
        return f"Binário: {no.operador}"
    if isinstance(no, Unario):
        return f"Unário: {no.operador}"
    if isinstance(no, Identificador):
        return f"Identificador: {no.nome}"
    if isinstance(no, Numero):
        return f"Número: {no.valor}"
    if isinstance(no, Booleano):
        return f"Booleano: {str(no.valor).lower()}"
    return str(no)


def _filhos(no):
    """Retorna os ramos filhos de cada tipo de nó."""
    if isinstance(no, Programa):
        return [
            ("Declarações", no.declaracoes),
            ("Comandos", no.comandos),
        ]
    if isinstance(no, Declaracao):
        return [("Identificadores", no.identificadores)]
    if isinstance(no, Atribuicao):
        return [("Expressão", no.expressao)]
    if isinstance(no, Leitura):
        return [("Identificadores", no.identificadores)]
    if isinstance(no, Escrita):
        return [("Expressões", no.expressoes)]
    if isinstance(no, Bloco):
        return [("Comandos", no.comandos)]
    if isinstance(no, Condicional):
        ramos = [
            ("Condição", no.condicao),
            ("Então", no.bloco_entao),
        ]
        if no.bloco_senao is not None:
            ramos.append(("Senão", no.bloco_senao))
        return ramos
    if isinstance(no, Binario):
        return [("", no.esquerda), ("", no.direita)]
    if isinstance(no, Unario):
        return [("", no.operando)]
    return []


def formatar_ast(arvore):
    """Converte a AST em uma árvore textual hierárquica."""
    linhas = []

    def desenhar(valor, prefixo="", ultimo=True, rotulo=None):
        conector = "└── " if ultimo else "├── "
        continuacao = "    " if ultimo else "│   "

        if rotulo is not None:
            linhas.append(prefixo + conector + rotulo)
            prefixo_filho = prefixo + continuacao
            if isinstance(valor, list):
                itens = valor
                for indice, item in enumerate(itens):
                    desenhar(
                        item,
                        prefixo_filho,
                        indice == len(itens) - 1,
                    )
            elif valor is not None:
                desenhar(valor, prefixo_filho, True)
            return

        if isinstance(valor, list):
            linhas.append(prefixo + conector + "Lista")
            for indice, item in enumerate(valor):
                desenhar(item, prefixo + continuacao, indice == len(valor) - 1)
            return

        if isinstance(valor, str):
            linhas.append(prefixo + conector + valor)
            return

        linhas.append(prefixo + conector + _descricao(valor))
        filhos = _filhos(valor)
        prefixo_filho = prefixo + continuacao
        for indice, (nome, filho) in enumerate(filhos):
            desenhar(
                filho,
                prefixo_filho,
                indice == len(filhos) - 1,
                rotulo=nome if nome else None,
            )

    # A raiz não precisa de conector de árvore.
    linhas.append(_descricao(arvore))
    for indice, (nome, filho) in enumerate(_filhos(arvore)):
        desenhar(filho, "", indice == len(_filhos(arvore)) - 1, rotulo=nome)

    return "\n".join(linhas)


def imprimir_ast(arvore):
    """Imprime a AST formatada no terminal."""
    print(formatar_ast(arvore))
