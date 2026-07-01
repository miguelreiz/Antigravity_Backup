"""
=============================================================================
PRESBYCOR — Pipeline Completo de Engenharia Reversa com ML/DL
=============================================================================
Autor: Antigravity AI
Data:  2026-07-01

COMO USAR:
1. Salve o arquivo HTML da página do Presbycor como 'calculos.html' nesta pasta
2. Execute: python pipeline_ml.py
3. O script extrai os dados, treina os modelos e exibe os resultados
=============================================================================
"""

import os
import sys
import json
import warnings
warnings.filterwarnings('ignore')

# ── Verificação e instalação de dependências ──────────────────────────────────
REQUIRED = ['pandas', 'numpy', 'scikit-learn', 'xgboost', 'matplotlib',
            'seaborn', 'beautifulsoup4', 'lxml', 'requests']

def install_if_missing(packages):
    import subprocess
    for pkg in packages:
        try:
            __import__(pkg.replace('-', '_').split('[')[0])
        except ImportError:
            print(f"  Instalando {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

print("🔧 Verificando dependências...")
install_if_missing(REQUIRED)
print("✅ Dependências OK\n")

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neural_network import MLPRegressor
import xgboost as xgb

# ── Configurações ─────────────────────────────────────────────────────────────
HTML_FILE    = 'calculos.html'
CSV_OUTPUT   = 'dados_presbycor.csv'
RESULTS_FILE = 'resultados_ml.json'
PLOTS_DIR    = 'plots'
os.makedirs(PLOTS_DIR, exist_ok=True)

# =============================================================================
# FASE 1 — EXTRAÇÃO DOS DADOS DO HTML
# =============================================================================
def extrair_dados_html(filepath):
    """
    Parseia o HTML do Presbycor e extrai os dados de todos os cálculos.
    Retorna um DataFrame com todas as variáveis encontradas.
    """
    print("=" * 60)
    print("FASE 1 — EXTRAÇÃO DOS DADOS")
    print("=" * 60)

    if not os.path.exists(filepath):
        print(f"⚠️  Arquivo '{filepath}' não encontrado!")
        print("   → Por favor, salve a página do Presbycor como 'calculos.html'")
        print("   → Abrindo modo DEMO com dados simulados para testar o pipeline...\n")
        return gerar_dados_demo()

    print(f"📄 Lendo: {filepath}")
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')

    # Tentar extrair tabelas
    tabelas = soup.find_all('table')
    print(f"   Tabelas encontradas: {len(tabelas)}")

    if tabelas:
        dfs = []
        for i, t in enumerate(tabelas):
            try:
                df_t = pd.read_html(str(t))[0]
                dfs.append(df_t)
                print(f"   Tabela {i+1}: {df_t.shape[0]} linhas × {df_t.shape[1]} colunas")
            except Exception as e:
                print(f"   Tabela {i+1}: erro ao parsear ({e})")

        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            print(f"\n✅ Total extraído: {len(df)} registros, {df.shape[1]} colunas")
            df.to_csv(CSV_OUTPUT, index=False)
            print(f"💾 Salvo em: {CSV_OUTPUT}")
            return df

    # Se não há tabelas, tentar extrair JSON embutido
    scripts = soup.find_all('script')
    for s in scripts:
        texto = s.get_text()
        if 'strategies' in texto.lower() or 'calcul' in texto.lower():
            try:
                inicio = texto.find('{')
                if inicio != -1:
                    dados_json = json.loads(texto[inicio:texto.rfind('}')+1])
                    df = pd.json_normalize(dados_json)
                    print(f"\n✅ Dados JSON extraídos: {df.shape}")
                    df.to_csv(CSV_OUTPUT, index=False)
                    return df
            except:
                pass

    print("⚠️  Estrutura HTML não reconhecida. Usando modo DEMO.")
    return gerar_dados_demo()


def gerar_dados_demo():
    """
    Gera dados simulados com estrutura típica de um sistema de cálculo
    oftalmológico (presbycor = cálculo de adição para presbiopia).
    Variáveis típicas: idade, refração, adição necessária, etc.
    """
    print("🎲 Gerando dados DEMO (estrutura típica Presbycor)...")
    np.random.seed(42)
    n = 420

    df = pd.DataFrame({
        'idade':          np.random.normal(52, 8, n).clip(40, 70),
        'esfera_od':      np.random.normal(-1.5, 2.5, n).round(2),
        'cilindro_od':    np.random.normal(-0.75, 1.0, n).clip(-4, 0).round(2),
        'eixo_od':        np.random.randint(0, 180, n),
        'esfera_oe':      np.random.normal(-1.5, 2.5, n).round(2),
        'cilindro_oe':    np.random.normal(-0.75, 1.0, n).clip(-4, 0).round(2),
        'eixo_oe':        np.random.randint(0, 180, n),
        'add_near':       np.random.choice([1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5], n),
        'dominancia':     np.random.choice(['OD', 'OE'], n),
        'avlonge_od':     np.random.uniform(0.8, 1.2, n).round(1),
        'avlonge_oe':     np.random.uniform(0.8, 1.2, n).round(1),
        'k1_od':          np.random.normal(43.5, 1.5, n).round(2),
        'k2_od':          np.random.normal(44.5, 1.5, n).round(2),
        'paquimetria':    np.random.normal(540, 35, n).round(0),
    })

    # Simular output típico (adição calculada pelo Presbycor)
    # Fórmula hipotética: Add = f(idade, esfera, add_near)
    df['output_adicao'] = (
        0.08 * (df['idade'] - 40)
        + 0.15 * df['add_near']
        - 0.05 * df['esfera_od']
        + np.random.normal(0, 0.1, n)
    ).round(2)

    print(f"✅ {len(df)} casos simulados gerados")
    df.to_csv(CSV_OUTPUT, index=False)
    return df


# =============================================================================
# FASE 2 — ANÁLISE EXPLORATÓRIA (EDA)
# =============================================================================
def eda(df):
    print("\n" + "=" * 60)
    print("FASE 2 — ANÁLISE EXPLORATÓRIA")
    print("=" * 60)

    print(f"\n📊 Shape: {df.shape}")
    print(f"📋 Colunas:\n   {list(df.columns)}")
    print(f"\n📈 Estatísticas:")
    print(df.describe().round(3).to_string())

    print(f"\n🔍 Valores nulos por coluna:")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0].to_string() if nulos.sum() > 0 else "   Nenhum valor nulo!")

    # Matriz de correlação
    df_num = df.select_dtypes(include=[np.number])
    if len(df_num.columns) > 1:
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(df_num.corr(), annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, ax=ax, square=True, linewidths=0.5)
        ax.set_title('Matriz de Correlação — Presbycor', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{PLOTS_DIR}/correlacao.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"\n📊 Gráfico de correlação salvo em: {PLOTS_DIR}/correlacao.png")

    return df_num


