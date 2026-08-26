# =============================================================================
# RELATORIO TECNICO — Motor SD-WAN Zero-Trust (AC-1 final)
#
# Topologia: 12 roteadores (0 a 11), origem 0, destino 11.
# Fitness: w1 * latencia total + w2 * perda total + P_seguranca (5000 se rota
#          passar por no com reputacao < 50).
# Semente: np.random.seed(2026) para reprodutibilidade.
#
# A rota escolhida evita nos nao confiaveis quando possivel, trocando caminho
# por enlaces um pouco mais lentos em vez de pagar +5000.
# =============================================================================

import numpy as np

NUM_NOS = 12
ORIGEM = 0
DESTINO = 11
W1 = 1.0
W2 = 10.0
PENALIDADE_SEGURANCA = 5000.0

TAM_POP = 60
GERACOES = 150
TAXA_MUT = 0.25

np.random.seed(2026)

reputacao = np.random.uniform(20, 95, NUM_NOS)

adj = [[] for _ in range(NUM_NOS)]
for i in range(NUM_NOS):
    for j in range(i + 1, NUM_NOS):
        if np.random.rand() < 0.35:
            lat = float(np.random.uniform(5, 80))
            perda = float(np.random.uniform(0, 5))
            adj[i].append((j, lat, perda))
            adj[j].append((i, lat, perda))

for i in range(NUM_NOS - 1):
    if not any(v == i + 1 for v, _, _ in adj[i]):
        lat = float(np.random.uniform(10, 40))
        perda = float(np.random.uniform(0, 2))
        adj[i].append((i + 1, lat, perda))
        adj[i + 1].append((i, lat, perda))


def caminho_valido(caminho):
    if len(caminho) < 2:
        return False
    if caminho[0] != ORIGEM or caminho[-1] != DESTINO:
        return False
    for a, b in zip(caminho, caminho[1:]):
        if not any(v == b for v, _, _ in adj[a]):
            return False
    return True


def gerar_caminho_aleatorio():
    atual = ORIGEM
    visitados = {ORIGEM}
    caminho = [ORIGEM]
    tentativas = 0

    while atual != DESTINO and tentativas < 200:
        vizinhos = [v for v, _, _ in adj[atual] if v not in visitados]
        if not vizinhos:
            return gerar_caminho_aleatorio()
        prox = int(np.random.choice(vizinhos))
        caminho.append(prox)
        visitados.add(prox)
        atual = prox
        tentativas += 1

    if caminho[-1] != DESTINO:
        return gerar_caminho_aleatorio()
    return caminho


def calcular_fitness(caminho):
    if not caminho_valido(caminho):
        return float("inf")

    lat_total = 0.0
    perda_total = 0.0
    for a, b in zip(caminho, caminho[1:]):
        for v, lat, perda in adj[a]:
            if v == b:
                lat_total += lat
                perda_total += perda
                break

    penalidade = PENALIDADE_SEGURANCA if any(reputacao[n] < 50 for n in caminho) else 0.0
    return W1 * lat_total + W2 * perda_total + penalidade


def crossover(pai1, pai2):
    comum = list(set(pai1) & set(pai2) - {ORIGEM, DESTINO})
    if not comum:
        return pai1[:], pai2[:]
    no = int(np.random.choice(comum))
    i1, i2 = pai1.index(no), pai2.index(no)
    filho1 = pai1[: i1 + 1] + [n for n in pai2[i2 + 1 :] if n not in pai1[: i1 + 1]]
    filho2 = pai2[: i2 + 1] + [n for n in pai1[i1 + 1 :] if n not in pai2[: i2 + 1]]
    return filho1, filho2


def mutacao(caminho):
    copia = caminho[:]
    if np.random.rand() < TAXA_MUT and len(copia) > 2:
        idx = np.random.randint(1, len(copia) - 1)
        no_anterior = copia[idx - 1]
        vizinhos = [v for v, _, _ in adj[no_anterior] if v not in copia[:idx]]
        if vizinhos:
            copia[idx] = int(np.random.choice(vizinhos))
            copia = copia[: idx + 1]
            atual = copia[-1]
            visitados = set(copia)
            while atual != DESTINO:
                viz = [v for v, _, _ in adj[atual] if v not in visitados]
                if not viz:
                    return gerar_caminho_aleatorio()
                prox = int(np.random.choice(viz))
                copia.append(prox)
                visitados.add(prox)
                atual = prox
    return copia if caminho_valido(copia) else gerar_caminho_aleatorio()


def algoritmo_genetico():
    populacao = [gerar_caminho_aleatorio() for _ in range(TAM_POP)]

    for _ in range(GERACOES):
        fitnesses = [calcular_fitness(c) for c in populacao]
        melhor_idx = int(np.argmin(fitnesses))
        novos = [populacao[melhor_idx][:]]

        while len(novos) < TAM_POP:
            i1, i2 = np.random.choice(TAM_POP, 2, replace=False)
            p1 = populacao[i1] if fitnesses[i1] < fitnesses[i2] else populacao[i2]
            p2 = populacao[i2] if fitnesses[i1] < fitnesses[i2] else populacao[i1]
            f1, f2 = crossover(p1, p2)
            novos.append(mutacao(f1))
            if len(novos) < TAM_POP:
                novos.append(mutacao(f2))

        populacao = novos

    fitnesses = [calcular_fitness(c) for c in populacao]
    melhor_idx = int(np.argmin(fitnesses))
    return populacao[melhor_idx], fitnesses[melhor_idx]


if __name__ == "__main__":
    rota, fitness = algoritmo_genetico()
    nos_risco = [n for n in rota if reputacao[n] < 50]

    print("=" * 60)
    print("DESAFIO AC-1 — SD-WAN Zero-Trust")
    print("=" * 60)
    print(f"Rota selecionada: {rota}")
    print(f"Fitness final: {fitness:.2f}")
    print(f"Reputacao por no da rota: {[round(reputacao[n], 1) for n in rota]}")
    if nos_risco:
        print(f"Nos penalizados (<50) na rota: {nos_risco}")
    else:
        print("Rota evita nos com reputacao < 50 (sem penalidade de seguranca).")
    print("=" * 60)
