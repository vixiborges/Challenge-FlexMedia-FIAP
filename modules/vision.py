"""
modules/vision.py
─────────────────────────────────────────────────────────────
Módulo de Visão Computacional do Tótem FlexMedia.

Responsabilidades:
  1. Pré-processar imagens recebidas (câmera ou upload)
  2. Extrair features visuais via histograma de cores (HSV)
  3. Classificar a imagem em uma das 4 categorias do tótem:
     arte | ciencia | historia | tecnologia
  4. Registrar o resultado no banco de dados Oracle

Abordagem:
  Como o ambiente pode não ter câmera disponível, o módulo
  suporta dois modos de entrada:
    - Arquivo de imagem (upload via Streamlit)
    - Dataset simulado (imagens de exemplo por categoria)

  A classificação usa um SVM treinado sobre features de cor
  (histograma HSV) — leve, rápido e sem dependência de GPU.
─────────────────────────────────────────────────────────────
"""

import os
import sys
import cv2
import joblib
import numpy as np
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────

BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VISION_MODEL_PATH = os.path.join(BASE_DIR, "models", "vision_model.pkl")
DATASET_DIR       = os.path.join(BASE_DIR, "data", "imagens")

CATEGORIAS = ["arte", "ciencia", "historia", "tecnologia"]

# Paletas de cor HSV associadas a cada categoria
# Usadas na geração do dataset simulado
PALETAS_CATEGORIA = {
    "arte": [
        (0,   200, 200),   # vermelho vibrante
        (20,  220, 210),   # laranja
        (280, 180, 190),   # violeta
        (340, 200, 210),   # rosa
    ],
    "ciencia": [
        (200, 180, 220),   # azul claro
        (220, 200, 230),   # azul médio
        (180, 160, 210),   # ciano
        (240, 150, 200),   # azul escuro
    ],
    "historia": [
        (30,  120, 160),   # marrom claro
        (25,  140, 140),   # bege escuro
        (35,  100, 120),   # sépia
        (20,   80, 100),   # tom terroso
    ],
    "tecnologia": [
        (120, 200, 220),   # verde neon
        (140, 180, 200),   # verde tecnológico
        (100, 160, 180),   # verde escuro
        (160, 150, 190),   # verde azulado
    ],
}


# ─────────────────────────────────────────────────────────────
# 1. GERAÇÃO DO DATASET SIMULADO
# ─────────────────────────────────────────────────────────────

def gerar_dataset_simulado(n_por_categoria: int = 60):
    """
    Gera imagens sintéticas por categoria usando paletas de cor.
    Cada imagem é um gradiente HSV com ruído gaussiano,
    simulando fotos reais com características visuais distintas.

    Salva em: data/imagens/<categoria>/img_NNN.png
    """
    print("[VISION] Gerando dataset simulado de imagens...")

    for categoria, paletas in PALETAS_CATEGORIA.items():
        pasta = os.path.join(DATASET_DIR, categoria)
        os.makedirs(pasta, exist_ok=True)

        for i in range(n_por_categoria):
            # Sorteia uma paleta base para esta imagem
            h_base, s_base, v_base = paletas[i % len(paletas)]

            # Cria imagem HSV 64x64 com variação aleatória
            h = np.full((64, 64), h_base, dtype=np.float32)
            s = np.full((64, 64), s_base, dtype=np.float32)
            v = np.full((64, 64), v_base, dtype=np.float32)

            # Adiciona ruído para variedade
            h += np.random.normal(0, 8,  (64, 64)).astype(np.float32)
            s += np.random.normal(0, 20, (64, 64)).astype(np.float32)
            v += np.random.normal(0, 20, (64, 64)).astype(np.float32)

            # Garante faixa válida para HSV
            h = np.clip(h, 0, 179).astype(np.uint8)
            s = np.clip(s, 0, 255).astype(np.uint8)
            v = np.clip(v, 0, 255).astype(np.uint8)

            hsv_img = cv2.merge([h, s, v])
            bgr_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

            caminho = os.path.join(pasta, f"img_{i:03d}.png")
            cv2.imwrite(caminho, bgr_img)

        print(f"  [{categoria}] {n_por_categoria} imagens geradas.")

    print(f"[VISION] Dataset salvo em: {DATASET_DIR}\n")


# ─────────────────────────────────────────────────────────────
# 2. EXTRAÇÃO DE FEATURES
# ─────────────────────────────────────────────────────────────

