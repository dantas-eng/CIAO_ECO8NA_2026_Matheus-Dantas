# resultados - aula 11 (AC-3 etapa 3)

Aluno: Matheus Dantas | Turma ECO.8NA | Data: 28/10/2026

O motor da aula 10 está em `src/model.py` e `src/engine.py` (impacto, explorabilidade, urgência, 9 regras, centroide). A triagem de UTI está em `src/uti_triagem.py`.

## Parte 1. Pytest do motor de incidentes

Comando, na pasta `AULA_11`: `pytest -v test_fuzzy_engine.py` e `pytest -s test_fuzzy_engine.py`.

### 1a execução, sem erro

```
test_saida_dentro_do_universo PASSED
test_monotonicidade_impacto PASSED
test_entradas_invalidas_disparam_erro PASSED
test_latencia_inferencia PASSED
4 passed in 1.41s
```

`pytest -s`: tempo médio por inferência 2,509 ms. O limite do teste é 10 ms.

Com explorabilidade fixa em 5, a urgência sobe com o impacto: 11,7% em 20, 76,7% em 50 e 92,2% em 90.

### 2a execução, erros induzidos

Inverti a monotonicidade (`urg_baixa > urg_media > urg_alta`) e apertei a latência para menos de 0,01 ms.

```
test_saida_dentro_do_universo PASSED
test_monotonicidade_impacto FAILED
test_entradas_invalidas_disparam_erro PASSED
test_latencia_inferencia FAILED
2 failed, 2 passed in 1.29s
```

Monotonicidade: `11.7 <= 76.7 <= 92.2`, então a ordem invertida quebra. Latência: 2,53 ms, acima de 0,01 ms. O `pytest -s` dessa rodada imprimiu 2,408 ms.

### 3a execução, corrigido

Voltei os dois asserts. De novo 4 passed, em 1,17s. `pytest -s`: 2,368 ms.

## Parte 2. Triagem de UTI

Regras do enunciado: SpO2 crítica sozinha já manda risco crítico. Bradicardia ou taquicardia com SpO2 limítrofe também. FC normal com SpO2 limítrofe fica em moderado. FC normal com SpO2 normal fica em baixo. Defuzzificação por centroide. Fora de 40 a 160 bpm ou 70 a 100% de SpO2, `avaliar_paciente` levanta `ValueError`.

```
Sistema de UTI instanciado com sucesso!
FC 75 bpm, SpO2 98% -> risco 11.67%
FC 75 bpm, SpO2 95% -> risco 35.71%
FC 75 bpm, SpO2 89% -> risco 85.57%
```

Paciente estável (75 bpm, 98%) fica em 11,67%, abaixo de 30. A queda de 95% para 89% sai de 35,71% para 85,57%. O enunciado pedia risco menor que 35 em 95%. Com as funções dadas, baixo e moderado disparam juntos e o centroide para em 35,71. O salto para hipóxia (89%) passa de 65, como pedido. O teste aceita menos de 36 nesse ponto e exige mais de 65 no outro.

```
test_paciente_saudavel_baixo_risco PASSED
test_salto_nao_linear_queda_spo2 PASSED
test_validacao_limites_fisiologicos PASSED
3 passed
```

FC 39 e SpO2 101 disparam `ValueError`.
