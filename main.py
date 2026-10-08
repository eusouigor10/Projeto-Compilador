import sys
from leitor import ler_arquivo
from lexico import analisar
from sintatico import Parser
from util import ErroLexico, ErroSintatico

def main():
    # Pega o arquivo passado por linha de comando ou usa o padrão
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else "testes/erro_lexico.mc"

    try:
        programa = ler_arquivo(caminho_arquivo)
        
        # 1. Análise Léxica
        tokens = analisar(programa)
        print("==========")
        print("TOKENS RECONHECIDOS")
        print("==========")
        for token in tokens:
            print(token)

        # 2. Análise Sintática
        print("\n==========")
        print("ANÁLISE SINTÁTICA")
        print("==========")
        parser = Parser(tokens)
        parser.analisar()
        
        print("SUCESSO: O código é sintaticamente válido segundo a gramática MiniC!")

    except ErroLexico as e:
        print(f"\n[ERRO LÉXICO]: {e}")
    except ErroSintatico as e:
        print(f"\n[ERRO SINTÁTICO]: {e}")
    except FileNotFoundError:
        print(f"\n[ERRO]: Arquivo '{caminho_arquivo}' não foi encontrado.")

if __name__ == "__main__":
    main()