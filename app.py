"""
app.py
─────────────────────────────────────────────────────────────
Interface principal do Tótem Inteligente FlexMedia.
Integra todos os módulos desenvolvidos nas etapas anteriores:
  - Banco de dados Oracle      (modules/db.py)
  - Modelo de perfil           (models/train_model.py)
  - Visão computacional        (modules/vision.py)
  - Chatbot                    (modules/chatbot.py)
  - Analytics                  (modules/analytics.py)

Abas da aplicação:
  🏠 Início        — apresentação do tótem e cadastro do visitante
  💬 Interagir     — chatbot e classificador de perfil
  📷 Visão         — upload e classificação de imagem
  📊 Analytics     — métricas e gráficos de engajamento
─────────────────────────────────────────────────────────────
"""

import streamlit as st
import time
from PIL import Image

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Tótem FlexMedia",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# ESTILOS GLOBAIS - TEMA LIGHT
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* Base - Light theme */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color:;
    background-image: none;
}

/* Títulos com fonte display */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #FA4D4D !important;
    letter-spacing: -0.02em;
}

/* Cards - Light */
.fm-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Header do tótem - Light gradient */
.totem-header {
    background: #f1f5f9;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.totem-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.totem-header h1 {
    color: #ffffff !important;
    font-size: 2.4rem !important;
    margin: 0 !important;
    font-weight: 800 !important;
}
.totem-header p {
    color: #000000 !important;
    font-size: 1.05rem;
    margin: 8px 0 0 0;
}

