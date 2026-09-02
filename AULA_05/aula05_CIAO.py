# AULA 05 - AC-2 Parte 1: PSO (4 missões)

import os
import random
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if os.environ.get("MPLBACKEND") == "Agg" or not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")


# =============================================================================
# MISSÃO 1: A PARTÍCULA SOLITÁRIA
# =============================================================================

random.seed(42)

ITERACOES = 20
W = 0.8
C1 = 1.5
C2 = 1.5
LIMITE = 10


def funcao(x):
    return x**2


posicao = random.uniform(-LIMITE, LIMITE)
velocidade = random.uniform(-1, 1)
fitness = funcao(posicao)

pBest_pos = posicao
pBest_fit = fitness

gBest_pos = posicao
gBest_fit = fitness

historico_pos = [posicao]
historico_fit = [fitness]

print("=" * 60)
print(" PARTÍCULA SOLITÁRIA PROcurando o MÍNIMO")
print("=" * 60)
print(f"\nPosição inicial: {posicao:.4f}")
print(f"Fitness inicial: {fitness:.4f}\n")

for i in range(ITERACOES):
    r1 = random.random()
    r2 = random.random()

    velocidade_nova = W * velocidade + C1 * r1 * (pBest_pos - posicao) + C2 * r2 * (gBest_pos - posicao)
    posicao_nova = posicao + velocidade_nova
    posicao_nova = np.clip(posicao_nova, -LIMITE, LIMITE)

    fitness_novo = funcao(posicao_nova)

    posicao = posicao_nova
    velocidade = velocidade_nova
    fitness = fitness_novo

    if fitness < pBest_fit:
        pBest_fit = fitness
        pBest_pos = posicao

    if fitness < gBest_fit:
        gBest_fit = fitness
        gBest_pos = posicao

    historico_pos.append(posicao)
    historico_fit.append(fitness)

    print(f"Iteração {i+1:2d}: pos = {posicao:7.4f}, fitness = {fitness:8.4f}")

print("\n" + "=" * 60)
print(" RESULTADO FINAL")
print("=" * 60)
print(f"Posição final: {posicao:.6f}")
print(f"Fitness final: {fitness:.6f}")
print(f"Ótimo global: x = 0.000000, f(x) = 0.000000")
print(f"Erro: {abs(posicao):.6f}")

x_plot = np.linspace(-LIMITE, LIMITE, 1000)
y_plot = funcao(x_plot)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x_plot, y_plot, "b-", linewidth=2, label="f(x)")
plt.scatter(
    historico_pos,
    [funcao(p) for p in historico_pos],
    color="red",
    s=50,
    alpha=0.6,
    label="Trajetória",
)
plt.scatter(posicao, fitness, color="green", s=200, marker="*", label="Final")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Trajetória da Partícula")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(range(ITERACOES + 1), historico_fit, "r-o", linewidth=2, markersize=4)
plt.xlabel("Iteração")
plt.ylabel("Fitness")
plt.title("Convergência")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("missao1_particula.png", dpi=100, bbox_inches="tight")
plt.close()


# =============================================================================
# MISSÃO 2: O ENXAME DE PARTÍCULAS
# =============================================================================

np.random.seed(42)
random.seed(42)

NUM_PARTICULAS = 20
ITERACOES = 50
W = 0.7
C1 = 1.8
C2 = 1.8
X_MIN, X_MAX = -2, 2
Y_MIN, Y_MAX = -1, 3


def rosenbrock(posicao):
    x, y = posicao
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


def criar_particula():
    posicao = np.array(
        [random.uniform(X_MIN, X_MAX), random.uniform(Y_MIN, Y_MAX)]
    )
    velocidade = np.random.uniform(-0.5, 0.5, 2)
    fitness = rosenbrock(posicao)
    return {
        "posicao": posicao,
        "velocidade": velocidade,
        "fitness": fitness,
        "pBest_pos": posicao.copy(),
        "pBest_fit": fitness,
    }


def atualizar_velocidade(particula, gBest_pos):
    r1 = np.random.random(2)
    r2 = np.random.random(2)
    return (
        W * particula["velocidade"]
        + C1 * r1 * (particula["pBest_pos"] - particula["posicao"])
        + C2 * r2 * (gBest_pos - particula["posicao"])
    )


def atualizar_posicao(particula):
    nova_pos = particula["posicao"] + particula["velocidade"]
    nova_pos[0] = np.clip(nova_pos[0], X_MIN, X_MAX)
    nova_pos[1] = np.clip(nova_pos[1], Y_MIN, Y_MAX)
    return nova_pos


enxame = []
for _ in range(NUM_PARTICULAS):
    enxame.append(criar_particula())

melhor = min(enxame, key=lambda p: p["fitness"])
gBest_pos = melhor["posicao"].copy()
gBest_fit = melhor["fitness"]

