# LABORATÓRIO 01 - ACO: Otimização por Colônia de Formigas
# AULA 06 CIAO - AC-2 Parte 2

# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

import os
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if os.environ.get("MPLBACKEND") == "Agg" or not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")

random.seed(42)


# ============================================================
# 2. REPRESENTAÇÃO DA REDE
# ============================================================

# Cada posição da matriz representa o custo para ir de um nó para outro.
# np.inf significa que não existe conexão direta entre os nós.

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


# ============================================================
# 3. PARÂMETROS DO ACO
# ============================================================

NUM_FORMIGAS = 20
NUM_ITERACOES = 50

ALPHA = 1.0
BETA = 2.0

TAXA_EVAPORACAO = 0.5
Q = 100

# ALPHA controla a influência do feromônio.
# BETA controla a influência do custo do caminho.
# Quanto maior BETA, maior a preferência por caminhos de menor custo.


# ============================================================
# 4. MATRIZ DE FEROMÔNIO
# ============================================================

# No início todos os caminhos existentes têm a mesma quantidade de feromônio.

feromonio = np.ones_like(CUSTOS, dtype=float)

# Onde não existe conexão, não existe feromônio.
feromonio[CUSTOS == np.inf] = 0

print("Matriz inicial de feromônio:")
print(feromonio)


# ============================================================
# 5. VIZINHOS DE UM NÓ
# ============================================================

# A formiga só pode caminhar para nós que possuem conexão direta.

def obter_vizinhos(no):

    vizinhos = []

    for proximo in range(len(CUSTOS)):

        # Ignora o próprio nó e as conexões inexistentes.
        if proximo != no and CUSTOS[no][proximo] != np.inf:
            vizinhos.append(proximo)

    return vizinhos


print("Vizinhos do nó 0:", obter_vizinhos(0))
print("Vizinhos do nó 2:", obter_vizinhos(2))


# ============================================================
# 6. ESCOLHENDO O PRÓXIMO NÓ
# ============================================================

# A formiga considera o feromônio e o custo do caminho.
# Mais feromônio e menor custo deixam o caminho mais atrativo.

def escolher_proximo(no_atual, visitados):

    vizinhos = obter_vizinhos(no_atual)

    # A formiga não pode voltar para um nó que já visitou.
    candidatos = [no for no in vizinhos if no not in visitados]

    if not candidatos:
        return None

    atratividades = []

    for proximo in candidatos:

        fer = feromonio[no_atual][proximo]
        custo = CUSTOS[no_atual][proximo]

        atratividade = (fer ** ALPHA) * ((1 / custo) ** BETA)

        atratividades.append(atratividade)

    # Transforma as atratividades em probabilidades.
    soma = sum(atratividades)
    probabilidades = [valor / soma for valor in atratividades]

    # A escolha é probabilística, então a formiga pode explorar caminhos novos.
    return random.choices(candidatos, weights=probabilidades, k=1)[0]


# ============================================================
# 7. CONSTRUINDO UMA ROTA
# ============================================================

def construir_rota():

    rota = [ORIGEM]
    atual = ORIGEM

    while atual != DESTINO:

        proximo = escolher_proximo(atual, rota)

        if proximo is None:
            return None

        rota.append(proximo)
        atual = proximo

    return rota


# Teste com algumas formigas.
print("\nRotas encontradas:")

for i in range(5):
    rota = construir_rota()
    print(f"Formiga {i + 1}: {rota}")


# ============================================================
# 8. CUSTO DA ROTA
# ============================================================

# O custo total é a soma dos custos de todos os enlaces utilizados.

def calcular_custo(rota):

    total = 0

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        total += CUSTOS[origem][destino]

    return total


rota = construir_rota()

if rota is not None:
    print("\nRota:", rota)
    print("Custo:", calcular_custo(rota))


# ============================================================
# 9. DEPÓSITO DE FEROMÔNIO
# ============================================================

# Depois de terminar a rota a formiga deixa feromônio no caminho percorrido.
# Rotas melhores recebem mais feromônio.

def depositar_feromonio(rota, custo):

    # Quanto menor o custo, maior o depósito.
    deposito = Q / custo

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        feromonio[origem][destino] += deposito


# ============================================================
# 10. EVAPORAÇÃO DO FEROMÔNIO
# ============================================================

# O feromônio não permanece para sempre. A evaporação abre espaço para
# novas experiências.

def evaporar_feromonio():

    global feromonio

    feromonio *= (1 - TAXA_EVAPORACAO)

    # Mantém zero onde não existe conexão.
    feromonio[CUSTOS == np.inf] = 0


# ============================================================
# 11. EXECUTANDO O ACO
# ============================================================

melhor_rota = None
melhor_custo = float("inf")

historico = []

for iteracao in range(NUM_ITERACOES):

    rotas = []

    # Cada formiga constrói uma rota.
    for _ in range(NUM_FORMIGAS):

        rota = construir_rota()

        if rota is not None:

            custo = calcular_custo(rota)

            rotas.append((rota, custo))

            # Guarda a melhor solução encontrada até agora.
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota.copy()

    # Primeiro diminui o feromônio existente.
    evaporar_feromonio()

    # Depois reforça os caminhos usados pelas formigas.
    for rota, custo in rotas:
        depositar_feromonio(rota, custo)

    # Guarda o melhor custo para visualizar a evolução.
    historico.append(melhor_custo)


print("\n========== RESULTADO ==========")
print("Melhor rota encontrada:", melhor_rota)
print("Melhor custo:", melhor_custo)


# ============================================================
# 12. CURVA DE CONVERGÊNCIA
# ============================================================

plt.figure(figsize=(10, 5))
plt.plot(historico)
plt.xlabel("Iteração")
plt.ylabel("Melhor custo")
plt.title("Convergência do ACO")
plt.grid()
plt.savefig("lab01_convergencia.png", dpi=120, bbox_inches="tight")
plt.close()


# ============================================================
# 13. MATRIZ FINAL DE FEROMÔNIO
# ============================================================

# Mostra onde o feromônio ficou mais concentrado depois da execução.

plt.figure(figsize=(7, 6))
plt.imshow(feromonio, cmap="hot")
plt.colorbar(label="Quantidade de feromônio")
plt.xlabel("Nó de destino")
plt.ylabel("Nó de origem")
plt.title("Memória Coletiva da Colônia")
plt.savefig("lab01_feromonio.png", dpi=120, bbox_inches="tight")
plt.close()

print("\nGráficos salvos: lab01_convergencia.png, lab01_feromonio.png")