# =============================================================================
# FASE 3 — TREINAMENTO DOS MODELOS
# =============================================================================
def treinar_modelos(df_num, target_col=None):
    print("\n" + "=" * 60)
    print("FASE 3 — TREINAMENTO DOS MODELOS ML/DL")
    print("=" * 60)

    # Identificar coluna alvo
    if target_col is None:
        # Tentar identificar automaticamente
        candidatos = [c for c in df_num.columns if any(
            k in c.lower() for k in ['output', 'result', 'adicao', 'add', 'target', 'score', 'calc']
        )]
        if candidatos:
            target_col = candidatos[0]
        else:
            target_col = df_num.columns[-1]  # última coluna por padrão

    print(f"\n🎯 Coluna alvo: '{target_col}'")
    feature_cols = [c for c in df_num.columns if c != target_col]
    print(f"📥 Features ({len(feature_cols)}): {feature_cols}")

    X = df_num[feature_cols].dropna()
    y = df_num.loc[X.index, target_col].dropna()
    X = X.loc[y.index]

    print(f"\n📦 Dataset: {len(X)} amostras, {len(feature_cols)} features")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    modelos = {
        'Regressão Linear': LinearRegression(),
        'Regressão Polinomial (grau 2)': Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('lin',  LinearRegression())
        ]),
        'Random Forest': RandomForestRegressor(
            n_estimators=300, max_depth=8, random_state=42, n_jobs=-1),
        'XGBoost': xgb.XGBRegressor(
            n_estimators=300, max_depth=6, learning_rate=0.05,
            random_state=42, verbosity=0),
        'Gradient Boosting': GradientBoostingRegressor(
            n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42),
        'Rede Neural (MLP)': MLPRegressor(
            hidden_layer_sizes=(128, 64, 32), max_iter=1000,
            random_state=42, early_stopping=True, validation_fraction=0.15),
    }

    resultados = {}
    melhor_r2 = -np.inf
    melhor_modelo = None

    print("\n" + "-" * 55)
    print(f"{'Modelo':<35} {'R²':>6} {'RMSE':>8} {'MAE':>8}")
    print("-" * 55)

    for nome, modelo in modelos.items():
        try:
            if 'Linear' in nome or 'Neural' in nome:
                modelo.fit(X_train_s, y_train)
                y_pred = modelo.predict(X_test_s)
            else:
                modelo.fit(X_train, y_train)
                y_pred = modelo.predict(X_test)

            r2   = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae  = mean_absolute_error(y_test, y_pred)

            resultados[nome] = {'R2': round(r2, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae, 4)}
            print(f"{nome:<35} {r2:>6.4f} {rmse:>8.4f} {mae:>8.4f}")

            if r2 > melhor_r2:
                melhor_r2 = r2
                melhor_modelo = nome

        except Exception as e:
            print(f"{nome:<35} ERRO: {e}")

    print("-" * 55)
    print(f"\n🏆 Melhor modelo: {melhor_modelo} (R² = {melhor_r2:.4f})")

    # Importância de features (Random Forest)
    rf = modelos['Random Forest']
    if hasattr(rf, 'feature_importances_'):
        imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
        print(f"\n🔑 Importância das variáveis (Random Forest):")
        for feat, val in imp.items():
            bar = '█' * int(val * 50)
            print(f"   {feat:<25} {val:.4f} {bar}")

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        imp.head(15).plot(kind='barh', ax=ax, color='steelblue')
        ax.set_title('Importância das Features — Random Forest', fontsize=14, fontweight='bold')
        ax.set_xlabel('Importância')
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(f'{PLOTS_DIR}/feature_importance.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"📊 Gráfico salvo em: {PLOTS_DIR}/feature_importance.png")

    # Salvar resultados
    with open(RESULTS_FILE, 'w') as f:
        json.dump({'modelos': resultados, 'melhor': melhor_modelo,
                   'features': feature_cols, 'target': target_col}, f, indent=2)
    print(f"\n💾 Resultados salvos em: {RESULTS_FILE}")

    return resultados, melhor_modelo, modelos, scaler, X_test, y_test, feature_cols


# =============================================================================
# FASE 4 — COMPARAÇÃO COM RESULTADOS DO GEMINI
# =============================================================================
def comparar_com_gemini(y_real, y_presbycor, y_gemini=None):
    """
    Compara os resultados do modelo reconstruído com o Presbycor real
    e com o modelo do Gemini (se fornecido).
    """
    print("\n" + "=" * 60)
    print("FASE 4 — COMPARAÇÃO DE RESULTADOS")
    print("=" * 60)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Scatter: Presbycor Real vs Modelo Reconstruído
    axes[0].scatter(y_real, y_presbycor, alpha=0.6, s=30, color='steelblue')
    lim = [min(y_real.min(), y_presbycor.min()), max(y_real.max(), y_presbycor.max())]
    axes[0].plot(lim, lim, 'r--', linewidth=2, label='Linha perfeita')
    axes[0].set_xlabel('Presbycor Real')
    axes[0].set_ylabel('Modelo Reconstruído')
    axes[0].set_title('Real vs. Reconstruído')
    axes[0].legend()

    # Distribuição dos resíduos
    residuos = y_real.values - y_presbycor
    axes[1].hist(residuos, bins=30, color='steelblue', edgecolor='white', alpha=0.8)
    axes[1].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Resíduo (Real − Predito)')
    axes[1].set_ylabel('Frequência')
    axes[1].set_title(f'Distribuição dos Resíduos\nMédia={residuos.mean():.4f}, DP={residuos.std():.4f}')

    plt.suptitle('Análise de Performance — Engenharia Reversa Presbycor', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/comparacao_resultados.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"📊 Gráfico de comparação salvo em: {PLOTS_DIR}/comparacao_resultados.png")


# =============================================================================
# MAIN — EXECUÇÃO COMPLETA
# =============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  PRESBYCOR — ENGENHARIA REVERSA COM ML/DL")
    print("  Antigravity AI | 2026")
    print("=" * 60)

    # FASE 1: Extração
    df = extrair_dados_html(HTML_FILE)

    # FASE 2: EDA
    df_num = eda(df)

    # FASE 3: Modelos
    if len(df_num.columns) >= 2:
        resultados, melhor, modelos, scaler, X_test, y_test, features = treinar_modelos(df_num)

        # FASE 4: Comparação
        melhor_modelo = modelos[melhor]
        if 'Linear' in melhor or 'Neural' in melhor:
            y_pred = melhor_modelo.predict(scaler.transform(X_test))
        else:
            y_pred = melhor_modelo.predict(X_test)

        comparar_com_gemini(y_test, y_pred)
    else:
        print("⚠️  Dados insuficientes para treinar modelos.")

    print("\n" + "=" * 60)
    print("✅ PIPELINE CONCLUÍDO!")
    print(f"   Arquivo de dados:    {CSV_OUTPUT}")
    print(f"   Resultados ML:       {RESULTS_FILE}")
    print(f"   Gráficos:            {PLOTS_DIR}/")
    print("=" * 60)
    print("\n💡 Próximo passo: Forneça o arquivo 'calculos.html' do Presbycor")
    print("   para substituir os dados demo por dados reais dos pacientes.")
