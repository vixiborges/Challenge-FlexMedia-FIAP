"""
models/train_model.py
─────────────────────────────────────────────────────────────
Treinamento do modelo de classificação de perfil de visitante.

O modelo recebe como entrada características da interação:
  - tipo_acao      (chatbot, imagem, menu, busca)
  - categoria      (arte, ciencia, historia, tecnologia)
  - duracao_seg    (tempo de interação em segundos)
  - satisfacao     (avaliação de 1 a 5)
  - idade_faixa    (jovem, adulto, idoso)

E prediz o perfil do visitante:
  → estudante | turista | pesquisador | profissional

Pipeline:
  1. Carrega dataset (CSV gerado pelo gerar_dados.py)
  2. Pré-processa e codifica variáveis categóricas
  3. Divide em treino (80%) e teste (20%)
  4. Treina Random Forest Classifier
  5. Avalia com acurácia, relatório de classificação e matriz de confusão
  6. Salva o modelo e o encoder em arquivos .pkl
─────────────────────────────────────────────────────────────
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ─────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_CSV = os.path.join(BASE_DIR, "data", "dataset.csv")
MODEL_PATH  = os.path.join(BASE_DIR, "models", "model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")
GRAFICO_CM  = os.path.join(BASE_DIR, "models", "confusion_matrix.png")
GRAFICO_IMP = os.path.join(BASE_DIR, "models", "feature_importance.png")


# ─────────────────────────────────────────────────────────────
# 1. CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────────────────────

def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega o CSV gerado pelo gerar_dados.py."""
    if not os.path.exists(caminho):
        print(f"[ERRO] Dataset não encontrado em: {caminho}")
        print("       Execute primeiro: python data/gerar_dados.py")
        sys.exit(1)

    df = pd.read_csv(caminho)
    print(f"[DADOS] Dataset carregado: {len(df)} registros, {df.shape[1]} colunas")
    print(f"[DADOS] Distribuição de perfis:\n{df['perfil'].value_counts().to_string()}\n")
    return df


# ─────────────────────────────────────────────────────────────
# 2. PRÉ-PROCESSAMENTO
# ─────────────────────────────────────────────────────────────

COLUNAS_CATEGORICAS = ["tipo_acao", "categoria", "idade_faixa"]
FEATURES = ["tipo_acao", "categoria", "duracao_seg", "satisfacao", "idade_faixa"]
TARGET   = "perfil"


def preprocessar(df: pd.DataFrame) -> tuple:
    """
    Codifica variáveis categóricas com LabelEncoder.
    Retorna X (features), y (target) e o dicionário de encoders.
    """
    df_proc = df.copy()
    encoders = {}

    for col in COLUNAS_CATEGORICAS:
        le = LabelEncoder()
        df_proc[col] = le.fit_transform(df_proc[col])
        encoders[col] = le
        print(f"[PRÉ-PROC] '{col}' codificado → classes: {list(le.classes_)}")

    # Codifica o target também
    le_target = LabelEncoder()
    df_proc[TARGET] = le_target.fit_transform(df_proc[TARGET])
    encoders[TARGET] = le_target
    print(f"[PRÉ-PROC] '{TARGET}' codificado → classes: {list(le_target.classes_)}\n")

    X = df_proc[FEATURES].values
    y = df_proc[TARGET].values

    return X, y, encoders


# ─────────────────────────────────────────────────────────────
# 3. DIVISÃO TREINO / TESTE
# ─────────────────────────────────────────────────────────────

