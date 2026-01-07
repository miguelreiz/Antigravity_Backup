# Infográfico 5.2: Fluxo de Decisão - Transferência de Algoritmo

**Objetivo Educacional:**
Um "Tradutor Universal" para aplicar a lógica PresbyCor em qualquer laser (Zeiss, Schwind, Nidek), não apenas Alcon.

---

## 1. Descrição Visual (Layout)

**Formato:** Fluxograma Vertical (Input -> Black Box -> Output).

### Bloco 1: O Paciente (Input)
*   Caixas de dados:
    *   **Q Pré-Operatório** (ex: -0.20).
    *   **Refração Alvo** (ex: Plano).
    *   **Pupila** (ex: 5.5mm).

### Bloco 2: A "Black Box" Matemática (O Processo)
*   **Fórmula Visível:**
    $$Z_4^0 (\mu m) = -0.5 \times \Delta Q$$
*   **Ação:** Conversão de "Fator Q" (Linguagem Alcon) para "Aberração Esférica" (Linguagem Universal/Zeiss).

### Bloco 3: O Output (Programação do Laser)
*   Três caminhos (Setas) para diferentes máquinas:
    *   **Caminho Alcon:** Input direto "Target Q = -0.80".
    *   **Caminho Zeiss (MEL 90):** Input "SA (c[4,0]) = -0.30 \mu m".
    *   **Caminho Schwind:** Input "Custom Corneal Wavefront" (Manipulação Zernike).

### Bloco 4: O "Fine Tuning" (Offset Miópico)
*   Alerta lateral: "**Regra de Ouro:** Adicionar sempre -0.50D a -0.75D de miopia (Micro-Monovisão) no olho não-dominante para potenciar o efeito."

---

## 2. Legenda Explicativa
"O algoritmo de Ghenassia é agnóstico ao hardware. Se o seu laser permite manipular aberração esférica, você pode realizar PresbyCor. A chave é a tradução da linguagem 'Q-Factor' para 'Zernike Z(4,0)'."
