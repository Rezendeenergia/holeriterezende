import streamlit as st
import pdfplumber
import re
import zipfile
import io
from pypdf import PdfReader, PdfWriter

st.set_page_config(
    page_title="Holerites · Rezende Energia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

/* ── BASE ── */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background: #F7F6F3 !important;
    font-family: 'Inter', sans-serif !important;
    color: #1C1C1E !important;
}
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── TOP BAR ── */
.rz-topbar {
    background: #FFFFFF;
    border-bottom: 1px solid #EBEBEB;
    padding: 0 48px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.rz-topbar-left { display: flex; align-items: center; gap: 12px; }
.rz-wordmark {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 17px;
    color: #1C1C1E;
    letter-spacing: -0.3px;
}
.rz-wordmark span { color: #F7931E; }
.rz-divpipe {
    width: 1px; height: 20px;
    background: #DDDDD8;
}
.rz-module {
    font-size: 13px;
    color: #888;
    font-weight: 500;
}
.rz-badge {
    background: #FFF4E8;
    color: #C96D00;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 100px;
    letter-spacing: 0.2px;
}

/* ── PAGE SHELL ── */
.rz-shell {
    max-width: 760px;
    margin: 0 auto;
    padding: 48px 24px 80px;
}

/* ── PAGE HEADER ── */
.rz-page-header { margin-bottom: 36px; }
.rz-page-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #F7931E;
    margin-bottom: 8px;
}
.rz-page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 30px;
    color: #1C1C1E;
    letter-spacing: -0.6px;
    line-height: 1.15;
    margin-bottom: 10px;
}
.rz-page-desc {
    font-size: 14px;
    color: #888;
    line-height: 1.6;
    max-width: 520px;
}

/* ── CARD ── */
.rz-card {
    background: #FFFFFF;
    border: 1px solid #EBEBEB;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
}
.rz-card-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #AAAAAA;
    margin-bottom: 16px;
}

