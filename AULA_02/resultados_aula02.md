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
