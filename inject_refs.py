import re

text = open('Chapter_2_Complete.md', 'r', encoding='utf-8').read()

replacements = [
    (r'cinco polinômios explicam 80% dos resultados clínicos em cirurgia de presbiopia:', r'cinco polinômios explicam 80% dos resultados clínicos em cirurgia de presbiopia: [7]'),
    (r'Lentes como ReSTOR e Tecnis Multifocal já tinham 10\+ anos de uso com zonas concêntricas comprovadas\.', r'Lentes como ReSTOR e Tecnis Multifocal já tinham 10+ anos de uso com zonas concêntricas comprovadas. [10]'),
    (r'causa instabilidade biomecânica \(regressão epitelial severa\)', r'causa instabilidade biomecânica (regressão epitelial severa) [11]'),
    (r'muitos topógrafos 2005-2010 NÃO mediam Q confiável\)', r'muitos topógrafos 2005-2010 NÃO mediam Q confiável) [12]'),
    (r'seguindo a ordem radial do polinómio de Zernike\.', r'seguindo a ordem radial do polinómio de Zernike. [13]'),
    (r'Positiva \(shift de \~\+0\.30 a \+0\.60 μm\)', r'Positiva (shift de ~+0.30 a +0.60 μm) [14]'),
    (r'SA positiva ligeira \(fisiológica\)', r'SA positiva ligeira (fisiológica) [15]'),
    (r'O RMS é a "nota final" da qualidade óptica:', r'O RMS é a "nota final" da qualidade óptica: [16]'),
    (r'fator de asfericidade \(Q\), também conhecido como', r'fator de asfericidade (Q), também conhecido como [17]'),
    (r'Considerar topography-guided ablation antes de presbiopia', r'Considerar topography-guided ablation antes de presbiopia [18]')
]

for p, r_str in replacements:
    text = re.sub(p, r_str, text, count=1)

open('Chapter_2_Complete.md', 'w', encoding='utf-8').write(text)
print('References injected.')