/* ── UPLOAD ZONE ── */
[data-testid="stFileUploader"] {
    background: #FAFAF8 !important;
    border: 1.5px dashed #DDDDD8 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #F7931E !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: #999 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] svg { fill: #F7931E !important; }
[data-testid="stBaseButton-secondary"] {
    background: #1C1C1E !important;
    color: #FFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* ── STEPS ── */
.rz-steps {
    display: flex;
    gap: 0;
    margin-bottom: 0;
}
.rz-step {
    flex: 1;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 20px 16px 0;
    position: relative;
}
.rz-step:not(:last-child)::after {
    content: '';
    position: absolute;
    right: 10px;
    top: 24px;
    width: 20px;
    height: 1px;
    background: #DDDDD8;
}
.rz-step-num {
    width: 28px; height: 28px;
    background: #F7F6F3;
    border: 1px solid #EBEBEB;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
    font-weight: 600;
    color: #888;
    flex-shrink: 0;
}
.rz-step-num.active {
    background: #FFF4E8;
    border-color: #FFD9A8;
    color: #C96D00;
}
.rz-step-text { font-size: 12px; color: #888; line-height: 1.4; padding-top: 5px; }
.rz-step-text strong { color: #444; font-weight: 600; display: block; margin-bottom: 2px; }

/* ── PROGRESS BAR ── */
[data-testid="stProgress"] {
    background: #EBEBEB !important;
    border-radius: 100px !important;
    height: 4px !important;
}
[data-testid="stProgress"] > div > div {
    background: #F7931E !important;
    border-radius: 100px !important;
}

/* ── STATS ── */
.rz-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.rz-stat {
    background: #FAFAF8;
    border: 1px solid #EBEBEB;
    border-radius: 12px;
    padding: 16px 20px;
}
.rz-stat-val {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #1C1C1E;
    letter-spacing: -0.5px;
    line-height: 1;
    margin-bottom: 4px;
}
.rz-stat-val span { color: #F7931E; }
.rz-stat-lbl {
    font-size: 12px;
    color: #AAAAAA;
    font-weight: 500;
}

/* ── EMPLOYEE LIST ── */
.rz-list { border-radius: 12px; overflow: hidden; border: 1px solid #EBEBEB; }
.rz-list-header {
    display: grid;
    grid-template-columns: 36px 1fr 200px;
    padding: 10px 16px;
    background: #FAFAF8;
    border-bottom: 1px solid #EBEBEB;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #BBBBBB;
}
.rz-list-row {
    display: grid;
    grid-template-columns: 36px 1fr 200px;
    padding: 11px 16px;
    border-bottom: 1px solid #F3F3F0;
    align-items: center;
    background: #FFFFFF;
    transition: background 0.1s;
}
.rz-list-row:last-child { border-bottom: none; }
.rz-list-row:hover { background: #FAFAF8; }
.rz-list-idx { font-size: 12px; color: #CCCCCC; font-weight: 500; }
.rz-list-name { font-size: 13px; font-weight: 500; color: #1C1C1E; }
.rz-list-file {
    font-size: 11px;
    color: #AAAAAA;
    text-align: right;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.rz-list-more {
    padding: 10px 16px;
    background: #FAFAF8;
    font-size: 12px;
    color: #AAAAAA;
    text-align: center;
    border-top: 1px solid #EBEBEB;
}

/* ── SUCCESS BANNER ── */
.rz-success {
    background: #F0FBF4;
    border: 1px solid #C3EDD1;
    border-radius: 12px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}
.rz-success-icon {
    width: 36px; height: 36px;
    background: #D6F5E3;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.rz-success-title {
    font-size: 14px;
    font-weight: 600;
    color: #1A7F3C;
    margin-bottom: 2px;
}
.rz-success-sub { font-size: 12px; color: #3DAE6A; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] > button {
    background: #1C1C1E !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 32px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.15s !important;
    letter-spacing: 0 !important;
}
[data-testid="stDownloadButton"] > button:hover { opacity: 0.85 !important; }

/* ── STATUS TEXT ── */
.rz-proc-status {
    font-size: 12px;
    color: #AAAAAA;
    margin-top: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── EMPTY STATE ── */
.rz-empty {
    text-align: center;
    padding: 40px 24px;
    color: #CCCCCC;
}
.rz-empty-icon {
    font-size: 32px;
    margin-bottom: 12px;
    opacity: 0.5;
}
.rz-empty-title { font-size: 14px; font-weight: 500; color: #BBBBBB; margin-bottom: 4px; }
.rz-empty-sub { font-size: 12px; color: #CCCCCC; }

/* ── FOOTER ── */
.rz-footer {
    text-align: center;
    margin-top: 56px;
    padding-top: 24px;
    border-top: 1px solid #EBEBEB;
    font-size: 12px;
    color: #CCCCCC;
}
.rz-footer b { color: #BBBBBB; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# Adicionar antes da função (pode ser logo acima de extract_name_and_mes)
MESES = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12",
}

def extract_name_and_mes(text: str):
    lines = text.split('\n') if text else []
    nome, mes_ano = None, None

    for line in lines:
        # Competência: "Março de 2026" → "03/2026"
        if mes_ano is None:
            m = re.search(r'(\w+)\s+de\s+(\d{4})', line, re.IGNORECASE)
            if m and m.group(1).lower() in MESES:
                mes_ano = f"{MESES[m.group(1).lower()]}-{m.group(2)}"

        # Nome: "137 ABRAAO NUNES DE OLIVEIRA 992205 1 1"
        if nome is None:
            n = re.match(r'^\d+\s+([A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇ][A-ZÁÉÍÓÚÀÂÊÔÃÕÜÇ\s]+?)\s+\d{6}\s', line)
            if n:
                nome = n.group(1).strip()

    return nome, mes_ano


def process_pdf(uploaded_file):
    try:
        raw = uploaded_file.read()
        pages_info = []

        progress_bar = st.progress(0)
        status_slot  = st.empty()

        with pdfplumber.open(io.BytesIO(raw)) as plumb:
            reader = PdfReader(io.BytesIO(raw))
            total  = len(plumb.pages)

            for i, page in enumerate(plumb.pages):
                text = page.extract_text() or ""
                nome, mes_ano = extract_name_and_mes(text)
                nome    = nome    or f"FUNCIONARIO_PAG_{i+1}"
                mes_ano = mes_ano or "COMPETENCIA"
                fname   = f"{nome} - {mes_ano}.pdf"
                pages_info.append((i, nome, mes_ano, fname))

                progress_bar.progress((i + 1) / total)
                status_slot.markdown(
                    f'<p class="rz-proc-status">Processando {i+1}/{total} · {nome}</p>',
                    unsafe_allow_html=True,
                )

            # Build ZIP
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i, nome, mes_ano, fname in pages_info:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    pdf_buf = io.BytesIO()
                    writer.write(pdf_buf)
                    zf.writestr(fname, pdf_buf.getvalue())

        # clear ephemeral widgets completely
        progress_bar.empty()
        status_slot.empty()

        return pages_info, zip_buf.getvalue(), None

    except Exception as e:
        return [], None, str(e)


# ── SESSION STATE ─────────────────────────────
if "result"    not in st.session_state: st.session_state.result    = None
if "error"     not in st.session_state: st.session_state.error     = None
if "last_file" not in st.session_state: st.session_state.last_file = None


# ── TOP BAR ──────────────────────────────────
st.markdown("""
<div class="rz-topbar">
  <div class="rz-topbar-left">
    <div class="rz-wordmark">Rezende<span>.</span></div>
    <div class="rz-divpipe"></div>
    <div class="rz-module">Recursos Humanos</div>
  </div>
  <div class="rz-badge">⚡ Uso Interno</div>
</div>
""", unsafe_allow_html=True)


# ── SHELL ────────────────────────────────────
st.markdown('<div class="rz-shell">', unsafe_allow_html=True)

st.markdown("""
<div class="rz-page-header">
  <div class="rz-page-eyebrow">Folha de Pagamento</div>
  <div class="rz-page-title">Separador de Holerites</div>
  <div class="rz-page-desc">
    Importe o PDF consolidado da folha. O sistema extrai e nomeia cada holerite automaticamente,
    entregando um arquivo ZIP pronto para distribuição.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rz-card">
  <div class="rz-card-title">Como funciona</div>
  <div class="rz-steps">
    <div class="rz-step">
      <div class="rz-step-num active">1</div>
      <div class="rz-step-text"><strong>Importe o PDF</strong>Folha consolidada do sistema</div>
    </div>
    <div class="rz-step">
      <div class="rz-step-num">2</div>
      <div class="rz-step-text"><strong>Processamento</strong>Leitura e separação automática</div>
    </div>
    <div class="rz-step">
      <div class="rz-step-num">3</div>
      <div class="rz-step-text"><strong>Download ZIP</strong>Holerites nomeados individualmente</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="rz-card">', unsafe_allow_html=True)
st.markdown('<div class="rz-card-title">Arquivo da folha</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    label="PDF da folha",
    type=["pdf"],
    label_visibility="collapsed",
    help="PDF consolidado exportado pelo sistema de folha de pagamento",
)

# Detect new upload → reset + process
if uploaded is not None:
    file_id = (uploaded.name, uploaded.size)
    if file_id != st.session_state.last_file:
        st.session_state.result    = None
        st.session_state.error     = None
        st.session_state.last_file = file_id

        with st.spinner("Analisando arquivo…"):
            pages_info, zip_bytes, err = process_pdf(uploaded)

        if err:
            st.session_state.error = err
        else:
            st.session_state.result = (pages_info, zip_bytes)

st.markdown('</div>', unsafe_allow_html=True)  # /rz-card upload

# ── RESULTS ──────────────────────────────────
if st.session_state.error:
    st.error(f"Erro ao processar o arquivo: {st.session_state.error}")

elif st.session_state.result:
    pages_info, zip_bytes = st.session_state.result
    total       = len(pages_info)
    competencia = pages_info[0][2] if pages_info else "—"
    mes_label   = competencia.split('-')[0][:3] if '-' in competencia else competencia[:3]
    ano_label   = competencia.split('-')[-1]    if '-' in competencia else ""
    zip_mb      = len(zip_bytes) / (1024 * 1024)
    zip_name    = f"Holerites_Rezende_{competencia}.zip"

    st.markdown(f"""
    <div class="rz-stats">
      <div class="rz-stat">
        <div class="rz-stat-val">{total}</div>
        <div class="rz-stat-lbl">Funcionários</div>
      </div>
      <div class="rz-stat">
        <div class="rz-stat-val"><span>{mes_label}</span></div>
        <div class="rz-stat-lbl">Competência · {ano_label}</div>
      </div>
      <div class="rz-stat">
        <div class="rz-stat-val">{zip_mb:.1f}<span style="font-size:16px">MB</span></div>
        <div class="rz-stat-lbl">Tamanho do ZIP</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    preview_n = 10
    rows_html = """
    <div class="rz-list">
      <div class="rz-list-header">
        <div>#</div><div>Funcionário</div><div style="text-align:right">Arquivo gerado</div>
      </div>
    """
    for idx, (_, nome, mes_ano, fname) in enumerate(pages_info[:preview_n]):
        rows_html += f"""
      <div class="rz-list-row">
        <div class="rz-list-idx">{idx+1}</div>
        <div class="rz-list-name">{nome}</div>
        <div class="rz-list-file">{fname}</div>
      </div>"""
    if total > preview_n:
        rows_html += f'<div class="rz-list-more">+ {total - preview_n} funcionários no arquivo</div>'
    rows_html += "</div>"

    st.markdown(rows_html, unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rz-success">
      <div class="rz-success-icon">✓</div>
      <div>
        <div class="rz-success-title">Processamento concluído com sucesso</div>
        <div class="rz-success-sub">{total} holerites · Competência {competencia} · {zip_mb:.1f} MB</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label=f"⬇  Baixar ZIP · {total} holerites · {zip_mb:.1f} MB",
        data=zip_bytes,
        file_name=zip_name,
        mime="application/zip",
        use_container_width=True,
    )

else:
    st.markdown("""
    <div class="rz-empty">
      <div class="rz-empty-icon">📄</div>
      <div class="rz-empty-title">Nenhum arquivo importado</div>
      <div class="rz-empty-sub">Selecione o PDF consolidado da folha de pagamento acima</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="rz-footer">
  <b>Rezende Energia</b> · Sistema de RH · Separador de Holerites · Uso Interno
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # /rz-shell
