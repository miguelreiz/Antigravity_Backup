# Infográfico 13.4: Árvore Decisão - Qual Técnica Corneana?

```mermaid
flowchart TD
    A[DECISÃO: CIRURGIA<br/>CORNEANA] --> B{PLATAFORMA<br/>DISPONÍVEL?}
    
    B --> C[Wavelight<br/>Alcon]
    B --> D[Schwind<br/>Amaris]
    B --> E[Zeiss<br/>MEL90]
    
    C --> F{ADD<br/>NECESSÁRIA?}
    D --> F
    E --> F
    
    F -->|≤ +1.75 D| G{PUPILA<br/>MESÓPICA?}
    F -->|> +1.75 D| H{PUPILA<br/>MESÓPICA?}
    
    G -->|< 6.5 mm| I[PRESBYOND<br/>ou Custom-Q<br/>✅ Recomendado]
    G -->|> 6.5 mm| J[Custom-Q<br/>Conservador]
    
    H -->|< 6.0 mm| K[PresbyMAX<br/>ou SUPRACOR<br/>⚠️ Halos moderados]
    H -->|> 6.0 mm| L[Custom-Q ou<br/>Reconsiderar RLE]
    
    I --> M{PERFIL<br/>PACIENTE?}
    M -->|Valoriza longe| N[Custom-Q]
    M -->|Valoriza inter+perto| O[PRESBYOND<br/>🏆 Best overall]
    
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style O fill:#81c784,stroke:#2e7d32,stroke-width:4px
    style K fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

**Recomendação Geral (múltiplas opções):**
1. **PRESBYOND** (se Zeiss + pupila OK) → Melhor balanço satisfação/halos
2. **Custom-Q** (personalização máxima)
3. **PresbyMAX** (add >+2.0 D)
4. **SUPRACOR** (nicho <5% população)
