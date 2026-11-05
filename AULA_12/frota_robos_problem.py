# Exercício 7. Frota de robôs de logística
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize


class FrotaRobosProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([5.0, 1.0]),
            xu=np.array([50.0, 4.0]),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        n_robos, velocidade = x[0], x[1]
        f1_custo = (n_robos * 25.0) + (velocidade ** 2) * 8.0
        f2_tempo = 120.0 / n_robos + 40.0 / velocidade
        g1 = n_robos * (velocidade ** 1.5) - 120.0
        out["F"] = [f1_custo, f2_tempo]
        out["G"] = [g1]


def tres_tradeoffs(X, F):
    i_custo = int(np.argmin(F[:, 0]))
    i_tempo = int(np.argmin(F[:, 1]))
    custo_n = (F[:, 0] - F[:, 0].min()) / (np.ptp(F[:, 0]) + 1e-9)
    tempo_n = (F[:, 1] - F[:, 1].min()) / (np.ptp(F[:, 1]) + 1e-9)
    dist = np.hypot(custo_n - 0.5, tempo_n - 0.5)
    dist[i_custo] = np.inf
    dist[i_tempo] = np.inf
    i_meio = int(np.argmin(dist))
    return i_custo, i_meio, i_tempo


if __name__ == "__main__":
    res = minimize(FrotaRobosProblem(), NSGA2(pop_size=40), termination=("n_gen", 60), seed=42)
    opt = res.opt
    F = np.atleast_2d(opt.get("F"))
    X = np.atleast_2d(opt.get("X"))
    G = np.atleast_2d(opt.get("G"))
    ok = G[:, 0] <= 1e-6
    X, F = X[ok], F[ok]
    print("[EX 07] viáveis na fronteira:", len(F))
    rotulos = ("menor custo", "intermediária", "menor tempo")
    for rotulo, i in zip(rotulos, tres_tradeoffs(X, F)):
        print(
            f"  {rotulo}: {X[i, 0]:.1f} robôs, {X[i, 1]:.2f} m/s | "
            f"custo {F[i, 0]:.1f} mil | tempo {F[i, 1]:.2f} min"
        )

    plt.figure(figsize=(7, 4))
    plt.scatter(F[:, 0], F[:, 1], color="navy", s=40)
    plt.xlabel("Custo (R$ mil)")
    plt.ylabel("Tempo de ciclo (min)")
    plt.title("Exercício 7. Fronteira da frota de robôs")
    plt.grid(True)
    saida = os.path.join(os.path.dirname(__file__) or ".", "ex07_frota_robos.png")
    plt.tight_layout()
    plt.savefig(saida, dpi=110)
    plt.close()
    print("  gráfico:", saida)
