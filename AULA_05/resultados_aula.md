# resultados - aula 05 (AC-2 Parte 1 - PSO)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 02/09/2026

## Missão 1 - Partícula solitária (f(x) = x²)

### Resultado

```
Posição inicial: 2.7885
Fitness inicial: 7.7759
...
Posição final: -0.027285
Fitness final: 0.000744
Ótimo global: x = 0.000000, f(x) = 0.000000
Erro: 0.027285
```

### Considerações

Uma partícula em 1D com w=0.8, c1=c2=1.5 e 20 iterações. A velocidade segue a fórmula padrão do PSO usando pBest e gBest (neste caso iguais, porque só existe uma partícula).

A posição cai de 2.79 para perto de zero. O fitness final (0.000744) não zera por completo: a partícula oscila um pouco nas últimas iterações, típico quando o passo ainda tem inércia.

### Reflexões

Completar os dois TODOs (velocidade e posição) foi direto depois de ver a fórmula no roteiro. Dá para entender o mecanismo antes de passar para o enxame.


## Missão 2 - Enxame na Rosenbrock

### Resultado

```
Início: Melhor fitness = 5.623448
Iteração  10: Melhor = 0.062847
Iteração  30: Melhor = 0.000857
Iteração  50: Melhor = 0.000106
Fim: Melhor fitness = 0.000106
Ótimo global: f(1,1) = 0.000000
```

### Considerações

20 partículas, 50 iterações, domínio x∈[-2,2] e y∈[-1,3]. Implementei `criar_particula`, `atualizar_velocidade` e `atualizar_posicao` com clip nos limites.

A Rosenbrock tem vale estreito em direção a (1,1). O enxame melhora rápido nas primeiras 30 iterações e termina com fitness 0.000106, bem perto do ótimo mas sem chegar exatamente a zero.

### Reflexões

Comparando com a Missão 1: o enxame converge melhor num problema 2D difícil. Várias partículas exploram regiões diferentes e o gBest puxa o grupo para o vale correto.


## Missão 3 - Logística (Optimus Tech)

### Resultado

```
50 clientes, 5 centros, demanda média 51.0
Iteração  20: Custo = 3716.12
Iteração 100: Custo = 3514.93
Tempo: 0.66 s
Centros: (2.70,5.32), (0.59,8.65), (5.47,1.76), (0.90,1.94), (7.74,6.12)
Custo total: 3514.93
```

### Considerações

Fitness retorna `-custo_total` (maximização do negativo do custo). Para cada cliente, somo distância ao centro mais próximo vezes demanda. O vetor da partícula tem 10 dimensões (x,y de cada centro).

O custo cai de 3716 para 3515 ao longo das 100 iterações. Os cinco centros ficam espalhados pela região 0–10, o que faz sentido para cobrir clientes aleatórios com seed 42.

### Reflexões

Foi a missão que mais código pediu (fitness + PSO completo em 10D). A lógica é parecida com a Missão 2, só que a função objetivo agora vem do problema real de logística.


## Missão 4 - Ajuste de parâmetros

### Resultado

```
| Experimento        | Custo Médio | Melhor Custo | Pior Custo  |
|--------------------|-------------|--------------|-------------|
| Padrão             |    3638.88 |      3547.08 |     3712.66 |
| Inércia Alta       |    3951.15 |      3772.40 |     4145.73 |
| Inércia Baixa      |    3647.04 |      3514.29 |     3797.89 |
| Cognitivo Alto     |    3750.04 |      3671.45 |     3808.38 |
| Social Alto        |    3952.36 |      3890.59 |     4051.99 |
| Mais Partículas    |    3635.02 |      3523.28 |     3677.28 |

Melhor configuração: Mais Partículas
Pior configuração: Social Alto
```

### Considerações

Seis experimentos, cada um com 5 execuções (mesmos clientes/demandas, seed 42). Variei w, c1, c2 e número de partículas.

"Mais Partículas" (60) teve menor custo médio (3635.02). "Social Alto" (c2=2.5) foi o pior (3952.36). Inércia alta (w=0.9) também piorou bastante, provavelmente por manter partículas explorando demais sem estabilizar.

### Reflexões

Rodar cinco vezes por configuração mostra variância: mesmo parâmetros não garantem o mesmo custo. A tabela ajuda a comparar sem confiar numa execução só.


## Relatório final

### Parte 1: O que aprendi

**O que é o PSO:** É um método de otimização inspirado em bando de pássaros. Cada partícula tem posição e velocidade no espaço de busca. A cada iteração, a velocidade combina inércia (w), memória pessoal (pBest) e influência do melhor do enxame (gBest).

**pBest vs gBest:** pBest é o melhor ponto que aquela partícula já visitou. gBest é o melhor entre todas. pBest evita que a partícula esqueça uma boa região que encontrou sozinha; gBest compartilha a descoberta do grupo.


### Parte 2: Experiência nas missões

| Missão | Encontrou o mínimo? | Observação | Dificuldade |
|--------|---------------------|------------|-------------|
| 1 | Sim (erro 0.027) | 20 iterações | Fácil |
| 2 | Quase (0.000106 vs 0) | Enxame mais eficiente que 1 partícula | Médio |
| 3 | Custo caiu ~354 unidades | 5 centros alocados | Médio |
| 4 | Melhor: 60 partículas | Pior: c2 alto | Médio |

**Missão 4 - parâmetros:**

- Melhor: w=0.7, c1=1.8, c2=1.8, 60 partículas
- Pior: w=0.7, c1=1.8, c2=2.5, 30 partículas

**Efeito dos parâmetros:**

- **Inércia (w):** w alto (0.9) aumentou o custo médio; w baixo (0.5) ficou perto do padrão.
- **Cognitivo (c1):** c1 alto puxou um pouco pior que o padrão.
- **Social (c2):** c2 alto foi o pior caso; o enxame converge cedo demais para um mínimo local.
- **Partículas:** dobrar para 60 melhorou a média com desvio menor.

**Recomendação:** Usaria w=0.7, c1=1.8, c2=1.8 com 60 partículas. Mais partículas cobrem melhor o espaço em 10 dimensões; c2 moderado evita convergência prematura.
