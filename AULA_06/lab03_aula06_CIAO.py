# LABORATÓRIO 03 - Completando o ACO
# AULA 06 CIAO - AC-2 Parte 2
#
# Os desafios pedem para completar as partes que estavam como TODO
# a partir do código estudado no Laboratório 01.

import random

import numpy as np

random.seed(42)


# ============================================================
# 1. REPRESENTAÇÃO DA REDE
# ============================================================

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
])

ORIGEM = 0
DESTINO = 5

NUM_FORMIGAS = 20
NUM_ITERACOES = 50

ALPHA = 1.0
BETA = 2.0

TAXA_EVAPORACAO = 0.5
Q = 100

feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0


# ============================================================
# 2. FUNÇÃO DE VIZINHOS (já vinha pronta)
# ============================================================

def obter_vizinhos(no):

    vizinhos = []

    for proximo in range(len(CUSTOS)):

        if proximo != no and CUSTOS[no][proximo] != np.inf:
            vizinhos.append(proximo)

    return vizinhos


# ============================================================
# 3. DESAFIO 1 - CALCULAR A ATRATIVIDADE
# ============================================================

# Fórmula do Laboratório 01:
# atratividade = feromônio^ALPHA * (1 / custo)^BETA

def calcular_atratividade(no_atual, proximo):

    fer = feromonio[no_atual][proximo]
    custo = CUSTOS[no_atual][proximo]

    atratividade = (fer ** ALPHA) * ((1 / custo) ** BETA)

    return atratividade


# ============================================================
# 4. DESAFIO 2 - EVAPORAÇÃO
# ============================================================

def evaporar_feromonio():

    global feromonio

    feromonio *= (1 - TAXA_EVAPORACAO)

    feromonio[CUSTOS == np.inf] = 0


# ============================================================
# 5. DESAFIO 3 - DEPÓSITO
# ============================================================

def depositar_feromonio(rota, custo):

    # Quanto menor o custo, maior deve ser o depósito.
    deposito = Q / custo

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        feromonio[origem][destino] += deposito


def calcular_custo(rota):

    total = 0

    for i in range(len(rota) - 1):
        total += CUSTOS[rota[i]][rota[i + 1]]

    return total


# ============================================================
# 6. DESAFIO 4 - CONSTRUIR UMA ROTA
# ============================================================

def construir_rota():

    rota = [ORIGEM]
    atual = ORIGEM

    while atual != DESTINO:

        # Descobre os vizinhos disponíveis.
        vizinhos = obter_vizinhos(atual)

        candidatos = [no for no in vizinhos if no not in rota]

        if not candidatos:
            return None

        # Calcula as atratividades.
        atratividades = []

        for proximo in candidatos:
            atratividades.append(calcular_atratividade(atual, proximo))

        # Transforma as atratividades em probabilidades.
        soma = sum(atratividades)
        probabilidades = [valor / soma for valor in atratividades]

        # Escolhe o próximo nó.
        proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]

        rota.append(proximo)
        atual = proximo

    return rota


# ============================================================
# 7. EXECUÇÃO
# ============================================================

melhor_rota = None
melhor_custo = float("inf")

for iteracao in range(NUM_ITERACOES):

    rotas = []

    for _ in range(NUM_FORMIGAS):

        rota = construir_rota()

        if rota is not None:

            custo = calcular_custo(rota)

            rotas.append((rota, custo))

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota.copy()

    evaporar_feromonio()

    for rota, custo in rotas:
        depositar_feromonio(rota, custo)

print("Melhor rota:", melhor_rota)
print("Melhor custo:", melhor_custo)
