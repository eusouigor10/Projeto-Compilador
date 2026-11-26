import sys
from collections import Counter

from leitor import ler_arquivo
from lexico import analisar as analisar_lexico
from sintatico import Parser
from util import ErroLexico, ErroSintatico
from visualizador_ast import imprimir_ast
from semantico import AnalisadorSemantico

# Permite escolher o arquivo pela linha de comando: python main.py testes/arquivo.mc
# Se nenhum arquivo for informado, usa o teste padrão abaixo.
CAMINHO_TESTE = sys.argv[1] if len(sys.argv) > 1 else "testes/sem_if.mc"

# Evita erro de codificação ao imprimir acentos/conectores no terminal do Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


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


def mostrar_tabela_simbolos(tabela):
    print("\nTabela de símbolos:")
    if not tabela.simbolos:
        print("  (vazia)")
        return
    print(f"  {'Variável':<20} Tipo")
    print(f"  {'-' * 20} {'-' * 6}")
    for nome, tipo in tabela.simbolos.items():
        print(f"  {nome:<20} {tipo}")


def main():
    lexico_ok = False
    sintatico_ok = False
    semantico_ok = False
    tokens = []
    arvore = None

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
            arvore = parser.analisar()

            if arvore:
                sintatico_ok = True
                print("Análise sintática concluída com sucesso.")
                print("Árvore sintática gerada:")
                imprimir_ast(arvore)

        except ErroSintatico as erro:
            print(f"FALHA SINTÁTICA: {erro}")
            print("Os tokens foram reconhecidos lexicalmente, mas a sequência "
                  "não obedece à gramática do MiniC.")

    # 4. Análise semântica: só pode ocorrer se a AST foi gerada
    imprimir_titulo("4. ANÁLISE SEMÂNTICA")

    if not sintatico_ok:
        print("Não executada porque a árvore sintática não foi gerada.")
    else:
        analisador = AnalisadorSemantico()
        erros_semanticos = analisador.analisar(arvore)

        mostrar_tabela_simbolos(analisador.tabela)

        if erros_semanticos:
            print(f"\nFALHA SEMÂNTICA: {len(erros_semanticos)} erro(s) encontrado(s):")
            for erro in erros_semanticos:
                print(f"  - {erro}")
        else:
            semantico_ok = True
            print("\nAnálise semântica concluída com sucesso.")
            print("Todas as variáveis estão declaradas e os tipos estão corretos.")

    # 5. Resultado geral
    imprimir_titulo("5. RESULTADO GERAL")
    print(f"Leitura do arquivo: {'OK' if codigo is not None else 'FALHA'}")
    print(f"Análise léxica:     {'OK' if lexico_ok else 'FALHA'}")
    if not lexico_ok:
        print("Análise sintática:  NÃO EXECUTADA")
    else:
        print(f"Análise sintática:  {'OK' if sintatico_ok else 'FALHA'}")
    if not sintatico_ok:
        print("Análise semântica:  NÃO EXECUTADA")
    else:
        print(f"Análise semântica:  {'OK' if semantico_ok else 'FALHA'}")


if __name__ == "__main__":
    main()