historico = {
    "melhor": [gBest_fit],
    "media": [np.mean([p["fitness"] for p in enxame])],
}

print("=" * 60)
print(" PSO - FUNÇÃO DE ROSENBROCK")
print("=" * 60)
print(f"Início: Melhor fitness = {gBest_fit:.6f}")

for iteracao in range(ITERACOES):
    for p in enxame:
        p["velocidade"] = atualizar_velocidade(p, gBest_pos)
        p["posicao"] = atualizar_posicao(p)
        p["fitness"] = rosenbrock(p["posicao"])

        if p["fitness"] < p["pBest_fit"]:
            p["pBest_fit"] = p["fitness"]
            p["pBest_pos"] = p["posicao"].copy()

        if p["fitness"] < gBest_fit:
            gBest_fit = p["fitness"]
            gBest_pos = p["posicao"].copy()

    historico["melhor"].append(gBest_fit)
    historico["media"].append(np.mean([p["fitness"] for p in enxame]))

    if (iteracao + 1) % 10 == 0:
        print(f"Iteração {iteracao+1:3d}: Melhor = {gBest_fit:.6f}")

print(f"\nFim: Melhor fitness = {gBest_fit:.6f}")
print("Ótimo global: f(1,1) = 0.000000")

best_pos = gBest_pos
best_fit = gBest_fit

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(historico["melhor"], "b-", linewidth=2, label="Melhor")
ax1.plot(historico["media"], "r--", linewidth=2, label="Média")
ax1.set_xlabel("Iteração")
ax1.set_ylabel("Fitness")
ax1.set_title("Convergência do PSO")
ax1.legend()
ax1.grid(True, alpha=0.3)

x_pos = [p["posicao"][0] for p in enxame]
y_pos = [p["posicao"][1] for p in enxame]

x_plot = np.linspace(X_MIN, X_MAX, 100)
y_plot = np.linspace(Y_MIN, Y_MAX, 100)
X, Y = np.meshgrid(x_plot, y_plot)
Z = np.array(
    [
        [rosenbrock([xi, yi]) for xi, yi in zip(row_x, row_y)]
        for row_x, row_y in zip(X, Y)
    ]
)

contour = ax2.contourf(X, Y, Z, levels=50, cmap="viridis", alpha=0.7)
ax2.scatter(x_pos, y_pos, color="white", s=30, alpha=0.7, label="Partículas")
ax2.scatter(
    best_pos[0], best_pos[1], color="red", s=200, marker="*", label="Melhor"
)
ax2.scatter(1, 1, color="yellow", s=100, marker="x", label="Ótimo (1,1)")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_title("Partículas no Espaço de Busca")
ax2.legend()
plt.colorbar(contour, ax=ax2)

plt.tight_layout()
plt.savefig("missao2_rosenbrock.png", dpi=100, bbox_inches="tight")
plt.close()


# =============================================================================
# MISSÃO 3: OTIMIZAÇÃO LOGÍSTICA
# =============================================================================

np.random.seed(42)

NUM_CLIENTES = 50
NUM_CENTROS = 5
NUM_PARTICULAS = 30
ITERACOES = 100
W = 0.7
C1 = 1.8
C2 = 1.8
LIMITE = 10

clientes = np.random.rand(NUM_CLIENTES, 2) * LIMITE
demandas = np.random.randint(1, 100, NUM_CLIENTES)

print("=" * 60)
print(" OPTIMUS TECH - LOGÍSTICA INTELIGENTE")
print("=" * 60)
print(f"\n DADOS DO PROBLEMA:")
print(f"   - {NUM_CLIENTES} clientes")
print(f"   - {NUM_CENTROS} centros de distribuição")
print(f"   - Demanda média: {np.mean(demandas):.1f} unidades")


def fitness(posicoes_centros):
    """
    Calcula o custo total de entrega.

    posicoes_centros: array de 10 elementos [x1,y1,x2,y2,...,x5,y5]
    Retorna: -custo_total (maximização)
    """
    centros = []
    for i in range(NUM_CENTROS):
        centros.append([posicoes_centros[2 * i], posicoes_centros[2 * i + 1]])

    custo_total = 0

    for cliente, demanda in zip(clientes, demandas):
        distancias = [
            np.sqrt((c[0] - cliente[0]) ** 2 + (c[1] - cliente[1]) ** 2)
            for c in centros
        ]
        centro_mais_proximo = min(distancias)
        custo_total += centro_mais_proximo * demanda

    return -custo_total


def criar_particula():
    posicao = np.random.uniform(0, LIMITE, NUM_CENTROS * 2)
    velocidade = np.random.uniform(-0.5, 0.5, NUM_CENTROS * 2)
    fit = fitness(posicao)
    return {
        "posicao": posicao,
        "velocidade": velocidade,
        "fitness": fit,
        "pBest_pos": posicao.copy(),
        "pBest_fit": fit,
    }


