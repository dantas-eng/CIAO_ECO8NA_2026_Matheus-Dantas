# Exercício 1. Variáveis inteiras no SOC (pods e analistas)
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize


class SOCInteiroProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([1, 1]),
            xu=np.array([30, 15]),
            vtype=int,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        pods, analistas = int(x[0]), int(x[1])
        f1_latencia = (400.0 / pods) + (150.0 / analistas)
        f2_custo = (pods * 18.0) + (analistas * 45.0)
        out["F"] = [f1_latencia, f2_custo]


algorithm = NSGA2(
    pop_size=30,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True,
)

res1 = minimize(SOCInteiroProblem(), algorithm, termination=("n_gen", 40), seed=42)
X = np.atleast_2d(res1.X)
F = np.atleast_2d(res1.F)

print("Amostra de 5 solucoes inteiras encontradas (Pods, Analistas):")
for sol_x, sol_f in zip(X[:5], F[:5]):
    print(
        f"Pods: {int(sol_x[0]):2d} | Analistas: {int(sol_x[1]):2d} => "
        f"Latencia: {sol_f[0]:6.2f}ms | Custo: R$ {sol_f[1]:6.2f}"
    )
print(f"Todas inteiras: {np.all(np.isclose(X, np.round(X)))}")

plt.figure(figsize=(7, 4))
plt.scatter(F[:, 0], F[:, 1], color="teal", s=60, edgecolor="black")
plt.title("Exercicio 1 - Fronteira de Pareto discreta")
plt.xlabel("Latencia (ms)")
plt.ylabel("Custo (R$/h)")
plt.grid(True, linestyle="--", alpha=0.6)
saida = os.path.join(os.path.dirname(__file__) or ".", "lab01_pareto.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("grafico:", saida)
