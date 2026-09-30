# resultados - aula 08 (fechamento AC-2)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 30/09/2026

## Lab 01 - PSO e balanceamento entre AZs

### Resultado

```
[LAB 01 - PSO balanceamento de carga]

População 10 partículas:
  W = [1e-06, 0.099994, 1e-06, 0.900002, 1e-06, 1e-06]
  sum(W) = 1.0000000000
  fitness final = 30.500070
  temperatura média ponderada = 30.5001 °C

População 30 partículas:
  W = [1e-06, 0.099994, 1e-06, 0.900002, 1e-06, 1e-06]
  sum(W) = 1.0000000000
  fitness final = 30.500070
  temperatura média ponderada = 30.5001 °C

População 50 partículas:
  W = [1e-06, 0.099994, 1e-06, 0.900002, 1e-06, 1e-06]
  sum(W) = 1.0000000000
  fitness final = 30.500070
  temperatura média ponderada = 30.5001 °C
```

| Partículas | sum(W) | Temp. média (°C) | Fitness |
|---:|---:|---:|---:|
| 10 | 1.000000 | 30.5001 | 30.5001 |
| 30 | 1.000000 | 30.5001 | 30.5001 |
| 50 | 1.000000 | 30.5001 | 30.5001 |

Gráfico: `lab01_pso_populacoes.png`.

### Considerações

Implementei o PSO contínuo com normalização a cada passo para manter sum(w)=1. A temperatura média ponderada ficou em torno de 30,5 °C porque o enxame concentrou carga na AZ4 (coeficiente 30). Usei penalidade externa quando alguma AZ passa de 75 °C; com essa distribuição ninguém estourou o limite. Com seed 42, 10, 30 e 50 partículas convergiram para o mesmo W.

## Lab 02 - AG binário em Edge

### Resultado

Estratégia A (fitness 0 se violar RAM ou CPU):
- Melhor indivíduo: `[0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0]`
- Valor 38, RAM 14 GB, CPU 8 cores
- Média fitness na última geração: 26,85 | desvio: 13,87

Estratégia B (penalidade proporcional ao excedente):
- Melhor indivíduo: `[1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0]`
- Valor 38, RAM 13 GB, CPU 8 cores
- Média fitness na última geração: 32,68 | desvio: 7,23

Gráfico: `lab02_ag_comparativo.png`.

### Considerações

Torneio, crossover de um ponto e mutação binária iguais nas duas runs. A estratégia A manteve diversidade Hamming um pouco maior (0,29 vs 0,22), mas a B deixou a média de fitness mais alta nas últimas gerações porque indivíduos quase válidos ainda contribuem com gradiente. As duas fecharam com valor 38; a B chegou com menos RAM (13 GB).

## Lab 03 - ACO para árvore de baixa latência

### Resultado

Matriz de adjacência final:

```
[[0 0 1 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 0 0]
 [1 1 0 0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 1 1 1 0 1 0 0 0]
 [0 0 0 0 0 1 0 1 0 0]
 [0 0 0 0 0 0 1 0 1 1]
 [0 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 1 0 0]]
```

Latência acumulada nos pares críticos: ACO 867,00 | aleatório (média 30 árvores) 1862,07 | ganho 53,44%. Árvore válida: sim.

### Considerações

Cada formiga monta árvore sem ciclo, só ligando nó novo à componente. Feromônio evapora com rho=0,2 e só reforça a melhor topologia da iteração. Comparar com árvore aleatória deixou claro o quanto a escolha de arestas importa na latência total entre pares.
