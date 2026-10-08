from collections import Counter

from leitor import ler_arquivo
from lexico import analisar as analisar_lexico
from sintatico import Parser
from util import ErroLexico, ErroSintatico


CAMINHO_TESTE = "testes/teste_geral.mc"


def imprimir_titulo(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def mostrar_resumo_tokens(tokens):
    imprimir_titulo("RESUMO DOS TOKENS")
    print(f"Total de tokens reconhecidos: {len(tokens)}")
    print("\nQuantidade por tipo:")

    quantidades = Counter(token.tipo for token in tokens)
    for tipo, quantidade in sorted(quantidades.items()):
        print(f"  {tipo:<22} {quantidade}")


def main():
    lexico_ok = False
    sintatico_ok = False
    tokens = []

    # 1. Leitura do arquivo-fonte
    imprimir_titulo("1. LEITURA DO CÓDIGO-FONTE")

    try:
        codigo = ler_arquivo(CAMINHO_TESTE)
    except OSError as erro:
        print(f"Não foi possível abrir o arquivo '{CAMINHO_TESTE}'.")
        print(f"Detalhes: {erro}")
        return

    print(f"Arquivo: {CAMINHO_TESTE}")
    print("\nCódigo-fonte:")
    print("-" * 60)
    print(codigo.rstrip())
    print("-" * 60)

    # 2. Análise léxica
    imprimir_titulo("2. ANÁLISE LÉXICA")

    try:
        tokens = analisar_lexico(codigo)
        lexico_ok = True
        print("Análise léxica concluída com sucesso.")
        print("\nTokens reconhecidos:")

        for indice, token in enumerate(tokens, start=1):
            print(f"{indice:03}. {token}")

        mostrar_resumo_tokens(tokens)

    except ErroLexico as erro:
        print(f"FALHA LÉXICA: {erro}")
        print("A análise sintática não será executada porque não foi "
              "possível gerar a sequência completa de tokens.")

    # 3. Análise sintática: só pode ocorrer se o lexer teve sucesso
    imprimir_titulo("3. ANÁLISE SINTÁTICA")

    if not lexico_ok:
        print("Não executada devido ao erro léxico.")
    else:
        try:
            parser = Parser(tokens)
            resultado = parser.analisar()

            if resultado:
                sintatico_ok = True
                print("Análise sintática concluída com sucesso.")
                print("O programa obedece à gramática implementada no parser.")
                print("Observação: esta versão do parser ainda não constrói a AST.")

        except ErroSintatico as erro:
            print(f"FALHA SINTÁTICA: {erro}")
            print("Os tokens foram reconhecidos lexicalmente, mas a sequência "
                  "não obedece à gramática do MiniC.")

    # 4. Resultado geral
    imprimir_titulo("4. RESULTADO GERAL")
    print(f"Leitura do arquivo: {'OK' if codigo is not None else 'FALHA'}")
    print(f"Análise léxica:     {'OK' if lexico_ok else 'FALHA'}")
    if not lexico_ok:
        print("Análise sintática:  NÃO EXECUTADA")
    else:
        print(f"Análise sintática:  {'OK' if sintatico_ok else 'FALHA'}")


if __name__ == "__main__":
    main()
