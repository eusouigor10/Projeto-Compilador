from leitor import ler_arquivo
from lexico import analisar

programa = ler_arquivo("testes/valido.mc")

tokens = analisar(programa)
print('==========')
print('PROGRAMA')
print('==========')
print(programa)
print('==========')
print('TOKENS')
print('==========')
for token in tokens:
    print(token)
print('==========')