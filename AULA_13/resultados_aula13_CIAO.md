# resultados - aula 13 (AC-4 parte final)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 18/11/2026

Seis scripts, `aula13_lab01.py` a `aula13_lab06.py`. Os ímpares vieram prontos no roteiro. Nos pares eu fechei os TODOs.

## Inteiros e contínuos

No exercício 1 o NSGA-II usa `IntegerRandomSampling` e `RoundingRepair` no SBX e no PM. Pods vão de 1 a 30, analistas de 1 a 15. População 30, 40 gerações, seed 42. As soluções saíram inteiras. Amostra das cinco primeiras:

```
Pods: 30 | Analistas: 15 => Latencia:  23.33ms | Custo: R$ 1215.00
Pods:  1 | Analistas:  1 => Latencia: 550.00ms | Custo: R$   63.00
Pods:  2 | Analistas:  1 => Latencia: 350.00ms | Custo: R$   81.00
Pods:  3 | Analistas:  1 => Latencia: 283.33ms | Custo: R$   99.00
Pods:  4 | Analistas:  1 => Latencia: 250.00ms | Custo: R$  117.00
```

SBX e PM trabalham em float. Sem o repair, o filho pode sair 2,4 pods ou 7,1 analistas, e isso não existe na escala. O sampling já nasce inteiro. O `RoundingRepair` arredonda depois do cruzamento e da mutação. Gráfico em `lab01_pareto.png`.

O exercício 2 é o mesmo arranjo no cluster: réplicas de 2 a 40, nós de 1 a 12, população 25, 35 gerações, seed 10. As 25 soluções ficaram inteiras. Menor tempo: 40 réplicas e 12 nós, 31,67 ms, USD 1500,00. Menor custo: 2 réplicas e 1 nó, 500,00 ms, USD 109,00.

No exercício 3 as variáveis são contínuas, de 0,1 a 10, e não tem `RoundingRepair`. Com 20 gerações e seed 42, a config A (eta 5, mutação 0,5) espalhou o objetivo 1 de 0,14 a 109,67. A config B (eta 30, mutação 0,05) ficou de 1,10 a 109,38. A A chegou mais perto do objetivo 1 baixo. Gráfico em `lab03_operadores.png`.

## Hipervolume (exercício 4)

Rede de sensores. Potência de 1 a 100 mW, intervalo de 1 a 60 s. População 40, seed 42 nas duas rodadas. Ponto de referência `[400, 600]`.

```
Hipervolume (10 geracoes): 226626.70
Hipervolume (80 geracoes): 226715.94
```

A diferença é 89,23. Dez gerações já cobriam quase a mesma área. As outras setenta só afinaram a fronteira.

## Escala hospitalar (exercício 6)

Médicos de 2 a 20, enfermeiros de 4 a 40, os dois inteiros. Custo = 1200 vezes médicos + 450 vezes enfermeiros. Espera = 180/médicos + 240/enfermeiros. A restrição é `espera - 25 <= 0`. NSGA-II com os operadores inteiros, população 40, 50 gerações, seed 42. Saíram 40 soluções viáveis.

`PseudoWeights` com 0,40 no custo e 0,60 na espera. A escala escolhida foi 17 médicos e 32 enfermeiros. Custo R$ 34800,00. Espera 18,09 min, abaixo dos 25.

No exercício 5, banco com pesos 30% custo e 70% tempo de query, a escolha foi 76,6 GB de RAM e 2755 IOPS: US$ 56,52/h e 8,06 ms. Gráfico em `lab05_mcdm.png`.
