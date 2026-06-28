import os
import pathlib
import re
import subprocess

# Paths
WORKSPACE = r"c:\Users\3D_OCT\Documents\Antigravity\Ice"
DEST_DIR = r"D:\ICE_Apresentacao"

pathlib.Path(WORKSPACE).mkdir(parents=True, exist_ok=True)
pathlib.Path(DEST_DIR).mkdir(parents=True, exist_ok=True)

PROJ_HTML = os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Ambrosio.html")
APRES_HTML = os.path.join(WORKSPACE, "apresentacao_ice_ambrosio.html")

PROJ_PDF = os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Ambrosio.pdf")
APRES_PDF = os.path.join(WORKSPACE, "ICE_Apresentacao_Ambrosio.pdf")

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

def spell_correct(text):
    # Orthographic corrections under Novo Acordo Ortográfico
    corrections = {
        r"\bco-autoria\b": "coautoria",
        r"\bCo-autoria\b": "Coautoria",
        r"\bco-autor\b": "coautor",
        r"\bCo-autor\b": "Coautor",
        r"\bco-investigadores\b": "coinvestigadores",
        r"\bCo-investigadores\b": "Coinvestigadores",
        r"\bco-investigador\b": "coinvestigador",
        r"\bCo-investigador\b": "Coinvestigador",
        r"\bacesso a base de dados\b": "acesso à base de dados",
        r"\bAcesso a base de dados\b": "Acesso à base de dados",
    }
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text)
    return text

# Write the updated HTML project document (without target article expansion or joint roadmap calls)
# We structure Section 8 as "Próximos Passos e Publicação Alvo" and remove other article cards.
# Also change "Colaborador Proposto" in meta to "Para Parecer Científico de".
HTML_PROJECT_CONTENT = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Projeto de Pesquisa — ICE · BrAIn 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400;1,600&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --navy:#0b1a2e;--navy2:#122240;--navy3:#1a3055;
  --blue:#1e6fa8;--blue2:#2892d7;--teal:#17a1a5;
  --gold:#c9a84c;--gold2:#e8c56e;
  --red:#c84b31;--green:#2d9e6b;
  --white:#f0f4f8;--gray:#7a92aa;--light:#dce8f5;
  --body:#1e2d42;
}
html{background:#e8edf4}
body{font-family:'Inter',sans-serif;background:#e8edf4;color:var(--body);line-height:1.72;font-size:14px;padding:40px 0 80px}

/* PAGE SHELL */
.page{
  width:210mm;max-width:900px;margin:0 auto;
  background:white;
  box-shadow:0 4px 40px rgba(0,0,0,.14);
  border-radius:4px;
  overflow:hidden;
}

/* HEADER BANNER */
.header{
  background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 45%,var(--navy3) 100%);
  padding:52px 56px 44px;
  position:relative;
  overflow:hidden;
}
.header::before{
  content:'';position:absolute;top:-60px;right:-60px;
  width:280px;height:280px;border-radius:50%;
  background:radial-gradient(circle,rgba(23,161,165,.18) 0%,transparent 70%);
}
.header::after{
  content:'';position:absolute;bottom:-40px;left:40%;
  width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,rgba(201,168,76,.1) 0%,transparent 70%);
}
.header-tag{
  font-size:10px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--teal);margin-bottom:14px;font-weight:500;
}
.header-title{
  font-family:'Lora',serif;
  font-size:26px;line-height:1.22;
  color:white;max-width:560px;margin-bottom:10px;font-weight:600;
}
.header-title em{color:var(--gold2);font-style:italic}
.header-sub{
  font-size:12.5px;color:rgba(220,232,245,.7);
  max-width:520px;margin-bottom:28px;line-height:1.55;
}
.header-meta{
  display:flex;gap:32px;flex-wrap:wrap;
  border-top:1px solid rgba(255,255,255,.1);
  padding-top:20px;margin-top:4px;
}
.meta-item{font-size:11px;color:rgba(220,232,245,.6)}
.meta-item strong{display:block;color:rgba(220,232,245,.95);font-size:12px;margin-bottom:2px}

/* BODY CONTENT */
.content{padding:48px 56px}

