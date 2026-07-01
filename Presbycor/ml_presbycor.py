import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. LOAD DATA
df = pd.read_csv(r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor\Presbycor_Database_Completo.csv")

# 2. TRANSFORM DATA (Melt OD and OS into individual eye records)
eyes_data = []
for idx, row in df.iterrows():
    # Common features
    age = pd.to_numeric(row.get("Age (years)"), errors="coerce")
    
    # Process OD
    if pd.notna(row.get("OD Pre Sphere (D)")):
        eyes_data.append({
            "eye": "OD",
            "age": age,
            "add": pd.to_numeric(row.get("OD Pre Min Add (D)"), errors="coerce"),
            "dominant": 1 if str(row.get("OD Dominant")).strip().lower() == "yes" else 0,
            
            # Pre-Op
            "sph_pre": pd.to_numeric(row.get("OD Pre Sphere (D)"), errors="coerce"),
            "cyl_pre": pd.to_numeric(row.get("OD Pre Cylinder (D)"), errors="coerce"),
            "k1": pd.to_numeric(row.get("OD Pre K1 (D)"), errors="coerce"),
            "k2": pd.to_numeric(row.get("OD Pre K2 (D)"), errors="coerce"),
            "q_pre": pd.to_numeric(row.get("OD Pre Asph Q"), errors="coerce"),
            "pachy": pd.to_numeric(row.get("OD Pre Pachy (um)"), errors="coerce"),
            
            # Target EQUI
            "equi_sph_target": pd.to_numeric(row.get("OD Equi Sphere (D)"), errors="coerce"),
            "equi_q_target": pd.to_numeric(row.get("OD Equi Q Target"), errors="coerce"),
            
            # Target DUAL
            "dual_sph_target": pd.to_numeric(row.get("OD Dual Sphere (D)"), errors="coerce"),
            "dual_q_target": pd.to_numeric(row.get("OD Dual Q Target"), errors="coerce"),
            
            # Target MONO
            "mono_sph_target": pd.to_numeric(row.get("OD Mono Sphere (D)"), errors="coerce"),
            "mono_q_target": pd.to_numeric(row.get("OD Mono Q Target"), errors="coerce"),
        })
        
    # Process OS
    if pd.notna(row.get("OS Pre Sphere (D)")):
        eyes_data.append({
            "eye": "OS",
            "age": age,
            "add": pd.to_numeric(row.get("OS Pre Min Add (D)"), errors="coerce"),
            "dominant": 1 if str(row.get("OS Dominant")).strip().lower() == "yes" else 0,
            
            # Pre-Op
            "sph_pre": pd.to_numeric(row.get("OS Pre Sphere (D)"), errors="coerce"),
            "cyl_pre": pd.to_numeric(row.get("OS Pre Cylinder (D)"), errors="coerce"),
            "k1": pd.to_numeric(row.get("OS Pre K1 (D)"), errors="coerce"),
            "k2": pd.to_numeric(row.get("OS Pre K2 (D)"), errors="coerce"),
            "q_pre": pd.to_numeric(row.get("OS Pre Asph Q"), errors="coerce"),
            "pachy": pd.to_numeric(row.get("OS Pre Pachy (um)"), errors="coerce"),
            
            # Target EQUI
            "equi_sph_target": pd.to_numeric(row.get("OS Equi Sphere (D)"), errors="coerce"),
            "equi_q_target": pd.to_numeric(row.get("OS Equi Q Target"), errors="coerce"),
            
            # Target DUAL
            "dual_sph_target": pd.to_numeric(row.get("OS Dual Sphere (D)"), errors="coerce"),
            "dual_q_target": pd.to_numeric(row.get("OS Dual Q Target"), errors="coerce"),
            
            # Target MONO
            "mono_sph_target": pd.to_numeric(row.get("OS Mono Sphere (D)"), errors="coerce"),
            "mono_q_target": pd.to_numeric(row.get("OS Mono Q Target"), errors="coerce"),
        })

df_eyes = pd.DataFrame(eyes_data)

# FEATURE ENGINEERING
df_eyes['k_mean'] = (df_eyes['k1'] + df_eyes['k2']) / 2
df_eyes['se_pre'] = df_eyes['sph_pre'] + (df_eyes['cyl_pre'] / 2)

# Remove rows missing essential pre-op data
core_features = ['sph_pre', 'cyl_pre', 'k_mean', 'q_pre', 'add', 'dominant']
df_eyes = df_eyes.dropna(subset=core_features).copy()

print(f"Total eyes available with complete Pre-Op data: {len(df_eyes)}")

# Function to train and evaluate a model for a specific target
def evaluate_target(df_eyes, target_col, target_name):
    print(f"\n{'='*50}\nANALYZING TARGET: {target_name}\n{'='*50}")
    
    # Filter rows that have this target successfully extracted
    df_clean = df_eyes.dropna(subset=[target_col]).copy()
    print(f"Valid Samples for {target_name}: {len(df_clean)}")
    
    if len(df_clean) < 10:
        print("Not enough samples to train.")
        return
        
    X = df_clean[core_features + ['se_pre']]
    y = df_clean[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Linear Regression (Base Reverse Engineering)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    r2_lr = r2_score(y_test, y_pred_lr)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    
    print(f"\n[Linear Regression]")
    print(f"R² Score: {r2_lr:.4f} (1.0 is perfect)")
    print(f"MAE Error: {mae_lr:.4f} Diopters")
    print("Coefficients:")
    for feat, coef in zip(X.columns, lr.coef_):
        print(f"  {feat:10s} : {coef:+.4f}")
    print(f"  Intercept  : {lr.intercept_:+.4f}")
    
    # 2. Random Forest Regressor (Non-linear pattern detection)
    rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    
    print(f"\n[Random Forest]")
    print(f"R² Score: {r2_rf:.4f}")
    print(f"MAE Error: {mae_rf:.4f} Diopters")
    print("Feature Importances:")
    importances = sorted(zip(X.columns, rf.feature_importances_), key=lambda x: x[1], reverse=True)
    for feat, imp in importances:
        print(f"  {feat:10s} : {imp*100:.1f}%")
        
    # Check for clamping/limits in the real data
    print(f"\nData Stats for {target_name}: Min={y.min():.2f}, Max={y.max():.2f}")

# Run for EQUI Targets
evaluate_target(df_eyes, 'equi_sph_target', 'EQUI Sphere Target (D)')
evaluate_target(df_eyes, 'equi_q_target', 'EQUI Q Target')
