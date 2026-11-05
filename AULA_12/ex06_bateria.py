# Exercício 6. Recarga de bateria com restrição de desgaste
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class EVBatteryProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([10.0, 15.0]),
            xu=np.array([150.0, 45.0]),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        potencia, temp = x[0], x[1]
        f1_tempo_recarga = 3000.0 / potencia
        f2_desgaste_bateria = (potencia ** 1.5) * (temp / 20.0)
        g1 = f2_desgaste_bateria - 1500.0
        out["F"] = [f1_tempo_recarga, f2_desgaste_bateria]
        out["G"] = [g1]


res = minimize(EVBatteryProblem(), NSGA2(pop_size=40), termination=("n_gen", 50), seed=42)
opt = res.opt
F = np.atleast_2d(opt.get("F"))
X = np.atleast_2d(opt.get("X"))
G = np.atleast_2d(opt.get("G"))
viaveis = G[:, 0] <= 1e-6
print("[EX 06] soluções na fronteira:", len(F), "| viáveis (G <= 0):", int(viaveis.sum()))
for i in np.argsort(F[:, 0]):
    if not viaveis[i]:
        continue
    print(
        f"  {X[i, 0]:6.1f} kW, {X[i, 1]:5.1f} C | "
        f"tempo {F[i, 0]:6.2f} | desgaste {F[i, 1]:7.1f} | G {G[i, 0]:7.1f}"
    )

plt.figure(figsize=(7, 4))
plt.scatter(F[viaveis, 0], F[viaveis, 1], color="crimson", s=40)
plt.xlabel("Tempo de recarga")
plt.ylabel("Desgaste")
plt.title("Exercício 6. Soluções viáveis (desgaste <= 1500)")
plt.grid(True)
saida = os.path.join(os.path.dirname(__file__) or ".", "ex06_bateria.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