/* SECTION HEADERS */
.sec{margin-bottom:32px}
.sec-label{
  font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--teal);font-weight:600;margin-bottom:6px;
}
.sec-title{
  font-family:'Lora',serif;font-size:18px;color:var(--navy);
  font-weight:600;margin-bottom:14px;line-height:1.3;
  padding-bottom:10px;border-bottom:2px solid #eef2f7;
}
.sec-title em{color:var(--gold);font-style:italic}
p{color:#3a4f63;font-size:13.5px;margin-bottom:12px;line-height:1.72}
strong{color:var(--navy);font-weight:600}

/* CALLOUT BOX */
.callout{
  border-left:4px solid var(--gold);
  padding:16px 20px;margin:20px 0;
  background:#fdf9f0;border-radius:0 10px 10px 0;
}
.callout p{font-family:'Lora',serif;font-size:14.5px;color:#2a3a4a;font-style:italic;margin:0;line-height:1.6}
.callout cite{font-size:11px;color:var(--gray);display:block;margin-top:6px;font-style:normal;font-family:'Inter',sans-serif}

/* HYPOTHESIS BOX */
.hyp{
  background:linear-gradient(135deg,#f0f7ff,#e8f4fd);
  border:1.5px solid rgba(40,146,215,.2);
  border-radius:12px;padding:22px 24px;margin:20px 0;
}
.hyp-label{font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--blue2);font-weight:600;margin-bottom:8px}
.hyp-text{font-size:14px;color:var(--navy);line-height:1.6}

/* FORMULA BOX */
.formula-box{
  background:var(--navy);border-radius:12px;
  padding:24px 28px;margin:20px 0;
  display:flex;flex-direction:column;gap:10px;
}
.formula-title{font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--teal);font-weight:600}
.formula-eq{
  font-family:'Lora',serif;font-size:15px;
  color:white;line-height:1.7;
}
.formula-eq em{color:var(--gold2)}
.formula-note{font-size:11px;color:rgba(220,232,245,.6);line-height:1.5}

/* GRID CARDS */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:16px 0}
.g4{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin:16px 0}
.card{border-radius:10px;padding:18px;border:1px solid #e2eaf4}
.card-teal{background:#f0fbfb;border-color:rgba(23,161,165,.25);border-left:3px solid var(--teal)}
.card-gold{background:#fdf9f0;border-color:rgba(201,168,76,.25);border-left:3px solid var(--gold)}
.card-blue{background:#f0f7ff;border-color:rgba(40,146,215,.2);border-left:3px solid var(--blue2)}
.card-green{background:#f0faf5;border-color:rgba(45,158,107,.22);border-left:3px solid var(--green)}
.card-red{background:#fff5f3;border-color:rgba(200,75,49,.2);border-left:3px solid var(--red)}
.card-gray{background:#f6f9fc;border-color:#dde6f0}
.card-title{font-size:11.5px;font-weight:700;color:var(--navy);margin-bottom:7px;letter-spacing:.01em}
.card-text{font-size:12px;color:#4a5f73;line-height:1.6}

/* STAT NUMBERS */
.stat-num{font-size:28px;font-weight:700;color:var(--blue2);line-height:1;margin-bottom:4px}
.stat-label{font-size:11px;color:var(--gray);line-height:1.4}
.stat-card{background:#f6f9fc;border:1px solid #dde6f0;border-radius:10px;padding:16px 14px;text-align:center}

/* TABLE */
.tbl{width:100%;border-collapse:collapse;font-size:12.5px;margin:14px 0}
.tbl th{background:#f0f4fa;color:var(--gray);font-weight:600;padding:9px 12px;text-align:left;border-bottom:1.5px solid #dde6f0;font-size:11px;text-transform:uppercase;letter-spacing:.07em}
.tbl td{padding:9px 12px;color:#3a4f63;border-bottom:1px solid #eef2f7;vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.tbl tr:hover td{background:#fafcff}

/* BADGE */
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;letter-spacing:.03em}
.b-green{background:rgba(45,158,107,.12);color:#1a7a4a;border:1px solid rgba(45,158,107,.25)}
.b-gold{background:rgba(201,168,76,.14);color:#8a6a10;border:1px solid rgba(201,168,76,.28)}
.b-red{background:rgba(200,75,49,.1);color:#9a2f1a;border:1px solid rgba(200,75,49,.22)}
.b-blue{background:rgba(40,146,215,.1);color:#1a55a0;border:1px solid rgba(40,146,215,.22)}
.b-teal{background:rgba(23,161,165,.1);color:#0a6e72;border:1px solid rgba(23,161,165,.22)}

/* TIMELINE */
.timeline{display:flex;flex-direction:column;gap:0;margin:16px 0}
.tl-item{display:flex;gap:16px;position:relative}
.tl-item::before{content:'';position:absolute;left:15px;top:30px;bottom:-4px;width:2px;background:#eef2f7}
.tl-item:last-child::before{display:none}
.tl-dot{width:32px;height:32px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid}
.tl-d1{background:#f0f7ff;color:var(--blue2);border-color:rgba(40,146,215,.4)}
.tl-d2{background:#f0fbfb;color:var(--teal);border-color:rgba(23,161,165,.4)}
.tl-d3{background:#fdf9f0;color:#8a6a10;border-color:rgba(201,168,76,.4)}
.tl-d4{background:#f0faf5;color:#1a7a4a;border-color:rgba(45,158,107,.4)}
.tl-body{padding-bottom:20px;flex:1}
.tl-period{font-size:10.5px;color:var(--teal);font-weight:600;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}
.tl-title{font-size:13px;font-weight:600;color:var(--navy);margin-bottom:4px}
.tl-desc{font-size:12px;color:#4a5f73;line-height:1.55}

/* ALERT */
.alert{border-radius:10px;padding:14px 18px;margin:16px 0;font-size:12.5px}
.a-note{background:#f0f7ff;border:1px solid rgba(40,146,215,.2);color:#1a3a6a}
.a-warn{background:#fff8f0;border:1px solid rgba(200,100,30,.25);color:#6a3a10}
.a-tip{background:#f0faf5;border:1px solid rgba(45,158,107,.22);color:#1a4a30}

/* DIVIDER */
.div{height:1px;background:#eef2f7;margin:32px 0}

/* SIGNATURE BLOCK */
.sig-block{
  background:var(--navy);color:white;
  border-radius:12px;padding:28px 32px;margin-top:32px;
  display:flex;justify-content:space-between;align-items:flex-start;
  flex-wrap:wrap;gap:24px;
}
.sig-left .sig-name{font-family:'Lora',serif;font-size:17px;font-weight:600;color:white;margin-bottom:4px}
.sig-left .sig-role{font-size:11.5px;color:rgba(220,232,245,.6);line-height:1.5}
.sig-right{text-align:right}
.sig-right .sig-label{font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--teal);margin-bottom:6px}
.sig-right .sig-contact{font-size:12px;color:rgba(220,232,245,.8);line-height:1.6}
.sig-badge{
  display:inline-block;background:rgba(201,168,76,.15);
  border:1px solid rgba(201,168,76,.3);
  color:var(--gold2);padding:4px 12px;border-radius:20px;
  font-size:10px;font-weight:600;letter-spacing:.08em;
  margin-top:8px;
}

/* PAGE BREAK HINTS */
@media print{
  body{background:white;padding:0}
  .page{box-shadow:none;border-radius:0;width:100%;max-width:100%}
  .sec{page-break-inside:avoid}
  .pb{page-break-before:always}
}
</style>
</head>
<body>
<div class="page">

<!-- HEADER -->
<div class="header">
  <div class="header-tag">Projeto de Pesquisa · BrAIn / Rio de Janeiro · Junho 2026</div>
  <div class="header-title">
    Índice de Coerência do Eixo (<em>ICE</em>):<br>
    Um preditor pré-operatório de resultado visual<br>no implante de anel intraestromal
  </div>
  <div class="header-sub">
    Documento científico detalhado para avaliação de relevância clínica e validação do protocolo retrospectivo/prospectivo em ceratocone.
  </div>
  <div class="header-meta">
    <div class="meta-item"><strong>Investigador Principal</strong>Miguel Reis — Biomecânica Corneana Computacional</div>
    <div class="meta-item"><strong>Destinado para Parecer de</strong>Prof. Dr. Renato Ambrósio Jr. — BrAIn</div>
    <div class="meta-item"><strong>Data de Submissão</strong>Junho 2026</div>
    <div class="meta-item"><strong>Objetivo do Envio</strong>Apresentação e Parecer de Relevância Científica</div>
  </div>
</div>

<!-- CONTENT -->
<div class="content">

<!-- 1. SUMÁRIO EXECUTIVO -->
<div class="sec">
  <div class="sec-label">Seção 1</div>
  <div class="sec-title">Sumário <em>Executivo</em></div>

  <div class="callout">
    <p>O Kmax informa a altura do incêndio. O ICE informa se a saída de emergência ainda está alinhada.</p>
    <cite>Analogia central do projeto: gravidade estrutural e coerência funcional são dimensões independentes.</cite>
  </div>

  <p>O <strong>Índice de Coerência do Eixo (ICE)</strong> é um índice pré-operatório desenvolvido para responder a uma pergunta que os índices existentes não respondem: <em>se o anel intraestromal corrigir a curvatura, o sistema visual deste paciente conseguirá converter essa melhora geométrica em ganho visual real?</em></p>

  <p>O paradoxo que motivou o projeto é documentado clinicamente: pacientes com Kmax idêntico, mesma paquimetria, mesmo estadiamento — e respostas visuais radicalmente diferentes ao anel. A hipótese do ICE é que a causa dessa variabilidade está no <strong>desacoplamento entre três eixos ópticos</strong>: o eixo de maior curvatura (topografia), o eixo do cilindro manifesto (refração) e o eixo da aberração comática (aberrometria). Quando esses três eixos apontam em direções diferentes, a melhora geométrica produzida pelo anel se fragmenta ao longo do sistema óptico e não se integra em ganho de acuidade.</p>

  <div class="g4">
    <div class="stat-card"><div class="stat-num">443</div><div class="stat-label">pares clínicos<br>Pentacam + OCT</div></div>
    <div class="stat-card"><div class="stat-num">660</div><div class="stat-label">perfis de curvatura<br>SPR Scheimpflug</div></div>
    <div class="stat-card"><div class="stat-num">24</div><div class="stat-label">modelos FEM<br>anisotrópicos HGO</div></div>
    <div class="stat-card"><div class="stat-num" style="font-size:22px">0,82</div><div class="stat-label">AUC ROC retrospectiva<br>predição ganho ≥3 linhas</div></div>
  </div>
</div>

<div class="div"></div>

<!-- 2. PROBLEMA E HIPÓTESE -->
<div class="sec">
  <div class="sec-label">Seção 2</div>
  <div class="sec-title">Problema e <em>Hipótese</em></div>

  <p>A literatura de ICRS em ceratocone documenta consistentemente uma variabilidade clínica que os nomogramas atuais não explicam. Estudos com mais de 300 olhos mostram que, entre pacientes operados com indicação tecnicamente adequada, cerca de <strong>27% obtêm ganho de BCVA inferior a duas linhas</strong>, mesmo com melhora objetiva da topografia. Essa dissociação entre resultado topográfico e resultado visual é o problema central que o ICE busca predizer.</p>

  <div class="hyp">
    <div class="hyp-label">Hipótese principal</div>
    <div class="hyp-text">O grau de coerência entre o eixo topográfico, o eixo refrativo e o eixo comático — quantificado pelo ICE — é um preditor independente do ganho de BCVA após ICRS, com desempenho discriminativo superior ao Kmax isolado (AUC > 0,75 no estudo prospectivo).</div>
  </div>

  <div class="g2">
    <div>
      <p style="font-size:12.5px"><strong>Por que o Kmax é insuficiente</strong></p>
      <p>O Kmax mede a magnitude da deformação corneana, mas não mede como essa deformação se propaga pelo sistema óptico. Dois olhos com Kmax 62 D podem ter:</p>
      <ul style="margin:8px 0 12px 18px;font-size:12.5px;color:#3a4f63;line-height:1.7">
        <li>Eixo topográfico e cilindro manifesto coincidentes (<strong>ICE alto</strong>) — sistema coerente, ganho esperado</li>
        <li>Eixo topográfico, cilindro e coma em meridianos diferentes (<strong>ICE baixo</strong>) — sistema fragmentado, ganho improvável</li>
      </ul>
    </div>
    <div>
      <p style="font-size:12.5px"><strong>O achado que sustenta a hipótese</strong></p>
      <p>Na análise de 660 perfis SPR, a correlação espacial entre os ápices da superfície anterior e posterior da córnea foi <strong>r = 0,028 (p = 0,50)</strong> — estatisticamente nula. O ápice posterior está, em média, 2,6 mm mais periférico, e em posição angular diferente. Isso significa que o eixo de referência convencional (K-steep) pode estar sistematicamente deslocado em relação ao eixo real do cone.</p>
    </div>
  </div>
</div>

<div class="div"></div>

<!-- 3. O ÍNDICE ICE -->
<div class="sec">
  <div class="sec-label">Seção 3</div>
  <div class="sec-title">O Índice ICE — <em>Definição Formal</em></div>

  <p>O ICE é um índice contínuo entre 0 e 1, produto de três componentes independentes, cada um capturando uma dimensão distinta da coerência óptico-geométrica.</p>

  <div class="formula-box">
    <div class="formula-title">Fórmula ICE 2.0 — Triádico</div>
    <div class="formula-eq">
      ICE = <em>ICE_astig</em> × <em>Optical_coherence</em> × <em>ICE_axis_triad</em>
    </div>
    <div class="formula-eq" style="font-size:13px;margin-top:4px;opacity:.85">
      = [1 − |Astig_T − Cyl| / (Astig_T + Cyl)]  ×  [LOA / (LOA + HOA)]  ×  [1 − D_max / 90°]
    </div>
    <div class="formula-note" style="margin-top:8px">
      D_max = max( |θ_topo − θ_cyl|, |θ_topo − θ_coma|, |θ_cyl − θ_coma| ) · 
      Astig_T = astigmatismo topográfico · Cyl = cilindro manifesto · 
      LOA = aberrações de baixa ordem · HOA = aberrações de alta ordem
    </div>
  </div>

  <div class="g3">
    <div class="card card-teal">
      <div class="card-title">Bloco 1 — Coerência de magnitude</div>
      <div class="card-text">Compara a magnitude do astigmatismo topográfico com o cilindro manifesto. Dissociação entre os dois indica que o sistema refrativo não está "lendo" o que a córnea impõe — frequentemente por adaptação neural ou erro de medida.</div>
    </div>
    <div class="card card-gold">
      <div class="card-title">Bloco 2 — Pureza óptica</div>
      <div class="card-text">Razão entre aberrações de baixa ordem (corrigíveis) e totais. Quando aberrações de alta ordem dominam, halos e imagens duplas persistem mesmo com boa refração manifesta — o ganho de BCVA é estruturalmente limitado.</div>
    </div>
    <div class="card card-red">
      <div class="card-title">Bloco 3 — Coerência angular triádica</div>
      <div class="card-text">Maior discordância angular entre os três eixos (topográfico, refrativo, comático). Eixos a &lt;15°: alta coerência. A &gt;30°: o anel posicionado no K-steep pode aumentar o coma ao invés de reduzi-lo.</div>
    </div>
  </div>

  <table class="tbl" style="margin-top:8px">
    <thead><tr><th>Faixa ICE</th><th>Classificação</th><th>Interpretação</th><th>Conduta proposta</th></tr></thead>
    <tbody>
      <tr><td><strong style="color:#1a7a4a">≥ 0,65</strong></td><td><span class="badge b-green">Tipo 1 — Coerente</span></td><td>Eixos alinhados, HOA controladas, magnitude concordante</td><td>Operar. Maximizar VEsférico. Prometer ganho objetivo.</td></tr>
      <tr><td><strong style="color:#8a6a10">0,50 – 0,64</strong></td><td><span class="badge b-gold">Zona cinzenta</span></td><td>Coerência parcial; pelo menos um bloco comprometido</td><td>Operar com cautela. Expectativa parcial com o paciente.</td></tr>
      <tr><td><strong style="color:#9a2f1a">&lt; 0,50</strong></td><td><span class="badge b-red">Tipo 2 — Discordante</span></td><td>Eixos fragmentados, HOA dominantes ou magnitude dissociada</td><td>Redefinir objetivo. Considerar CXL, lente escleral ou anel tectônico.</td></tr>
    </tbody>
  </table>
</div>

<div class="div"></div>

<!-- 4. FUNDAMENTO BIOMECÂNICO -->
<div class="sec">
  <div class="sec-label">Seção 4</div>
  <div class="sec-title">Fundamento <em>Biomecânico</em> — Modelos FEM</div>

  <p>Para validar a premissa física do ICE — de que o desalinhamento entre o eixo do anel e o eixo real do cone reduz a eficácia da correção — foram desenvolvidos 24 modelos de elementos finitos utilizando o software FEBio com material anisotrópico Holzapfel-Gasser-Ogden (HGO), que reproduz a organização fibrilar do estroma.</p>

  <div class="g2">
    <div class="card card-blue">
      <div class="card-title">Resultado principal — FEM</div>
      <div class="card-text">O anel alinhado ao eixo principal do cone gera resposta apical <strong>1,24× mais eficiente</strong> do que o anel desalinhado em 30°. O desalinhamento de 30° reduz a eficácia apical em ~19%, com redistribuição da tensão para o meridiano perpendicular — potencialmente agravando o coma ao invés de reduzi-lo.</div>
    </div>
    <div class="card card-green">
      <div class="card-title">Implicação clínica direta</div>
      <div class="card-text">ICE alto significa que o eixo convencional de referência (K-steep) e o eixo real do cone estão alinhados — o anel posicionado pelo nomograma padrão está no campo de força correto. ICE baixo significa desperdício mecânico: parte da força corretiva age no meridiano errado.</div>
    </div>
  </div>

  <div class="alert a-note">
    <strong>Dissociação anterior-posterior (achado original):</strong> Na análise de 660 olhos, a correlação entre posição do ápice anterior e posterior foi r = 0,028 (p = 0,50 — nula). Isso significa que o ápice anterior — ponto de referência para o K-steep — não prediz a posição do ápice posterior, que é o verdadeiro motor biomecânico do ceratocone. O ICE captura parte dessa dissociação ao incluir o eixo comático, que reflete aberrações produzidas pela superfície posterior.
  </div>
</div>

<div class="div"></div>

<!-- 5. DADOS PRELIMINARES -->
<div class="sec">
  <div class="sec-label">Seção 5</div>
  <div class="sec-title">Dados Preliminares <em>(Retrospectivo)</em></div>

  <p>A análise retrospectiva utilizou dados de 8 estudos publicados entre 2013 e 2024, totalizando <strong>300 olhos com ICRS</strong>, recodificados segundo os critérios ICE a partir dos dados disponibilizados nos artigos. Os grupos foram definidos pelo ICE calculado retroativamente com os Blocos 1 e 2 (sem aberrometria — ICE biádico).</p>

  <div class="g3" style="margin-bottom:20px">
    <div class="stat-card">
      <div class="stat-num" style="color:var(--green)">+4,2</div>
      <div class="stat-label">linhas BCVA médio<br>ICE alto (n=118)</div>
    </div>
    <div class="stat-card">
      <div class="stat-num" style="color:#8a6a10">+2,8</div>
      <div class="stat-label">linhas BCVA médio<br>ICE moderado (n=102)</div>
    </div>
    <div class="stat-card">
      <div class="stat-num" style="color:var(--red)">+1,6</div>
      <div class="stat-label">linhas BCVA médio<br>ICE baixo (n=80)</div>
    </div>
  </div>

  <table class="tbl">
    <thead><tr><th>Métrica</th><th>AUC (predição ganho ≥ 3 linhas)</th><th>IC 95%</th><th>Comparação ICE</th></tr></thead>
    <tbody>
      <tr><td><strong>ICE</strong></td><td><strong style="color:var(--green)">0,82</strong></td><td>0,76 – 0,87</td><td>—</td></tr>
      <tr><td>Kmax</td><td>0,68</td><td>0,61 – 0,75</td><td>DeLong p = 0,012</td></tr>
      <tr><td>Paquimetria mínima</td><td>0,64</td><td>0,57 – 0,71</td><td>DeLong p = 0,004</td></tr>
      <tr><td>Estadiamento Amsler-Krumeich</td><td>0,61</td><td>0,54 – 0,68</td><td>DeLong p &lt; 0,001</td></tr>
    </tbody>
  </table>

  <div class="alert a-warn" style="margin-top:8px">
    <strong>Limitação crítica:</strong> Estes dados são retroativos e baseados na reconstrução do ICE a partir de publicações de terceiros. O Bloco 3 (θ_coma) não pôde ser calculado por ausência de dados de aberrometria na maioria dos estudos — o ICE utilizado é biádico (Blocos 1 e 2). A AUC de 0,82 deve ser interpretada como estimativa conservadora do potencial do índice triádico completo.
  </div>
</div>

<div class="div pb"></div>

<!-- 6. PROTOCOLO PROSPECTIVO -->
<div class="sec">
  <div class="sec-label">Seção 6</div>
  <div class="sec-title">Protocolo de Estudo <em>Prospectivo Proposto</em></div>

  <div class="hyp">
    <div class="hyp-label">Delineamento</div>
    <div class="hyp-text">Estudo de coorte prospectivo, multicêntrico, com cegamento do cirurgião para o resultado do ICE até o desfecho primário. Período de acompanhamento: 6 meses pós-operatório.</div>
  </div>

  <div class="g2">
    <div>
      <p style="font-size:12.5px;font-weight:600;color:var(--navy)">Critérios de inclusão</p>
      <ul style="margin:6px 0 14px 16px;font-size:12.5px;color:#3a4f63;line-height:1.7">
        <li>Ceratocone confirmado (BAD-D ≥ 1,6 ou Kmax ≥ 47,2 D)</li>
        <li>Candidato a ICRS por indicação clínica independente</li>
        <li>CDVA ≤ 20/40 com melhor correção</li>
        <li>Idade ≥ 18 anos</li>
        <li>Dados disponíveis: Pentacam + aberrometria + refração manifesta</li>
      </ul>
      <p style="font-size:12.5px;font-weight:600;color:var(--navy)">Critérios de exclusão</p>
      <ul style="margin:6px 0 0 16px;font-size:12.5px;color:#3a4f63;line-height:1.7">
        <li>Cirurgia corneana prévia</li>
        <li>Paquimetria mínima &lt; 350 µm</li>
        <li>Doença ocular associada (glaucoma, uveíte)</li>
        <li>CXL simultâneo (grupo separado, análise secundária)</li>
      </ul>
    </div>
    <div>
      <p style="font-size:12.5px;font-weight:600;color:var(--navy)">Tamanho amostral</p>
      <table class="tbl" style="margin-bottom:14px">
        <thead><tr><th>Parâmetro</th><th>Valor</th></tr></thead>
        <tbody>
          <tr><td>AUC esperada (ICE triádico)</td><td>0,82</td></tr>
          <tr><td>AUC nula (H0)</td><td>0,70</td></tr>
          <tr><td>Poder estatístico (1−β)</td><td>80%</td></tr>
          <tr><td>α bilateral</td><td>0,05</td></tr>
          <tr><td><strong>N necessário</strong></td><td><strong>168 olhos</strong></td></tr>
          <tr><td>N proposto (+ 20% perdas)</td><td><strong>202 olhos</strong></td></tr>
        </tbody>
      </table>
      <div class="alert a-tip"><strong>Viabilidade:</strong> Com o volume do BrAIn e centros parceiros, N=202 é alcançável em 12–18 meses.</div>
    </div>
  </div>

  <p style="font-size:12.5px;font-weight:600;color:var(--navy);margin-bottom:8px">Desfechos</p>
  <table class="tbl">
    <thead><tr><th>Desfecho</th><th>Medida</th><th>Momento</th></tr></thead>
    <tbody>
      <tr><td><strong>Primário</strong></td><td>Ganho de BCVA ≥ 3 linhas Snellen (predito pelo ICE)</td><td>6 meses</td></tr>
      <tr><td>Secundário 1</td><td>Redução de Kmax ≥ 2 D</td><td>3 e 6 meses</td></tr>
      <tr><td>Secundário 2</td><td>Variação de coma RMS</td><td>6 meses</td></tr>
      <tr><td>Secundário 3</td><td>Satisfação subjetiva (VFQ-25)</td><td>6 meses</td></tr>
      <tr><td>Secundário 4</td><td>Necessidade de explante ou reposicionamento</td><td>12 meses</td></tr>
    </tbody>
  </table>
</div>

<div class="div"></div>

<!-- 7. CRONOGRAMA -->
<div class="sec">
  <div class="sec-label">Seção 7</div>
  <div class="sec-title">Cronograma <em>Proposto</em></div>

  <div class="timeline">
    <div class="tl-item">
      <div class="tl-dot tl-d1">M0</div>
      <div class="tl-body">
        <div class="tl-period">Mês 0–2 · Preparação</div>
        <div class="tl-title">Cálculo ICE retrospectivo + calibração da fórmula</div>
        <div class="tl-desc">Calcular ICE biádico nos 443 pares disponíveis. Ajustar limiares de classificação com dados locais. Desenvolver planilha/ferramenta de cálculo automático a partir do export Pentacam.</div>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot tl-d2">M2</div>
      <div class="tl-body">
        <div class="tl-period">Mês 2–4 · Protocolo e aprovação</div>
        <div class="tl-title">Submissão ao CEP + treinamento dos centros</div>
        <div class="tl-desc">Elaborar protocolo formal com coinvestigadores. Submeter ao Comitê de Ética. Treinar equipe de coleta (Pentacam + aberrômetro + refração padronizada). Definir SOP de cegamento.</div>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot tl-d3">M4</div>
      <div class="tl-body">
        <div class="tl-period">Mês 4–18 · Coleta de dados</div>
        <div class="tl-title">Recrutamento e seguimento prospectivo</div>
        <div class="tl-desc">Meta: 202 olhos em 14 meses. Avaliação pré-operatória (ICE calculado e selado), cirurgia por indicação clínica padrão, avaliação 1m / 3m / 6m com equipe diferente do calculador do ICE.</div>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot tl-d4">M18</div>
      <div class="tl-body">
        <div class="tl-period">Mês 18–22 · Análise e publicação</div>
        <div class="tl-title">Análise estatística, escrita e submissão</div>
        <div class="tl-desc">Análise ROC primária. Regressão logística multivariada. Curvas Kaplan-Meier para desfechos secundários. Submissão ao <em>Journal of Refractive Surgery</em> ou <em>Cornea</em>.</div>
      </div>
    </div>
  </div>
</div>

<div class="div"></div>

<!-- 8. VALIDAÇÃO E PUBLICAÇÃO ALVO -->
<div class="sec">
  <div class="sec-label">Seção 8</div>
  <div class="sec-title">Recursos Desenvolvidos e <em>Publicação Alvo</em></div>

  <p>Este projeto visa consolidar a validação do índice ICE através do protocolo prospectivo apresentado. Os recursos e resultados já desenvolvidos estão estruturados para fundamentar uma publicação científica.</p>

  <div class="g2">
    <div class="card card-gold">
      <div class="card-title">Recursos e Dados já Desenvolvidos</div>
      <div class="card-text">
        <ul style="margin-left:14px;line-height:1.8;font-size:12px">
          <li>Dados retrospectivos: 443 pares Pentacam/OCT Triton consolidados</li>
          <li>660 curvaturas SPR analisadas (evidência da dissociação A-P)</li>
          <li>24 modelos FEM HGO rodados e validados no FEBio</li>
          <li>Fórmula ICE 2.0 implementada e rotina de cálculo automatizada</li>
          <li>Revisão sistemática concluída de 8 estudos clínicos de base</li>
          <li>Rascunho inicial do artigo e material complementar estruturados</li>
        </ul>
      </div>
    </div>
    <div class="card card-blue">
      <div class="card-title">Requisitos Técnicos para Validação</div>
      <div class="card-text">
        <ul style="margin-left:14px;line-height:1.8;font-size:12px">
          <li>Coorte prospectiva com exames completos pré e pós-operatórios</li>
          <li>Dados de aberrometria por rastreamento de raios (Bloco 3)</li>
          <li>Acompanhamento clínico padronizado aos 6 meses de BCVA</li>
          <li>Cegamento estrito da equipe de refração pós-operatória</li>
          <li>Análise estatística ROC para redefinição final de limiares</li>
          <li>Integração com dados adicionais (TBI e BAD-D) como covariáveis</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="card card-gray" style="margin-top:12px">
    <div class="card-title">Publicação Científica Alvo (Artigo Principal)</div>
    <div class="card-text">
      <strong>Veículo:</strong> <em>Journal of Refractive Surgery</em> ou <em>Cornea</em><br>
      <strong>Título Proposto:</strong> "Validação prospectiva do Índice de Coerência do Eixo (ICE) como preditor de ganho visual após implante de anel intraestromal em ceratocone".<br>
      <strong>Escopo:</strong> Apresentar a fundamentação biofísica do índice (SPR/FEM), calibração retrospectiva da fórmula (AUC 0,82) e comprovação prospectiva de acurácia discriminativa a 6 meses.
    </div>
  </div>

  <div class="alert a-tip" style="margin-top:14px">
    <strong>Análise Retrospectiva Piloto:</strong> Os dados retrospectivos fundamentais (curvaturas Pentacam, eixos ópticos e refração pré e pós) para calibração do ICE biádico piloto podem ser estruturados diretamente a partir de bases de dados consolidadas existentes de pacientes já submetidos a implantes de anel.
  </div>
</div>

<div class="div"></div>

<!-- 9. POSIÇÃO HONESTA / LIMITAÇÕES -->
<div class="sec">
  <div class="sec-label">Seção 9</div>
  <div class="sec-title">Posição Honesta — <em>Limitações e Incertezas</em></div>

  <table class="tbl">
    <thead><tr><th>Limitação</th><th>Status</th><th>Mitigação</th></tr></thead>
    <tbody>
      <tr><td>AUC baseada em dados retrospectivos e biádicos</td><td><span class="badge b-gold">Parcial</span></td><td>Estudo prospectivo com ICE triádico completo</td></tr>
      <tr><td>θ_coma ausente na fórmula atual (dados limitados)</td><td><span class="badge b-red">Pendente</span></td><td>Inclusão de aberrometria sistemática no protocolo prospectivo</td></tr>
      <tr><td>ICE-score (0–1) e ICE-min (°) não formalizados como métricas distintas</td><td><span class="badge b-gold">Em revisão</span></td><td>Artigo metodológico separado define ambos</td></tr>
      <tr><td>Limiares (0,50 / 0,65) derivados de dados de terceiros</td><td><span class="badge b-red">Provisório</span></td><td>Análise ROC primária do estudo prospectivo redefine</td></tr>
      <tr><td>Modelos FEM com geometria simplificada</td><td><span class="badge b-blue">Robusto</span></td><td>24 modelos com variação de parâmetros; achado 1,24× consistente</td></tr>
      <tr><td>Dissociação A-P ainda não publicada</td><td><span class="badge b-teal">Pronto</span></td><td>Dados completos, análise finalizada, rascunho disponível</td></tr>
    </tbody>
  </table>

  <div class="alert a-note" style="margin-top:8px">
    O ICE é, neste momento, uma <strong>hipótese biofisicamente fundamentada com suporte retrospectivo moderado</strong>. Não é um índice clínico validado. A presente proposta destina-se à avaliação crítica de relevância científica por parte do Prof. Dr. Renato Ambrósio Jr., com vistas a validar o potencial biomédico e clínico do protocolo apresentado.
  </div>
</div>

<div class="div"></div>

<!-- ASSINATURA -->
<div class="sig-block">
  <div class="sig-left">
    <div class="sig-name">Miguel Reis</div>
    <div class="sig-role">
      Biomecânica Corneana Computacional<br>
      Projeto AVBC-ICRS · Junho 2026
    </div>
    <div class="sig-badge">ICE — Índice de Coerência do Eixo</div>
  </div>
  <div class="sig-right">
    <div class="sig-label">Destinatário da Avaliação</div>
    <div class="sig-contact">
      Prof. Dr. Renato Ambrósio Jr.<br>
      BrAIn — Rio de Janeiro<br>
      Para Avaliação de Relevância Científica
    </div>
  </div>
</div>

</div><!-- /content -->
</div><!-- /page -->
</body>
</html>"""

# Generate updated Markdown content (using raw string, updated to match Section 8 and recipient tone)
MARKDOWN_PROJECT_CONTENT = r"""# Índice de Coerência do Eixo (ICE): Um preditor pré-operatório de resultado visual no implante de anel intraestromal

**Projeto de Pesquisa · BrAIn / Rio de Janeiro · Junho 2026**  
**Projeto de pesquisa de validação do ICE**  
*Fundamentada em 443 pares clínicos, 660 perfis de curvatura SPR e 24 modelos de elementos finitos.*

---

### Metadados do Projeto
* **Investigador Principal:** Miguel Reis — Biomecânica Corneana Computacional
* **Destinatário da Avaliação:** Prof. Dr. Renato Ambrósio Jr. — BrAIn
* **Data de Submissão:** Junho 2026
* **Objetivo:** Apresentação do projeto para avaliação de relevância científica e viabilidade do protocolo.

---

## Seção 1: Sumário Executivo

> **Analogia Central:** "O Kmax informa a altura do incêndio. O ICE informa se a saída de emergência ainda está alinhada."  
> *Gravidade estrutural e coerência funcional são dimensões independentes.*

O **Índice de Coerência do Eixo (ICE)** é um índice pré-operatório desenvolvido para responder a uma pergunta que os índices existentes não respondem: *se o anel intraestromal corrigir a curvatura, o sistema visual deste paciente conseguirá converter essa melhora geométrica em ganho visual real?*

O paradoxo que motivou o projeto é documentado clinicamente: pacientes com Kmax idêntico, mesma paquimetria, mesmo estadiamento — e respostas visuais radicalmente diferentes ao anel. A hipótese do ICE é que a causa dessa variabilidade está no **desacoplamento entre três eixos ópticos**: o eixo de maior curvatura (topografia), o eixo do cilindro manifesto (refração) e o eixo da aberração comática (aberrometria). Quando esses três eixos apontam em direções diferentes, a melhora geométrica produzida pelo anel se fragmenta ao longo do sistema óptico e não se integra em ganho de acuidade.

### Indicadores Base
* **443** pares clínicos (Pentacam + OCT Triton)
* **660** perfis de curvatura (SPR Scheimpflug)
* **24** modelos de elementos finitos (anisotrópicos HGO)
* **0,82** de AUC ROC retrospectiva na predição de ganho $\ge 3$ linhas de BCVA

---

## Seção 2: Problema e Hipótese

A literatura de ICRS em ceratocone documenta consistentemente uma variabilidade clínica que os nomogramas atuais não explicam. Estudos com mais de 300 olhos mostram que, entre pacientes operados com indicação tecnicamente adequada, cerca de **27% obtêm ganho de BCVA inferior a duas linhas**, mesmo com melhora objetiva da topografia. Essa dissociação entre resultado topográfico e resultado visual é o problema central que o ICE busca predizer.

> **Hipótese Principal:**  
> O grau de coerência entre o eixo topográfico, o eixo refrativo e o eixo comático — quantificado pelo ICE — é um preditor independente do ganho de BCVA após ICRS, com desempenho discriminativo superior ao Kmax isolado (AUC > 0,75 no estudo prospectivo).

### Por que o Kmax é insuficiente?
O Kmax mede a magnitude da deformação corneana, mas não mede como essa deformação se propaga pelo sistema óptico. Dois olhos com Kmax de 62 D podem ter:
1. **Eixo topográfico e cilindro manifesto coincidentes (ICE alto):** sistema coerente, ganho esperado.
2. **Eixo topográfico, cilindro e coma em meridianos diferentes (ICE baixo):** sistema fragmentado, ganho improvável.

### O achado que sustenta a hipótese
Na análise de 660 perfis SPR, a correlação espacial entre os ápices da superfície anterior e posterior da córnea foi de $r = 0,028$ ($p = 0,50$) — estatisticamente nula. O ápice posterior está, em média, 2,6 mm mais periférico, e em posição angular diferente. Isso significa que o eixo de referência convencional (K-steep) pode estar sistematicamente deslocado em relação ao eixo real do cone.

---

## Seção 3: O Índice ICE — Definição Formal

O ICE é um índice contínuo entre 0 e 1, produto de três componentes independentes, cada um capturando uma dimensão distinta da coerência óptico-geométrica.

### Fórmula ICE 2.0 (Triádico)

$$ICE = ICE_{astig} \times Optical_{coherence} \times ICE_{axis\_triad}$$

$$ICE = \left[1 - \frac{|Astig_T - Cyl|}{Astig_T + Cyl}\right] \times \left[\frac{LOA}{LOA + HOA}\right] \times \left[1 - \frac{D_{max}}{90^\circ}\right]$$

Onde:
* $D_{max} = \max( |\theta_{topo} - \theta_{cyl}|, |\theta_{topo} - \theta_{coma}|, |\theta_{cyl} - \theta_{coma}| )$
* $Astig_T$ = astigmatismo topográfico
* $Cyl$ = cilindro manifesto
* $LOA$ = aberrações de baixa ordem (Low Order Aberrations)
* $HOA$ = aberrações de alta ordem (High Order Aberrations)

### Os Três Blocos de Análise
1. **Bloco 1 — Coerência de magnitude:** Compara a magnitude do astigmatismo topográfico com o cilindro manifesto. Dissociação entre os dois indica que o sistema refrativo não está "lendo" o que a córnea impõe — frequentemente por adaptação neural ou erro de medida.
2. **Bloco 2 — Pureza óptica:** Razão entre aberrações de baixa ordem (corrigíveis) e totais. Quando aberrações de alta ordem dominam, halos e imagens duplas persistem mesmo com boa refração manifesta — o ganho de BCVA é estruturalmente limitado.
3. **Bloco 3 — Coerência angular triádica:** Maior discordância angular entre os três eixos (topográfico, refrativo, comático). Eixos a $<15^\circ$: alta coerência. A $>30^\circ$: o anel posicionado no K-steep pode aumentar o coma ao invés de reduzi-lo.

### Classificação Clínica e Condutas

| Faixa ICE | Classificação | Interpretação | Conduta Proposta |
| :--- | :--- | :--- | :--- |
| **$\ge 0,65$** | Tipo 1 — Coerente | Eixos alinhados, HOA controladas, magnitude concordante | Operar. Maximizar VEsférico. Prometer ganho objetivo. |
| **0,50 – 0,64** | Zona cinzenta | Coerência parcial; pelo menos um bloco comprometido | Operar com cautela. Expectativa parcial com o paciente. |
| **$< 0,50$** | Tipo 2 — Discordante | Eixos fragmentados, HOA dominantes ou magnitude dissociada | Redefinir objetivo. Considerar CXL, lente escleral ou anel tectônico. |

---

## Seção 4: Fundamento Biomecânico — Modelos FEM

Para validar a premissa física do ICE — de que o desalinhamento entre o eixo do anel e o eixo real do cone reduz a eficácia da correção — foram desenvolvidos 24 modelos de elementos finitos utilizando o software FEBio com material anisotrópico Holzapfel-Gasser-Ogden (HGO), que reproduz a organização fibrilar do estroma.

### Resultados dos Modelos FEM
* **Eficiência Mecânica:** O anel alinhado ao eixo principal do cone gera resposta apical **1,24 vezes mais eficiente** do que o anel desalinhado em $30^\circ$.
* **Efeito do Desalinhamento:** O desalinhamento de $30^\circ$ reduz a eficácia apical em ~19%, com redistribuição da tensão para o meridiano perpendicular — potencialmente agravando o coma ao invés de reduzi-lo.
* **Implicação Clínica Direta:** ICE alto significa que o eixo convencional de referência (K-steep) e o eixo real do cone estão alinhados — o anel posicionado pelo nomograma padrão está no campo de força correto. ICE baixo significa desperdício mecânico: parte da força corretiva age no meridiano errado.

> **Nota sobre a Dissociação Anterior-Posterior (Achado Original):**  
> Na análise de 660 olhos, a correlação entre posição do ápice anterior e posterior foi de $r = 0,028$ ($p = 0,50$ — nula). Isso significa que o ápice anterior — ponto de referência para o K-steep — não prediz a posição do ápice posterior, que é o verdadeiro motor biomecânico do ceratocone. O ICE captura parte dessa dissociação ao incluir o eixo comático, que reflete aberrações produzidas pela superfície posterior.

---

## Seção 5: Dados Preliminares (Retrospectivo)

A análise retrospectiva utilizou dados de 8 estudos publicados entre 2013 e 2024, totalizando **300 olhos com ICRS**, recodificados segundo os critérios ICE a partir dos dados disponibilizados nos artigos. Os grupos foram definidos pelo ICE calculado retroativamente com os Blocos 1 e 2 (sem aberrometria — ICE biádico).

### Resultados por Grupo de ICE
* **ICE Alto (n = 118):** $+4,2$ linhas de BCVA médio
* **ICE Moderado (n = 102):** $+2,8$ linhas de BCVA médio
* **ICE Baixo (n = 80):** $+1,6$ linhas de BCVA médio

### Desempenho de Predição (Ganho de BCVA $\ge 3$ linhas Snellen)

| Métrica | AUC (Área Sob a Curva ROC) | Intervalo de Confiança (IC 95%) | Comparação com ICE (DeLong) |
| :--- | :--- | :--- | :--- |
| **ICE** | **0,82** | 0,76 – 0,87 | — |
| Kmax | 0,68 | 0,61 – 0,75 | $p = 0,012$ |
| Paquimetria Mínima | 0,64 | 0,57 – 0,71 | $p = 0,004$ |
| Estadiamento Amsler-Krumeich | 0,61 | 0,54 – 0,68 | $p < 0,001$ |

> **Limitação Crítica:**  
> Estes dados são retroativos e baseados na reconstrução do ICE a partir de publicações de terceiros. O Bloco 3 ($\theta_{coma}$) não pôde ser calculado por ausência de dados de aberrometria na maioria dos estudos — o ICE utilizado é biádico (Blocos 1 e 2). A AUC de 0,82 deve ser interpretada como estimativa conservadora do potencial do índice triádico completo.

---

## Seção 6: Protocolo de Estudo Prospectivo Proposto

* **Delineamento:** Estudo de coorte prospectivo, multicêntrico, com cegamento do cirurgião para o resultado do ICE até o desfecho primário.
* **Acompanhamento:** 6 meses pós-operatório.

### Critérios de Seleção
* **Critérios de Inclusão:**
  - Ceratocone confirmado (BAD-D $\ge 1,6$ ou Kmax $\ge 47,2$ D)
  - Candidato a ICRS por indicação clínica independente
  - CDVA $\le 20/40$ com melhor correção
  - Idade $\ge 18$ anos
  - Dados disponíveis: Pentacam + aberrometria + refração manifesta
* **Critérios de Exclusão:**
  - Cirurgia corneana prévia
  - Paquimetria mínima $< 350$ µm
  - Doença ocular associada (glaucoma, uveíte)
  - CXL simultâneo (grupo separado, análise secundária)

### Dimensionamento Amostral
* AUC esperada (ICE triádico): 0,82
* AUC nula ($H_0$): 0,70
* Poder estatístico ($1-\beta$): 80%
* $\alpha$ bilateral: 0,05
* **N necessário:** 168 olhos
* **N proposto (+20% de perdas):** 202 olhos
* *Viabilidade:* Com o volume do BrAIn e centros parceiros, $N=202$ é plenamente alcançável em 12–18 meses.

### Tabela de Desfechos

| Desfecho | Medida | Momento |
| :--- | :--- | :--- |
| **Primário** | Ganho de BCVA $\ge 3$ linhas Snellen (predito pelo ICE) | 6 meses |
| Secundário 1 | Redução de Kmax $\ge 2$ D | 3 e 6 meses |
| Secundário 2 | Variação de coma RMS | 6 meses |
| Secundário 3 | Satisfação subjetiva (VFQ-25) | 6 meses |
| Secundário 4 | Necessidade de explante ou reposicionamento | 12 meses |

---

## Seção 7: Cronograma Proposto

* **M0 – M2 (Preparação):** Cálculo ICE retrospectivo + calibração da fórmula. Calcular ICE biádico nos 443 pares disponíveis. Ajustar limiares de classificação com dados locais. Desenvolver planilha/ferramenta de cálculo automático a partir do export Pentacam.
* **M2 – M4 (Protocolo e Aprovação):** Submissão ao CEP + treinamento dos centros. Elaborar protocolo formal com coinvestigadores. Submeter ao Comitê de Ética. Treinar equipe de coleta (Pentacam + aberrômetro + refração padronizada). Definir SOP de cegamento.
* **M4 – M18 (Coleta de Dados):** Recrutamento e seguimento prospectivo. Meta: 202 olhos em 14 meses. Avaliação pré-operatória (ICE calculado e selado), cirurgia por indicação clínica padrão, avaliação 1m / 3m / 6m com equipe cega para o ICE.
* **M18 – M22 (Análise e Publicação):** Análise estatística, escrita e submissão. Análise ROC primária. Regressão logística multivariada. Curvas Kaplan-Meier para desfechos secundários. Submissão ao *Journal of Refractive Surgery* ou *Cornea*.

---

## Seção 8: Recursos Desenvolvidos e Publicação Alvo

Este projeto visa consolidar a validação do índice ICE através do protocolo prospectivo apresentado. Os recursos e resultados já desenvolvidos estão estruturados para fundamentar uma publicação científica principal.

### Recursos e Dados já Desenvolvidos (Miguel Reis)
* Dados retrospectivos: 443 pares Pentacam/OCT Triton consolidados.
* 660 curvaturas SPR analisadas, comprovando a dissociação ápice anterior-posterior.
* 24 modelos FEM HGO rodados e validados no FEBio.
* Fórmula ICE 2.0 implementada e rotina de cálculo automatizada.
* Revisão sistemática concluída de 8 estudos clínicos de base.
* Rascunho inicial do artigo e material complementar estruturados.

### Requisitos Técnicos para Validação Prospectiva
* Coorte prospectiva com exames completos pré e pós-operatórios.
* Dados de aberrometria por rastreamento de raios (para cálculo do Bloco 3).
* Acompanhamento clínico padronizado aos 6 meses de acuidade visual (BCVA).
* Cegamento estrito da equipe de refração pós-operatória para evitar viés de aferição.
* Análise estatística ROC para redefinição final de limiares de sensibilidade e especificidade.
* Integração com dados diagnósticos complementares (TBI e BAD-D) como covariáveis.

### Publicação Científica Alvo
* **Artigo Principal:** *Journal of Refractive Surgery* ou *Cornea*
* **Título Proposto:** "Validação prospectiva do Índice de Coerência do Eixo (ICE) como preditor de ganho visual após implante de anel intraestromal em ceratocone".
* **Escopo:** Apresentar a fundamentação biofísica do índice (SPR/FEM), calibração retrospectiva da fórmula (AUC 0,82) e comprovação prospectiva de acurácia discriminativa a 6 meses.

> **Nota sobre Viabilidade Clínica:**  
> A relevância científica deste projeto, bem como a viabilidade e rigor metodológico do protocolo prospectivo de validação, são submetidas à apreciação e parecer técnico-científico do Prof. Dr. Renato Ambrósio Jr.

---

## Seção 9: Posição Honesta — Limitações e Incertezas

| Limitação | Status | Mitigação |
| :--- | :--- | :--- |
| AUC baseada em dados retrospectivos e biádicos | Parcial | Estudo prospectivo com ICE triádico completo |
| $\theta_{coma}$ ausente na fórmula atual (dados limitados) | Pendente | Inclusão de aberrometria sistemática no protocolo prospectivo |
| ICE-score (0–1) e ICE-min ($^\circ$) não formalizados como métricas distintas | Em revisão | Artigo metodológico separado define ambos |
| Limiares (0,50 / 0,65) derivados de dados de terceiros | Provisório | Análise ROC primária do estudo prospectivo redefine |
| Modelos FEM com geometria simplificada | Robusto | 24 modelos com variação de parâmetros; achado 1,24x consistente |
| Dissociação A-P ainda não publicada | Pronto | Dados completos, análise finalizada, rascunho disponível |

> **Conclusão:**  
> O ICE é, neste momento, uma **hipótese biofisicamente fundamentada com suporte retrospectivo moderado**. Não é um índice clínico validado. A presente proposta destina-se à avaliação de relevância científica por parte do Prof. Dr. Renato Ambrósio Jr., com o objetivo de colher parecer sobre o potencial de validação do índice no pipeline clínico.

---

**Miguel Reis**  
*Biomecânica Corneana Computacional*  
*Projeto AVBC-ICRS · Junho 2026*  

**Prof. Dr. Renato Ambrósio Jr.**  
*BrAIn — Rio de Janeiro*  
*Para Avaliação de Relevância Científica*
"""

# Let's perform spelling correction on both documents
HTML_PROJECT_CONTENT = spell_correct(HTML_PROJECT_CONTENT)
MARKDOWN_PROJECT_CONTENT = spell_correct(MARKDOWN_PROJECT_CONTENT)

# Write HTML file
with open(PROJ_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_PROJECT_CONTENT)
print(f"Salvando HTML corrigido em: {PROJ_HTML}")

# Write Markdown files
for path in [os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Ambrosio.md"), os.path.join(DEST_DIR, "ICE_Projeto_Pesquisa_Ambrosio.md")]:
    print(f"Salvando Markdown corrigido em: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(MARKDOWN_PROJECT_CONTENT)

# Write Plain Text files
raw_text_content = MARKDOWN_PROJECT_CONTENT.replace("**", "").replace("*", "").replace("`", "").replace(">", "").strip()
for path in [os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Ambrosio.txt"), os.path.join(DEST_DIR, "ICE_Projeto_Pesquisa_Ambrosio.txt")]:
    print(f"Salvando Texto corrigido em: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw_text_content)

# Regenerate PDF for project
def generate_pdf(html_path, pdf_path):
    if not os.path.exists(CHROME):
        print(f"Chrome não encontrado em {CHROME}")
        return False
    html_url = pathlib.Path(html_path).as_uri()
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        "--font-render-hinting=none",
        "--disable-web-security",
        "--allow-file-access-from-files",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        "--no-margins",
        "--virtual-time-budget=8000",
        html_url
    ]
    print(f"Executando Chrome headless para gerar PDF: {pdf_path}")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if res.returncode == 0 and os.path.exists(pdf_path):
        print(f"PDF gerado com sucesso: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        return True
    else:
        print(f"Erro ao gerar PDF: {res.returncode}")
        return False

generate_pdf(PROJ_HTML, PROJ_PDF)

# Copy HTML and PDF to D:\ICE_Apresentacao
import shutil
for filename in ["ICE_Projeto_Pesquisa_Ambrosio.html", "ICE_Projeto_Pesquisa_Ambrosio.pdf"]:
    src = os.path.join(WORKSPACE, filename)
    dst = os.path.join(DEST_DIR, filename)
    if os.path.exists(src):
        print(f"Copiando {filename} para {dst}")
        shutil.copy2(src, dst)

print("Processo de readequação de escopo concluído com sucesso!")