def atualizar_velocidade(particula, gBest_pos):
    dim = NUM_CENTROS * 2
    r1 = np.random.random(dim)
    r2 = np.random.random(dim)
    return (
        W * particula["velocidade"]
        + C1 * r1 * (particula["pBest_pos"] - particula["posicao"])
        + C2 * r2 * (gBest_pos - particula["posicao"])
    )


def atualizar_posicao(particula):
    return np.clip(particula["posicao"] + particula["velocidade"], 0, LIMITE)


enxame = []
for _ in range(NUM_PARTICULAS):
    enxame.append(criar_particula())

melhor = max(enxame, key=lambda p: p["fitness"])
gBest_pos = melhor["posicao"].copy()
gBest_fit = melhor["fitness"]

historico = [gBest_fit]

print("\n OTIMIZANDO...")
start_time = time.time()

for iteracao in range(ITERACOES):
    for p in enxame:
        p["velocidade"] = atualizar_velocidade(p, gBest_pos)
        p["posicao"] = atualizar_posicao(p)
        p["fitness"] = fitness(p["posicao"])

        if p["fitness"] > p["pBest_fit"]:
            p["pBest_fit"] = p["fitness"]
            p["pBest_pos"] = p["posicao"].copy()

        if p["fitness"] > gBest_fit:
            gBest_fit = p["fitness"]
            gBest_pos = p["posicao"].copy()

    historico.append(gBest_fit)

    if (iteracao + 1) % 20 == 0:
        print(f"  Iteração {iteracao+1:3d}: Custo = {abs(gBest_fit):.2f}")

execution_time = time.time() - start_time

best_pos = gBest_pos
best_fit = gBest_fit

centros = []
for i in range(NUM_CENTROS):
    centros.append([best_pos[2 * i], best_pos[2 * i + 1]])

print(f"\n RESULTADO FINAL:")
print(f"   Tempo de execução: {execution_time:.2f} segundos")
print(f"   Custo total: {abs(best_fit):.2f}")
print(f"   Melhor custo possível: 0.00")
print(f"   Centros de distribuição:")
for i, centro in enumerate(centros):
    print(f"      Centro {i+1}: ({centro[0]:.2f}, {centro[1]:.2f})")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.scatter(clientes[:, 0], clientes[:, 1], c="blue", s=30, alpha=0.6, label="Clientes")
for i, centro in enumerate(centros):
    ax1.scatter(
        centro[0],
        centro[1],
        c="red",
        s=200,
        marker="s",
        label=f"Centro {i+1}" if i == 0 else "",
    )
    ax1.annotate(
        f"C{i+1}",
        (centro[0], centro[1]),
        fontsize=10,
        ha="center",
        va="bottom",
        weight="bold",
    )

ax1.set_xlabel("Coordenada X")
ax1.set_ylabel("Coordenada Y")
ax1.set_title("Clientes e Centros de Distribuição")
ax1.legend()
ax1.grid(True, alpha=0.3)

custo_historico = [-h for h in historico]
ax2.plot(custo_historico, "b-", linewidth=2)
ax2.set_xlabel("Iteração")
ax2.set_ylabel("Custo Total")
ax2.set_title("Convergência da Otimização")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("missao3_logistica.png", dpi=100, bbox_inches="tight")
plt.close()


# =============================================================================
# MISSÃO 4: OTIMIZAÇÃO DOS PARÂMETROS DO PSO
# =============================================================================

np.random.seed(42)

BASE_PARAMS = {
    "num_particulas": 30,
    "iteracoes": 50,
    "w": 0.7,
    "c1": 1.8,
    "c2": 1.8,
    "limite": 10,
    "num_centros": 5,
    "num_clientes": 50,
}

EXPERIMENTOS = [
    {"nome": "Padrão", "params": BASE_PARAMS.copy()},
    {"nome": "Inércia Alta", "params": {**BASE_PARAMS, "w": 0.9}},
    {"nome": "Inércia Baixa", "params": {**BASE_PARAMS, "w": 0.5}},
    {"nome": "Cognitivo Alto", "params": {**BASE_PARAMS, "c1": 2.5}},
    {"nome": "Social Alto", "params": {**BASE_PARAMS, "c2": 2.5}},
    {"nome": "Mais Partículas", "params": {**BASE_PARAMS, "num_particulas": 60}},
]

clientes = np.random.rand(BASE_PARAMS["num_clientes"], 2) * BASE_PARAMS["limite"]
demandas = np.random.randint(1, 100, BASE_PARAMS["num_clientes"])


