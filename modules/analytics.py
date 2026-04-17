"""
modules/analytics.py  (v2 — tema light + correção de gráficos)
─────────────────────────────────────────────────────────────
Correção aplicada: cada função agora chama plt.close("all")
antes de criar sua figura, evitando que o Streamlit reutilize
figuras antigas quando as funções são chamadas via cache.

Tema atualizado para light (fundo branco, acento #FA4D4D),
consistente com o app.py revisado.
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

matplotlib.use("Agg")   # backend não-interativo — obrigatório no Streamlit

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────────────────────
# PALETAS — tema light
# ─────────────────────────────────────────────────────────────

CORES_CATEGORIA = {
    "arte":       "#b91c1c",
    "ciencia":    "#0369a1",
    "historia":   "#b45309",
    "tecnologia": "#15803d",
}

CORES_PERFIL = {
    "estudante":    "#7c3aed",
    "turista":      "#db2777",
    "pesquisador":  "#059669",
    "profissional": "#2563eb",
}

CORES_ACAO = {
    "chatbot": "#15803d",
    "imagem":  "#0369a1",
    "menu":    "#b45309",
    "busca":   "#b91c1c",
}

# Tema light dos gráficos
TEMA = {
    "bg":      "#ffffff",
    "axes":    "#f8fafc",
    "grid":    "#e2e8f0",
    "texto":   "#64748b",
    "titulo":  "#1e293b",
    "borda":   "#e2e8f0",
    "acento":  "#FA4D4D",
}

def _aplicar_tema(ax, fig):
    """Aplica o tema light em qualquer eixo matplotlib."""
    fig.patch.set_facecolor(TEMA["bg"])
    ax.set_facecolor(TEMA["axes"])
    ax.tick_params(colors=TEMA["texto"], labelsize=9)
    ax.xaxis.label.set_color(TEMA["texto"])
    ax.yaxis.label.set_color(TEMA["texto"])
    ax.title.set_color(TEMA["titulo"])
    for spine in ax.spines.values():
        spine.set_edgecolor(TEMA["borda"])
    ax.grid(color=TEMA["grid"], linestyle="--", linewidth=0.6, zorder=0)


# ─────────────────────────────────────────────────────────────
# CARREGAMENTO DE DADOS
# ─────────────────────────────────────────────────────────────

def _carregar_df() -> pd.DataFrame:
    """
    Tenta carregar do Oracle; fallback para CSV local.
    """
    try:
        from modules.db import listar_interacoes
        rows = listar_interacoes(limit=2000)
        if rows:
            df = pd.DataFrame(rows)
            if "registrado_em" in df.columns:
                df["registrado_em"] = pd.to_datetime(df["registrado_em"], errors="coerce")
                df["hora"] = df["registrado_em"].dt.hour
            return df
    except Exception:
        pass

    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "dataset.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df["hora"] = np.random.randint(8, 20, size=len(df))
        return df

    return pd.DataFrame()


# ─────────────────────────────────────────────────────────────
# GRÁFICO 1 — INTERAÇÕES POR CATEGORIA
# ─────────────────────────────────────────────────────────────

def grafico_interacoes_por_categoria():
    """Barras horizontais com volume de interações por categoria."""
    # ← CORREÇÃO: fecha qualquer figura aberta antes de criar a nova
    plt.close("all")

    df = _carregar_df()
    if df.empty or "categoria" not in df.columns:
        return None

    contagem = (
        df["categoria"]
        .value_counts()
        .reindex(["arte", "ciencia", "historia", "tecnologia"], fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6, 3.6))
    _aplicar_tema(ax, fig)

    categorias = contagem.index.tolist()
    valores    = contagem.values
    cores      = [CORES_CATEGORIA.get(c, "#888") for c in categorias]

    bars = ax.barh(categorias, valores, color=cores, height=0.52, zorder=3)

    for bar, val in zip(bars, valores):
        ax.text(
            bar.get_width() + max(valores) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center", ha="left",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
        )

    ax.set_xlabel("Número de interações", fontsize=9)
    ax.set_title("Interações por Categoria", fontsize=12,
                 fontweight="bold", pad=10, color=TEMA["titulo"])
    ax.set_yticklabels([c.title() for c in categorias], fontsize=10)
    ax.set_xlim(0, max(valores) * 1.18 if max(valores) > 0 else 1)
    ax.spines[["top", "right", "left"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 2 — SATISFAÇÃO POR TIPO DE AÇÃO
# ─────────────────────────────────────────────────────────────

def grafico_satisfacao_por_tipo():
    """Barras verticais com satisfação média por tipo de ação."""
    plt.close("all")

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

    if medias.empty:
        return None

    fig, ax = plt.subplots(figsize=(6, 3.6))
    _aplicar_tema(ax, fig)

    tipos = medias.index.tolist()
    vals  = medias.values
    cores = [CORES_ACAO.get(t, "#888") for t in tipos]

    bars = ax.bar(tipos, vals, color=cores, width=0.48, zorder=3)

    media_geral = df["satisfacao"].mean()
    ax.axhline(media_geral, color="#94a3b8", linestyle="--", linewidth=1.2, zorder=4)
    ax.text(
        len(tipos) - 0.55, media_geral + 0.06,
        f"Média: {media_geral:.2f}",
        color=TEMA["texto"], fontsize=8, ha="right",
    )

    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{val:.2f}",
            ha="center", va="bottom",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
        )

    ax.set_ylim(0, 5.8)
    ax.set_ylabel("Satisfação média (1–5)", fontsize=9)
    ax.set_title("Satisfação por Tipo de Ação", fontsize=12,
                 fontweight="bold", pad=10, color=TEMA["titulo"])
    ax.set_xticklabels([t.title() for t in tipos], fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 3 — INTERAÇÕES POR HORA DO DIA
# ─────────────────────────────────────────────────────────────

def grafico_interacoes_por_hora():
    """Linha temporal de interações por hora do dia com destaque de pico."""
    plt.close("all")

    df = _carregar_df()
    if df.empty or "hora" not in df.columns:
        return None

    por_hora = (
        df["hora"]
        .value_counts()
        .reindex(range(8, 21), fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6, 3.6))
    _aplicar_tema(ax, fig)

    horas  = por_hora.index.tolist()
    counts = por_hora.values

    ax.fill_between(horas, counts, alpha=0.12, color=TEMA["acento"], zorder=2)
    ax.plot(horas, counts, color=TEMA["acento"], linewidth=2.5,
            marker="o", markersize=5, zorder=3)

    idx_pico = int(np.argmax(counts))
    ax.annotate(
        f"Pico: {horas[idx_pico]}h ({counts[idx_pico]})",
        xy=(horas[idx_pico], counts[idx_pico]),
        xytext=(horas[idx_pico] + 0.6, counts[idx_pico] + max(counts) * 0.1),
        color="#b45309", fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.2),
    )

    ax.set_xlabel("Hora do dia", fontsize=9)
    ax.set_ylabel("Nº de interações", fontsize=9)
    ax.set_title("Interações por Hora do Dia", fontsize=12,
                 fontweight="bold", pad=10, color=TEMA["titulo"])
    ax.set_xticks(horas)
    ax.set_xticklabels([f"{h}h" for h in horas], fontsize=8, rotation=45)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# GRÁFICO 4 — DISTRIBUIÇÃO DE PERFIS (donut)
# ─────────────────────────────────────────────────────────────

def grafico_perfis_visitantes():
    """Donut com proporção de cada perfil de visitante."""
    plt.close("all")

    df = _carregar_df()
    if df.empty or "perfil" not in df.columns:
        return None

    df_filtrado = df[df["perfil"] != "indefinido"]
    if df_filtrado.empty:
        return None

    contagem = df_filtrado["perfil"].value_counts()
    perfis   = contagem.index.tolist()
    valores  = contagem.values
    cores    = [CORES_PERFIL.get(p, "#888") for p in perfis]

    fig, ax = plt.subplots(figsize=(6, 3.6))
    _aplicar_tema(ax, fig)
    ax.set_facecolor(TEMA["bg"])
    fig.patch.set_facecolor(TEMA["bg"])

    wedges, _, autotexts = ax.pie(
        valores,
        labels=None,
        colors=cores,
        autopct="%1.1f%%",
        pctdistance=0.78,
        startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=TEMA["bg"], linewidth=2),
    )

    for at in autotexts:
        at.set_color("#ffffff")
        at.set_fontsize(8)
        at.set_fontweight("bold")

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

    ax.text(0, 0, f"{sum(valores)}\nvisitas",
            ha="center", va="center",
            color=TEMA["titulo"], fontsize=10, fontweight="bold",
            linespacing=1.5)

    ax.set_title("Distribuição de Perfis", fontsize=12,
                 fontweight="bold", pad=10, color=TEMA["titulo"])

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────
# EXPORTAÇÃO DO RELATÓRIO CSV
# ─────────────────────────────────────────────────────────────

def exportar_relatorio_csv(caminho: str = "data/relatorio_analitico.csv"):
    df = _carregar_df()
    if df.empty:
        print("[ANALYTICS] Sem dados para exportar.")
        return

    os.makedirs(os.path.dirname(caminho) if os.path.dirname(caminho) else ".", exist_ok=True)

    with open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write("# INTERACOES POR CATEGORIA\n")
        df["categoria"].value_counts().reset_index() \
            .rename(columns={"index": "categoria", "categoria": "total"}) \
            .to_csv(f, index=False)

        f.write("\n# SATISFACAO MEDIA POR TIPO DE ACAO\n")
        df.groupby("tipo_acao")["satisfacao"].mean().round(2).reset_index() \
            .rename(columns={"satisfacao": "media_satisfacao"}) \
            .to_csv(f, index=False)

        if "hora" in df.columns:
            f.write("\n# INTERACOES POR HORA DO DIA\n")
            df["hora"].value_counts().sort_index().reset_index() \
                .rename(columns={"index": "hora", "hora": "total"}) \
                .to_csv(f, index=False)

        if "perfil" in df.columns:
            f.write("\n# DISTRIBUICAO DE PERFIS\n")
            df[df["perfil"] != "indefinido"]["perfil"].value_counts().reset_index() \
                .rename(columns={"index": "perfil", "perfil": "total"}) \
                .to_csv(f, index=False)

    print(f"[ANALYTICS] Relatório exportado → {caminho}")


# ─────────────────────────────────────────────────────────────
# MÉTRICAS RESUMIDAS
# ─────────────────────────────────────────────────────────────

def calcular_metricas_resumo() -> dict:
    df = _carregar_df()
    if df.empty:
        return {"total_interacoes": 0, "satisfacao_media": 0,
                "categoria_top": "—", "visitantes_unicos": 0}
    return {
        "total_interacoes":  len(df),
        "satisfacao_media":  round(df["satisfacao"].mean(), 2) if "satisfacao" in df.columns else 0,
        "categoria_top":     df["categoria"].mode()[0].title() if "categoria" in df.columns else "—",
        "visitantes_unicos": df["nome"].nunique() if "nome" in df.columns else len(df),
    }


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO DIRETA
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n📊 Gerando gráficos analíticos — Tótem FlexMedia\n")
    os.makedirs("data/graficos", exist_ok=True)

    funcoes = {
        "data/graficos/interacoes_por_categoria.png": grafico_interacoes_por_categoria,
        "data/graficos/satisfacao_por_tipo.png":      grafico_satisfacao_por_tipo,
        "data/graficos/interacoes_por_hora.png":      grafico_interacoes_por_hora,
        "data/graficos/perfis_visitantes.png":        grafico_perfis_visitantes,
    }

    for caminho, func in funcoes.items():
        fig = func()
        if fig:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=TEMA["bg"])
            plt.close(fig)
            print(f"  [OK] {caminho}")
        else:
            print(f"  [AVISO] Sem dados: {caminho}")

    exportar_relatorio_csv()
    print("\n✅ Analytics concluído.")
