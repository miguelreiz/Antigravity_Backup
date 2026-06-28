"""
runner.py — Orquestrador do pipeline FEM-VOLUME ICRS.

Fluxo:
  1. Gera 3 malhas Gmsh (Baseline, Triangular, Oval)
  2. Exporta 3 modelos FEBio (.feb) com material HGO anisotrópico
  3. Executa o solver FEBio 4 em sequência
"""

import os
import subprocess


def run_pipeline():
    print("=" * 60)
    print("  FEM-VOLUME ICRS PIPELINE  (Fase 4 — HGO Anisotrópico)")
    print("=" * 60)

    # ---- 1. Geração de Malhas ----
    print("\n[1/3] Gerando malhas Hex8 via Gmsh...")
    import gmsh
    from mesh_generator import generate_cornea_ring_mesh

    configs = [
        ("cornea_baseline.msh", False, "triangular"),
        ("cornea_triangular.msh", True, "triangular"),
        ("cornea_oval.msh", True, "oval"),
    ]

    for filename, has_ring, profile in configs:
        generate_cornea_ring_mesh(
            output_filename=filename,
            has_ring=has_ring,
            ring_profile=profile,
        )
        gmsh.finalize()

    # ---- 2. Exportação FEBio ----
    print("\n[2/3] Exportando modelos FEBio v4 (HGO)...")
    from febio_builder import export_to_febio

    exports = [
        ("cornea_baseline.msh", "model_baseline.feb", True),
        ("cornea_triangular.msh", "model_triangular.feb", False),
        ("cornea_oval.msh", "model_oval.feb", False),
    ]

    for msh_file, feb_file, is_baseline in exports:
        gmsh.initialize()
        gmsh.open(msh_file)
        export_to_febio(output_feb_file=feb_file, baseline=is_baseline)
        gmsh.finalize()

    # ---- 3. Execução do Solver ----
    print("\n[3/3] Executando FEBio 4 Solver...")
    febio_path = r"C:\Program Files\FEBioStudio\bin\febio4.exe"

    feb_files = ["model_baseline.feb", "model_triangular.feb", "model_oval.feb"]
    for feb_file in feb_files:
        print(f"\n  --> {feb_file}")
        result = subprocess.run(
            [febio_path, "-i", feb_file],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"      [OK] Convergiu com sucesso.")
        else:
            print(f"      [FALHA] Simulação não convergiu.")
            # Extrair linha de erro do stdout do FEBio
            for line in result.stdout.split("\n"):
                if "ERROR" in line or "FAILED" in line:
                    print(f"      {line.strip()}")

    print("\n" + "=" * 60)
    print("  Pipeline concluído.")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
