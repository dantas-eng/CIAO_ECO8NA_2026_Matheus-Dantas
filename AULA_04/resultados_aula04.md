# resultados - aula 04

## Lab 01 - AG combinatório (TSP)

## Resultado

```
============================================================
RESULTADOS — ALGORITMO GENÉTICO
============================================================
Melhor rota encontrada: [0 4 1 6 9 7 2 8 3 5]
Custo base da rota: 290.31
Penalidade: 0.00
Fitness final: 290.31
Tempo de execução: 712.96 ms
============================================================
```

## Considerações

Este lab usa o código do `demo_professor.py` (o repositório do professor ainda não publica `lab01_aula04_CIAO.py`). A solução é uma permutação de 10 nós formando rota fechada. O AG aplica crossover OX, mutação swap, seleção por torneio e elitismo.

O fitness soma distâncias e penaliza enlaces acima de 50 unidades. Nesta execução nenhum enlace violou o limite, então penalidade ficou zero e o fitness igualou o custo base (290.31).

## Reflexões

São 10! rotas possíveis, inviável testar todas. O AG encontrou `[0 4 1 6 9 7 2 8 3 5]` em 150 gerações. Na AULA 03 o cromossomo era binário; aqui é ordem de visita aos nós.


## Lab 02 - Penalização de SLA

## Resultado

```
[Exercício 2] Custo Total (Com Penalizações de SLA): 1160.00 ms
```

## Considerações

Código alinhado ao Exercício 2 do `roteiro_aula04_CIAO.md`, com `np.random.seed(15)`. A função soma latências e acrescenta +1000 ms por enlace acima de 50 ms.

Com a rota `[0, 1, 2, 3, 4, 5]`, só o enlace 3 → 4 passa de 50 ms (62.04 ms). A soma das latências reais fica perto de 160 ms; com uma violação o total sobe para 1160 ms.

## Reflexões

Uma única violação de SLA já transforma a rota em opção cara na avaliação. Isso força o AG (ou qualquer otimizador) a evitar trechos inviáveis, mesmo que pareçam curtos isoladamente.


## Lab 03 - Elitismo na estabilidade

## Resultado

```
[Exercício 1] Menor Custo Obtido (Elitismo=True): 198.84
```

Comparação extra (mesma seed 42, alterando só a flag):

```
Sem elitismo (USAR_ELITISMO=False): 181.98
Com elitismo (USAR_ELITISMO=True): 198.84
```

## Considerações

Script baseado no Exercício 1 do roteiro. Com `USAR_ELITISMO = True`, o melhor indivíduo passa direto para a próxima geração. O menor custo final foi 198.84 após 80 gerações.

Rodei também com elitismo desligado para comparar. Nesta seed o custo final ficou menor (181.98), mas isso veio da sorte da mutação/seleção, não de convergência garantida.

## Reflexões

Elitismo protege boas soluções já encontradas. Não garante o melhor resultado global em toda execução, mas reduz o risco de perder o melhor indivíduo no meio das gerações.

## Desafio 03 - Alocação de tarefas em servidores

## Resultado

```
============================================================
DESAFIO 03 — Alocacao de tarefas em servidores
============================================================
Melhor makespan encontrado: 138 s
Carga por servidor: [132, 134, 138, 137]
============================================================
```

## Considerações

Cada indivíduo do AG é um vetor de 20 posições (tarefa → servidor 0..3). O fitness é o makespan: a maior soma de tempos entre os quatro servidores. Com elitismo, crossover de um ponto e mutação aleatória, o AG equilibrou as cargas perto de 138 s.

## Reflexões

Minimizar o makespan é diferente de minimizar a soma total (que seria fixa). O AG precisa evitar concentrar tarefas longas no mesmo servidor, como a de 60 s.


## Desafio AC-1 - SD-WAN Zero-Trust

## Resultado

```
============================================================
DESAFIO AC-1 — SD-WAN Zero-Trust
============================================================
Rota selecionada: [0, 10, 11]
Fitness final: 5111.55
Nos penalizados (<50) na rota: [0, 10, 11]
============================================================
```

## Considerações

Topologia gerada com `np.random.seed(2026)`. A fitness combina latência, perda de pacotes e penalidade de 5000 quando a rota passa por nó com reputação abaixo de 50. Nesta execução o caminho curto `[0, 10, 11]` ainda cruzou nós de baixa reputação; o valor alto de fitness reflete a penalidade de segurança.

## Reflexões

Em SD-WAN zero-trust, latência baixa não basta se a rota passa por nós não confiáveis. O peso da penalidade (5000) domina o fitness e força o algoritmo a buscar rotas mais longas, porém seguras, quando a topologia permitir.
