# resultados - aula 06 (AC-2 Parte 2 - ACO)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 09/09/2026

## Lab 01 - ACO na rede (nó 0 → nó 5)

### Resultado

```
Vizinhos do nó 0: [1, 2]
Vizinhos do nó 2: [0, 1, 3, 4]

Rotas encontradas (5 formigas):
Formiga 1: [0, 1, 2, 3, 4, 5]
Formiga 2: [0, 1, 2, 3, 4, 5]
...
Formiga 5: [0, 2, 1, 3, 4, 5]

========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

Gráficos gerados: `lab01_convergencia.png`, `lab01_feromonio.png`.

### Considerações

Implementei o ciclo completo: formigas construem rotas, calculam custo, evaporam feromônio e depositam nas arestas usadas. Com seed 42, a maioria das formigas iniciais seguiu o mesmo caminho, mas a Formiga 5 explorou outra ordem (passou pelo nó 2 antes do 1).

O custo 8.0 veio da rota 0→1→2→3→4→5 (2+1+2+1+2). A curva de convergência estabiliza rápido porque o grafo é pequeno e o melhor caminho aparece cedo.

### Questões do lab

**1. Por que várias formigas?** Uma formiga só vê um caminho por vez. Várias formigas testam rotas diferentes na mesma iteração e a colônia acumula experiência mais rápido.

**2. Por que rota barata recebe mais feromônio?** O depósito é Q/custo. Custo menor → mais feromônio → aresta mais atrativa na próxima rodada. As próximas formigas tendem a repetir o que já funcionou.

**3. Sem evaporação?** O feromônio das primeiras rotas (mesmo ruins) ficaria para sempre. O algoritmo pararia de explorar alternativas melhores. A evaporação dá chance a rotas novas.


## Lab 02 - Experimentos com parâmetros

### Resultado (resumo)

| Experimento | Parâmetro alterado | Melhor rota | Custo |
|-------------|-------------------|-------------|-------|
| Base | — | [0,1,2,3,4,5] | 8.0 |
| 1a | ALPHA=0.1 | [0,1,2,4,5] | 8.0 |
| 1b | ALPHA=5.0 | [0,1,2,3,4,5] | 8.0 |
| 2a | BETA=0.5 | [0,1,2,3,4,5] | 8.0 |
| 2b | BETA=5.0 | [0,1,2,3,4,5] | 8.0 |
| 3a | evap=0.1 | [0,1,2,3,4,5] | 8.0 |
| 3b | evap=0.9 | [0,1,2,3,4,5] | 8.0 |
| 4a | 5 formigas | [0,1,2,3,4,5] | 8.0 |
| 4b | 50 formigas | [0,1,2,3,4,5] | 8.0 |

Feromônio máximo variou bastante: evaporação 0.1 acumulou ~2486; evaporação 0.9 ficou em ~278. Com 5 formigas o máximo foi ~125; com 50 formigas ~1250.

### Considerações

Neste grafo pequeno, quase todos os experimentos acharam custo 8.0. A diferença apareceu mais na concentração de feromônio e na rota intermediária (ALPHA baixo favoreceu [0,1,2,4,5] em vez de passar pelo 3).

ALPHA alto aumenta a influência da experiência acumulada. BETA alto pesa mais o custo imediato de cada aresta. Evaporação alta "esquece" rápido; evaporação baixa mantém trilhas antigas por mais tempo. Mais formigas depositam mais feromônio por iteração.

Não gerei uma curva de convergência por experimento porque em todos os nove cenários a curva ficou igual: o custo 8.0 aparece logo nas primeiras iterações e não muda mais. Por isso usei o feromônio máximo como critério de comparação, que é onde os parâmetros realmente mostram diferença.

### Reflexões

O lab 02 é mais interpretação do que código novo. Rodar os nove cenários ajudou a ver que parâmetro mexe em exploração vs memória, mesmo quando o custo final é igual.


## Lab 03 - Completando os TODOs

### Resultado

```
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

### Considerações

Completei `calcular_atratividade`, `evaporar_feromonio`, `depositar_feromonio` e `construir_rota` conforme o roteiro. O resultado bate com o Lab 01, o que confirma que os TODOs estavam alinhados com a lógica da aula.

### Questões do lab

**1. Por que 1/custo em vez de custo?** Queremos arestas baratas mais atrativas. Custo direto faria arestas caras parecerem melhores. O inverso transforma "menor custo" em "maior atratividade".

**2. Mais feromônio na rota?** A atratividade sobe porque τ entra elevado a ALPHA. Caminhos reforçados ficam mais prováveis na escolha probabilística.

**3. Por que não revisitar nó?** Evita ciclo infinito e força caminho simples até o destino. Sem essa regra a formiga poderia ficar girando no grafo.


## Lab 04 - ACO do zero

### Resultado

```
========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

Gráfico: `lab04_convergencia.png`.

### Considerações

Montei o algoritmo seguindo os 12 requisitos do roteiro, com funções próprias (`montar_rota`, `reforcar`, `evaporar`), a matriz de custos fornecida e os parâmetros mínimos. O melhor custo foi 8.0 de novo.

A variação de parâmetros pedida no final deste lab é a mesma dos nove cenários do Lab 02, então não repeti os testes aqui.

### Questões finais

**1. Como o feromônio ajuda a aprender?** Rotas boas ganham mais feromônio; nas próximas iterações essas arestas têm maior chance de serem escolhidas. A colônia reforça o que funciona.

**2. Explorar vs aproveitar?** Explorar é testar caminhos novos (escolha probabilística). Aproveitar é seguir arestas já marcadas com feromônio. O ACO equilibra os dois via ALPHA, BETA e evaporação.

**3. Rede muito maior, o que ajustar primeiro?** Eu testaria NUM_FORMIGAS e NUM_ITERACOES. Mais formigas exploram mais o grafo por rodada; mais iterações dão tempo para o feromônio convergir. Em rede grande, poucas formigas podem nem visitar boas regiões.


## Síntese da aula

ACO combina exploração (várias formigas, escolha probabilística) e memória coletiva (feromônio + evaporação). Neste exercício o ótimo foi custo 8 na rota 0→1→2→3→4→5. A aula também introduziu a ideia de algoritmos híbridos (GA + busca local, PSO + refinamento), que será o próximo passo natural depois do ACO puro.
