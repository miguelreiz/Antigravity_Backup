# Infográfico 1.4: Árvore de Decisão Cirúrgica - Síndrome do Cristalino Disfuncional (DLS)

```mermaid
graph TD
    %% Estilos e Definições
    classDef stage1 fill:#e6fffa,stroke:#00aa00,stroke-width:2px,color:#003300;
    classDef stage2 fill:#fffde7,stroke:#ffcc00,stroke-width:2px,color:#333300;
    classDef stage3 fill:#ffebee,stroke:#cc0000,stroke-width:2px,color:#330000;
    classDef decision fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:#00213b;
    classDef result fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#2a0033;

    Start[Paciente Presbita Sintomático<br/>(45-65 Anos)]:::decision --> Eval[Avaliação Diagnóstica:<br/>LOCS III, Pentacam, HD Analyzer]:::decision

    Eval --> S1{Estádio 1: Disfunção Precoce}
    Eval --> S2{Estádio 2: Disfunção Moderada}
    Eval --> S3{Estádio 3: Catarata/DLS Avançada}

    %% Estágio 1
    S1:::stage1 -- "Cristalino Claro<br/>OSI < 1.0<br/>Idade 45-55" --> Corneal[Correção Corneana Preferencial]:::result
    Corneal --> P1[PresbyLASIK / Custom-Q]
    Corneal --> P2[PRESBYOND]
    
    %% Estágio 2 (Zona Cinzenta)
    S2:::stage2 -- "Opacidade Leve<br/>OSI 1.0-2.5<br/>Age 50-60" --> Decision{Análise Multifatorial}:::decision
    Decision -- "Baixa Hipermetropia<br/>Sem Glare<br/>Deseja evitar intraocular" --> Corneal
    Decision -- "Alta Hipermetropia<br/>Glare Noturno<br/>Deseja solução definitiva" --> Lens[Troca de Lente Refrativa - RLE]:::result

    %% Estágio 3
    S3:::stage3 -- "Opacidade Significativa<br/>OSI > 2.5<br/>Perda de BCVA" --> Lens
    Lens --> L1[LIO Trifocal / EDOF]
    Lens --> L2[LIO Monofocal (Monovisão)]

    %% Detalhes Gráficos
    linkStyle default stroke:#333,stroke-width:1px;
```

**Legenda:**
*   **Estádio 1 (Verde):** Cristalino funcional, foco na córnea.
*   **Estádio 2 (Amarelo):** Zona de decisão personalizada.
*   **Estádio 3 (Vermelho):** Falha lenticular, troca mandatória.
