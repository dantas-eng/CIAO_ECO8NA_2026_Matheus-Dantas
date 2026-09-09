# LABORATÓRIO 02 - Experimentando o ACO
# AULA 06 CIAO - AC-2 Parte 2
#
# O código do Lab 01 já está pronto. Aqui o trabalho é mudar os parâmetros,
# executar de novo e registrar os resultados.

import random

import numpy as np

random.seed(42)


# ============================================================
# REDE (mesma do Laboratório 01)
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
Q = 100


# ============================================================
# ACO DO LAB 01, AGORA RECEBENDO OS PARÂMETROS
# ============================================================

def rodar_experimento(nome, num_formigas, num_iteracoes, alpha, beta, taxa_evaporacao):

    feromonio = np.ones_like(CUSTOS, dtype=float)
    feromonio[CUSTOS == np.inf] = 0

    melhor_rota = None
    melhor_custo = float("inf")

    for iteracao in range(num_iteracoes):

        rotas = []

        for _ in range(num_formigas):

            # --- construção da rota ---
            rota = [ORIGEM]
            atual = ORIGEM

            while atual != DESTINO:

                candidatos = []

                for proximo in range(len(CUSTOS)):

                    if proximo == atual:
                        continue

                    if CUSTOS[atual][proximo] == np.inf:
                        continue

                    if proximo in rota:
                        continue

                    candidatos.append(proximo)

                if not candidatos:
                    rota = None
                    break

                atratividades = []

                for proximo in candidatos:

                    fer = feromonio[atual][proximo]
                    custo = CUSTOS[atual][proximo]

                    atratividades.append((fer ** alpha) * ((1 / custo) ** beta))

                soma = sum(atratividades)
                probabilidades = [valor / soma for valor in atratividades]

                proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]

                rota.append(proximo)
                atual = proximo

            if rota is None:
                continue

            # --- custo da rota ---
            custo = 0

            for i in range(len(rota) - 1):
                custo += CUSTOS[rota[i]][rota[i + 1]]

            rotas.append((rota, custo))

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota.copy()

        # --- evaporação ---
        feromonio *= (1 - taxa_evaporacao)
        feromonio[CUSTOS == np.inf] = 0

        # --- depósito ---
        for rota, custo in rotas:

            deposito = Q / custo

            for i in range(len(rota) - 1):
                feromonio[rota[i]][rota[i + 1]] += deposito

    print("\n========== RESULTADO DO EXPERIMENTO ==========")
    print("Experimento:", nome)
    print("Número de formigas:", num_formigas)
    print("Número de iterações:", num_iteracoes)
    print("ALPHA:", alpha)
    print("BETA:", beta)
    print("Taxa de evaporação:", taxa_evaporacao)
    print("Melhor rota:", melhor_rota)
    print("Melhor custo:", melhor_custo)
    print("Feromônio máximo:", float(np.max(feromonio)))


# ============================================================
# EXPERIMENTO BASE
# ============================================================

rodar_experimento("Base", 20, 50, 1.0, 2.0, 0.5)


# ============================================================
# EXPERIMENTO 1 - INFLUÊNCIA DO ALPHA
# ============================================================

rodar_experimento("1a - ALPHA = 0.1", 20, 50, 0.1, 2.0, 0.5)
rodar_experimento("1b - ALPHA = 5.0", 20, 50, 5.0, 2.0, 0.5)


# ============================================================
# EXPERIMENTO 2 - INFLUÊNCIA DO BETA
# ============================================================

rodar_experimento("2a - BETA = 0.5", 20, 50, 1.0, 0.5, 0.5)
rodar_experimento("2b - BETA = 5.0", 20, 50, 1.0, 5.0, 0.5)


# ============================================================
# EXPERIMENTO 3 - EVAPORAÇÃO
# ============================================================

rodar_experimento("3a - evaporação = 0.1", 20, 50, 1.0, 2.0, 0.1)
rodar_experimento("3b - evaporação = 0.9", 20, 50, 1.0, 2.0, 0.9)


# ============================================================
# EXPERIMENTO 4 - NÚMERO DE FORMIGAS
# ============================================================

rodar_experimento("4a - 5 formigas", 5, 50, 1.0, 2.0, 0.5)
rodar_experimento("4b - 50 formigas", 50, 50, 1.0, 2.0, 0.5)
