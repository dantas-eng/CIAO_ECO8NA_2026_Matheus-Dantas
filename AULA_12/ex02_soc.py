# Exercício 2. Triagem de incidentes SOC
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class SOCAllocationProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([1.0, 1.0]),
            xu=np.array([50.0, 10.0]),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        analistas, regimento = x[0], x[1]
        f1_custo = analistas * 100.0 + regimento * 50.0
        f2_tempo = 200.0 / analistas + 50.0 / regimento
        out["F"] = [f1_custo, f2_tempo]


res = minimize(
    SOCAllocationProblem(),
    NSGA2(pop_size=30),
    termination=("n_gen", 40),
    seed=42,
)
F = np.atleast_2d(res.F)
X = np.atleast_2d(res.X)
print("[EX 02] soluções:", len(F))
i_custo = int(np.argmin(F[:, 0]))
i_tempo = int(np.argmin(F[:, 1]))
print(
    f"  menor custo: {X[i_custo, 0]:.1f} analistas, {X[i_custo, 1]:.1f} regimentos | "
    f"R$ {F[i_custo, 0]:.2f} | {F[i_custo, 1]:.2f} min"
)
print(
    f"  menor tempo: {X[i_tempo, 0]:.1f} analistas, {X[i_tempo, 1]:.1f} regimentos | "
    f"R$ {F[i_tempo, 0]:.2f} | {F[i_tempo, 1]:.2f} min"
)

plt.figure(figsize=(7, 4))
plt.scatter(F[:, 0], F[:, 1], color="darkorange", s=40)
plt.xlabel("Custo (R$)")
plt.ylabel("Tempo de resposta (min)")
plt.title("Exercício 2. SOC: custo x tempo")
plt.grid(True)
saida = os.path.join(os.path.dirname(__file__) or ".", "ex02_pareto_soc.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
