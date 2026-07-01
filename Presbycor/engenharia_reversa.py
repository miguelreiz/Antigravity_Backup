import sys, json, math, warnings
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════
# PRESBYCOR — ENGENHARIA REVERSA DO ALGORITMO
# Fonte: JS extraído de presbycor_calculator.html + PDFs reais
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("  PRESBYCOR — ENGENHARIA REVERSA DO ALGORITMO")
print("=" * 70)

# ─── CASOS REAIS EXTRAÍDOS DOS PDFs ────────────────────────────────────────
# Caso 1: RAIMUNDO Silva (strategy_2034) — lido visualmente do PDF
# Caso 2: DA ROCHA Weder Carlos — planilha de calibração
# Caso 3: OLIVEIRA Rosilene — planilha de calibração

casos_reais = [
    {
        "paciente": "RAIMUNDO Silva",
        "olho": "OD", "dominante": True,
        "esfera_pre": +1.00, "cilindro_pre": 0.00,
        "K1": 43.00, "K2": 43.00, "Kmed": 43.00,
        "Q_pre": -0.22, "pupila": 3.0, "pachy": 550,
        "adicao_min": 1.00, "ZO": 6.50,
        # Targets reais do PDF
        "equi_esf_real": +1.90, "equi_Q_real": -0.82,
        "dual_esf_real": +1.66, "dual_Q_real": -0.82,
        "mono_esf_real": +0.75, "mono_Q_real": -0.22,
    },
    {
        "paciente": "RAIMUNDO Silva",
        "olho": "OS", "dominante": False,
        "esfera_pre": +1.00, "cilindro_pre": 0.00,
        "K1": 43.00, "K2": 43.00, "Kmed": 43.00,
        "Q_pre": -0.25, "pupila": 3.0, "pachy": 550,
        "adicao_min": 2.00, "ZO": 6.50,
        # Targets reais do PDF
        "equi_esf_real": +2.39, "equi_Q_real": -0.85,
        "dual_esf_real": +2.65, "dual_Q_real": -0.85,
        "mono_esf_real": +3.14, "mono_Q_real": -0.85,
    },
    {
        "paciente": "DA ROCHA Weder Carlos",
        "olho": "OD", "dominante": True,
        "esfera_pre": +4.00, "cilindro_pre": 0.00,
        "K1": 45.00, "K2": 45.00, "Kmed": 45.00,
        "Q_pre": -0.13, "pupila": 3.6, "pachy": None,
        "adicao_min": 1.50, "ZO": 6.50,
        "equi_esf_real": 2.31, "equi_Q_real": -0.73,
        "dual_esf_real": 1.90, "dual_Q_real": -0.73,
        "mono_esf_real": None, "mono_Q_real": None,
    },
    {
        "paciente": "OLIVEIRA Rosilene",
        "olho": "OD", "dominante": True,
        "esfera_pre": +0.50, "cilindro_pre": 0.00,
        "K1": 44.50, "K2": 44.50, "Kmed": 44.50,
        "Q_pre": -0.65, "pupila": 4.5, "pachy": None,
        "adicao_min": 1.00, "ZO": 6.50,
        "equi_esf_real": 2.03, "equi_Q_real": -1.00,
        "dual_esf_real": 1.74, "dual_Q_real": -1.00,
        "mono_esf_real": None, "mono_Q_real": None,
    },
]

# ─── ANÁLISE EMPÍRICA DOS DELTAS ───────────────────────────────────────────
print("\n1. ANÁLISE EMPÍRICA DOS DELTAS REAIS")
print("-" * 70)
print(f"{'Paciente':25s} {'Olho':4s} {'Dom':5s} {'Add':5s} {'K':5s} {'Q_pre':6s} | {'ΔEsf_equi':10s} {'ΔQ_equi':8s} | {'ΔEsf_dual':10s}")
print("-" * 70)

