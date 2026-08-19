# resultados - aula 03

## Lab 01 - Algoritmo genético (x²)

## Resultado

```
==================================================
ALGORITMO GENÉTICO PASSO A PASSO
==================================================

População inicial: [[1, 0, 0, 1, 0], [1, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 1, 1]]

==================== GERAÇÃO 0 ====================

Avaliação dos indivíduos:
  [1, 0, 0, 1, 0] → x=18 → f(x)=324
  [1, 0, 0, 1, 1] → x=19 → f(x)=361
  [0, 0, 0, 1, 1] → x= 3 → f(x)=  9
  [0, 0, 1, 0, 0] → x= 4 → f(x)= 16
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 0, 0, 1, 1] → x= 3 → f(x)=  9

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 1 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 0] → x=26 → f(x)=676

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 2 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [0, 1, 1, 1, 0] → x=14 → f(x)=196
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 3 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [0, 1, 1, 1, 0] → x=14 → f(x)=196
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 0, 0, 1, 1] → x=19 → f(x)=361

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 4 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 0, 1, 1, 1] → x=23 → f(x)=529
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 1, 1, 0] → x=30 → f(x)=900

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 5 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 0, 1, 1, 0] → x=22 → f(x)=484
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [0, 1, 0, 1, 0] → x=10 → f(x)=100
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 6 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 7 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 0, 0, 0] → x=24 → f(x)=576
  [1, 1, 0, 1, 0] → x=26 → f(x)=676
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [0, 1, 1, 1, 1] → x=15 → f(x)=225

 Melhor: x = 31 → f(x) = 961

==================================================
RESULTADO FINAL
==================================================

Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961

Ótimo global: x = 31, f(x) = 961
Erro: 0
```

Na população inicial já surgiu o indivíduo [1, 1, 1, 1, 1] com x = 31 e f(x) = 961. O melhor final foi o mesmo, com erro 0.

## Considerações

Cada solução usa 5 bits (0 ou 1), convertidos em decimal entre 0 e 31. O fitness é f(x) = x².

A população começa com 6 indivíduos aleatórios. A cada geração o código calcula o fitness, guarda o melhor (elitismo), seleciona pais por roleta, faz crossover e mutação (10% por bit), e monta a nova população.

Na geração 0 o melhor já foi x = 31 (961), porque um indivíduo sorteado era todos 1s. Nas gerações seguintes o melhor ficou em 961, mas a população ainda tinha indivíduos piores por causa do crossover e da mutação.

## Reflexões

Nesta execução o AG achou o ótimo logo na geração 0. O elitismo manteve x = 31 nas gerações seguintes. Em outra rodada, com população inicial pior, provavelmente levaria mais gerações para chegar perto de 961.


