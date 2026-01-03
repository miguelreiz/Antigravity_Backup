# Infográfico 13.3: Árvore Decisão - Triagem Inicial

```mermaid
flowchart TD
    A["Paciente: 'Quero eliminar<br/>óculos de leitura'"] --> B{IDADE?}
    
    B -->|< 40 anos| C[RECUSAR<br/>Sem presbiopia real]
    B -->|≥ 40 anos| D{ADD<br/>NECESSÁRIA?}
    
    D -->|< +1.00 D| E[OBSERVAR<br/>Ainda consegue<br/>acomodar]
    D -->|≥ +1.00 D| F{EXPECTATIVAS?}
    
    F -->|REALISTAS<br/>Aceita trade-offs<br/>Óculos ocasionais OK| G[✅ CANDIDATO<br/>POTENCIAL<br/>→ Propedêutica]
    F -->|IRREALISTAS<br/>'Visão perfeita 20/15<br/>longe E J1 perto'| H[EDUCAR ou<br/>RECUSAR]
    
    G --> I[Prosseguir:<br/>Árvore 2<br/>Propedêutica]
    
    style C fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style E fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style G fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

**Exclusões Triagem:**
- ❌ Idade <40 (sem presbiopia verdadeira)
- ❌ Expectativas: "20/15 longe E J1 perto sem trade-offs"
- ❌ Profissões críticas (piloto comercial, neurocirurgião)
- ❌ Depressão severa não-tratada
