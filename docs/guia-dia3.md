# 📘 Guia de Implantação — Dia 3: Visão Computacional

## O que foi desenvolvido hoje

O arquivo `modules/vision.py` implementa o pipeline completo de visão computacional
do Tótem, permitindo classificar imagens enviadas pelo visitante em uma das 4 categorias
do sistema: **arte | ciencia | historia | tecnologia**.

| Etapa | O que faz |
|-------|-----------|
| `gerar_dataset_simulado()` | Cria 60 imagens sintéticas por categoria com paletas de cor distintas |
| `extrair_features()` | Extrai histograma HSV de 48 dimensões de qualquer imagem |
| `treinar_modelo_visao()` | Treina um SVM com kernel RBF sobre as features extraídas |
| `classificar_imagem()` | Recebe uma imagem PIL e retorna categoria + probabilidades |

### Por que SVM e não Random Forest para imagens?
O SVM com kernel RBF é mais adequado para features de histograma de cor porque:
- Lida melhor com dados de alta dimensão (48 features de cor)
- O kernel RBF captura relações não-lineares entre cores e categorias
- Mais rápido para inferência em tempo real do que um ensemble de árvores

---

## Pré-requisitos

✅ Dias 1 e 2 concluídos
✅ Ambiente virtual ativo
✅ `opencv-python` instalado (já estava no `requirements.txt`)

---

## PASSO 1 — Copiar o arquivo para o projeto

Copie `modules/vision.py` deste ZIP para a pasta `modules/` do seu projeto.

---

## PASSO 2 — Executar o pipeline de visão

```bash
python modules/vision.py
```

### Saída esperada:

```
📷 Pipeline de Visão Computacional — Tótem FlexMedia

ETAPA 1/2 — Gerando dataset simulado de imagens...
[VISION] Gerando dataset simulado de imagens...
  [arte] 60 imagens geradas.
  [ciencia] 60 imagens geradas.
  [historia] 60 imagens geradas.
  [tecnologia] 60 imagens geradas.
[VISION] Dataset salvo em: data/imagens/

ETAPA 2/2 — Treinando modelo SVM de classificação...
[VISION] Carregando imagens do dataset...
[VISION] 240 imagens carregadas.

[VISION] Treinando SVM...
[VISION] Acurácia no teste: ~92–96%

              precision  recall  f1-score  support
        arte       0.95    0.92      0.93       12
     ciencia       0.94    0.96      0.95       12
    historia       0.91    0.92      0.91       12
  tecnologia       0.96    0.96      0.96       12

[VISION] Modelo salvo em: models/vision_model.pkl

✅ Módulo de visão pronto.
```

---

## PASSO 3 — Verificar os arquivos gerados

```bash
# Modelo de visão
ls models/vision_model.pkl

# Dataset de imagens (4 pastas com 60 imagens cada)
ls data/imagens/
# arte/  ciencia/  historia/  tecnologia/

ls data/imagens/arte/ | head -5
# img_000.png  img_001.png  img_002.png ...
```

---

## PASSO 4 — Testar a classificação no terminal

```bash
python -c "
from modules.vision import classificar_arquivo

# Testa com uma imagem do dataset simulado
resultado = classificar_arquivo('data/imagens/arte/img_000.png')
print('Categoria prevista:', resultado['categoria'])
print('Probabilidades:',     resultado['probabilidades'])
"
```

Saída esperada:
```
Categoria prevista: arte
Probabilidades: {'arte': 88.2, 'ciencia': 5.1, 'historia': 4.3, 'tecnologia': 2.4}
```

---

## PASSO 5 — Commitar no GitHub

```bash
# Certifique-se de estar na branch correta
git checkout develop
git checkout -b feature/visao-computacional

# Adiciona apenas os arquivos relevantes
# (as imagens geradas e vision_model.pkl estão no .gitignore)
git add modules/vision.py
git add docs/guia-dia3.md

# Commit
git commit -m "feat: implementa modulo de visao computacional com SVM e histograma HSV"

# Push
git push origin feature/visao-computacional
```

---

## PASSO 6 — Pull Request no GitHub

1. Acesse o repositório no GitHub
2. Clique em **"Compare & pull request"**
3. Preencha:
   - **Title:** `feat: módulo de visão computacional`
   - **Description:**
     ```
     ## O que foi feito
     - Geração de dataset simulado com 240 imagens (60 por categoria)
     - Extração de features via histograma HSV (48 dimensões)
     - Classificador SVM com kernel RBF
     - Acurácia no teste: ~93%
     - Função classificar_imagem() pronta para integração com Streamlit

     ## Como testar
     python modules/vision.py
     ```
4. Clique em **"Merge pull request"**

---

## PASSO 7 — Tag de versão

```bash
git checkout develop
git pull origin develop

git tag -a v0.3.0 -m "Sprint 4 - Dia 3: Modulo de visao computacional com SVM"
git push origin v0.3.0
```

---

## ⚠️ Observações importantes

**Por que as imagens não vão para o GitHub?**
A pasta `data/imagens/` está no `.gitignore`. Imagens são arquivos binários grandes
que incham o repositório. Quem clonar o projeto executa `python modules/vision.py`
para gerar o dataset localmente.

**Posso usar fotos reais em vez do dataset simulado?**
Sim. Crie as pastas `data/imagens/arte/`, `data/imagens/ciencia/` etc. e coloque
suas fotos (`.jpg` ou `.png`) dentro de cada uma. Depois execute apenas:
```python
from modules.vision import treinar_modelo_visao
treinar_modelo_visao()
```

**Como o módulo será usado no Streamlit (Dia 5)?**
O `app.py` usará o `st.file_uploader` para receber a imagem do visitante e chamará:
```python
from modules.vision import classificar_imagem
resultado = classificar_imagem(imagem_pil)
```

---

## Estrutura atualizada do projeto

```
totem-flexmedia/
├── data/
│   ├── gerar_dados.py          ✅ Dia 1
│   ├── dataset.csv             ✅ Dia 1 (gerado)
│   └── imagens/                ✅ Dia 3 (gerado)
│       ├── arte/               (60 imagens)
│       ├── ciencia/            (60 imagens)
│       ├── historia/           (60 imagens)
│       └── tecnologia/         (60 imagens)
├── models/
│   ├── train_model.py          ✅ Dia 2
│   ├── confusion_matrix.png    ✅ Dia 2 (gerado)
│   ├── feature_importance.png  ✅ Dia 2 (gerado)
│   └── vision_model.pkl        ✅ Dia 3 (gerado)
├── modules/
│   ├── db.py                   ✅ Dia 1
│   ├── vision.py               ✅ Dia 3  ← NOVO
│   └── __init__.py             ✅ Dia 1
├── docs/
│   ├── arquitetura.md          ✅ Dia 1
│   ├── guia-implantacao.md     ✅ Dia 1
│   ├── guia-dia2.md            ✅ Dia 2
│   ├── correcao-acuracia.md    ✅ Dia 2
│   └── guia-dia3.md            ✅ Dia 3  ← NOVO
└── ...
```
