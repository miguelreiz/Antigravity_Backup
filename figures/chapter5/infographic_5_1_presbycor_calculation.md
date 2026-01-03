# Infográfico 5.1: PresbyCor/Custom-Q - Fluxo de Cálculo

```mermaid
flowchart TD
    A[DADOS PRÉ-OP] --> B[K médio<br/>Q pré-op<br/>Add desejada<br/>Dominância]
    
    B --> C{OLHO?}
    
    C -->|DOMINANTE| D[Q-Target<br/>Tabela 5.3.1<br/>Add → Q]
    C -->|NÃO-DOMINANTE| E[Q-Target<br/>Mais negativo<br/>+0.1 vs dominante]
    
    D --> F[CÁLCULO ΔQ]
    E --> F
    
    F --> G[ΔQ = Q_target - Q_preop]
    
    G --> H[COMPENSAÇÃO<br/>ESFÉRICA<br/>S_comp = |ΔQ| × K × 0.75]
    
    H --> I[PROGRAMAÇÃO LASER]
    
    I --> J{Plataforma?}
    
    J -->|Wavelight| K[Custom-Q Mode<br/>Input: Q-target<br/>S_comp automático]
    J -->|Contoura| L[Topoguided Mode<br/>Adjust Q manually]
    J -->|Outra| M[Transferir cálculos<br/>Ver Capítulo 5.6]
    
    K --> N[VALIDAÇÃO]
    L --> N
    M --> N
    
    N --> O{RSB previsto<br/>>300 μm?}
    O -->|SIM| P[✅ PROSSEGUIR]
    O -->|NÃO| Q[❌ RECALCULAR<br/>ou RLE]
    
    style A fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style P fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:3px
```

**Exemplo Cálculo:**
- K = 43.00 D, Q_pré = -0.25, Add = +1.75 D
- Q_target = -0.70 (Tabela)
- ΔQ = -0.45
- S_comp = 0.45 × 43 × 0.75 = **+14.5 D** (shift hipermetrópico)
