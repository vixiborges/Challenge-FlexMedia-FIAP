"""
modules/analytics.py
─────────────────────────────────────────────────────────────
Módulo de Analytics do Tótem FlexMedia.

Responsabilidades:
  1. Consultar o banco Oracle via db.py
  2. Transformar os dados em DataFrames Pandas
  3. Gerar 4 gráficos de engajamento prontos para o Streamlit:
       - grafico_interacoes_por_categoria()  → barras horizontais
       - grafico_satisfacao_por_tipo()       → barras agrupadas
       - grafico_interacoes_por_hora()       → linha temporal
       - grafico_perfis_visitantes()         → pizza/donut
  4. Exportar relatório analítico em CSV

Todos os gráficos seguem o tema escuro da interface e
retornam objetos matplotlib.figure.Figure para o st.pyplot().
─────────────────────────────────────────────────────────────
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────────────────────
# TEMA GLOBAL DOS GRÁFICOS
# ─────────────────────────────────────────────────────────────

CORES_CATEGORIA = {
    "arte":       "#ff6464",
    "ciencia":    "#00c8ff",
    "historia":   "#ffb432",
    "tecnologia": "#00c896",
}

CORES_PERFIL = {
    "estudante":    "#a78bfa",
    "turista":      "#f472b6",
    "pesquisador":  "#34d399",
    "profissional": "#60a5fa",
}

CORES_ACAO = {
    "chatbot": "#00c896",
    "imagem":  "#00c8ff",
    "menu":    "#ffb432",
    "busca":   "#ff6464",
}

# Tema escuro consistente com o app.py
TEMA = {
    "bg":         "#0a0e1a",
    "bg_axes":    "#111827",
    "grid":       "#1f2937",
    "texto":      "#9ca3af",
    "titulo":     "#e8f0fe",
    "borda":      "#1f2937",
}

matplotlib.rcParams.update({
    "figure.facecolor":  TEMA["bg"],
    "axes.facecolor":    TEMA["bg_axes"],
    "axes.edgecolor":    TEMA["borda"],
    "axes.labelcolor":   TEMA["texto"],
    "xtick.color":       TEMA["texto"],
    "ytick.color":       TEMA["texto"],
    "text.color":        TEMA["titulo"],
    "grid.color":        TEMA["grid"],
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "font.size":         10,
})


# ─────────────────────────────────────────────────────────────
# CARREGAMENTO DE DADOS
# ─────────────────────────────────────────────────────────────

def _carregar_df() -> pd.DataFrame:
    """
    Carrega as interações do Oracle e retorna um DataFrame.
    Fallback: lê o dataset.csv se o banco estiver indisponível.
    """
    try:
        from modules.db import listar_interacoes
        rows = listar_interacoes(limit=2000)
        if rows:
            df = pd.DataFrame(rows)
            # Garante que registrado_em é datetime
            if "registrado_em" in df.columns:
                df["registrado_em"] = pd.to_datetime(df["registrado_em"], errors="coerce")
                df["hora"] = df["registrado_em"].dt.hour
            return df
    except Exception:
        pass

    # Fallback: CSV gerado no Dia 1
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "dataset.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df["hora"] = np.random.randint(8, 20, size=len(df))   # simula hora de acesso
        return df

    return pd.DataFrame()


# ─────────────────────────────────────────────────────────────
# GRÁFICO 1 — INTERAÇÕES POR CATEGORIA (barras horizontais)
# ─────────────────────────────────────────────────────────────

def grafico_interacoes_por_categoria() -> plt.Figure | None:
    """
    Barras horizontais mostrando o volume de interações
    por categoria temática (arte, ciencia, historia, tecnologia).
    """
    df = _carregar_df()
    if df.empty or "categoria" not in df.columns:
        return None

    contagem = (
        df["categoria"]
        .value_counts()
        .reindex(["arte", "ciencia", "historia", "tecnologia"], fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(TEMA["bg"])

    categorias = contagem.index.tolist()
    valores    = contagem.values
    cores      = [CORES_CATEGORIA.get(c, "#888") for c in categorias]

    bars = ax.barh(categorias, valores, color=cores, height=0.55, zorder=3)

    # Rótulo de valor ao lado de cada barra
    for bar, val in zip(bars, valores):
        ax.text(
            bar.get_width() + max(valores) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center", ha="left",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
        )

    ax.set_xlabel("Número de interações", color=TEMA["texto"], fontsize=9)
    ax.set_title("Interações por Categoria", color=TEMA["titulo"],
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_yticklabels([c.title() for c in categorias], fontsize=10)
    ax.set_xlim(0, max(valores) * 1.18)
    ax.grid(axis="x", zorder=0)
    ax.spines[["top","right","left"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 2 — SATISFAÇÃO MÉDIA POR TIPO DE AÇÃO (barras)
# ─────────────────────────────────────────────────────────────

def grafico_satisfacao_por_tipo() -> plt.Figure | None:
    """
    Barras verticais com a satisfação média (1-5)
    para cada tipo de ação: chatbot, imagem, menu, busca.
    Inclui linha de referência na média geral.
    """
    df = _carregar_df()
    if df.empty or "satisfacao" not in df.columns or "tipo_acao" not in df.columns:
        return None

    medias = (
        df.groupby("tipo_acao")["satisfacao"]
        .mean()
        .reindex(["chatbot", "imagem", "menu", "busca"])
        .dropna()
        .round(2)
    )

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(TEMA["bg"])

    tipos = medias.index.tolist()
    vals  = medias.values
    cores = [CORES_ACAO.get(t, "#888") for t in tipos]

    bars = ax.bar(tipos, vals, color=cores, width=0.5, zorder=3)

    # Linha de média geral
    media_geral = df["satisfacao"].mean()
    ax.axhline(media_geral, color="#0f766e", linestyle="--",
               linewidth=1.2, zorder=4)
    ax.text(len(tipos) - 0.5, media_geral + 0.05,
            f"Média geral: {media_geral:.2f}",
            color=TEMA["texto"], fontsize=8, ha="right")

    # Rótulo em cima de cada barra
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{val:.2f}",
            ha="center", va="bottom",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
        )

    ax.set_ylim(0, 5.6)
    ax.set_ylabel("Satisfação média (1–5)", color=TEMA["texto"], fontsize=9)
    ax.set_title("Satisfação por Tipo de Ação", color=TEMA["titulo"],
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xticklabels([t.title() for t in tipos], fontsize=10)
    ax.grid(axis="y", zorder=0)
    ax.spines[["top","right"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 3 — INTERAÇÕES POR HORA DO DIA (linha)
# ─────────────────────────────────────────────────────────────

def grafico_interacoes_por_hora() -> plt.Figure | None:
    """
    Gráfico de linha mostrando o volume de interações
    distribuído pelas horas do dia (08h–20h).
    Útil para identificar horários de pico de visitação.
    """
    df = _carregar_df()
    if df.empty or "hora" not in df.columns:
        return None

    por_hora = (
        df["hora"]
        .value_counts()
        .reindex(range(8, 21), fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(TEMA["bg"])

    horas  = por_hora.index.tolist()
    counts = por_hora.values

    # Área preenchida + linha
    ax.fill_between(horas, counts, alpha=0.15, color="#00c896", zorder=2)
    ax.plot(horas, counts, color="#00c896", linewidth=2.5,
            marker="o", markersize=5, zorder=3)

    # Destaque no horário de pico
    idx_pico = int(np.argmax(counts))
    ax.annotate(
        f"Pico: {horas[idx_pico]}h ({counts[idx_pico]})",
        xy=(horas[idx_pico], counts[idx_pico]),
        xytext=(horas[idx_pico] + 0.5, counts[idx_pico] + max(counts) * 0.08),
        color="#ffb432", fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#ffb432", lw=1.2),
    )

    ax.set_xlabel("Hora do dia", color=TEMA["texto"], fontsize=9)
    ax.set_ylabel("Nº de interações", color=TEMA["texto"], fontsize=9)
    ax.set_title("Interações por Hora do Dia", color=TEMA["titulo"],
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(horas)
    ax.set_xticklabels([f"{h}h" for h in horas], fontsize=8, rotation=45)
    ax.grid(axis="y", zorder=0)
    ax.spines[["top","right"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 4 — DISTRIBUIÇÃO DE PERFIS (donut)
# ─────────────────────────────────────────────────────────────

def grafico_perfis_visitantes() -> plt.Figure | None:
    """
    Gráfico donut mostrando a proporção de cada perfil
    de visitante identificado pelo modelo de classificação.
    """
    df = _carregar_df()
    if df.empty or "perfil" not in df.columns:
        return None

    # Remove perfis indefinidos (cadastros sem interação classificada)
    df_filtrado = df[df["perfil"] != "indefinido"]
    if df_filtrado.empty:
        return None

    contagem = df_filtrado["perfil"].value_counts()
    perfis   = contagem.index.tolist()
    valores  = contagem.values
    cores    = [CORES_PERFIL.get(p, "#888") for p in perfis]

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(TEMA["bg"])

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=None,
        colors=cores,
        autopct="%1.1f%%",
        pctdistance=0.78,
        startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=TEMA["bg"], linewidth=2),
    )

    for at in autotexts:
        at.set_color(TEMA["bg"])
        at.set_fontsize(9)
        at.set_fontweight("bold")

    # Legenda lateral
    legenda = [
        mpatches.Patch(color=cores[i], label=perfis[i].title())
        for i in range(len(perfis))
    ]
    ax.legend(
        handles=legenda,
        loc="center left",
        bbox_to_anchor=(0.85, 0.5),
        frameon=False,
        labelcolor=TEMA["titulo"],
        fontsize=9,
    )

    # Texto central do donut
    ax.text(0, 0, f"{sum(valores)}\nvisitas",
            ha="center", va="center",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
            linespacing=1.5)

    ax.set_title("Distribuição de Perfis", color=TEMA["titulo"],
                 fontsize=12, fontweight="bold", pad=12)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# EXPORTAÇÃO DO RELATÓRIO ANALÍTICO
# ─────────────────────────────────────────────────────────────

def exportar_relatorio_csv(caminho: str = "data/relatorio_analitico.csv"):
    """
    Exporta um relatório consolidado em CSV com:
      - Total de interações por categoria
      - Satisfação média por tipo de ação
      - Volume de interações por hora
      - Contagem de perfis de visitantes
    Usado como base para o Relatório Analítico Final da Sprint 4.
    """
    df = _carregar_df()
    if df.empty:
        print("[ANALYTICS] Sem dados para exportar.")
        return

    os.makedirs(os.path.dirname(caminho) if os.path.dirname(caminho) else ".", exist_ok=True)

    with open(caminho, "w", encoding="utf-8", newline="") as f:

        # Seção 1
        f.write("# INTERAÇÕES POR CATEGORIA\n")
        df["categoria"].value_counts().reset_index() \
            .rename(columns={"index": "categoria", "categoria": "total"}) \
            .to_csv(f, index=False)

        f.write("\n# SATISFAÇÃO MÉDIA POR TIPO DE AÇÃO\n")
        df.groupby("tipo_acao")["satisfacao"].mean().round(2).reset_index() \
            .rename(columns={"satisfacao": "media_satisfacao"}) \
            .to_csv(f, index=False)

        if "hora" in df.columns:
            f.write("\n# INTERAÇÕES POR HORA DO DIA\n")
            df["hora"].value_counts().sort_index().reset_index() \
                .rename(columns={"index": "hora", "hora": "total"}) \
                .to_csv(f, index=False)

        if "perfil" in df.columns:
            f.write("\n# DISTRIBUIÇÃO DE PERFIS\n")
            df[df["perfil"] != "indefinido"]["perfil"].value_counts().reset_index() \
                .rename(columns={"index": "perfil", "perfil": "total"}) \
                .to_csv(f, index=False)

    print(f"[ANALYTICS] Relatório exportado → {caminho}")


# ─────────────────────────────────────────────────────────────
# MÉTRICAS RESUMIDAS (usadas no topo da aba Analytics)
# ─────────────────────────────────────────────────────────────

def calcular_metricas_resumo() -> dict:
    """
    Retorna um dict com as 4 métricas exibidas no topo do dashboard:
      - total_interacoes
      - satisfacao_media
      - categoria_top
      - visitantes_unicos
    """
    df = _carregar_df()
    if df.empty:
        return {
            "total_interacoes":  0,
            "satisfacao_media":  0,
            "categoria_top":     "—",
            "visitantes_unicos": 0,
        }

    return {
        "total_interacoes":  len(df),
        "satisfacao_media":  round(df["satisfacao"].mean(), 2) if "satisfacao" in df.columns else 0,
        "categoria_top":     df["categoria"].mode()[0].title() if "categoria" in df.columns else "—",
        "visitantes_unicos": df["nome"].nunique() if "nome" in df.columns else len(df),
    }


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO DIRETA — gera e salva todos os gráficos
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n📊 Gerando relatório analítico — Tótem FlexMedia\n")

    os.makedirs("data/graficos", exist_ok=True)

    graficos = {
        "data/graficos/interacoes_por_categoria.png": grafico_interacoes_por_categoria,
        "data/graficos/satisfacao_por_tipo.png":      grafico_satisfacao_por_tipo,
        "data/graficos/interacoes_por_hora.png":      grafico_interacoes_por_hora,
        "data/graficos/perfis_visitantes.png":        grafico_perfis_visitantes,
    }

    for caminho, func in graficos.items():
        fig = func()
        if fig:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=TEMA["bg"])
            plt.close(fig)
            print(f"  [OK] {caminho}")
        else:
            print(f"  [AVISO] Sem dados para: {caminho}")

    exportar_relatorio_csv()

    metricas = calcular_metricas_resumo()
    print("\n  Métricas resumo:")
    for k, v in metricas.items():
        print(f"    {k:25s}: {v}")

    print("\n✅ Analytics concluído.")
