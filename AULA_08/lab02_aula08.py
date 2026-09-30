# LAB 02 - AG binário para microsserviços em Edge
# AULA 08 CIAO - fechamento AC-2

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

N_SERVICES = 15
MAX_RAM = 16
MAX_CPU = 8
POP_SIZE = 40
GENERATIONS = 60
MUTATION_RATE = 0.05
TOURNAMENT_K = 3

business_value = np.array([8, 6, 5, 9, 4, 7, 3, 10, 6, 5, 4, 8, 7, 5, 9], dtype=float)
ram_gb = np.array([3, 2, 2, 4, 1, 3, 1, 5, 2, 2, 1, 4, 3, 2, 4], dtype=float)
cpu_cores = np.array([2, 1, 1, 3, 1, 2, 1, 3, 1, 2, 1, 2, 2, 1, 3], dtype=float)


def totals(ind):
    mask = ind.astype(bool)
    return (
        float(np.sum(business_value[mask])),
        float(np.sum(ram_gb[mask])),
        float(np.sum(cpu_cores[mask])),
    )


def fitness_rigid(ind):
    value, ram, cpu = totals(ind)
    if ram > MAX_RAM or cpu > MAX_CPU:
        return 0.0
    return value


def fitness_proportional(ind):
    value, ram, cpu = totals(ind)
    excess_ram = max(0.0, ram - MAX_RAM)
    excess_cpu = max(0.0, cpu - MAX_CPU)
    if excess_ram == 0 and excess_cpu == 0:
        return value
    penalty = (excess_ram / MAX_RAM + excess_cpu / MAX_CPU) * value
    return max(0.0, value - penalty)


def tournament_select(pop, fits):
    idx = np.random.choice(len(pop), TOURNAMENT_K, replace=False)
    best = idx[np.argmax(fits[idx])]
    return pop[best].copy()


def single_point_crossover(p1, p2):
    point = np.random.randint(1, N_SERVICES)
    c1 = np.concatenate([p1[:point], p2[point:]])
    c2 = np.concatenate([p2[:point], p1[point:]])
    return c1, c2


def mutate(ind):
    out = ind.copy()
    for i in range(N_SERVICES):
        if np.random.rand() < MUTATION_RATE:
            out[i] = 1 - out[i]
    return out


def population_diversity(pop):
    dists = []
    for i in range(len(pop)):
        for j in range(i + 1, len(pop)):
            dists.append(np.mean(pop[i] != pop[j]))
    return float(np.mean(dists)) if dists else 0.0


def run_ga(fitness_fn):
    pop = np.random.randint(0, 2, size=(POP_SIZE, N_SERVICES))
    mean_hist, std_hist, div_hist = [], [], []
    best_ind = pop[0].copy()
    best_fit = -1.0

    for _ in range(GENERATIONS):
        fits = np.array([fitness_fn(ind) for ind in pop])
        mean_hist.append(float(np.mean(fits)))
        std_hist.append(float(np.std(fits)))
        div_hist.append(population_diversity(pop))
        gen_best = int(np.argmax(fits))
        if fits[gen_best] > best_fit:
            best_fit = float(fits[gen_best])
            best_ind = pop[gen_best].copy()

        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = tournament_select(pop, fits)
            p2 = tournament_select(pop, fits)
            c1, c2 = single_point_crossover(p1, p2)
            new_pop.append(mutate(c1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(mutate(c2))
        pop = np.array(new_pop)

    return {
        "best_ind": best_ind,
        "best_fit": best_fit,
        "mean_hist": mean_hist,
        "std_hist": std_hist,
        "div_hist": div_hist,
    }


print("[LAB 02 - AG microsserviços Edge]")
res_a = run_ga(fitness_rigid)
res_b = run_ga(fitness_proportional)

for label, res in (("Estratégia A (penalidade rígida)", res_a), ("Estratégia B (proporcional)", res_b)):
    val, ram, cpu = totals(res["best_ind"])
    print(f"\n{label}:")
    print(f"  Melhor indivíduo: {res['best_ind'].astype(int).tolist()}")
    print(f"  Fitness final: {res['best_fit']:.2f} | Valor: {val:.0f} | RAM: {ram:.0f} GB | CPU: {cpu:.0f} cores")
    print(f"  Média fitness (última geração): {res['mean_hist'][-1]:.4f}")
    print(f"  Desvio-padrão (última geração): {res['std_hist'][-1]:.4f}")
    print(f"  Diversidade média (Hamming): {np.mean(res['div_hist']):.4f}")

div_a = float(np.mean(res_a["div_hist"]))
div_b = float(np.mean(res_b["div_hist"]))
print("\nComparativo de diversidade genética (média ao longo das gerações):")
print(f"  A: {div_a:.4f} | B: {div_b:.4f}")
if div_b > div_a:
    print("  A estratégia B manteve população mais heterogênea.")
else:
    print("  A estratégia A manteve população mais heterogênea.")

if res_b["best_fit"] >= res_a["best_fit"]:
    print("  Melhor combinação final: estratégia B.")
else:
    print("  Melhor combinação final: estratégia A.")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(res_a["mean_hist"], label="média A")
axes[0].plot(res_b["mean_hist"], label="média B")
axes[0].set_title("Fitness médio por geração")
axes[0].set_xlabel("Geração")
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[1].plot(res_a["std_hist"], label="desvio A")
axes[1].plot(res_b["std_hist"], label="desvio B")
axes[1].set_title("Desvio-padrão do fitness")
axes[1].set_xlabel("Geração")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "lab02_ag_comparativo.png"), dpi=100)
plt.close()
print("\nGráfico salvo: lab02_ag_comparativo.png")