/* Badge de categoria - Light theme */
.categoria-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.badge-arte        { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.badge-ciencia     { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
.badge-historia    { background: #ffedd5; color: #b45309; border: 1px solid #fed7aa; }
.badge-tecnologia  { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }

/* Métrica destacada - Light */
.fm-metric {
    text-align: center;
    padding: 20px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.fm-metric .valor {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #FA4D4D !important;
    line-height: 1;
}
.fm-metric .label {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Tabs - Light */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #475569 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background:;
    color: white !important;
}

/* Inputs - Light theme: dark text on light background */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
    border-color: #0f766e !important;
    box-shadow: 0 0 0 1px #0f766e !important;
}

/* Botões - Light */
.stButton > button {
    background: #FA4D4D !important;
    color: #000000;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}

/* Mensagens do chat - Light */
.msg-visitante {
    background: #e0f2fe;
    border: 1px solid #bae6fd;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 18px;
    margin: 8px 0;
    color: #0c4a6e;
    text-align: right;
}
.msg-totem {
    background: #dcfce7;
    border: 1px solid #bbf7d0;
    border-radius: 14px 14px 14px 4px;
    padding: 12px 18px;
    margin: 8px 0;
    color: #14532d;
}
.msg-label {
    font-size: 0.72rem;
    opacity: 0.6;
    font-family: 'Syne', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
    color: ;
}

/* Barra de probabilidade - Light */
.prob-bar-bg {
    background: #e2e8f0;
    border-radius: 999px;
    height: 8px;
    margin: 4px 0 12px 0;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: #FA4D4D !important;
    transition: width 0.6s ease;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

/* Texto geral */
p, li, span, div {
    color: #1e293b;
}

/* Links */
a {
    color: #0f766e;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# IMPORTS DOS MÓDULOS (com tratamento de erro amigável)
# ─────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def carregar_modulos():
    """Importa os módulos do projeto uma única vez."""
    erros = []
    modulos = {}

    try:
        from modules.db import (
            inserir_visitante, inserir_interacao,
            listar_interacoes, contar_interacoes_por_categoria,
            media_satisfacao_por_tipo, registrar_log,
        )
        modulos["db"] = {
            "inserir_visitante": inserir_visitante,
            "inserir_interacao": inserir_interacao,
            "listar_interacoes": listar_interacoes,
            "contar_por_categoria": contar_interacoes_por_categoria,
            "media_satisfacao": media_satisfacao_por_tipo,
            "registrar_log": registrar_log,
        }
    except Exception as e:
        erros.append(f"❌ **db.py**: {e}")

    try:
        from models.train_model import prever_perfil
        modulos["classificador"] = prever_perfil
    except Exception as e:
        erros.append(f"❌ **train_model.py**: {e}")

    try:
        from modules.vision import classificar_imagem
        modulos["vision"] = classificar_imagem
    except Exception as e:
        erros.append(f"❌ **vision.py**: {e}")

    try:
        from modules.chatbot import processar_mensagem, iniciar_conversa
        modulos["chatbot"] = {
            "processar": processar_mensagem,
            "iniciar": iniciar_conversa,
        }
    except Exception as e:
        erros.append(f"❌ **chatbot.py**: {e}")

    try:
        from modules.analytics import (
            grafico_interacoes_por_categoria,
            grafico_satisfacao_por_tipo,
            grafico_interacoes_por_hora,
            grafico_perfis_visitantes,
        )
        modulos["analytics"] = {
            "por_categoria": grafico_interacoes_por_categoria,
            "satisfacao":    grafico_satisfacao_por_tipo,
            "por_hora":      grafico_interacoes_por_hora,
            "perfis":        grafico_perfis_visitantes,
        }
    except Exception as e:
        erros.append(f"❌ **analytics.py**: {e}")

    return modulos, erros


modulos, erros_import = carregar_modulos()

if erros_import:
    with st.expander("⚠️ Módulos com erro de importação", expanded=False):
        for e in erros_import:
            st.markdown(e)


# ─────────────────────────────────────────────────────────────
# ESTADO DA SESSÃO
# ─────────────────────────────────────────────────────────────

if "visitante_id"   not in st.session_state: st.session_state.visitante_id   = None
if "visitante_nome" not in st.session_state: st.session_state.visitante_nome = None
if "historico_chat" not in st.session_state: st.session_state.historico_chat = []
if "ctx_chat"       not in st.session_state: st.session_state.ctx_chat       = {}


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="totem-header">
    <h1>🖥️ Tótem Inteligente FlexMedia</h1>
    <p>Sistema interativo de informação e análise de visitantes</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ABAS
# ─────────────────────────────────────────────────────────────

aba_inicio, aba_interagir, aba_visao, aba_analytics = st.tabs([
    "🏠  Início",
    "💬  Interagir",
    "📷  Visão",
    "📊  Analytics",
])


# ══════════════════════════════════════════════════════════════
# ABA 1 — INÍCIO
# ══════════════════════════════════════════════════════════════

with aba_inicio:
    col_bem_vindo, col_cadastro = st.columns([1.2, 1], gap="large")

    with col_bem_vindo:
        st.markdown("### Bem-vindo ao Tótem")
        st.markdown("""
<div class="fm-card">
<p style="color:#334155; line-height:1.8; margin:0">
Este tótem foi desenvolvido para enriquecer sua experiência de visita.
Aqui você pode explorar conteúdos sobre <b style="color:#b91c1c">Arte</b>,
<b style="color:#0369a1">Ciência</b>, <b style="color:#b45309">História</b>
e <b style="color:#15803d">Tecnologia</b>, interagir com nosso assistente
virtual e receber recomendações personalizadas com base no seu perfil.
</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("#### Como usar")
        for icone, aba, desc in [
            ("💬", "Interagir", "Converse com o assistente virtual ou use os menus de navegação"),
            ("📷", "Visão",     "Envie uma imagem para o tótem identificar sua categoria temática"),
            ("📊", "Analytics", "Veja os dados de engajamento e padrões de uso do tótem"),
        ]:
            st.markdown(f"""
<div class="fm-card" style="padding:16px 20px; margin-bottom:10px">
<span style="font-size:1.3rem">{icone}</span>
<b style="font-family:'Syne',sans-serif; color:#1e293b; margin-left:10px">{aba}</b>
<span style="color:#64748b; font-size:0.9rem; margin-left:6px">— {desc}</span>
</div>
""", unsafe_allow_html=True)

    with col_cadastro:
        st.markdown("### Identificação")
        st.markdown("""
<div class="fm-card">
<p style="color:#64748b; font-size:0.88rem; margin:0 0 16px 0">
Cadastre-se para uma experiência personalizada.
</p>
""", unsafe_allow_html=True)

        nome_input   = st.text_input("Seu nome", placeholder="Ex: Ana Lima")
        faixa_input  = st.selectbox("Faixa etária", ["jovem", "adulto", "idoso"])

        if st.button("Entrar no Tótem →", use_container_width=True):
            if nome_input.strip():
                if "db" in modulos:
                    try:
                        vid = modulos["db"]["inserir_visitante"](
                            nome=nome_input.strip(),
                            perfil="indefinido",
                            idade_faixa=faixa_input,
                        )
                        st.session_state.visitante_id   = vid
                        st.session_state.visitante_nome = nome_input.strip()
                        st.session_state.historico_chat = []
                        st.session_state.ctx_chat       = {}
                        st.success(f"Bem-vindo(a), **{nome_input.strip()}**! 👋")
                        modulos["db"]["registrar_log"]("app", f"Visitante '{nome_input}' registrado.", "INFO")
                    except Exception as e:
                        st.error(f"Erro ao registrar visitante: {e}")
                else:
                    st.session_state.visitante_nome = nome_input.strip()
                    st.info("Módulo de banco indisponível — sessão local ativa.")
            else:
                st.warning("Por favor, informe seu nome.")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.visitante_nome:
            st.markdown(f"""
<div class="fm-card" style="border-color:#000000; padding:16px 20px">
<span style="color:#000000; font-family:'Syne',sans-serif; font-weight:700">✓ Sessão ativa</span><br>
<span style="color:#475569; font-size:0.9rem">{st.session_state.visitante_nome}</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ABA 2 — INTERAGIR
# ══════════════════════════════════════════════════════════════

with aba_interagir:
    if not st.session_state.visitante_nome:
        st.info("👈 Cadastre-se na aba **Início** para começar a interagir.")
    else:
        col_chat, col_classif = st.columns([1.3, 1], gap="large")

        # ── CHATBOT ──
        with col_chat:
            st.markdown("### 💬 Assistente Virtual")

            # Inicializa conversa se necessário
            if not st.session_state.historico_chat and "chatbot" in modulos:
                boas_vindas = modulos["chatbot"]["iniciar"](st.session_state.visitante_nome)
                st.session_state.historico_chat.append(("totem", boas_vindas))

            # Exibe histórico
            chat_html = ""
            for papel, msg in st.session_state.historico_chat[-10:]:
                if papel == "visitante":
                    chat_html += f'<div class="msg-label" style="text-align:right">{st.session_state.visitante_nome}</div><div class="msg-visitante">{msg}</div>'
                else:
                    chat_html += f'<div class="msg-label">Tótem FlexMedia</div><div class="msg-totem">{msg}</div>'

            st.markdown(f'<div style="max-height:380px; overflow-y:auto; padding-right:4px">{chat_html}</div>', unsafe_allow_html=True)

            # Input de mensagem
            with st.form("form_chat", clear_on_submit=True):
                col_msg, col_btn = st.columns([4, 1])
                with col_msg:
                    mensagem = st.text_input("", placeholder="Digite sua pergunta...", label_visibility="collapsed")
                with col_btn:
                    enviado = st.form_submit_button("→")

            if enviado and mensagem.strip():
                st.session_state.historico_chat.append(("visitante", mensagem.strip()))

                if "chatbot" in modulos:
                    try:
                        resposta, st.session_state.ctx_chat = modulos["chatbot"]["processar"](
                            mensagem.strip(), st.session_state.ctx_chat
                        )
                    except Exception as e:
                        resposta = f"Desculpe, ocorreu um erro: {e}"
                else:
                    resposta = "Módulo de chatbot indisponível no momento."

                st.session_state.historico_chat.append(("totem", resposta))

                # Registra interação no banco
                if "db" in modulos and st.session_state.visitante_id:
                    try:
                        modulos["db"]["inserir_interacao"](
                            visitante_id=st.session_state.visitante_id,
                            tipo_acao="chatbot",
                            categoria=st.session_state.ctx_chat.get("ultima_categoria", "geral"),
                            duracao_seg=len(mensagem) * 2,
                            satisfacao=4,
                        )
                    except Exception:
                        pass

                st.rerun()

        # ── CLASSIFICADOR DE PERFIL ──
        with col_classif:
            st.markdown("### 🧠 Classificador de Perfil")
            st.markdown("""
<div class="fm-card" style="padding:16px 20px">
<p style="color:#64748b; font-size:0.88rem; margin:0">
Simule uma interação para descobrir o perfil previsto pelo modelo de IA.
</p>
</div>
""", unsafe_allow_html=True)

            tipo_sel  = st.selectbox("Tipo de ação",   ["chatbot", "imagem", "menu", "busca"],    key="tipo_cl")
            categ_sel = st.selectbox("Categoria",       ["arte", "ciencia", "historia", "tecnologia"], key="categ_cl")
            dur_sel   = st.slider("Duração (segundos)", 10, 300, 90, key="dur_cl")
            sat_sel   = st.slider("Satisfação (1-5)",   1,   5,   4, key="sat_cl")
            fx_sel    = st.selectbox("Faixa etária",   ["jovem", "adulto", "idoso"], key="fx_cl")

            if st.button("Classificar Perfil", use_container_width=True):
                if "classificador" in modulos:
                    try:
                        resultado = modulos["classificador"](
                            tipo_acao=tipo_sel, categoria=categ_sel,
                            duracao_seg=dur_sel, satisfacao=sat_sel,
                            idade_faixa=fx_sel,
                        )
                        perfil = resultado["perfil_previsto"]
                        probs  = resultado["probabilidades"]

                        st.markdown(f"""
<div class="fm-card" style="border-color:#000000; text-align:center; padding:20px">
<div style="font-size:0.8rem; color:#000000 !important; font-family:'Syne',sans-serif; text-transform:uppercase; letter-spacing:0.08em">Perfil previsto</div>
<div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:#FA4D4D; margin:8px 0">{perfil.title()}</div>
</div>
""", unsafe_allow_html=True)

                        st.markdown("**Probabilidades por perfil:**")
                        for p, v in sorted(probs.items(), key=lambda x: -x[1]):
                            st.markdown(f"""
<div style="display:flex; justify-content:space-between; margin-bottom:2px">
<span style="color:#334155; font-size:0.85rem">{p.title()}</span>
<span style="color:#0f766e; font-size:0.85rem; font-family:'Syne',sans-serif">{v}%</span>
</div>
<div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{v}%"></div></div>
""", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Erro na classificação: {e}")
                else:
                    st.warning("Modelo não carregado. Execute `python models/train_model.py`.")


# ══════════════════════════════════════════════════════════════
# ABA 3 — VISÃO COMPUTACIONAL
# ══════════════════════════════════════════════════════════════

with aba_visao:
    st.markdown("### 📷 Classificação de Imagem")

    col_upload, col_result = st.columns([1, 1.2], gap="large")

    with col_upload:
        st.markdown("""
<div class="fm-card">
<p style="color:#64748b; font-size:0.88rem; margin:0 0 12px 0">
Envie uma imagem para o tótem identificar sua categoria temática:
Arte, Ciência, História ou Tecnologia.
</p>
</div>
""", unsafe_allow_html=True)

        arquivo = st.file_uploader(
            "Selecione uma imagem",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        if arquivo:
            img_pil = Image.open(arquivo).convert("RGB")
            st.image(img_pil, caption="Imagem enviada", use_container_width=True)

            if st.button("Classificar Imagem →", use_container_width=True):
                if "vision" in modulos:
                    with st.spinner("Analisando imagem..."):
                        try:
                            resultado = modulos["vision"](img_pil)
                            st.session_state["ultimo_resultado_visao"] = resultado

                            if "db" in modulos and st.session_state.visitante_id:
                                modulos["db"]["inserir_interacao"](
                                    visitante_id=st.session_state.visitante_id,
                                    tipo_acao="imagem",
                                    categoria=resultado["categoria"],
                                    duracao_seg=15,
                                    satisfacao=4,
                                )
                        except Exception as e:
                            st.error(f"Erro na classificação: {e}")
                else:
                    st.warning("Módulo de visão indisponível. Execute `python modules/vision.py`.")

    with col_result:
        res = st.session_state.get("ultimo_resultado_visao")
        if res:
            cat   = res["categoria"]
            probs = res["probabilidades"]
            badge_class = f"badge-{cat}"

            st.markdown(f"""
<div class="fm-card" style="text-align:center; padding:28px">
<div style="font-size:0.75rem; color:#64748b; font-family:'Syne',sans-serif; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:12px">Categoria identificada</div>
<span class="categoria-badge {badge_class}" style="font-size:1.1rem; padding:10px 28px">{cat.upper()}</span>
</div>
""", unsafe_allow_html=True)

            st.markdown("**Confiança por categoria:**")
            cores = {"arte": "#b91c1c", "ciencia": "#0369a1", "historia": "#b45309", "tecnologia": "#15803d"}
            for c, v in sorted(probs.items(), key=lambda x: -x[1]):
                cor = cores.get(c, "#0f766e")
                st.markdown(f"""
<div style="display:flex; justify-content:space-between; margin-bottom:2px">
<span style="color:#334155; font-size:0.85rem">{c.title()}</span>
<span style="color:{cor}; font-size:0.85rem; font-family:'Syne',sans-serif">{v}%</span>
</div>
<div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{v}%; background:{cor}"></div></div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="fm-card" style="text-align:center; padding:48px 24px">
<div style="font-size:3rem; margin-bottom:12px">📷</div>
<div style="color:#64748b; font-size:0.9rem">
Envie uma imagem ao lado para ver a classificação aqui.
</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ABA 4 — ANALYTICS
# ══════════════════════════════════════════════════════════════

with aba_analytics:
    st.markdown("### 📊 Painel de Analytics")

    if "analytics" not in modulos or "db" not in modulos:
        st.warning("Módulos de analytics ou banco indisponíveis.")
    else:
        try:
            # Métricas resumidas
            interacoes = modulos["db"]["listar_interacoes"](limit=1000)
            total      = len(interacoes)
            sat_media  = round(sum(r.get("satisfacao", 0) for r in interacoes) / total, 2) if total else 0
            categorias = modulos["db"]["contar_por_categoria"]()
            top_cat    = categorias[0]["categoria"].title() if categorias else "—"

            c1, c2, c3, c4 = st.columns(4)
            for col, valor, label in [
                (c1, total,      "Interações totais"),
                (c2, sat_media,  "Satisfação média"),
                (c3, top_cat,    "Categoria top"),
                (c4, len(set(r.get("nome","") for r in interacoes)), "Visitantes únicos"),
            ]:
                with col:
                    st.markdown(f"""
                        <div class="fm-metric">
                        <div class="valor">{valor}</div>
                        <div class="label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gráficos
            col_g1, col_g2 = st.columns(2, gap="large")
            with col_g1:
                fig = modulos["analytics"]["por_categoria"]()
                if fig: st.pyplot(fig)
            with col_g2:
                fig = modulos["analytics"]["satisfacao"]()
                if fig: st.pyplot(fig)

            col_g3, col_g4 = st.columns(2, gap="large")
            with col_g3:
                fig = modulos["analytics"]["por_hora"]()
                if fig: st.pyplot(fig)
            with col_g4:
                fig = modulos["analytics"]["perfis"]()
                if fig: st.pyplot(fig)

        except Exception as e:
            st.error(f"Erro ao carregar analytics: {e}")

    # Tabela de interações recentes
    st.markdown("---")
    st.markdown("#### Interações Recentes")
    if "db" in modulos:
        try:
            rows = modulos["db"]["listar_interacoes"](limit=20)
            if rows:
                import pandas as pd
                df = pd.DataFrame(rows)[["nome", "perfil", "tipo_acao", "categoria", "duracao_seg", "satisfacao"]]
                df.columns = ["Visitante", "Perfil", "Tipo", "Categoria", "Duração (s)", "Satisfação"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhuma interação registrada ainda.")
        except Exception as e:
            st.error(f"Erro ao carregar tabela: {e}")


# ─────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding:32px 0 16px; color:#94a3b8; font-size:0.78rem; font-family:'Syne',sans-serif; letter-spacing:0.05em">
TÓTEM INTELIGENTE FLEXMEDIA · FIAP CHALLENGE SPRINT 4 · 2025
</div>
""", unsafe_allow_html=True)