def extrair_features(imagem_bgr: np.ndarray) -> np.ndarray:
    """
    Extrai um vetor de features de cor a partir de uma imagem BGR.

    Pipeline:
      1. Redimensiona para 64x64 (padronização)
      2. Converte para HSV (mais robusto a variações de iluminação)
      3. Calcula histograma de cada canal (H, S, V) com 16 bins
      4. Normaliza e concatena → vetor de 48 features

    Por que histograma HSV?
      - Leve e rápido (sem GPU)
      - Captura a "assinatura de cor" da imagem
      - HSV é mais invariante a luz do que RGB
    """
    img = cv2.resize(imagem_bgr, (64, 64))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    features = []
    for canal in range(3):  # H, S, V
        hist = cv2.calcHist([hsv], [canal], None, [16], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        features.extend(hist)

    return np.array(features, dtype=np.float32)


def extrair_features_pil(imagem_pil: Image.Image) -> np.ndarray:
    """Wrapper para imagens PIL (vindas do Streamlit file_uploader)."""
    imagem_bgr = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
    return extrair_features(imagem_bgr)


# ─────────────────────────────────────────────────────────────
# 3. TREINAMENTO DO MODELO DE VISÃO
# ─────────────────────────────────────────────────────────────

def treinar_modelo_visao():
    """
    Treina um SVM sobre o dataset simulado de imagens.
    Salva o modelo em models/vision_model.pkl.
    """
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report

    print("[VISION] Carregando imagens do dataset...")

    X, y = [], []
    for categoria in CATEGORIAS:
        pasta = os.path.join(DATASET_DIR, categoria)
        if not os.path.exists(pasta):
            print(f"[VISION] Pasta não encontrada: {pasta}")
            print("         Execute primeiro: gerar_dataset_simulado()")
            return

        arquivos = [f for f in os.listdir(pasta) if f.endswith(".png")]
        for arquivo in arquivos:
            caminho = os.path.join(pasta, arquivo)
            img = cv2.imread(caminho)
            if img is not None:
                features = extrair_features(img)
                X.append(features)
                y.append(categoria)

    X = np.array(X)
    y = np.array(y)
    print(f"[VISION] {len(X)} imagens carregadas.\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("[VISION] Treinando SVM...")
    modelo = SVC(kernel="rbf", C=10, gamma="scale", probability=True)
    modelo.fit(X_train, y_train)

    y_pred   = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    print(f"[VISION] Acurácia no teste: {acuracia * 100:.2f}%")
    print("\n" + classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(VISION_MODEL_PATH), exist_ok=True)
    joblib.dump(modelo, VISION_MODEL_PATH)
    print(f"[VISION] Modelo salvo em: {VISION_MODEL_PATH}")

    return acuracia


# ─────────────────────────────────────────────────────────────
# 4. CLASSIFICAÇÃO DE IMAGEM
# ─────────────────────────────────────────────────────────────

def classificar_imagem(imagem_pil: Image.Image) -> dict:
    """
    Recebe uma imagem PIL (do Streamlit) e retorna:
      - categoria prevista
      - probabilidades por categoria
      - miniatura processada (para exibir no dashboard)

    Exemplo de uso no app.py:
        resultado = classificar_imagem(imagem_pil)
        st.write(resultado["categoria"])
    """
    if not os.path.exists(VISION_MODEL_PATH):
        raise FileNotFoundError(
            "Modelo de visão não encontrado.\n"
            "Execute: python modules/vision.py"
        )

    modelo   = joblib.load(VISION_MODEL_PATH)
    features = extrair_features_pil(imagem_pil).reshape(1, -1)

    categoria    = modelo.predict(features)[0]
    probabilidades = modelo.predict_proba(features)[0]

    # Miniatura para exibição no Streamlit
    thumb = imagem_pil.copy()
    thumb.thumbnail((200, 200))

    return {
        "categoria": categoria,
        "probabilidades": {
            cat: round(float(prob) * 100, 1)
            for cat, prob in zip(modelo.classes_, probabilidades)
        },
        "thumbnail": thumb,
    }


def classificar_arquivo(caminho_arquivo: str) -> dict:
    """Wrapper para classificar a partir de um caminho de arquivo."""
    img_pil = Image.open(caminho_arquivo).convert("RGB")
    return classificar_imagem(img_pil)


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO DIRETA — gera dataset e treina o modelo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n📷 Pipeline de Visão Computacional — Tótem FlexMedia\n")

    print("ETAPA 1/2 — Gerando dataset simulado de imagens...")
    gerar_dataset_simulado(n_por_categoria=60)

    print("ETAPA 2/2 — Treinando modelo SVM de classificação...")
    treinar_modelo_visao()

    print("\n✅ Módulo de visão pronto.")
    print("   Use classificar_imagem(pil_image) no app.py para classificar imagens.\n")