def dividir_dados(X, y, test_size: float = 0.2, random_state: int = 42):
    """Divide os dados em conjuntos de treino e teste."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"[SPLIT] Treino: {len(X_train)} amostras | Teste: {len(X_test)} amostras\n")
    return X_train, X_test, y_train, y_test


# ─────────────────────────────────────────────────────────────
# 4. TREINAMENTO DO MODELO
# ─────────────────────────────────────────────────────────────

def treinar_modelo(X_train, y_train) -> RandomForestClassifier:
    """
    Treina um RandomForestClassifier com 100 árvores.
    Random Forest foi escolhido por:
      - Boa performance com dados tabulares mistos
      - Resistência a overfitting
      - Geração nativa de importância de features
    """
    print("[TREINO] Iniciando treinamento do Random Forest...")

    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1      # usa todos os núcleos disponíveis
    )
    modelo.fit(X_train, y_train)

    print("[TREINO] Treinamento concluído.\n")
    return modelo


# ─────────────────────────────────────────────────────────────
# 5. AVALIAÇÃO
# ─────────────────────────────────────────────────────────────

def avaliar_modelo(modelo, X_train, X_test, y_train, y_test, encoders):
    """Avalia o modelo com métricas e gera gráficos."""
    classes = encoders[TARGET].classes_

    # Acurácia no treino e teste
    acc_treino = accuracy_score(y_train, modelo.predict(X_train))
    acc_teste  = accuracy_score(y_test,  modelo.predict(X_test))

    print("=" * 55)
    print("  RESULTADOS DA AVALIAÇÃO")
    print("=" * 55)
    print(f"  Acurácia no Treino : {acc_treino * 100:.2f}%")
    print(f"  Acurácia no Teste  : {acc_teste  * 100:.2f}%")

    # Validação cruzada (5-fold) para estimativa mais robusta
    cv_scores = cross_val_score(modelo, X_train, y_train, cv=5, scoring="accuracy")
    print(f"  Cross-Val (5-fold) : {cv_scores.mean() * 100:.2f}% ± {cv_scores.std() * 100:.2f}%")
    print("=" * 55)

    # Relatório completo
    y_pred = modelo.predict(X_test)
    print("\n  Relatório de Classificação:\n")
    print(classification_report(y_test, y_pred, target_names=classes))

    # Gráfico 1: Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(7, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=classes, yticklabels=classes
    )
    plt.title("Matriz de Confusão — Classificador de Perfil")
    plt.xlabel("Previsto")
    plt.ylabel("Real")
    plt.tight_layout()
    plt.savefig(GRAFICO_CM, dpi=150)
    plt.close()
    print(f"[GRÁFICO] Matriz de confusão salva em: {GRAFICO_CM}")

    # Gráfico 2: Importância das Features
    importancias = modelo.feature_importances_
    feat_df = pd.DataFrame({
        "feature": FEATURES,
        "importancia": importancias
    }).sort_values("importancia", ascending=True)

    plt.figure(figsize=(7, 4))
    plt.barh(feat_df["feature"], feat_df["importancia"], color="#2563EB")
    plt.title("Importância das Features — Random Forest")
    plt.xlabel("Importância")
    plt.tight_layout()
    plt.savefig(GRAFICO_IMP, dpi=150)
    plt.close()
    print(f"[GRÁFICO] Importância das features salva em: {GRAFICO_IMP}\n")

    return acc_teste


# ─────────────────────────────────────────────────────────────
# 6. PERSISTÊNCIA DO MODELO
# ─────────────────────────────────────────────────────────────

def salvar_modelo(modelo, encoders):
    """Salva o modelo treinado e os encoders em arquivos .pkl."""
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    joblib.dump(modelo,   MODEL_PATH)
    joblib.dump(encoders, ENCODER_PATH)

    print(f"[SALVO] Modelo   → {MODEL_PATH}")
    print(f"[SALVO] Encoders → {ENCODER_PATH}")


def carregar_modelo():
    """
    Carrega o modelo e os encoders salvos.
    Usado pelos módulos da aplicação (chatbot, analytics).
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Modelo não encontrado. Execute: python models/train_model.py"
        )
    modelo   = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    return modelo, encoders


# ─────────────────────────────────────────────────────────────
# 7. FUNÇÃO DE PREDIÇÃO (usada pelo app Streamlit)
# ─────────────────────────────────────────────────────────────

def prever_perfil(tipo_acao: str, categoria: str,
                  duracao_seg: int, satisfacao: int,
                  idade_faixa: str) -> dict:
    """
    Recebe os dados de uma interação e retorna o perfil previsto
    com as probabilidades de cada classe.

    Exemplo de uso:
        resultado = prever_perfil("chatbot", "ciencia", 90, 4, "jovem")
        print(resultado["perfil_previsto"])  # → "estudante"
    """
    modelo, encoders = carregar_modelo()

    # Codifica os valores categóricos com os encoders treinados
    tipo_enc   = encoders["tipo_acao"].transform([tipo_acao])[0]
    categ_enc  = encoders["categoria"].transform([categoria])[0]
    idade_enc  = encoders["idade_faixa"].transform([idade_faixa])[0]

    X = np.array([[tipo_enc, categ_enc, duracao_seg, satisfacao, idade_enc]])

    perfil_idx   = modelo.predict(X)[0]
    probabilidades = modelo.predict_proba(X)[0]
    perfil_nome  = encoders[TARGET].inverse_transform([perfil_idx])[0]

    resultado = {
        "perfil_previsto": perfil_nome,
        "probabilidades": {
            classe: round(float(prob) * 100, 1)
            for classe, prob in zip(encoders[TARGET].classes_, probabilidades)
        }
    }
    return resultado


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🤖 Iniciando pipeline de treinamento — Tótem FlexMedia\n")

    df                             = carregar_dados(DATASET_CSV)
    X, y, encoders                 = preprocessar(df)
    X_train, X_test, y_train, y_test = dividir_dados(X, y)
    modelo                         = treinar_modelo(X_train, y_train)
    acuracia                       = avaliar_modelo(modelo, X_train, X_test, y_train, y_test, encoders)
    salvar_modelo(modelo, encoders)

    print("\n✅ Pipeline concluído com sucesso!")
    print(f"   Acurácia final no conjunto de teste: {acuracia * 100:.2f}%\n")
