# LABORATÓRIO 04 - ACO do zero
# AULA 06 CIAO - AC-2 Parte 2
#
# Missão: montar o ACO seguindo os 12 requisitos do roteiro, sem partir
# do arquivo do Lab 01.

import os
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if os.environ.get("MPLBACKEND") == "Agg" or not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")

random.seed(42)


# ------------------------------------------------------------
# Requisito 1 - representar a rede com uma matriz de custos
# ------------------------------------------------------------

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

# Parâmetros mínimos pedidos no roteiro
NUM_FORMIGAS = 20
NUM_ITERACOES = 50

ALPHA = 1.0
BETA = 2.0

TAXA_EVAPORACAO = 0.5
Q = 100


# ------------------------------------------------------------
# Requisito 2 - criar a matriz de feromônio
# ------------------------------------------------------------

feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0


def vizinhos_de(no):

    lista = []

    for j in range(len(CUSTOS)):

        if j != no and CUSTOS[no][j] != np.inf:
            lista.append(j)

    return lista


# ------------------------------------------------------------
# Requisitos 4 e 5 - a formiga monta a rota e não repete nó
# ------------------------------------------------------------

def proximo_no(atual, visitados):

    candidatos = []

    for n in vizinhos_de(atual):

        if n not in visitados:
            candidatos.append(n)

    if not candidatos:
        return None

    pesos = []

    for n in candidatos:

        tau = feromonio[atual][n]
        custo = CUSTOS[atual][n]

        pesos.append((tau ** ALPHA) * ((1 / custo) ** BETA))

    total = sum(pesos)
    probs = [p / total for p in pesos]

    return random.choices(candidatos, weights=probs, k=1)[0]


def montar_rota():

    caminho = [ORIGEM]
    no = ORIGEM

    while no != DESTINO:

        seguinte = proximo_no(no, caminho)

        if seguinte is None:
            return None

        caminho.append(seguinte)
        no = seguinte

    return caminho


# ------------------------------------------------------------
# Requisito 6 - calcular o custo de cada rota
# ------------------------------------------------------------

def custo_da_rota(rota):

    total = 0

    for i in range(len(rota) - 1):
        total += CUSTOS[rota[i]][rota[i + 1]]

    return total


# ------------------------------------------------------------
# Requisitos 7 e 8 - reforçar as boas rotas e evaporar
# ------------------------------------------------------------

def reforcar(rota, custo):

    delta = Q / custo

    for i in range(len(rota) - 1):
        feromonio[rota[i]][rota[i + 1]] += delta


def evaporar():

    global feromonio

    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0


# ------------------------------------------------------------
# Requisito 9 - repetir por várias iterações
# ------------------------------------------------------------

melhor_rota = None
melhor_custo = float("inf")

historico = []

for iteracao in range(NUM_ITERACOES):

    encontradas = []

    # Requisito 3 - várias formigas por iteração
    for _ in range(NUM_FORMIGAS):

        rota = montar_rota()

        if rota is None:
            continue

        custo = custo_da_rota(rota)
        encontradas.append((rota, custo))

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_rota = rota.copy()

    evaporar()

    for rota, custo in encontradas:
        reforcar(rota, custo)

    historico.append(melhor_custo)


# ------------------------------------------------------------
# Requisitos 10 e 11 - informar a melhor rota e o custo
# ------------------------------------------------------------

print("========== RESULTADO ==========")
print("Melhor rota encontrada:", melhor_rota)
print("Melhor custo:", melhor_custo)


# ------------------------------------------------------------
# Requisito 12 - gráfico da evolução do melhor custo
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))
plt.plot(historico)
plt.xlabel("Iteração")
plt.ylabel("Melhor custo")
plt.title("Convergência do ACO (Lab 04)")
plt.grid()
plt.savefig("lab04_convergencia.png", dpi=120, bbox_inches="tight")
plt.close()

print("Gráfico salvo: lab04_convergencia.png")
