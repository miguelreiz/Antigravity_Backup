# Infográfico 13.2: Árvore Decisão - Corneana vs RLE

```mermaid
flowchart TD
    A[CÓRNEA VIÁVEL<br/>Propedêutica OK] --> B{IDADE?}
    
    B -->|< 55 anos| C{DLS?}
    B -->|≥ 55 anos| D{DLS?}
    
    C -->|DLS 1-2| E[CIRURGIA<br/>CORNEANA]
    C -->|DLS 3-4| F{OSI?}
    
    D -->|DLS 1-2| G{AVALIAR MAIS}
    D -->|DLS 3-4| H[RLE<br/>PREFERÍVEL]
    
    F -->|< 1.5| E
    F -->|> 2.0| H
    
    G --> I{OSI?}
    I -->|< 1.5| E
    I -->|> 2.0| H
    
    E --> J[Caps 4-8:<br/>Qual Técnica]
    H --> K[Cap 12:<br/>IOL Selection]
    
    style E fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style H fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style A fill:#fff9c4,stroke:#f57f17,stroke-width:2px
```

**Contexto:** Algoritmo Capítulo 12 (Corneal vs Lenticular)

**Decisão Simplificada:**
- Idade <52 + DLS 1-2 + OSI <1.5 = **CORNEANA**
- Idade >60 + DLS 3-4 ou OSI >2.0 = **RLE**
- Zona cinzenta (52-60) = Análise individual