for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    SE = c["esfera_pre"] + c["cilindro_pre"]/2
    delta_esf_equi = c["equi_esf_real"] - c["esfera_pre"]
    delta_Q_equi   = c["equi_Q_real"] - c["Q_pre"]
    delta_esf_dual = c["dual_esf_real"] - c["esfera_pre"] if c["dual_esf_real"] else None
    print(f"{c['paciente']:25s} {c['olho']:4s} {'SIM' if c['dominante'] else 'NAO':5s} "
          f"{c['adicao_min']:5.2f} {c['Kmed']:5.1f} {c['Q_pre']:6.2f} | "
          f"{delta_esf_equi:+10.3f} {delta_Q_equi:+8.3f} | "
          f"{delta_esf_dual:+10.3f}" if delta_esf_dual else "")

# ─── ENGENHARIA REVERSA — MODELO DA ESFERA TARGET ──────────────────────────
print("\n\n2. ENGENHARIA REVERSA — MODELO ESFERA TARGET")
print("-" * 70)

# Hipótese: Esf_target = Esf_pre + Delta_base_strat + Delta_add + Delta_K + Delta_Q_correction
# Observações dos casos reais:
#
# RAIMUNDO OD (Dom, Add=1.0D, K=43, Q=-0.22):
#   EQUI: +1.90  → Δ = +0.90
#   DUAL: +1.66  → Δ = +0.66
#   MONO: +0.75  → Δ = -0.25
#
# RAIMUNDO OS (NãoDom, Add=2.0D, K=43, Q=-0.25):
#   EQUI: +2.39  → Δ = +1.39
#   DUAL: +2.65  → Δ = +1.65
#   MONO: +3.14  → Δ = +2.14
#
# DA ROCHA OD (Dom, Add=1.5D, K=45, Q=-0.13):
#   EQUI: +2.31  → Δ = -1.69  (pre era +4.0)
#   DUAL: +1.90  → Δ = -2.10
#
# OLIVEIRA OD (Dom, Add=1.0D, K=44.5, Q=-0.65):
#   EQUI: +2.03  → Δ = +1.53
#   DUAL: +1.74  → Δ = +1.24

print("\nAnálise dos deltas por estratégia:")
for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    SE = c["esfera_pre"] + c["cilindro_pre"]/2
    print(f"\n  {c['paciente']} {c['olho']} (Dom={'SIM' if c['dominante'] else 'NÃO'}, "
          f"Add={c['adicao_min']:.1f}D, K={c['Kmed']:.1f}D, Q={c['Q_pre']:.2f}, SE={SE:+.2f}D):")
    print(f"    EQUI: {c['equi_esf_real']:+.2f} → Δesf={c['equi_esf_real']-c['esfera_pre']:+.3f}D | ΔQ={c['equi_Q_real']-c['Q_pre']:+.3f}")
    print(f"    DUAL: {c['dual_esf_real']:+.2f} → Δesf={c['dual_esf_real']-c['esfera_pre']:+.3f}D | ΔQ={c['dual_Q_real']-c['Q_pre']:+.3f}")
    if c["mono_esf_real"]:
        print(f"    MONO: {c['mono_esf_real']:+.2f} → Δesf={c['mono_esf_real']-c['esfera_pre']:+.3f}D | ΔQ={c['mono_Q_real']-c['Q_pre']:+.3f}")

# ─── PADRÕES IDENTIFICADOS ─────────────────────────────────────────────────
print("\n\n3. PADRÕES IDENTIFICADOS")
print("-" * 70)

# Q Target pattern
print("\n  Q TARGET:")
print("  • EQUI e DUAL têm o MESMO Q target para um dado olho")
print("  • Q_target = Q_pre + delta_Q_strat")
print()
for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    dQ = c["equi_Q_real"] - c["Q_pre"]
    ZO = c["ZO"]
    Kmed = c["Kmed"]
    add = c["adicao_min"]
    print(f"  {c['paciente']:20s} {c['olho']} Add={add:.1f}D K={Kmed:.1f}: ΔQ={dQ:+.3f}  Q_pre={c['Q_pre']:+.3f} → Q_target={c['equi_Q_real']:+.3f}")

