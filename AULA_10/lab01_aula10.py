"""
Lab 01 - Aula 10 (AC-3 Sprint 2): motor de inferência Mamdani e superfície 3D.
Urgência de correção de um incidente a partir do Impacto (%) e da Explorabilidade (0-10).

Instalação: pip install numpy matplotlib scikit-fuzzy
Execução:   python lab01_aula10.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def montar_sistema(critica="trimf", defuzz="centroid"):
    impacto = ctrl.Antecedent(np.arange(0, 101, 1), "impacto")              # % do sistema afetado
    explorab = ctrl.Antecedent(np.arange(0, 10.1, 0.1), "explorabilidade")  # 0 a 10
    urgencia = ctrl.Consequent(np.arange(0, 101, 1), "urgencia", defuzzify_method=defuzz)  # %

    impacto["baixo"] = fuzz.trimf(impacto.universe, [0, 0, 40])
    impacto["medio"] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto["alto"] = fuzz.trimf(impacto.universe, [60, 100, 100])

    explorab["baixa"] = fuzz.trimf(explorab.universe, [0, 0, 4])
    explorab["moderada"] = fuzz.trimf(explorab.universe, [2, 5, 8])
    explorab["alta"] = fuzz.trimf(explorab.universe, [6, 10, 10])

    urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 30])
    urgencia["media"] = fuzz.trimf(urgencia.universe, [20, 40, 60])
    urgencia["alta"] = fuzz.trimf(urgencia.universe, [50, 70, 90])
    if critica == "trapmf":  # Abordagem A: platô encostado na borda superior
        urgencia["critica"] = fuzz.trapmf(urgencia.universe, [75, 90, 100, 100])
    else:
        urgencia["critica"] = fuzz.trimf(urgencia.universe, [75, 100, 100])

    # matriz 3x3: linha = impacto, coluna = explorabilidade
    matriz = {
        "baixo": {"baixa": "baixa", "moderada": "baixa", "alta": "media"},
        "medio": {"baixa": "media", "moderada": "alta", "alta": "alta"},
        "alto": {"baixa": "critica", "moderada": "critica", "alta": "critica"},
    }
    regras = [ctrl.Rule(impacto[i] & explorab[e], urgencia[u])
              for i, linha in matriz.items() for e, u in linha.items()]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(regras)), urgencia


def calcular(sim, imp, exp):
    sim.input["impacto"] = imp
    sim.input["explorabilidade"] = exp
    sim.compute()
    return sim.output["urgencia"]


if __name__ == "__main__":
    # ---------- Desafio dos extremos ----------
    configs = [("Centroide + triângulo", "trimf", "centroid"),
               ("A) Centroide + trapézio", "trapmf", "centroid"),
               ("B) MOM + triângulo", "trimf", "mom")]
    pontos = [(0, 0), (50, 5), (60, 6), (70, 7), (100, 10)]
    print(f"{'configuração':<26}" + "".join(f"{str(p):>11}" for p in pontos))
    for nome, crit, dfz in configs:
        sim, _ = montar_sistema(crit, dfz)
        print(f"{nome:<26}" + "".join(f"{calcular(sim, *p):>10.2f}%" for p in pontos))

    # suavidade: maior salto entre pontos vizinhos na diagonal (0,0) -> (100,10), passo de 2,5
    print("\nmaior salto na diagonal (passo 2,5% / 0,25):")
    for nome, crit, dfz in configs:
        sim, _ = montar_sistema(crit, dfz)
        diag = [calcular(sim, k * 2.5, k * 0.25) for k in range(41)]
        print(f"  {nome:<26} {np.abs(np.diff(diag)).max():6.2f} pontos percentuais")

    # 1) saída com o centroide para a entrada máxima
    sim, urgencia = montar_sistema()
    calcular(sim, 100, 10)
    urgencia.view(sim=sim)
    plt.savefig("saida_centroide.png", dpi=110)

    # ---------- Superfície de decisão 3D ----------
    imps = np.linspace(0, 100, 41)
    exps = np.linspace(0, 10, 41)
    X, Y = np.meshgrid(imps, exps)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = calcular(sim, X[i, j], Y[i, j])  # falha se algum ponto ficar sem regra
    assert not np.isnan(Z).any(), "lacuna de cobertura na base de regras"
    print(f"\nsuperfície: {Z.size} pontos, urgência de {Z.min():.2f}% a {Z.max():.2f}%")

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    s = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax.set_xlabel("Impacto (%)")
    ax.set_ylabel("Explorabilidade (0-10)")
    ax.set_zlabel("Urgência (%)")
    ax.set_title("Superfície de decisão - Mamdani (centroide)")
    ax.view_init(30, 225)
    fig.colorbar(s, shrink=0.6)
    plt.savefig("superficie_decisao.png", dpi=110)
    print("Gráficos salvos: saida_centroide.png, superficie_decisao.png")
