# LAB 01 - PSO contínuo para balanceamento de carga em datacenters
# AULA 08 CIAO - fechamento AC-2

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0], dtype=float)
TEMP_LIMIT = 75.0
PENALTY_K = 500.0
DIM = len(C)
W_INERTIA = 0.7
C1 = 1.5
C2 = 1.5
ITERATIONS = 80
VMAX = 0.2


def normalize_weights(pos):
    w = np.clip(pos, 1e-6, None)
    return w / w.sum()


def az_temperatures(w):
    return C + 50.0 * w


def fitness(w):
    w = normalize_weights(w)
    mean_temp = float(np.dot(w, C))
    temps = az_temperatures(w)
    penalty = PENALTY_K * np.sum(np.maximum(0.0, temps - TEMP_LIMIT) ** 2)
    return mean_temp + penalty


class PSOContinuous:
    def __init__(self, n_particles, dim):
        self.n_particles = n_particles
        self.dim = dim
        self.positions = np.random.uniform(0.1, 1.0, size=(n_particles, dim))
        for i in range(n_particles):
            self.positions[i] = normalize_weights(self.positions[i])
        self.velocities = np.random.uniform(-VMAX, VMAX, size=(n_particles, dim))
        self.pbest_pos = self.positions.copy()
        self.pbest_fit = np.array([fitness(p) for p in self.positions])
        g_idx = int(np.argmin(self.pbest_fit))
        self.gbest_pos = self.pbest_pos[g_idx].copy()
        self.gbest_fit = float(self.pbest_fit[g_idx])
        self.history = []

    def step(self):
        r1 = np.random.rand(self.n_particles, self.dim)
        r2 = np.random.rand(self.n_particles, self.dim)
        self.velocities = (
            W_INERTIA * self.velocities
            + C1 * r1 * (self.pbest_pos - self.positions)
            + C2 * r2 * (self.gbest_pos - self.positions)
        )
        self.velocities = np.clip(self.velocities, -VMAX, VMAX)
        self.positions = self.positions + self.velocities
        for i in range(self.n_particles):
            self.positions[i] = normalize_weights(self.positions[i])
            f = fitness(self.positions[i])
            if f < self.pbest_fit[i]:
                self.pbest_fit[i] = f
                self.pbest_pos[i] = self.positions[i].copy()
            if f < self.gbest_fit:
                self.gbest_fit = f
                self.gbest_pos = self.positions[i].copy()

    def run(self):
        self.history = []
        for _ in range(ITERATIONS):
            self.step()
            self.history.append(self.gbest_fit)
        return self.gbest_pos.copy(), self.history


def run_population_size(n_particles):
    pso = PSOContinuous(n_particles, DIM)
    w_best, hist = pso.run()
    w_best = normalize_weights(w_best)
    return {
        "n": n_particles,
        "W": w_best,
        "sum_w": float(w_best.sum()),
        "fitness": float(pso.gbest_fit),
        "mean_temp": float(np.dot(w_best, C)),
        "history": hist,
    }


print("[LAB 01 - PSO balanceamento de carga]")
results = []
histories = {}
for n in (10, 30, 50):
    r = run_population_size(n)
    results.append(r)
    histories[n] = r["history"]
    print(f"\nPopulação {n} partículas:")
    print(f"  W = {np.round(r['W'], 6).tolist()}")
    print(f"  sum(W) = {r['sum_w']:.10f}")
    print(f"  fitness final = {r['fitness']:.6f}")
    print(f"  temperatura média ponderada = {r['mean_temp']:.4f} °C")

print("\nTabela resumo (melhor W por população):")
print("| Partículas | sum(W) | Temp. média (°C) | Fitness |")
print("|---:|---:|---:|---:|")
for r in results:
    print(f"| {r['n']} | {r['sum_w']:.6f} | {r['mean_temp']:.4f} | {r['fitness']:.4f} |")

plt.figure(figsize=(8, 5))
for n, hist in histories.items():
    plt.plot(hist, label=f"{n} partículas")
plt.xlabel("Iteração")
plt.ylabel("Fitness (gbest)")
plt.title("Lab 01 - convergência PSO por tamanho de enxame")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "lab01_pso_populacoes.png"), dpi=100)
plt.close()
print("\nGráfico salvo: lab01_pso_populacoes.png")