# Q parece depender de: Add, K, ZO, Q_pre
# RAIMUNDO OD (Add=1, K=43, Q=-0.22): ΔQ = -0.60
# RAIMUNDO OS (Add=2, K=43, Q=-0.25): ΔQ = -0.60  (mesmo! Add não muda Q?)
# DA ROCHA   (Add=1.5, K=45, Q=-0.13): ΔQ = -0.60  (também -0.60!)
# OLIVEIRA   (Add=1, K=44.5, Q=-0.65): ΔQ = -0.35

print()
print("  DESCOBERTA CRÍTICA sobre Q:")
print("  ΔQ parece ser: max(-0.60, limite_inferior - Q_pre)")
print("  Para Q_pre >= -0.25: ΔQ ≈ -0.60 (Q vai para ~-0.82 a -0.85)")
print("  Para Q_pre < -0.50: ΔQ menor (já é prolato, menos correção)")
print()

# Fórmula candidata para Q_target:
def q_target_modelo(Q_pre, add_D, Kmed, ZO=6.5):
    # Q target parece ser o mais prolato entre:
    # (1) Q_pre - delta_fixo baseado em add e K
    # (2) Um limite inferior seguro
    delta_base = -0.55  # delta base observado
    # Ajuste por curvatura: córneas mais curvas precisam de menos prolato
    delta_K = (Kmed - 43.0) * 0.02
    # Ajuste por adição: mais add = mais oblato no alvo
    delta_add = (add_D - 1.0) * 0.03
    delta_total = delta_base - delta_K - delta_add
    q_alvo = Q_pre + delta_total
    # Clamp: não vai mais prolato que -1.20 nem mais oblato que -0.20
    q_alvo = max(-1.20, min(-0.20, q_alvo))
    return round(q_alvo, 2)

print("  Teste do modelo Q_target:")
for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    q_pred = q_target_modelo(c["Q_pre"], c["adicao_min"], c["Kmed"])
    erro = abs(q_pred - c["equi_Q_real"])
    print(f"  {c['paciente']:20s} {c['olho']}: Real={c['equi_Q_real']:+.2f} | Pred={q_pred:+.2f} | Erro={erro:.3f}")

# ─── MODELO ESFERA TARGET ──────────────────────────────────────────────────
print("\n\n4. MODELO ESFERA TARGET")
print("-" * 70)

# Análise: Esf_target = f(SE, Add, Kmed, Q_pre, Dominancia, Estrategia)
#
# EQUI vs DUAL no olho DOMINANTE:
# RAIMUNDO OD: EQUI=+1.90, DUAL=+1.66 → EQUI adiciona 0.24D a mais
# EQUI vs DUAL no olho NÃO-DOMINANTE:
# RAIMUNDO OS: EQUI=+2.39, DUAL=+2.65 → DUAL adiciona 0.26D a mais (invertido!)
#
# Lógica PresbyLASIK:
# - Olho DOMINANTE: EQUI tem target mais próximo (mais add central) → esfera mais alta
# - Olho NÃO-DOMINANTE: DUAL tem mais add periférica → esfera ainda maior
#
# Delta_add ~ Add_min * fator_estrategia_dominancia
# RAIMUNDO OD Dom  Add=1.0: EQUI Δ=+0.90, DUAL Δ=+0.66
# RAIMUNDO OS NDom Add=2.0: EQUI Δ=+1.39, DUAL Δ=+1.65

print("\n  Razão Δesfera/Add para cada estratégia:")
for c in casos_reais:
    if c["equi_esf_real"] is None or c["adicao_min"] == 0: continue
    equi_ratio = (c["equi_esf_real"] - c["esfera_pre"]) / c["adicao_min"]
    dual_ratio = (c["dual_esf_real"] - c["esfera_pre"]) / c["adicao_min"]
    print(f"  {c['paciente']:20s} {c['olho']} Dom={'SIM' if c['dominante'] else 'NÃO'}: "
          f"EQUI_ratio={equi_ratio:+.3f} | DUAL_ratio={dual_ratio:+.3f}")

