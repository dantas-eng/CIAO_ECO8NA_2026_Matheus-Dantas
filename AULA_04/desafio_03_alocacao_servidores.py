# Desafio 03 — Balanceamento de carga em servidores (AC-1 final)
# Objetivo: minimizar o makespan (maior carga entre 4 servidores)

import numpy as np

T = [12, 35, 40, 8, 15, 22, 19, 45, 60, 31, 14, 28, 50, 18, 25, 33, 42, 10, 5, 29]
NUM_TAREFAS = len(T)
NUM_SERVIDORES = 4

TAM_POP = 80
GERACOES = 200
TAXA_MUT = 0.15

np.random.seed(42)


def calcular_makespan(alocacao):
    cargas = [0] * NUM_SERVIDORES
    for tarefa, servidor in enumerate(alocacao):
        cargas[servidor] += T[tarefa]
    return max(cargas)


def criar_individuo():
    return np.random.randint(0, NUM_SERVIDORES, size=NUM_TAREFAS)


def crossover(pai1, pai2):
    ponto = np.random.randint(1, NUM_TAREFAS)
    filho1 = np.concatenate([pai1[:ponto], pai2[ponto:]])
    filho2 = np.concatenate([pai2[:ponto], pai1[ponto:]])
    return filho1, filho2


def mutacao(ind):
    copia = ind.copy()
    for i in range(NUM_TAREFAS):
        if np.random.rand() < TAXA_MUT:
            copia[i] = np.random.randint(0, NUM_SERVIDORES)
    return copia


def algoritmo_genetico():
    populacao = [criar_individuo() for _ in range(TAM_POP)]

    for _ in range(GERACOES):
        custos = [calcular_makespan(ind) for ind in populacao]
        melhor_idx = int(np.argmin(custos))
        novos = [populacao[melhor_idx].copy()]

        while len(novos) < TAM_POP:
            i1, i2 = np.random.choice(TAM_POP, 2, replace=False)
            pai1 = populacao[i1] if custos[i1] < custos[i2] else populacao[i2]
            pai2 = populacao[i2] if custos[i1] < custos[i2] else populacao[i1]
            f1, f2 = crossover(pai1, pai2)
            novos.append(mutacao(f1))
            if len(novos) < TAM_POP:
                novos.append(mutacao(f2))

        populacao = novos

    custos_finais = [calcular_makespan(ind) for ind in populacao]
    melhor_idx = int(np.argmin(custos_finais))
    return populacao[melhor_idx], custos_finais[melhor_idx]


if __name__ == "__main__":
    melhor_alocacao, makespan = algoritmo_genetico()
    cargas = [0] * NUM_SERVIDORES
    for tarefa, servidor in enumerate(melhor_alocacao):
        cargas[servidor] += T[tarefa]

    print("=" * 60)
    print("DESAFIO 03 — Alocacao de tarefas em servidores")
    print("=" * 60)
    print(f"Melhor makespan encontrado: {makespan} s")
    print(f"Alocacao (tarefa -> servidor): {list(melhor_alocacao)}")
    print(f"Carga por servidor: {cargas}")
    print("=" * 60)
