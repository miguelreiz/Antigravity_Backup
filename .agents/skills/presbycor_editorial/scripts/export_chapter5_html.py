#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta Chapter_5_Complete.md para HTML auto-contido com imagens em base64.
Abre em qualquer browser sem dependências externas.
"""
import re
import base64
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MD_FILE      = PROJECT_ROOT / "Chapter_5_Complete.md"
OUTPUT_HTML  = PROJECT_ROOT / "_Distributable_Book" / "Chapter_05_PresbyCor_Complete.html"
FIGURES_DIR  = PROJECT_ROOT / "figures"


def img_to_base64(img_path_md: str):
    """Converte path de imagem markdown em data URI base64."""
    clean = img_path_md.lstrip("./").replace("/", "\\")
    candidate = PROJECT_ROOT / clean
    if candidate.exists():
        data = candidate.read_bytes()
        b64 = base64.b64encode(data).decode()
        ext = candidate.suffix.lower().lstrip(".")
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{b64}"
    # Busca recursiva em figures/
    fname = Path(img_path_md).name
    for ch_dir in FIGURES_DIR.glob("*"):
        cp = ch_dir / fname
        if cp.exists():
            data = cp.read_bytes()
            b64 = base64.b64encode(data).decode()
            return f"data:image/png;base64,{b64}"
    return None


def inline_fmt(text: str) -> str:
    """Aplica formatação inline: negrito, itálico, código."""
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*",     r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",         r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`",           r"<code>\1</code>", text)
    # Fórmulas simples entre $$
    text = re.sub(r"\$\$?([^$]+)\$\$?", r"<em class='formula'>\1</em>", text)
    return text


md_text = MD_FILE.read_text(encoding="utf-8")
lines   = md_text.splitlines()
n       = len(lines)

html_body   = []
i           = 0
in_alert    = False
alert_type  = ""
alert_buf   = []
in_table    = False
table_buf   = []

ALERT_CLASSES = {
    "NOTE": "note", "IMPORTANT": "important",
    "WARNING": "warning", "CAUTION": "caution", "TIP": "tip",
}

while i < n:
    line = lines[i].rstrip()

    # ── Alert box ─────────────────────────────────────────────────────
    alert_start = re.match(r"^> \[!(NOTE|IMPORTANT|WARNING|CAUTION|TIP)\]", line)
    if alert_start and not in_alert:
        in_alert   = True
        alert_type = alert_start.group(1)
        alert_buf  = []
        i += 1
        continue

    if in_alert:
        if line.startswith(">"):
            alert_buf.append(line[1:].strip())
            i += 1
            continue
        else:
            cls   = ALERT_CLASSES.get(alert_type, "note")
            label = {"NOTE": "Nota", "IMPORTANT": "Importante",
                     "WARNING": "Aviso", "CAUTION": "Atenção", "TIP": "Pérola Clínica"}.get(alert_type, alert_type)
            content = " ".join(alert_buf)
            html_body.append(f'<div class="alert {cls}"><strong>[{label}]</strong> {inline_fmt(content)}</div>')
            in_alert = False
            # não incrementa i — reprocessa linha atual

    # ── Heading ───────────────────────────────────────────────────────
    hm = re.match(r"^(#{1,4})\s+(.*)", line)
    if hm:
        level = len(hm.group(1))
        title = inline_fmt(hm.group(2))
        anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        html_body.append(f'<h{level} id="{anchor}">{title}</h{level}>')
        i += 1
        continue

    # ── Tabela ────────────────────────────────────────────────────────
    if re.match(r"^\s*\|", line):
        table_buf = []
        while i < n and re.match(r"^\s*\|", lines[i]):
            table_buf.append(lines[i])
            i += 1
        if len(table_buf) >= 2:
            html_body.append('<table>')
            for ti, tline in enumerate(table_buf):
                cells = [c.strip() for c in tline.strip("|").split("|")]
                if re.match(r"^[-:\s|]+$", tline):
                    continue
                tag = "th" if ti == 0 else "td"
                row = "".join(f"<{tag}>{inline_fmt(c)}</{tag}>" for c in cells)
                html_body.append(f"<tr>{row}</tr>")
            html_body.append('</table>')
        continue

    # ── Figura ────────────────────────────────────────────────────────
    fig_m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
    if fig_m:
        alt  = fig_m.group(1)
        path = fig_m.group(2)
        b64  = img_to_base64(path)
        if b64:
            html_body.append(f'<div class="fig"><img src="{b64}" alt="{alt}"></div>')
            print(f"  ✓ Imagem embutida: {Path(path).name}")
        else:
            html_body.append(f'<div class="fig placeholder">[ Figura não encontrada: {Path(path).name} ]</div>')
            print(f"  ⚠ Não encontrada: {path}")
        # Linha seguinte pode ser legenda *...*
        if i + 1 < n and lines[i+1].strip().startswith("*"):
            i += 1
            cap = lines[i].strip().strip("*")
            html_body.append(f'<p class="caption">{inline_fmt(cap)}</p>')
        i += 1
        continue

    # Legenda isolada *Figura...* ou *Figure...*
    if re.match(r"^\*Figura\s", line) or re.match(r"^\*Figure\s", line):
        cap = line.strip().strip("*")
        html_body.append(f'<p class="caption">{inline_fmt(cap)}</p>')
        i += 1
        continue

    # ── Fórmula ———————————————————————————————————————————————————————
    if "$$" in line:
        formula = re.sub(r"\$\$", "", line).strip()
        html_body.append(f'<p class="formula-block"><em>{formula}</em></p>')
        i += 1
        continue

    # ── Separador ─────────────────────────────────────────────────────
    if re.match(r"^---+$", line.strip()):
        html_body.append("<hr>")
        i += 1
        continue

    # ── Lista ─────────────────────────────────────────────────────────
    ul_m = re.match(r"^(\s*)([-*+])\s+(.*)", line)
    if ul_m:
        indent = len(ul_m.group(1)) // 2
        text   = inline_fmt(ul_m.group(3))
        margin = indent * 20
        html_body.append(f'<p style="margin-left:{margin+20}px;text-indent:-16px;margin-top:3px">• {text}</p>')
        i += 1
        continue

    ol_m = re.match(r"^(\s*)(\d+)\.\s+(.*)", line)
    if ol_m:
        num   = ol_m.group(2)
        text  = inline_fmt(ol_m.group(3))
        indent = len(ol_m.group(1)) // 2
        margin = indent * 20
        html_body.append(f'<p style="margin-left:{margin+20}px;text-indent:-18px;margin-top:3px">{num}. {text}</p>')
        i += 1
        continue

    # ── Linha em branco ───────────────────────────────────────────────
    if not line.strip():
        i += 1
        continue

    # ── Parágrafo normal ──────────────────────────────────────────────
    html_body.append(f"<p>{inline_fmt(line)}</p>")
    i += 1

# Fechar alert pendente
if in_alert and alert_buf:
    cls   = ALERT_CLASSES.get(alert_type, "note")
    content = " ".join(alert_buf)
    html_body.append(f'<div class="alert {cls}"><strong>[{alert_type}]</strong> {inline_fmt(content)}</div>')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Capítulo 5 — PresbyCor e Alcon Custom-Q | PresbyCor Book</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;1,400&display=swap');
  body {{
    font-family: 'Source Sans 3', 'Times New Roman', serif;
    max-width: 860px;
    margin: 40px auto;
    padding: 30px 40px;
    line-height: 1.75;
    color: #1a1a1a;
    background: #fdfcf9;
  }}
  h1 {{
    font-family: 'IM Fell English', serif;
    color: #1a3a5c;
    font-size: 2em;
    border-bottom: 3px solid #1a3a5c;
    padding-bottom: 12px;
    margin-top: 50px;
  }}
  h2 {{
    color: #1a3a5c;
    font-size: 1.45em;
    margin-top: 40px;
    border-left: 4px solid #1a3a5c;
    padding-left: 12px;
  }}
  h3 {{
    color: #2c5f8a;
    font-size: 1.2em;
    margin-top: 28px;
  }}
  h4 {{
    color: #2c5f8a;
    font-size: 1.05em;
    font-style: italic;
    margin-top: 20px;
  }}
  p {{
    text-align: justify;
    margin: 8px 0;
  }}
  .fig {{
    text-align: center;
    margin: 30px auto 6px;
    max-width: 100%;
  }}
  .fig img {{
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 3px 14px rgba(0,0,0,0.12);
  }}
  .caption {{
    text-align: center;
    font-style: italic;
    font-size: 0.88em;
    color: #555;
    margin: 4px 20px 28px;
  }}
  .placeholder {{
    background: #f5f5f5;
    border: 2px dashed #aaa;
    padding: 18px;
    color: #777;
    font-style: italic;
    text-align: center;
    border-radius: 6px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 18px 0;
    font-size: 0.93em;
  }}
  th, td {{
    border: 1px solid #ccc;
    padding: 8px 12px;
    vertical-align: top;
  }}
  th {{
    background: #1a3a5c;
    color: #fff;
    font-weight: 600;
    text-align: center;
  }}
  tr:nth-child(even) td {{ background: #f8f9fa; }}
  .alert {{
    border-left: 5px solid #2c5f8a;
    background: #ebf4ff;
    padding: 12px 16px;
    margin: 18px 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.95em;
  }}
  .alert.important {{ border-left-color: #f59e0b; background: #fff8e1; }}
  .alert.warning   {{ border-left-color: #dc2626; background: #fff3f3; }}
  .alert.caution   {{ border-left-color: #dc2626; background: #fff3f3; }}
  .alert.tip       {{ border-left-color: #16a34a; background: #f0fdf4; }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 35px 0;
  }}
  code {{
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
  }}
  .formula-block {{
    text-align: center;
    font-style: italic;
    padding: 10px;
    background: #f8f8f8;
    border-radius: 4px;
    margin: 12px 40px;
  }}
  em.formula {{
    font-style: italic;
    color: #1a3a5c;
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""

OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
final_html = HTML_TEMPLATE.format(body="\n".join(html_body))
OUTPUT_HTML.write_text(final_html, encoding="utf-8")
size_kb = OUTPUT_HTML.stat().st_size // 1024
print(f"\n[OK] HTML gerado: {OUTPUT_HTML}")
print(f"     Tamanho: {size_kb} KB")
print(f"     Abrir no browser — imagens em base64 embutidas, sem dependências externas.")
