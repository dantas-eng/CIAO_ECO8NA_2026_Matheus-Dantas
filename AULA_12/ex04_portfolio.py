# Exercício 4. Portfólio: risco x retorno, com teto de 100% alocado
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class PortfolioProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([0.0, 0.0]),
            xu=np.array([100.0, 100.0]),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        rf, acoes = x[0], x[1]
        retorno = rf * 0.08 + acoes * 0.18
        f1_retorno_negativo = -retorno
        f2_risco = rf * 0.02 + acoes * 0.25
        out["F"] = [f1_retorno_negativo, f2_risco]
        out["G"] = [rf + acoes - 100.0]


res = minimize(PortfolioProblem(), NSGA2(pop_size=40), termination=("n_gen", 40), seed=42)
opt = res.opt
F = np.atleast_2d(opt.get("F"))
X = np.atleast_2d(opt.get("X"))
retorno = -F[:, 0]
risco = F[:, 1]
print("[EX 04] soluções viáveis na fronteira:", len(F))
i_ret = int(np.argmax(retorno))
i_risco = int(np.argmin(risco))
print(
    f"  maior retorno: RF {X[i_ret, 0]:.1f}% ações {X[i_ret, 1]:.1f}% | "
    f"retorno {retorno[i_ret]:.2f} | risco {risco[i_ret]:.2f}"
)
print(
    f"  menor risco: RF {X[i_risco, 0]:.1f}% ações {X[i_risco, 1]:.1f}% | "
    f"retorno {retorno[i_risco]:.2f} | risco {risco[i_risco]:.2f}"
)

plt.figure(figsize=(7, 4))
plt.scatter(risco, retorno, color="teal", s=40)
plt.xlabel("Risco")
plt.ylabel("Retorno")
plt.title("Exercício 4. Risco x retorno")
plt.grid(True)
saida = os.path.join(os.path.dirname(__file__) or ".", "ex04_risco_retorno.png")
plt.tight_layout()
plt.savefig(saida, dpi=110)
plt.close()
print("  gráfico:", saida)
