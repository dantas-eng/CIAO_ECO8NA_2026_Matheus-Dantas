"""
AULA DE LÓGICA FUZZY - Código 2 (laboratório dos alunos)

Mesmo problema da gorjeta, agora com a biblioteca scikit-fuzzy.
Você vai: (1) rodar, (2) ver os gráficos, (3) fazer os experimentos no final.

Instalação:  pip install numpy matplotlib scikit-fuzzy
Execução:    python 02_laboratorio_skfuzzy.py
"""
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------- 1) Variáveis linguísticas (universos de discurso) ----------
servico = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "servico")   # nota 0-10
comida = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "comida")     # nota 0-10
gorjeta = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta")   # % da conta

# ---------- 2) Conjuntos fuzzy (funções de pertinência) ----------
for var in (servico, comida):
    var["ruim"] = fuzz.trimf(var.universe, [0, 0, 5])
    var["medio"] = fuzz.trimf(var.universe, [0, 5, 10])
    var["bom"] = fuzz.trimf(var.universe, [5, 10, 10])

gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta["alta"] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

# ---------- 3) Base de regras  (| = OU, & = E, ~ = NÃO) ----------
regras = [
    ctrl.Rule(servico["ruim"] | comida["ruim"], gorjeta["baixa"]),
    ctrl.Rule(servico["medio"], gorjeta["media"]),
    ctrl.Rule(servico["bom"] | comida["bom"], gorjeta["alta"]),
]

# ---------- 4) Simulação ----------
sistema = ctrl.ControlSystem(regras)
sim = ctrl.ControlSystemSimulation(sistema)


def pedir_nota(texto, padrao):
    """Lê uma nota de 0 a 10; se o aluno só apertar Enter, usa o padrão."""
    resposta = input(f"{texto} (0-10) [{padrao}]: ").strip()
    return float(resposta.replace(",", ".")) if resposta else padrao


sim.input["servico"] = pedir_nota("Nota do serviço", 7)
sim.input["comida"] = pedir_nota("Nota da comida", 3)
sim.compute()
print(f"\n=> Gorjeta sugerida: {sim.output['gorjeta']:.1f}%")

# ---------- 5) Gráficos ----------
servico.view()                 # funções de pertinência do serviço
plt.savefig("lab02_servico.png", dpi=110)
comida.view()                  # funções de pertinência da comida
plt.savefig("lab02_comida.png", dpi=110)
gorjeta.view(sim=sim)          # área agregada + linha do centroide (resultado)
plt.savefig("lab02_defuzzificacao.png", dpi=110)
plt.show()

# ======================= EXPERIMENTOS =======================
# 1) Troque a regra 2 por:  servico["medio"] & comida["medio"]
#    O que mudou no resultado para (7, 3)? Por quê?
# 2) Troque os triângulos de "servico" por trapézios (fuzz.trapmf) ou
#    gaussianas (fuzz.gaussmf, [media, desvio]). O resultado ficou mais suave?
# 3) Compare métodos de defuzzificação:
#      gorjeta = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta",
#                                defuzzify_method="mom")   # "centroid", "bisector", "mom"...
# 4) Adicione um 4º conjunto "excelente" ao serviço e escreva a regra nova.
# 5) Teste (0, 0), (10, 10), (5, 5): o comportamento é o que você esperava?


# ======================= EXPERIMENTOS (codigo) =======================
def sistema_gorjeta(termos="tri", regra2="servico", metodo="centroid", excelente=False):
    """Monta o sistema da gorjeta com a mudanca de cada experimento."""
    s = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "servico")
    c = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "comida")
    g = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta", defuzzify_method=metodo)
    for v in (s, c):
        v["ruim"] = fuzz.trimf(v.universe, [0, 0, 5])
        v["medio"] = fuzz.trimf(v.universe, [0, 5, 10])
        v["bom"] = fuzz.trimf(v.universe, [5, 10, 10])
    if termos == "trap":    # experimento 2 (trapezios)
        s["ruim"] = fuzz.trapmf(s.universe, [0, 0, 2, 5])
        s["medio"] = fuzz.trapmf(s.universe, [2, 4, 6, 8])
        s["bom"] = fuzz.trapmf(s.universe, [5, 8, 10, 10])
    if termos == "gauss":   # experimento 2 (gaussianas)
        s["ruim"] = fuzz.gaussmf(s.universe, 0, 1.8)
        s["medio"] = fuzz.gaussmf(s.universe, 5, 1.8)
        s["bom"] = fuzz.gaussmf(s.universe, 10, 1.8)
    if excelente:           # experimento 4 (4o conjunto)
        s["excelente"] = fuzz.trimf(s.universe, [8, 10, 10])
    g["baixa"] = fuzz.trimf(g.universe, [0, 0, 13])
    g["media"] = fuzz.trimf(g.universe, [0, 13, 25])
    g["alta"] = fuzz.trimf(g.universe, [13, 25, 25])
    regra_2 = s["medio"] if regra2 == "servico" else (s["medio"] & c["medio"])  # experimento 1
    r = [ctrl.Rule(s["ruim"] | c["ruim"], g["baixa"]),
         ctrl.Rule(regra_2, g["media"]),
         ctrl.Rule(s["bom"] | c["bom"], g["alta"])]
    if excelente:
        r.append(ctrl.Rule(s["excelente"], g["alta"]))  # regra nova
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(r))


def rodar(sistema, nota_servico, nota_comida):
    sistema.input["servico"] = nota_servico
    sistema.input["comida"] = nota_comida
    sistema.compute()
    return sistema.output["gorjeta"]


if __name__ == "__main__":
    print("\n===== EXPERIMENTOS =====")
    print(f"base (7,3)                       : {rodar(sistema_gorjeta(), 7, 3):.2f}%")
    print(f"1) regra 2 com E (7,3)           : {rodar(sistema_gorjeta(regra2='e'), 7, 3):.2f}%")
    print(f"2) servico trapezoidal (7,3)     : {rodar(sistema_gorjeta(termos='trap'), 7, 3):.2f}%")
    print(f"2) servico gaussiano (7,3)       : {rodar(sistema_gorjeta(termos='gauss'), 7, 3):.2f}%")
    for m in ("centroid", "bisector", "mom"):
        print(f"3) defuzzificacao {m} (7,3)".ljust(33) + f": {rodar(sistema_gorjeta(metodo=m), 7, 3):.2f}%")
    print(f"4) com 'excelente' (7,3)         : {rodar(sistema_gorjeta(excelente=True), 7, 3):.2f}%")
    for a, b in [(0, 0), (10, 10), (5, 5)]:
        print(f"5) ({a},{b})".ljust(33) + f": {rodar(sistema_gorjeta(), a, b):.2f}%")
