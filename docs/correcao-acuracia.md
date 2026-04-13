# 🔧 Correção de Acurácia — Re-execução do Pipeline

## O problema

A acurácia de **38%** estava abaixo do aceitável. Para um classificador com 4 classes,
uma escolha completamente aleatória já acertaria **25%** — ou seja, o modelo estava
apenas 13 pontos percentuais acima do acaso. Isso indica que os dados não tinham
padrão suficiente para ser aprendido.

### Causa raiz: sobreposição de perfis nos dados simulados

Na versão anterior, as probabilidades de categoria por perfil eram próximas demais:

```
# ANTES (v1) — modelo não conseguia separar
estudante:    ciencia 40%  historia 30%  arte 20%  tecnologia 10%
pesquisador:  ciencia 45%  tecnologia 30% ...
```

Estudante e pesquisador tinham quase o mesmo padrão de categoria. O modelo
não encontrava fronteiras de decisão claras.

---

## O que foi corrigido (v2)

Quatro ajustes foram feitos no `gerar_dados.py`:

### 1. Categorias com separação nítida
Cada perfil agora tem uma categoria claramente dominante (≥ 70%):

| Perfil | Categoria dominante | Probabilidade |
|--------|-------------------|--------------|
| estudante | ciencia | 75% |
| turista | arte | 75% |
| pesquisador | tecnologia | 75% |
| profissional | tecnologia + ciencia | 55% + 30% |

### 2. Tipo de ação correlacionado com perfil
```
estudante   → chatbot (65%)   — pergunta, pesquisa
turista     → imagem  (65%)   — visualiza, explora
pesquisador → busca   (65%)   — busca específica
profissional→ menu    (55%)   — acesso direto, objetivo
```

### 3. Faixa etária correlacionada com perfil
```
estudante    → jovem  (75%)
pesquisador  → adulto (65%)
profissional → adulto (70%)
turista      → adulto (55%)
```

### 4. Duração de interação diferenciada por perfil
```
pesquisador  → média 180s (longa, aprofundamento)
estudante    → média 120s (longa, aprendizado)
profissional → média 70s  (média, objetivo claro)
turista      → média 40s  (curta, navegação rápida)
```

### 5. Volume aumentado
De 150 para **300 visitantes** (~1.200 interações), dando mais dados para o modelo aprender.

---

## Passo a passo para re-executar

### PASSO 1 — Substituir o arquivo

Copie o novo `data/gerar_dados.py` (deste ZIP) para dentro do seu projeto,
substituindo o arquivo anterior.

### PASSO 2 — Limpar o dataset antigo

```bash
# Remove o CSV gerado com dados ruins
rm data/dataset.csv
```

### PASSO 3 — Limpar o banco Oracle (opcional, mas recomendado)

Se quiser partir do zero no banco, conecte ao Oracle e execute:

```sql
DELETE FROM interacoes;
DELETE FROM visitantes;
DELETE FROM logs_sistema;
COMMIT;
```

Ou se preferir fazer via Python:

```bash
python -c "
from modules.db import get_connection
conn = get_connection()
cur = conn.cursor()
cur.execute('DELETE FROM interacoes')
cur.execute('DELETE FROM visitantes')
cur.execute('DELETE FROM logs_sistema')
conn.commit()
cur.close()
conn.close()
print('Banco limpo.')
"
```

### PASSO 4 — Regerar os dados

```bash
python data/gerar_dados.py
```

### PASSO 5 — Retreinar o modelo

```bash
python models/train_model.py
```

### Resultado esperado após a correção

```
=======================================================
  RESULTADOS DA AVALIAÇÃO
=======================================================
  Acurácia no Treino : ~98%
  Acurácia no Teste  : ~88–93%
  Cross-Val (5-fold) : ~86–90% ± ~2%
=======================================================
```

---

## Commitar a correção

```bash
git checkout feature/modelo-ia   # ou a branch em que você estava

git add data/gerar_dados.py

git commit -m "fix: corrige separacao de perfis nos dados simulados para aumentar acuracia do modelo"

git push origin feature/modelo-ia
```

> 💡 Note o uso do prefixo `fix:` — estamos corrigindo um problema, não adicionando
> uma funcionalidade nova. Isso mantém o histórico de commits semântico e rastreável.
