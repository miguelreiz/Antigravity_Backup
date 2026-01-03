# Infográfico 9.1: Algoritmo Desafio Pós-Refrativo

```mermaid
flowchart TD
    A[Paciente Presbiópico<br/>PÓS-LASIK/PRK Prévio] --> B[AVALIAÇÃO<br/>ESPECÍFICA]
    
    B --> C{RSB ATUAL<br/>OCT?}
    
    C -->|> 320 μm| D{Q PÓS-LASIK?}
    C -->|< 320 μm| E[❌ CIRURGIA<br/>CORNEANA<br/>CONTRAINDICADA<br/>→ RLE única opção]
    
    D -->|Oblato<br/>+0.3 a +0.7| F{ABERROMETRIA<br/>HOA?}
    D -->|Muito oblato<br/>>+0.8| E
    
    F -->|Coma <0.30 μm<br/>SA aceitável| G{DLS +<br/>IDADE?}
    F -->|Coma >0.40 μm<br/>ou Trefoil alto| H[Enhancement<br/>Topoguiado ANTES<br/>de presbiópico]
    
    G -->|DLS 1-2<br/>Idade <58| I[Custom-Q<br/>MODIFICADO<br/>Q-target conservador]
    G -->|DLS 3-4<br/>ou Idade >60| E
    
    I --> J{Sucesso?}
    J -->|SIM<br/>UCDVA/UCNVA OK| K[✅ Seguimento<br/>Standard]
    J -->|NÃO<br/>Insatisfação| L[Reversão ou<br/>RLE]
    
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style I fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

**Critérios Absolutos Pós-LASIK:**
- RSB <320 μm = **Contraindicado** (risco ectasia crítico)
- Q >+0.8 (muito oblato) = Geralmente **RLE preferível**
- HOA severas baseline = Enhancement topoguiado PRIMEIRO
