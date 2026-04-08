"""
data/gerar_dados.py
─────────────────────────────────────────────────────────────
Script de geração de dados simulados para o Tótem FlexMedia.
Popula o banco Oracle com visitantes e interações realistas,
e também exporta um CSV para uso no treinamento do modelo de IA.
─────────────────────────────────────────────────────────────
"""

import sys
import os
import random
import csv
from datetime import datetime, timedelta

# Garante que os módulos do projeto estão no path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker
from modules.db import (
    criar_tabelas,
    inserir_visitante,
    inserir_interacao,
    registrar_log
)

fake = Faker("pt_BR")
random.seed(42)

# ─────────────────────────────────────────────────────────────
# CONSTANTES DE DOMÍNIO
# ─────────────────────────────────────────────────────────────

PERFIS = ["estudante", "turista", "pesquisador", "profissional"]
FAIXAS = ["jovem", "adulto", "idoso"]
TIPOS_ACAO = ["chatbot", "imagem", "menu", "busca"]
CATEGORIAS = ["arte", "ciencia", "historia", "tecnologia"]

# Probabilidades por perfil (qual categoria cada perfil tende a escolher)
PREFS_PERFIL = {
    "estudante":     {"ciencia": 0.4, "historia": 0.3, "arte": 0.2, "tecnologia": 0.1},
    "turista":       {"arte": 0.4, "historia": 0.35, "ciencia": 0.15, "tecnologia": 0.1},
    "pesquisador":   {"ciencia": 0.45, "tecnologia": 0.3, "historia": 0.15, "arte": 0.1},
    "profissional":  {"tecnologia": 0.45, "ciencia": 0.3, "arte": 0.15, "historia": 0.1},
}

# Faixa de duração (segundos) por tipo de ação
DURACAO_ACAO = {
    "chatbot": (30, 180),
    "imagem":  (10, 60),
    "menu":    (5, 30),
    "busca":   (15, 90),
}


def escolher_categoria(perfil: str) -> str:
    """Escolhe uma categoria com base nas preferências do perfil."""
    prefs = PREFS_PERFIL[perfil]
    return random.choices(list(prefs.keys()), weights=list(prefs.values()))[0]


def gerar_satisfacao(duracao: int, categoria: str) -> int:
    """
    Gera uma nota de satisfação (1-5) com leve correlação:
    interações mais longas tendem a ter satisfação maior.
    """
    base = min(5, max(1, int(duracao / 40) + 1))
    ruido = random.randint(-1, 1)
    return max(1, min(5, base + ruido))


# ─────────────────────────────────────────────────────────────
# GERAÇÃO E INSERÇÃO NO BANCO
# ─────────────────────────────────────────────────────────────

def popular_banco(n_visitantes: int = 100, interacoes_por_visitante: tuple = (1, 5)):
    """
    Insere N visitantes e suas interações no banco Oracle.
    Retorna a lista de registros gerados (para exportar CSV).
    """
    print(f"\n[DADOS] Criando tabelas (se não existirem)...")
    criar_tabelas()

    registros_csv = []

    print(f"[DADOS] Gerando {n_visitantes} visitantes...\n")
    for i in range(n_visitantes):
        perfil = random.choice(PERFIS)
        faixa = random.choice(FAIXAS)
        nome = fake.name()

        vid = inserir_visitante(nome=nome, perfil=perfil, idade_faixa=faixa)

        n_interacoes = random.randint(*interacoes_por_visitante)
        for _ in range(n_interacoes):
            tipo = random.choice(TIPOS_ACAO)
            categoria = escolher_categoria(perfil)
            duracao = random.randint(*DURACAO_ACAO[tipo])
            satisfacao = gerar_satisfacao(duracao, categoria)

            inserir_interacao(
                visitante_id=vid,
                tipo_acao=tipo,
                categoria=categoria,
                duracao_seg=duracao,
                satisfacao=satisfacao
            )

            registros_csv.append({
                "perfil": perfil,
                "idade_faixa": faixa,
                "tipo_acao": tipo,
                "categoria": categoria,
                "duracao_seg": duracao,
                "satisfacao": satisfacao,
            })

        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{n_visitantes} visitantes inseridos...")

    registrar_log("gerar_dados", f"{n_visitantes} visitantes gerados com sucesso.", "INFO")
    print(f"\n[DADOS] Inserção concluída. Total de interações: {len(registros_csv)}")
    return registros_csv


# ─────────────────────────────────────────────────────────────
# EXPORTAÇÃO CSV
# ─────────────────────────────────────────────────────────────

def exportar_csv(registros: list[dict], caminho: str = "data/dataset.csv"):
    """Salva os registros em CSV para uso no treinamento do modelo."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    colunas = ["perfil", "idade_faixa", "tipo_acao", "categoria", "duracao_seg", "satisfacao"]

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(registros)

    print(f"[CSV] Dataset exportado para: {caminho} ({len(registros)} linhas)")


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    registros = popular_banco(n_visitantes=150, interacoes_por_visitante=(2, 6))
    exportar_csv(registros, caminho="data/dataset.csv")
    print("\n[OK] Dia 1 concluído. Banco populado e CSV gerado.")
