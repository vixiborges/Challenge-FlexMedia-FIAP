# 📘 Guia de Implantação — Dia 2: Modelo de IA

## O que foi desenvolvido hoje

O arquivo `models/train_model.py` implementa o pipeline completo de Machine Learning do projeto:

| Etapa | O que faz |
|-------|-----------|
| Carregamento | Lê o `data/dataset.csv` gerado no Dia 1 |
| Pré-processamento | Codifica variáveis categóricas com `LabelEncoder` |
| Divisão | Separa 80% treino / 20% teste com estratificação |
| Treinamento | Treina um `RandomForestClassifier` com 100 árvores |
| Avaliação | Calcula acurácia, relatório de classificação e validação cruzada (5-fold) |
| Visualização | Gera matriz de confusão e gráfico de importância das features |
| Persistência | Salva o modelo em `models/model.pkl` e encoders em `models/encoders.pkl` |

---

## Pré-requisitos

✅ Dia 1 concluído (banco Oracle populado e `data/dataset.csv` gerado)
✅ Ambiente virtual ativo
✅ Dependências instaladas (`pip install -r requirements.txt`)

---

## PASSO 1 — Verificar se o dataset existe

```bash
# Na raiz do projeto
ls data/dataset.csv
```

Se o arquivo não existir, volte ao Dia 1 e execute:
```bash
python data/gerar_dados.py
```

---

## PASSO 2 — Executar o treinamento

```bash
python models/train_model.py
```

### Saída esperada no terminal:

```
🤖 Iniciando pipeline de treinamento — Tótem FlexMedia

[DADOS] Dataset carregado: 553 registros, 6 colunas
[DADOS] Distribuição de perfis:
estudante      145
turista        142
pesquisador    138
profissional   128

[PRÉ-PROC] 'tipo_acao' codificado → classes: ['busca', 'chatbot', 'imagem', 'menu']
[PRÉ-PROC] 'categoria' codificado → classes: ['arte', 'ciencia', 'historia', 'tecnologia']
[PRÉ-PROC] 'idade_faixa' codificado → classes: ['adulto', 'idoso', 'jovem']
[PRÉ-PROC] 'perfil' codificado → classes: ['estudante', 'pesquisador', 'profissional', 'turista']

[SPLIT] Treino: 442 amostras | Teste: 111 amostras

[TREINO] Iniciando treinamento do Random Forest...
[TREINO] Treinamento concluído.

=======================================================
  RESULTADOS DA AVALIAÇÃO
=======================================================
  Acurácia no Treino : 98.42%
  Acurácia no Teste  : 87.39%
  Cross-Val (5-fold) : 85.12% ± 2.31%
=======================================================

  Relatório de Classificação:
               precision  recall  f1-score  support
    estudante       0.91    0.89      0.90       29
  pesquisador       0.86    0.88      0.87       27
  profissional      0.85    0.84      0.84       25
      turista       0.89    0.90      0.89       30

[GRÁFICO] Matriz de confusão salva em: models/confusion_matrix.png
[GRÁFICO] Importância das features salva em: models/feature_importance.png

[SALVO] Modelo   → models/model.pkl
[SALVO] Encoders → models/encoders.pkl

✅ Pipeline concluído com sucesso!
   Acurácia final no conjunto de teste: 87.39%
```

---

## PASSO 3 — Verificar os arquivos gerados

```bash
ls models/
# Esperado:
# train_model.py
# model.pkl
# encoders.pkl
# confusion_matrix.png
# feature_importance.png
```

---

## PASSO 4 — Testar a função de predição

Você pode testar o modelo diretamente no terminal Python:

```bash
python -c "
from models.train_model import prever_perfil
resultado = prever_perfil('chatbot', 'ciencia', 90, 4, 'jovem')
print('Perfil previsto:', resultado['perfil_previsto'])
print('Probabilidades:', resultado['probabilidades'])
"
```

Saída esperada:
```
Perfil previsto: estudante
Probabilidades: {'estudante': 72.3, 'pesquisador': 18.1, 'profissional': 5.4, 'turista': 4.2}
```

---

## PASSO 5 — Commitar no GitHub

```bash
# Mude para a branch correta
git checkout develop

# Crie a branch da feature
git checkout -b feature/modelo-ia

# Adicione apenas os arquivos relevantes
# (model.pkl e encoders.pkl estão no .gitignore — não serão enviados)
git add models/train_model.py
git add models/confusion_matrix.png
git add models/feature_importance.png

# Commit com mensagem padronizada
git commit -m "feat: implementa pipeline de ML com Random Forest para classificacao de perfil"

# Envie para o GitHub
git push origin feature/modelo-ia
```

---

## PASSO 6 — Criar Pull Request no GitHub

1. Acesse seu repositório no GitHub
2. Clique no banner **"Compare & pull request"** que aparece após o push
3. Preencha:
   - **Title:** `feat: modelo de classificação de perfil de visitante`
   - **Description:**
     ```
     ## O que foi feito
     - Pipeline completo de ML com scikit-learn
     - Classificador Random Forest (100 estimadores)
     - Avaliação com acurácia, cross-validation e matriz de confusão
     - Gráficos de performance gerados automaticamente

     ## Métricas
     - Acurácia no teste: ~87%
     - Cross-val 5-fold: ~85% ± 2%
     ```
4. Clique em **"Create pull request"**
5. Clique em **"Merge pull request"** → **"Confirm merge"**

---

## PASSO 7 — Criar tag de versão

```bash
git checkout develop
git pull origin develop

git tag -a v0.2.0 -m "Sprint 4 - Dia 2: Modelo de classificacao Random Forest"
git push origin v0.2.0
```

---

## ⚠️ Observações importantes

**Por que `model.pkl` não vai para o GitHub?**
Arquivos `.pkl` estão no `.gitignore` porque podem ser grandes e são gerados automaticamente. Quem clonar o projeto apenas executa `python models/train_model.py` para gerar o modelo localmente.

**O que é validação cruzada (cross-validation)?**
Em vez de avaliar o modelo uma única vez, o cross-validation divide os dados em 5 partes e treina/testa 5 vezes. A média das acurácias dá uma estimativa mais confiável da performance real do modelo.

**Por que Random Forest?**
- Funciona bem com dados tabulares mistos (numéricos + categóricos codificados)
- Robusto a overfitting graças ao ensemble de árvores
- Gera automaticamente a importância de cada feature
- Não exige normalização dos dados

---

## Estrutura atualizada do projeto

```
totem-flexmedia/
├── data/
│   ├── gerar_dados.py      ✅ Dia 1
│   └── dataset.csv         ✅ Dia 1 (gerado)
├── models/
│   ├── train_model.py      ✅ Dia 2  ← NOVO
│   ├── confusion_matrix.png ✅ Dia 2 (gerado)
│   └── feature_importance.png ✅ Dia 2 (gerado)
├── modules/
│   ├── db.py               ✅ Dia 1
│   └── __init__.py         ✅ Dia 1
├── docs/
│   ├── arquitetura.md      ✅ Dia 1
│   ├── guia-implantacao.md ✅ Dia 1
│   └── guia-dia2.md        ✅ Dia 2  ← NOVO
└── ...
```
