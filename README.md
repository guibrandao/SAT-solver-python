# Resolvedor SAT-CNF
Este código é parte do projeto da disciplina **Projeto e Complexidade de Algoritmos 1** na Universidade de Brasília no período 1/2025. Ele decide o problema de Satisfatibilidade de Fórmulas Booleanas utilizando o [Algoritmo DPLL](https://en.wikipedia.org/wiki/DPLL_algorithm). Além de apenas decidir se uma fórmula dada é satisfatível, ele também retorna uma possível solução, caso exista.

Tiramos inspiração [desta fonte](https://github.com/safwankdb/SAT-Solver-using-DPLL) e executamos algumas modificações que contemplam aceitar fórmulas com variáveis de comprimento maior que 1 e indexação. Isso nos livra da limitaçao (pelo tamanho do nosso alfabeto) de variáveis que podemos adicionar ná fórmula. Além disso, integramos com um código para a [Transformação de Tseytin](https://pt.wikipedia.org/wiki/Transformação_de_Tseytin), transformando qualquer fórmula booleana em uma fórmula em [Forma Normal Conjuntiva](https://en.wikipedia.org/wiki/Conjunctive_normal_form) que preserva satisfatibilidade.  

## Como Usar
Escrevemos em um arquivo texto uma fórmula em FNC separando as cláusulas por linha. Por exemplo:
```
A B C
!A D B
!C E B
E !B
```
Salvamos este arquivo em .txt e executamos o seguinte comando no Terminal:

```
$ python3 DPLL.py <diretorio>/<arquivo>.txt
```

Podemos também escrever a fórmula desejada diretamente como entrada para o programa, após executá-lo.

## Exemplo

Para a fórmula FNC = (A+B+C)(!A+D+B)(!C+E+B)(E+!B), retornaremos

```
FNC = (A+B+C)(!A+D+B)(!C+E+B)(E+!B)
Cláusulas unitárias = []
FNC após propagação unitária = (E+!B)(!C+E+B)(!A+D+B)(A+B+C)

FNC = (E+!B)(!C+E+B)(!A+D+B)(A+B+C)(E)
Cláusulas unitárias = ['E']
FNC após propagação unitária = (!A+D+B)(A+B+C)

FNC = (!A+D+B)(A+B+C)(A)
Cláusulas unitárias = ['A']
FNC após propagação unitária = (D+B)

FNC = (D+B)(D)
Cláusulas unitárias = ['D']
FNC após propagação unitária = ()

Número de Decisões = 4
Propagaões Unitárias = 3

Resultado: SATISFATÍVEL
Solução:
		E = Verdadeiro
		A = Verdadeiro
		D = Verdadeiro
```

### Observação
É possível que, em execuçoes diferentes, o algoritmo retorne atribuições válidas diferentes para a mesma fórmula caso esta seja satisfatível. Isso se deve ao fato de uma fórmula poder ter mais de uma atribuição que a torne verdadeira. No entanto, o que importa é que a decisão sobre a satisfatibilidade em si esteja correta.
