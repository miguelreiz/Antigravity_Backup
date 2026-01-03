# Infográfico 11.1: Algoritmo Gestão Descentramento

```mermaid
flowchart TD
    A[Suspeita Descentramento<br/>Diplopia, Halos Assimétricos<br/>BCVA <20/30] --> B[TOPOGRAFIA]
    
    B --> C{Quantificar<br/>Descentramento}
    
    C -->|< 0.5 mm| D[OBSERVAR<br/>Provável neuroadaptação]
    C -->|> 0.5 mm| E[Medir Coma<br/>Aberrometria]
    
    E --> F{Coma?}
    
    F -->|< 0.30 μm| G[Aguardar<br/>6 meses]
    F -->|> 0.30 μm| H{Sintomático?}
    
    H -->|NÃO| G
    H -->|SIM| I{RSB OK?}
    
    I -->|SIM<br/>>300μm| J[T-CAT<br/>Enhancement<br/>Topoguiado]
    I -->|NÃO<br/><300μm| K[RGP ou RLE<br/>Não ablacionar mais]
    
    G --> L{Melhoria<br/>6 meses?}
    L -->|SIM| M[Continue<br/>Observação]
    L -->|NÃO| I
    
    style A fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style K fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

**Critérios Decisão:**
- Descentramento <0.5mm → Observar (neuroadaptação pode compensar)
- Descentramento >0.5mm + Coma >0.30μm + Sintomático → **Enhancement indicado**
- RSB insuficiente (<300μm) → **Não tocar** (RGP ou RLE)