def fitness(posicoes_centros, clientes, demandas, num_centros):
    centros = [posicoes_centros[2 * i : 2 * i + 2] for i in range(num_centros)]
    custo_total = 0

    for cliente, demanda in zip(clientes, demandas):
        distancias = [
            np.sqrt((c[0] - cliente[0]) ** 2 + (c[1] - cliente[1]) ** 2)
            for c in centros
        ]
        custo_total += min(distancias) * demanda

    return -custo_total


def executar_pso(params, clientes, demandas):
    num_particulas = params["num_particulas"]
    iteracoes = params["iteracoes"]
    w = params["w"]
    c1 = params["c1"]
    c2 = params["c2"]
    limite = params["limite"]
    num_centros = params["num_centros"]
    dim = num_centros * 2

    enxame = []
    for _ in range(num_particulas):
        posicao = np.random.uniform(0, limite, dim)
        velocidade = np.random.uniform(-0.5, 0.5, dim)
        fit = fitness(posicao, clientes, demandas, num_centros)
        enxame.append(
            {
                "posicao": posicao,
                "velocidade": velocidade,
                "fitness": fit,
                "pBest_pos": posicao.copy(),
                "pBest_fit": fit,
            }
        )

    melhor = max(enxame, key=lambda p: p["fitness"])
    gBest_pos = melhor["posicao"].copy()
    gBest_fit = melhor["fitness"]

    historico = [gBest_fit]

    for _ in range(iteracoes):
        for p in enxame:
            r1 = np.random.random(dim)
            r2 = np.random.random(dim)

            p["velocidade"] = (
                w * p["velocidade"]
                + c1 * r1 * (p["pBest_pos"] - p["posicao"])
                + c2 * r2 * (gBest_pos - p["posicao"])
            )

            p["posicao"] = np.clip(p["posicao"] + p["velocidade"], 0, limite)
            p["fitness"] = fitness(p["posicao"], clientes, demandas, num_centros)

            if p["fitness"] > p["pBest_fit"]:
                p["pBest_fit"] = p["fitness"]
                p["pBest_pos"] = p["posicao"].copy()

            if p["fitness"] > gBest_fit:
                gBest_fit = p["fitness"]
                gBest_pos = p["posicao"].copy()

        historico.append(gBest_fit)

    return gBest_fit, historico


print("=" * 60)
print(" EXPERIMENTOS COM PARÂMETROS DO PSO")
print("=" * 60)

resultados = {}

for exp in EXPERIMENTOS:
    print(f"\n Experimento: {exp['nome']}")
    print(
        f"   Parâmetros: w={exp['params']['w']}, c1={exp['params']['c1']}, "
        f"c2={exp['params']['c2']}, partículas={exp['params']['num_particulas']}"
    )

    execucoes = 5
    custos = []
    historicos = []

    for _ in range(execucoes):
        custo_final, historico = executar_pso(exp["params"], clientes, demandas)
        custos.append(custo_final)
        historicos.append(historico)

    resultados[exp["nome"]] = {
        "custo_medio": -np.mean(custos),
        "custo_std": np.std(custos),
        "melhor_custo": -max(custos),
        "pior_custo": -min(custos),
        "historico": np.mean(historicos, axis=0),
    }

    print(
        f"   Custo médio: {resultados[exp['nome']]['custo_medio']:.2f} ± "
        f"{resultados[exp['nome']]['custo_std']:.2f}"
    )

print("\n" + "=" * 60)
print(" ANÁLISE DOS RESULTADOS")
print("=" * 60)

print("\n| Experimento        | Custo Médio | Melhor Custo | Pior Custo  |")
print("|--------------------|-------------|--------------|-------------|")
for nome, data in resultados.items():
    print(
        f"| {nome:<18} | {data['custo_medio']:10.2f} | {data['melhor_custo']:12.2f} | "
        f"{data['pior_custo']:11.2f} |"
    )

plt.figure(figsize=(14, 8))

for nome, data in resultados.items():
    custo_hist = [-h for h in data["historico"]]
    plt.plot(custo_hist, linewidth=2, label=nome)

plt.xlabel("Iteração")
plt.ylabel("Custo Total")
plt.title("Comparação de Desempenho dos Parâmetros do PSO")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("missao4_parametros.png", dpi=100, bbox_inches="tight")
plt.close()

print("\n" + "=" * 60)
print(" ANÁLISE E CONCLUSÕES")
print("=" * 60)
print("\n1. Qual configuração obteve o MELHOR resultado?")
print("   →", min(resultados.items(), key=lambda x: x[1]["custo_medio"])[0])

print("\n2. Qual configuração obteve o PIOR resultado?")
print("   →", max(resultados.items(), key=lambda x: x[1]["custo_medio"])[0])

print("\n3. O que você observou sobre o efeito de:")
print("   - Inércia (w):")
print("   - Cognitivo (c1):")
print("   - Social (c2):")
print("   - Número de partículas:")

print("\n4. Qual configuração você recomenda para este problema? Por quê?")
