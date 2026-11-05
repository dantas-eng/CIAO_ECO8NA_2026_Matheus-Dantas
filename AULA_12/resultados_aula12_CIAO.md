# resultados - aula 12, exercícios do lab (AC-4 parte 1)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 04/11/2026

O `demo_nsga2.py` continua valendo para os cinco servidores. Este arquivo cobre os sete exercícios de `lab_aula12.txt`.

## Exercício 1. Cloud

vCPUs de 1 a 32. Custo = 15 por vCPU. Latência = 300 / vCPUs. NSGA-II, 20 indivíduos, 30 gerações, seed 1.

```
[EX 01] soluções: 20
  vCPUs  1.00 | custo R$   15.00 | latência 300.00 ms
  vCPUs  1.41 | custo R$   21.10 | latência 213.25 ms
  vCPUs  5.00 | custo R$   74.99 | latência  60.01 ms
  vCPUs 14.68 | custo R$  220.24 | latência  20.43 ms
  vCPUs 22.63 | custo R$  339.52 | latência  13.25 ms
  menor custo: R$ 15.00 | menor latência: 9.38 ms
```

1 vCPU custa R$ 15 e espera 300 ms. O outro extremo chega perto de 32 vCPUs, cerca de 9,38 ms. Gráfico: `ex01_pareto_cloud.png`.

## Exercício 2. SOC

Custo = 100 por analista + 50 por regimento. Tempo = 200 / analistas + 50 / regimento. População 30, 40 gerações, seed 42.

```
[EX 02] soluções: 30
  menor custo: 1.0 analistas, 1.0 regimentos | R$ 150.09 | 249.83 min
  menor tempo: 50.0 analistas, 10.0 regimentos | R$ 5499.15 | 9.00 min
```

O canto barato deixa o tempo em cerca de 250 min. O canto rápido usa o teto das duas variáveis e cai para 9 min, por quase R$ 5.500. Gráfico: `ex02_pareto_soc.png`.

## Exercício 3. Drones

Três objetivos: tempo, custo e CO2. População 40, 50 gerações, seed 42.

```
[EX 03] soluções: 40
  menor tempo: vel 80.0, carga 1.24 | tempo 12.50 | custo 702.02 | CO2 96.74
  menor custo: vel 10.0, carga 1.00 | tempo 100.00 | custo 60.00 | CO2 15.00
  menor CO2: vel 10.0, carga 5.00 | tempo 100.00 | custo 260.00 | CO2 3.00
```

Velocidade máxima encurta o tempo e estoura custo e CO2. Carga máxima com velocidade mínima é o menor CO2, mas o tempo fica em 100. Gráfico: `ex03_pareto_drones.png`.

## Exercício 4. Portfólio

Retorno = 0,08 na renda fixa e 0,18 nas ações. O pymoo minimiza, então o retorno entra com sinal negativo. Risco = 0,02 na renda fixa e 0,25 nas ações. A soma das duas fatias não passa de 100%.

```
[EX 04] soluções viáveis na fronteira: 40
  maior retorno: RF 15.2% ações 84.3% | retorno 16.40 | risco 21.39
  menor risco: RF 0.0% ações 0.0% | retorno 0.00 | risco 0.00
```

Risco zero é não investir. O maior retorno da fronteira põe a maior parte em ações e ainda cabe no teto de 100%. Gráfico: `ex04_risco_retorno.png`.

## Exercício 5. Modelos

Profundidade de 1 a 30, estimadores de 10 a 200. População 30, 40 gerações, seed 7.

```
[EX 05] soluções: 30
  menor erro: profundidade 30.0, árvores 199.9 | erro 0.0072 | 105.95 ms
  menor latência: profundidade 1.0, árvores 10.0 | erro 0.4963 | 5.20 ms
```

Árvore rasa e poucas árvores respondem em 5,20 ms e erram mais. O outro canto quase zera o erro e passa de 100 ms. Gráfico: `ex05_erro_latencia.png`.

## Exercício 6. Bateria

Desgaste não pode passar de 1500. `n_ieq_constr=1` e `G = desgaste - 1500`. População 40, 50 gerações, seed 42. As 40 da fronteira saíram viáveis. Os extremos:

```
[EX 06] soluções na fronteira: 40 | viáveis (G <= 0): 40
  150.0 kW, 15.0 C | tempo  20.00 | desgaste 1377.8 | G -122.2
   10.0 kW, 15.0 C | tempo 299.99 | desgaste   23.7 | G -1476.3
```

A recarga mais curta usa 150 kW e 15 °C, ainda abaixo de 1500 de desgaste. Baixar a potência alonga o tempo e alivia a bateria. A lista completa ficou no console do `ex06_bateria.py`. Gráfico: `ex06_bateria.png`.

## Exercício 7. Frota de robôs

`frota_robos_problem.py`. Custo = 25 por robô + 8 vezes a velocidade ao quadrado, em R$ mil. Tempo = 120 / robôs + 40 / velocidade. Consumo `robôs * velocidade^1.5` não passa de 120. População 40, 60 gerações, seed 42.

```
[EX 07] viáveis na fronteira: 40
  menor custo: 5.0 robôs, 1.00 m/s | custo 133.0 mil | tempo 63.95 min
  intermediária: 7.7 robôs, 2.81 m/s | custo 255.4 mil | tempo 29.84 min
  menor tempo: 16.8 robôs, 3.71 m/s | custo 530.3 mil | tempo 17.93 min
```

Cinco robôs a 1 m/s é o piso do custo e o ciclo mais longo. A do meio corta o tempo pela metade pagando cerca de R$ 255 mil. A mais rápida ainda respeita a bateria, com 16,8 robôs a 3,71 m/s. Gráfico: `ex07_frota_robos.png`.
