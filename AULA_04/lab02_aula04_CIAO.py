# ATIVIDADE 2: Inserção de penalidades por descumprimento de SLA
# Fonte: roteiro_aula04_CIAO.md — Exercício 2

import numpy as np

np.random.seed(15)
matriz_latencia = np.random.uniform(5, 80, (6, 6))


def calcular_custo_com_sla(rota, matriz, limite_sla=50.0):
    custo_total = 0.0
    penalidade = 0.0

    for i in range(len(rota) - 1):
        latencia_enlace = matriz[rota[i], rota[i + 1]]
        custo_total += latencia_enlace

        # Incrementa a penalidade caso a latência do enlace ultrapasse o SLA
        if latencia_enlace > limite_sla:
            penalidade += 1000.0

    return custo_total + penalidade


rota_teste = np.array([0, 1, 2, 3, 4, 5])
custo_final = calcular_custo_com_sla(rota_teste, matriz_latencia)

print(f"[Exercício 2] Custo Total (Com Penalizações de SLA): {custo_final:.2f} ms")
