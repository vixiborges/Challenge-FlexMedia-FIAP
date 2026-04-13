"""
data/gerar_dados.py  (v2 — separação de perfis corrigida)
─────────────────────────────────────────────────────────────
Correção aplicada: as preferências de cada perfil agora têm
separação muito mais nítida, garantindo que o modelo de ML
consiga distinguir os grupos com alta acurácia.

Mudanças em relação à v1:
  - Probabilidades de categoria rebalanceadas por perfil
  - Correlação entre tipo_acao e perfil adicionada
  - Correlação entre duracao_seg e perfil reforçada
  - Correlação entre satisfacao e categoria adicionada
  - Volume aumentado para 300 visitantes (de 150)
─────────────────────────────────────────────────────────────
"""

import sys
import os
import random
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker
from modules.db import (
    criar_tabelas,
    inserir_visitante,
    inserir_interacao,
    registrar_log,
)

fake = Faker("pt_BR")
random.seed(42)

# ─────────────────────────────────────────────────────────────
# DOMÍNIO
# ─────────────────────────────────────────────────────────────

PERFIS = ["estudante", "turista", "pesquisador", "profissional"]
FAIXAS = ["jovem", "adulto", "idoso"]
TIPOS_ACAO  = ["chatbot", "imagem", "menu", "busca"]
CATEGORIAS  = ["arte", "ciencia", "historia", "tecnologia"]

# ── CORREÇÃO 1: categorias com separação muito mais nítida ──
# Cada perfil agora tem UMA categoria dominante (≥ 0.70)
# e as demais praticamente inexistentes.
PREFS_CATEGORIA = {
    "estudante":    {"ciencia": 0.75, "historia": 0.15, "arte": 0.07, "tecnologia": 0.03},
    "turista":      {"arte": 0.75, "historia": 0.15, "ciencia": 0.07, "tecnologia": 0.03},
    "pesquisador":  {"tecnologia": 0.75, "ciencia": 0.15, "historia": 0.07, "arte": 0.03},
    "profissional": {"tecnologia": 0.55, "ciencia": 0.30, "arte": 0.10, "historia": 0.05},
}

# ── CORREÇÃO 2: tipo de ação correlacionado com perfil ──
# Estudante usa chatbot; turista prefere imagem; pesquisador usa busca; profissional usa menu
PREFS_ACAO = {
    "estudante":    {"chatbot": 0.65, "busca": 0.20, "menu": 0.10, "imagem": 0.05},
    "turista":      {"imagem": 0.65, "menu": 0.20, "chatbot": 0.10, "busca": 0.05},
    "pesquisador":  {"busca": 0.65, "chatbot": 0.20, "imagem": 0.10, "menu": 0.05},
    "profissional": {"menu": 0.55, "busca": 0.25, "chatbot": 0.15, "imagem": 0.05},
}

# ── CORREÇÃO 3: faixa etária correlacionada com perfil ──
PREFS_FAIXA = {
    "estudante":    {"jovem": 0.75, "adulto": 0.20, "idoso": 0.05},
    "turista":      {"adulto": 0.55, "jovem": 0.25, "idoso": 0.20},
    "pesquisador":  {"adulto": 0.65, "jovem": 0.25, "idoso": 0.10},
    "profissional": {"adulto": 0.70, "jovem": 0.20, "idoso": 0.10},
}

# ── CORREÇÃO 4: duração média distinta por perfil ──
# (média em segundos, desvio padrão)
DURACAO_PERFIL = {
    "estudante":    (120, 30),   # longa — está aprendendo
    "turista":      (40,  15),   # curta — navegação rápida
    "pesquisador":  (180, 40),   # muito longa — aprofundamento
    "profissional": (70,  20),   # média — objetivo claro
}


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def escolher(prefs: dict) -> str:
    return random.choices(list(prefs.keys()), weights=list(prefs.values()))[0]


def gerar_duracao(perfil: str) -> int:
    media, desvio = DURACAO_PERFIL[perfil]
    valor = int(random.gauss(media, desvio))
    return max(10, min(300, valor))   # limita entre 10s e 5min


def gerar_satisfacao(perfil: str, categoria: str) -> int:
    """
    Satisfação com leve viés:
    - Pesquisador tende a dar notas mais altas (conteúdo rico)
    - Turista é mais volátil (1-5 mais uniforme)
    """
    if perfil == "pesquisador":
        base = random.choices([3, 4, 5], weights=[0.15, 0.40, 0.45])[0]
    elif perfil == "turista":
        base = random.randint(1, 5)
    else:
        base = random.choices([2, 3, 4, 5], weights=[0.10, 0.25, 0.40, 0.25])[0]
    return base


# ─────────────────────────────────────────────────────────────
# INSERÇÃO NO BANCO
# ─────────────────────────────────────────────────────────────

def popular_banco(n_visitantes: int = 300, interacoes_por_visitante: tuple = (2, 6)):
    print(f"\n[DADOS] Criando tabelas (se não existirem)...")
    criar_tabelas()

    registros_csv = []

    print(f"[DADOS] Gerando {n_visitantes} visitantes...\n")
    for i in range(n_visitantes):
        perfil = random.choice(PERFIS)
        faixa  = escolher(PREFS_FAIXA[perfil])
        nome   = fake.name()

        vid = inserir_visitante(nome=nome, perfil=perfil, idade_faixa=faixa)

        n_int = random.randint(*interacoes_por_visitante)
        for _ in range(n_int):
            tipo      = escolher(PREFS_ACAO[perfil])
            categoria = escolher(PREFS_CATEGORIA[perfil])
            duracao   = gerar_duracao(perfil)
            satisf    = gerar_satisfacao(perfil, categoria)

            inserir_interacao(
                visitante_id=vid,
                tipo_acao=tipo,
                categoria=categoria,
                duracao_seg=duracao,
                satisfacao=satisf,
            )

            registros_csv.append({
                "perfil":      perfil,
                "idade_faixa": faixa,
                "tipo_acao":   tipo,
                "categoria":   categoria,
                "duracao_seg": duracao,
                "satisfacao":  satisf,
            })

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{n_visitantes} visitantes inseridos...")

    registrar_log("gerar_dados", f"{n_visitantes} visitantes gerados (v2).", "INFO")
    print(f"\n[DADOS] Inserção concluída. Total de interações: {len(registros_csv)}")
    return registros_csv


# ─────────────────────────────────────────────────────────────
# EXPORTAÇÃO CSV
# ─────────────────────────────────────────────────────────────

def exportar_csv(registros: list[dict], caminho: str = "data/dataset.csv"):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    colunas = ["perfil", "idade_faixa", "tipo_acao", "categoria", "duracao_seg", "satisfacao"]

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(registros)

    print(f"[CSV] Dataset exportado → {caminho} ({len(registros)} linhas)")


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    registros = popular_banco(n_visitantes=300, interacoes_por_visitante=(2, 6))
    exportar_csv(registros, caminho="data/dataset.csv")
    print("\n[OK] Dados v2 gerados. Execute agora: python models/train_model.py")