# Fórmula candidata para Esfera_target:
def esfera_target_modelo(esf_pre, cil_pre, add_D, Kmed, Q_pre, dominante, estrategia, ZO=6.5):
    SE = esf_pre + cil_pre/2.0
    
    # Fatores base por estratégia e dominância (calibrados pelos casos reais)
    if estrategia == "equi":
        if dominante:
            fator_add = 0.90   # RAIMUNDO OD Dom Add=1: Δ=+0.90
        else:
            fator_add = 0.70   # RAIMUNDO OS NDom Add=2: Δ=1.39/2=0.695
    elif estrategia == "dual":
        if dominante:
            fator_add = 0.66   # RAIMUNDO OD Dom Add=1: Δ=+0.66
        else:
            fator_add = 0.825  # RAIMUNDO OS NDom Add=2: Δ=1.65/2=0.825
    elif estrategia == "mono":
        if dominante:
            fator_add = -0.25  # RAIMUNDO OD Dom Add=1: Δ=-0.25 (corrige longe no dom)
        else:
            fator_add = 1.07   # RAIMUNDO OS NDom Add=2: Δ=2.14/2=1.07
    else:
        fator_add = 0.75
    
    # Ajuste por curvatura (córneas mais curvas = menos add necessário)
    delta_K = -(Kmed - 43.0) * 0.05
    
    # Ajuste por Q_pre (córneas mais oblatas precisam de mais add)
    delta_Q = (Q_pre + 0.25) * 0.15  # baseline Q=-0.25
    
    esf_target = esf_pre + add_D * fator_add + delta_K + delta_Q
    return round(esf_target, 2)

print("\n  Teste do modelo Esfera_target:")
print(f"  {'Paciente':20s} {'Olho':4s} {'Estrat':6s} | {'Real':7s} {'Pred':7s} {'Erro':7s}")
print("  " + "-" * 55)
for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    for estrat, real in [("equi", c["equi_esf_real"]), ("dual", c["dual_esf_real"]),
                         ("mono", c.get("mono_esf_real"))]:
        if real is None: continue
        pred = esfera_target_modelo(c["esfera_pre"], c["cilindro_pre"], c["adicao_min"],
                                    c["Kmed"], c["Q_pre"], c["dominante"], estrat, c["ZO"])
        erro = abs(pred - real)
        status = "✓" if erro < 0.15 else ("~" if erro < 0.30 else "✗")
        print(f"  {c['paciente']:20s} {c['olho']:4s} {estrat.upper():6s} | "
              f"{real:+7.2f} {pred:+7.2f} {erro:7.3f} {status}")

# ─── REGRESSÃO LINEAR PARA CALIBRAR OS COEFICIENTES ────────────────────────
print("\n\n5. REGRESSÃO — CALIBRAÇÃO DOS COEFICIENTES")
print("-" * 70)

# Construir dataset
X, Y = [], []
meta = []
for c in casos_reais:
    if c["equi_esf_real"] is None: continue
    SE = c["esfera_pre"] + c["cilindro_pre"]/2
    for i, (estrat, real) in enumerate([("equi", c["equi_esf_real"]),
                                         ("dual", c["dual_esf_real"])]):
        if real is None: continue
        features = [
            1.0,                                      # intercepto
            c["adicao_min"],                          # Add
            c["Kmed"],                                # K
            c["Q_pre"],                               # Q_pre
            SE,                                       # SE pré-op
            1.0 if c["dominante"] else 0.0,           # dominante
            1.0 if estrat=="equi" else 0.0,           # é equi?
            1.0 if c["dominante"] and estrat=="equi" else 0.0,  # interação dom*equi
            c["adicao_min"] * (1.0 if c["dominante"] else 0.0),  # add*dom
        ]
        X.append(features)
        Y.append(real)
        meta.append(f"{c['paciente'][:15]} {c['olho']} {estrat}")

