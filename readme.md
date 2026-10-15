# Compilador MiniC (Etapa 1) — Análise Léxica, Sintática e AST

Este repositório contém a implementação da **Parte 1** do projeto prático da disciplina de **Compiladores** (Prof. Paulo Roberto de Oliveira). O objetivo desta etapa é construir o Front-End de um compilador para a linguagem **MiniC**, cobrindo a análise léxica, a análise sintática descendente recursiva e a construção da Árvore Sintática Abstrata (AST).

---

## Sobre a Linguagem MiniC

A **MiniC** é uma linguagem de programação simplificada com sintaxe inspirada na linguagem C.

- **Tipos suportados:** `int` e `bool` (com literais `true` e `false`).
- **Palavras reservadas:** `program`, `int`, `bool`, `if`, `else`, `read`, `write`, `true`, `false`.
- **Operadores:**
  - **Aritméticos:** `+`, `-`, `*`, `/`
  - **Relacionais:** `<`, `<=`, `>`, `>=`, `==`, `!=`
  - **Lógicos:** `&&`, `||`, `!`
  - **Atribuição:** `=`
- **Delimitadores:** `(`, `)`, `{`, `}`, `;`, `,`
- **Particularidades:** Diferencia maiúsculas de minúsculas (_case-sensitive_), não possui vetores/funções/loops nesta versão, e exige declarações de variáveis antes dos comandos.

---

## Arquitetura do Projeto

O projeto foi modularizado em Python sem o uso de dependências externas para garantir clareza pedagógica e facilitar a extensão para as próximas etapas (análise semântica e geração de código intermediário).

```text
.
├── main.py                 # Ponto de entrada do compilador
├── leitor.py               # Módulo responsável pela leitura de arquivos-fonte
├── lexico.py               # Analisador Léxico (Lexer)
├── sintatico.py            # Analisador Sintático (Parser) e definição dos Nós da AST
├── util.py                 # Mapeamento de tokens, palavras reservadas e exceções
├── visualizador_ast.py     # Renderizador hierárquico da AST em formato textual
└── testes/                 # Arquivos com programas de teste em MiniC
```

---

## Como Executar

### Pré-requisitos

- **Python 3.10+** instalado na máquina.

### Passo a Passo

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/compilador-minic.git
   cd compilador-minic
   ```

2. **Execute o compilador:**
   ```bash
   python main.py
   ```

---

## Relatório Técnico de Implementação

### 1. Análise Léxica (`lexico.py` / `util.py`)

O **Analisador Léxico** realiza uma varredura sequencial sobre a string do código-fonte e converte o fluxo de caracteres em uma lista de objetos `Token`.

- **Tokens e Operadores Compostos:** Trata operadores simples e de dois caracteres (`==`, `<=`, `>=`, `!=`, `&&`, `||`) verificando o Lookahead do próximo caractere.
- **Gestão de Espaços e Linhas:** Espaços em branco e tabulações são ignorados, enquanto quebras de linha (`\n`) incrementam o contador de linhas para garantir mensagens de erro precisas.
- **Tratamento de Erros:** Dispara a exceção `ErroLexico` com a indicação da linha caso um caractere inválido seja encontrado.

### 2. Análise Sintática (`sintatico.py`)

O **Analisador Sintático** foi construído utilizando a técnica **Descendente Recursiva** (`Parser`), validando se a sequência de tokens está em conformidade com a Gramática Livre de Contexto da linguagem MiniC.

- **Precedência de Operadores:** Garantida através da hierarquia de métodos de expressões: `expressao_logica` -> `expressao_and` -> `expressao_relacional` -> `expressao_aritmetica` -> `termo` -> `fator`.
- **Tratamento de Erros:** Lança exceções `ErroSintatico` detalhadas indicando a linha, o token recebido e o símbolo esperado.

### 3. Construção da AST (`sintatico.py` & `visualizador_ast.py`)

A **Árvore Sintática Abstrata (AST)** é gerada simultaneamente à análise sintática:

- **Nós Tipados:** Utiliza `dataclasses` em Python (`Programa`, `Declaracao`, `Atribuicao`, `Condicional`, `Binario`, `Unario`, etc.).
- **Limpeza Sintática:** Símbolos estruturais e delimitadores como `;`, `{`, `}`, `(` e `)` são descartados na AST, preservando apenas a semântica do programa para as fases seguintes.
- **Visualização:** O módulo `visualizador_ast.py` imprime a árvore de forma limpa e visual no terminal utilizando conectores de caracteres (`├──`, `└──`).

---

## Estrutura de Testes

Os testes incluem programas MiniC cobrindo:

- Programas válidos com expressões aritméticas, condicionais e E/S (`read`/`write`).
- Tratamento de falhas por **Erros Léxicos** (caracteres não reconhecidos).
- Tratamento de falhas por **Erros Sintáticos** (estruturas malformadas ou falta de ponto e vírgula).

---

## Autores

- Igor Daré Grubisich
- Kauan Gomes Cardoso
