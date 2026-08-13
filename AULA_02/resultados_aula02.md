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
