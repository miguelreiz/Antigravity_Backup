# Infográfico 13.1: Master Decision Pathway

```mermaid
flowchart TD
    A[Paciente Presbiópico<br/>Consulta Inicial] --> B{TRIAGEM INICIAL<br/>Idade, Add, Expectativas}
    B -->|Candidato<br/>Potencial| C[PROPEDÊUTICA COMPLETA<br/>Capítulo 3]
    B -->|Não-Candidato| Z1[Óculos/LC]
    
    C --> D{CÓRNEA<br/>ADEQUADA?}
    D -->|Sim| E[AVALIAÇÃO CRISTALINO<br/>DLS, OSI, Densitometria]
    D -->|Não<br/>BAD-D >1.6<br/>Olho Seco Severo| Z2[Contraindicado<br/>ou RLE]
    
    E --> F{Decisão<br/>Cirúrgica}
    F -->|Corneana<br/>Favorece| G[QUAL TÉCNICA?<br/>Capítulos 4-8]
    F -->|RLE<br/>Favorece| H[RLE<br/>Capítulo 12]
    
    G --> I{Plataforma/<br/>Add/Pupila}
    I -->|Add ≤1.75D<br/>Pupila flex| J[Custom-Q ou<br/>PRESBYOND]
    I -->|Add >2.0D<br/>Pupila <6.5mm| K[PresbyMAX ou<br/>SUPRACOR]
    
    J --> L[CIRURGIA]
    K --> L
    H --> L
    
    L --> M[FOLLOW-UP &<br/>NEUROADAPTAÇÃO<br/>Capítulo 10]
    
    M --> N{Resultado<br/>12 meses}
    N -->|Sucesso<br/>~91%| O[ALTA]
    N -->|Complicação/<br/>Insatisfação| P[Gestão/Enhancement/<br/>Reversão<br/>Capítulo 11]
    
    style A fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style L fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Z1 fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Z2 fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#fff9c4,stroke:#f57f17,stroke-width:2px
```

**Descrição:** Fluxograma master consolidando todo o processo decisional desde consulta inicial até outcome final, integrando conhecimento dos 13 capítulos.

**Como Usar:**
- Este arquivo renderiza automaticamente no GitHub
- Para editar: https://mermaid.live (copie/cole o código acima)
- Exportar PNG: Use Mermaid Live Editor → Actions → PNG
