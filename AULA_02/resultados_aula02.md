# resultados - aula 02

## Lab 01 - Mochila

## Resultado

Foi executada a enumeracao completa do problema da mochila. Saida obtida:

```
Total de solucoes avaliadas: 32
Tempo de execucao: 0.000034 segundos
Melhor valor encontrado: 9
Combinacao otima (0=nao leva, 1=leva): (1, 1, 0, 1, 1)

Itens escolhidos:
 - Livro (peso: 2 , valor: 3 )
 - Fone (peso: 1 , valor: 2 )
 - Carregador (peso: 1 , valor: 3 )
 - Chocolate (peso: 1 , valor: 1 )
```

O melhor valor foi 9, combinacao (1, 1, 0, 1, 1). Entraram Livro, Fone, Carregador e Chocolate. A Camiseta ficou de fora. Peso total 5, igual a capacidade.

## Consideracoes

Cada item pode entrar ou nao (0 ou 1). Com 5 itens ha 2^5 = 32 combinacoes. O codigo testa todas e fica com a melhor valida.

Com 15 itens seriam 32768 combinacoes (2^15). Ainda roda rapido, mas o espaco cresce exponencialmente. Com 30 itens passa de 1 bilhao.

## Reflexoes

Sao 32 combinacoes porque cada um dos 5 itens tem 2 opcoes. Com 15 itens seriam 32768, ainda executavel em pouco tempo, mas o crescimento e exponencial. Problemas parecidos: mochila de viagem, compras com orcamento fixo, escolha de materias dentro da carga horaria.


## Lab 02 - TSP

## Resultado

O TSP foi resolvido por forca bruta para 4, 5 e 6 cidades.

```
=================================================================
RESULTADOS DA FORCA-BRUTA NO TSP
=================================================================

>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000081

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000129

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000669

=================================================================
OBSERVE: o numero de rotas cresce como (n-1)!  (fatorial)
4 cidades -> 6 rotas | 5 -> 24 | 6 -> 120 | 10 -> 362880 | 15 -> 87 bilhoes
=================================================================
```

| Cidades | Rotas | Tempo (s) | Melhor custo |
|---------|-------|-----------|--------------|
| 4 | 6 | 0.000081 | 80 |
| 5 | 24 | 0.000129 | 41 |
| 6 | 120 | 0.000669 | 91 |

## Consideracoes

O numero de rotas segue (n-1)!: 3!=6, 4!=24, 5!=120. Nao e linear nem quadratico, cresce muito mais rapido.

Para 10 cidades seriam 362880 rotas. Com 6 cidades o tempo foi 0.000669 s para 120 rotas. Conta grosseira: 362880 / 120 * 0.000669, cerca de 2 s no mesmo computador.

## Reflexoes

O TSP e considerado dificil porque o tempo explode com o numero de cidades. Mesmo com algoritmo correto, instancias grandes demoram demais por forca bruta.


## Lab 03 - Heuristica gulosa

## Resultado

Foram rodadas 20 instancias aleatorias da mochila (12 itens, capacidade 30).

```
Rodando 20 instancias...
Instancia  1 | Otimo:  199 | Gulosa:  199 | Gap:   0.0%
Instancia  2 | Otimo:  170 | Gulosa:  170 | Gap:   0.0%
Instancia  3 | Otimo:  155 | Gulosa:  155 | Gap:   0.0%
Instancia  4 | Otimo:  147 | Gulosa:  147 | Gap:   0.0%
Instancia  5 | Otimo:  261 | Gulosa:  261 | Gap:   0.0%
Instancia  6 | Otimo:  214 | Gulosa:  214 | Gap:   0.0%
Instancia  7 | Otimo:  191 | Gulosa:  187 | Gap:   2.1%
Instancia  8 | Otimo:  183 | Gulosa:  183 | Gap:   0.0%
Instancia  9 | Otimo:  215 | Gulosa:  206 | Gap:   4.2%
Instancia 10 | Otimo:  174 | Gulosa:  174 | Gap:   0.0%
Instancia 11 | Otimo:  262 | Gulosa:  262 | Gap:   0.0%
Instancia 12 | Otimo:  206 | Gulosa:  206 | Gap:   0.0%
Instancia 13 | Otimo:  231 | Gulosa:  231 | Gap:   0.0%
Instancia 14 | Otimo:  309 | Gulosa:  309 | Gap:   0.0%
Instancia 15 | Otimo:  294 | Gulosa:  294 | Gap:   0.0%
Instancia 16 | Otimo:  247 | Gulosa:  247 | Gap:   0.0%
Instancia 17 | Otimo:  136 | Gulosa:  134 | Gap:   1.5%
Instancia 18 | Otimo:  212 | Gulosa:  212 | Gap:   0.0%
Instancia 19 | Otimo:  243 | Gulosa:  243 | Gap:   0.0%
Instancia 20 | Otimo:  193 | Gulosa:  193 | Gap:   0.0%

===== RESUMO =====
Gap medio     : 0.39%
Gap minimo    : 0.00%
Gap maximo    : 4.19%
Desvio padrao : 1.03%
```

## Consideracoes

A heuristica gulosa escolhe itens com maior valor/peso primeiro. Gap medio 0.39%, maximo 4.19%. Na maioria das instancias bateu o otimo.

## Reflexoes

Para testes rapidos a gulosa parece suficiente neste experimento. Preferiria forca bruta quando n e pequeno e o otimo e obrigatorio.