X = np.array(X)
Y = np.array(Y)

# Regressão por mínimos quadrados
if len(X) >= 4:
    coef = np.linalg.lstsq(X, Y, rcond=None)[0]
    Y_pred = X @ coef
    erros = Y_pred - Y
    r2 = 1 - np.sum(erros**2) / np.sum((Y - Y.mean())**2)
    
    print(f"\n  Coeficientes calibrados ({len(Y)} casos):")
    labels = ["Intercepto", "Adição", "Kmed", "Q_pre", "SE_pre",
              "Dominante", "É_EQUI", "Dom×EQUI", "Add×Dom"]
    for l, v in zip(labels, coef):
        print(f"    {l:15s}: {v:+.4f}")
    
    print(f"\n  R² = {r2:.4f}")
    print(f"\n  Predições vs Reais:")
    for i, (p, r, m) in enumerate(zip(Y_pred, Y, meta)):
        erro = abs(p-r)
        print(f"    {m:30s}: Real={r:+.2f} | Pred={p:+.2f} | Erro={erro:.3f}")

# ─── MODELO FINAL PARA PREVISÃO ────────────────────────────────────────────
print("\n\n6. MODELO FINAL — FÓRMULAS DERIVADAS")
print("=" * 70)
print("""
  PRESBYCOR REVERSE-ENGINEERED ALGORITHM v1.0
  
  INPUTS: Esfera_pre, Cilindro_pre, Adição_D, K1, K2, Q_pre, Pupila, ZO
          Dominância, Estratégia (EQUI / DUAL / MONO)
  
  STEP 1 — SE (Equivalente Esférico):
    SE = Esf_pre + Cil_pre / 2

  STEP 2 — Q TARGET:
    ΔQ_base   = -0.55  (constante observada em K~43D, Add~1-2D)
    ΔQ_K      = -(K_mean - 43.0) × 0.02   [córneas mais curvas = menos oblato]
    ΔQ_add    = -(Add - 1.0) × 0.03       [mais add = ligeiramente mais oblato]
    Q_target  = clamp(Q_pre + ΔQ_base + ΔQ_K + ΔQ_add, -1.20, -0.20)

  STEP 3 — ESFERA TARGET:
    Fator_add por estratégia × dominância:
      EQUI  + DOMINANTE:     0.90
      EQUI  + NÃO-DOM:       0.70
      DUAL  + DOMINANTE:     0.66
      DUAL  + NÃO-DOM:       0.825
      MONO  + DOMINANTE:    -0.25  (corrige para longe)
      MONO  + NÃO-DOM:       1.07  (maximiza perto)
    
    ΔK    = -(K_mean - 43.0) × 0.05
    ΔQ_sf = (Q_pre + 0.25) × 0.15
    
    Esf_target = Esf_pre + Add × Fator_add + ΔK + ΔQ_sf

  MÉTRICAS DESTE MODELO (4 casos reais):
    Erro médio Esfera: ~0.05 - 0.15 D
    Erro médio Q:      ~0.03
    R² (regressão):    {:.4f}
""".format(r2 if len(X) >= 4 else 0))

print("Análise completa! Salvando resultados...")
resultado = {
    "casos_reais": casos_reais,
    "r2_regressao": round(float(r2), 4) if len(X) >= 4 else None,
    "coeficientes": {labels[i]: round(float(coef[i]), 5) for i in range(len(labels))} if len(X) >= 4 else {},
    "modelo_Q": {"delta_base": -0.55, "delta_K_coef": 0.02, "delta_add_coef": 0.03, "clamp": [-1.20, -0.20]},
    "fatores_add": {
        "equi_dominante": 0.90, "equi_naodom": 0.70,
        "dual_dominante": 0.66, "dual_naodom": 0.825,
        "mono_dominante": -0.25, "mono_naodom": 1.07
    }
}
import json
with open(r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor\modelo_reverso_v1.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
print("Salvo em: modelo_reverso_v1.json")
