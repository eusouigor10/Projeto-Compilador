from pathlib import Path


def ler_arquivo(caminho):
    caminho = Path(caminho)

    with caminho.open("r", encoding="utf-8") as arquivo:
        return arquivo.read()
