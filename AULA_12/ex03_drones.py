# Exercício 3. Logística de drones (3 objetivos)
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class DroneProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=3, xl=np.array([10.0, 1.0]), xu=np.array([80.0, 5.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        velocidade, carga = x[0], x[1]
        f1_tempo = 1000.0 / velocidade
        f2_custo = (velocidade ** 2) * 0.1 + (carga * 50)
        f3_co2 = (velocidade * 1.5) / carga
        out["F"] = [f1_tempo, f2_custo, f3_co2]


res3 = minimize(DroneProblem(), NSGA2(pop_size=40), termination=("n_gen", 50), seed=42)
F = np.atleast_2d(res3.F)
X = np.atleast_2d(res3.X)
print("[EX 03] soluções:", len(F))
for nome, col in (("menor tempo", 0), ("menor custo", 1), ("menor CO2", 2)):
    i = int(np.argmin(F[:, col]))
    print(
        f"  {nome}: vel {X[i, 0]:.1f}, carga {X[i, 1]:.2f} | "
        f"tempo {F[i, 0]:.2f} | custo {F[i, 1]:.2f} | CO2 {F[i, 2]:.2f}"
    )

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(F[:, 0], F[:, 1], F[:, 2], color="green", s=40)
ax.set_xlabel("Tempo")
ax.set_ylabel("Custo")
ax.set_zlabel("CO2")
plt.title("Exercício 3. Pareto 3D: drones")
saida = os.path.join(os.path.dirname(__file__) or ".", "ex03_pareto_drones.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
