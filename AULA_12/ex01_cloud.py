# Exercício 1. Compra de servidores cloud (custo x latência)
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class CloudProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=1, n_obj=2, xl=np.array([1.0]), xu=np.array([32.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        vcpus = x[0]
        f1_custo = vcpus * 15.0
        f2_latencia = 300.0 / vcpus
        out["F"] = [f1_custo, f2_latencia]


res1 = minimize(CloudProblem(), NSGA2(pop_size=20), termination=("n_gen", 30), seed=1)
F = np.atleast_2d(res1.F)
X = np.atleast_2d(res1.X)
print("[EX 01] soluções:", len(F))
ordem = np.argsort(F[:, 0])
for i in ordem[:: max(1, len(ordem) // 5)]:
    print(f"  vCPUs {X[i, 0]:5.2f} | custo R$ {F[i, 0]:7.2f} | latência {F[i, 1]:6.2f} ms")
print(f"  menor custo: R$ {F[:, 0].min():.2f} | menor latência: {F[:, 1].min():.2f} ms")

plt.figure(figsize=(7, 4))
plt.scatter(F[:, 0], F[:, 1], color="blue", s=50)
plt.title("Exercício 1. Fronteira de Pareto: cloud")
plt.xlabel("Custo (R$)")
plt.ylabel("Latência (ms)")
plt.grid(True)
saida = os.path.join(os.path.dirname(__file__) or ".", "ex01_pareto_cloud.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
