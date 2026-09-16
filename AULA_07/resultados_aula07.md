# resultados - aula 07 (AC2 Parte 2 - meta-heurísticas)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 16/09/2026

## Lab 01 - ACO com busca local 2-opt

### Resultado

```
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```

Gráfico: `lab01_convergencia.png`.

### Considerações

Primeiro o ACO monta a rota no sorteio; em seguida o 2-opt tenta encurtar invertendo pedaços do caminho. Cada formiga explora na construção e já refina na busca local. Com seed 42, o custo caiu cedo e parou em 70.

### Questões do lab

**1. Como o 2-opt afeta exploration vs exploitation?**  
O ACO sozinho tende a repetir caminhos que já acumularam feromônio. O 2-opt puxa cada solução para um mínimo local antes de depositar feromônio, ou seja, intensifica (exploitation). Isso acelera a convergência, mas se o 2-opt for forte demais sem evaporação boa, a colônia pode fixar cedo em rotas que parecem ótimas localmente.

**2. E se rho = 0 (sem evaporação)?**  
O feromônio nunca some. Caminhos encontrados no começo continuam dominando as probabilidades, mesmo que exista rota melhor. A curva de convergência trava cedo e o algoritmo perde capacidade de explorar alternativas.


## Lab 02 - Algoritmo genético (mochila)

### Resultado

```
[LAB 02 - SUCESSO]
Melhor indivíduo: [0, 1, 1, 1, 1] | Fitness: 15
Peso total: 8 | Valor total: 15
```

Ativos escolhidos: índices 1, 2, 3 e 4 (pesos 2+1+4+1 = 8, valores 2+1+10+2 = 15).

### Considerações

Completei os dois TODOs (fitness com penalização e seleção por torneio) e liguei o loop evolutivo. Em 10 gerações já apareceu combinação válida com valor 15, peso 8, dentro do limite 15.

### Questões do lab

**1. Papel da mutação e mutação a 100%?**  
Mutação introduz bits novos e evita que toda a população fique igual (estagnação). Com taxa 100%, cada gene vira sorteio puro a cada geração. O AG vira busca aleatória, sem herdar boas combinações dos pais.

**2. Por que fitness 0 quando estoura peso?**  
Sem penalização, indivíduos inválidos podem ter valor alto e "enganar" a seleção. Zerar o fitness separa soluções factíveis das infactíveis e empurra a população para dentro da restrição.


## Lab 03 - PSO

### Resultado

```
[LAB 03 - SUCESSO] Melhor posição (gbest): [-0.01309447 -0.02659493]
Fitness final: 0.000879
```

### Considerações

A linha de velocidade do TODO ficou com inércia (w), termo cognitivo (c1) e social (c2). O gbest terminou perto de (0, 0), que é o mínimo da esférica.

### Questões do lab

**1. c1 = 0, o que muda?**  
A partícula deixa de puxar em direção ao seu próprio pbest. Ela passa a seguir só o gbest e a inércia. O enxame fica mais homogêneo e corre risco de convergir cedo demais para um ótimo local se a função não for simples como a esférica.

**2. Função da inércia w?**  
w controla quanto da velocidade anterior se mantém. w alto deixa a partícula "deslizar" e explorar mais regiões. w baixo freia rápido e favorece refinamento perto do melhor ponto conhecido.


## Lab 04 - Feromônio e evaporação

### Resultado

```
[LAB 04 - SUCESSO] Matriz de Feromônio Atualizada:
[[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```

Depois de rho=0.25, tudo caiu para 0.75 e os arcos dos caminhos mock receberam +1/6 ≈ 0.1667.

### Considerações

A função primeiro multiplica a matriz por (1-rho) e depois deposita 1/custo em cada aresta usada. Os enlaces 0→2, 2→1, 1→3 e 0→1, 1→3 ficaram mais fortes.

### Questões do lab

**1. Por que evaporação é necessária?**  
Sem esquecer trilhas antigas, o algoritmo reforça caminhos ruins descobertos no início. A evaporação equilibra memória e exploração.

**2. Grafos complexos sem evaporação?**  
O feromônio se acumula em poucos caminhos e o ACO para de testar rotas melhores escondidas no grafo. Em redes grandes isso piora muito a qualidade final.

**3. Relação entre latência e eta (atratividade)?**  
Na heurística do ACO, eta costuma ser 1/latência (ou 1/custo). Enlace mais curto → eta maior → maior chance de ser escolhido quando o feromônio ainda está fraco.


## Lab 05 - Memético (busca local)

### Resultado

```
[LAB 05 - SUCESSO] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
Solução Refinada: [ 2.47553974 -3.04650038] | Fitness: 35.7154
```

### Considerações

O hill climbing sorteia vizinhos com ruído pequeno e só aceita melhora. Em 20 passos já baixou o fitness, mas longe do (0,0) global. Faz sentido: Rastrigin tem vários mínimos locais e o passo é bem curto.

### Questões do lab

**1. AG puro vs memético?**  
O AG puro troca população e espera que crossover/mutação encontrem boas regiões. O memético adiciona busca local em cada indivíduo (ou em parte deles), misturando evolução global com refinamento individual.

**2. Custo de aplicar busca local em todos a cada geração?**  
O tempo por geração sobe bastante, porque cada indivíduo vira várias avaliações extras da função objetivo. Em populações grandes ou funções caras, isso pode inviabilizar o tempo de execução se não houver critério de parada ou busca local parcial.
