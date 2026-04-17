# 📘 Guia — Entrega Final: Chatbot + Correção dos Gráficos

## Arquivos desta entrega

| Arquivo | Situação |
|---------|---------|
| `modules/chatbot.py` | ✅ Novo — módulo de diálogo completo |
| `modules/analytics.py` | ✅ Corrigido — tema light + 4 gráficos funcionando |

---

## PARTE 1 — Chatbot

### O que foi implementado

O `chatbot.py` é um sistema de diálogo baseado em regras com detecção de intenção
por expressões regulares, cobrindo 14 intenções diferentes:

| Intenção | Exemplos de gatilho |
|----------|-------------------|
| `saudacao` | "oi", "olá", "bom dia" |
| `despedida` | "tchau", "até logo", "obrigado" |
| `ajuda` | "ajuda", "o que você faz", "como funciona" |
| `arte` | "arte", "galeria", "pintura", "escultura" |
| `ciencia` | "ciência", "planetário", "laboratório", "DNA" |
| `historia` | "história", "acervo", "linha do tempo" |
| `tecnologia` | "tecnologia", "robótica", "IA", "computação" |
| `ingressos` | "ingresso", "preço", "gratuito", "meia-entrada" |
| `horario` | "horário", "abre", "fecha", "que horas" |
| `acessibilidade` | "acessibilidade", "cadeira de rodas", "elevador" |
| `estacionamento` | "estacionamento", "vaga", "carro" |
| `alimentacao` | "comer", "restaurante", "café", "fome" |
| `loja` | "loja", "souvenir", "livro", "presente" |
| Acompanhamento | "e os destaques?", "qual o horário?", "tem dica?" |

A última categoria consultada é salva no contexto — o visitante pode perguntar
"e os destaques?" logo após "me fale sobre ciência" e receberá os destaques
de ciência corretamente.

### Funções públicas

```python
# Mensagem de boas-vindas (chamada ao iniciar sessão)
from modules.chatbot import iniciar_conversa
msg = iniciar_conversa("Ana")

# Processamento de mensagem (chamada a cada turno)
from modules.chatbot import processar_mensagem
resposta, ctx = processar_mensagem("me fale sobre tecnologia", {})
resposta, ctx = processar_mensagem("quais são os destaques?", ctx)
```

---

## PARTE 2 — Correção dos Gráficos Analytics

### Causa do problema

O Streamlit usa `@st.cache_resource` para evitar recarregar módulos a cada
interação. Isso fazia com que as funções de gráfico retornassem a mesma figura
já renderizada anteriormente — apenas o primeiro gráfico aparecia, os demais
ficavam em branco ou repetiam o primeiro.

### Correção aplicada

Cada função de gráfico agora começa com `plt.close("all")` antes de criar
sua figura. Isso garante que o matplotlib parte de um estado limpo a cada
chamada, independente do cache do Streamlit.

```python
# ANTES (problema)
def grafico_interacoes_por_categoria():
    fig, ax = plt.subplots(...)   # reutilizava figura anterior
    ...

# DEPOIS (corrigido)
def grafico_interacoes_por_categoria():
    plt.close("all")              # ← fecha qualquer figura aberta
    fig, ax = plt.subplots(...)   # cria figura nova e isolada
    ...
```

Além disso, o backend foi fixado como `Agg` (não-interativo) via
`matplotlib.use("Agg")` no topo do módulo — obrigatório para uso com Streamlit.

---

## Passo a passo de instalação

### PASSO 1 — Copiar os arquivos

```
modules/chatbot.py    → substitui qualquer versão anterior (ou cria o arquivo)
modules/analytics.py  → substitui a versão do Dia 6
```

### PASSO 2 — Testar o chatbot

```bash
python -c "
from modules.chatbot import iniciar_conversa, processar_mensagem

print(iniciar_conversa('Ana'))
print('---')

ctx = {}
r, ctx = processar_mensagem('me fale sobre tecnologia', ctx)
print(r)
print('---')

r, ctx = processar_mensagem('quais são os destaques?', ctx)
print(r)
"
```

### PASSO 3 — Testar os gráficos

```bash
python modules/analytics.py
```

Todos os 4 arquivos devem ser gerados em `data/graficos/`.

### PASSO 4 — Rodar o app e validar tudo

```bash
streamlit run app.py
```

Checklist final:
- [ ] Aba **Interagir** → chatbot responde com boas-vindas ao se cadastrar
- [ ] Aba **Interagir** → chatbot responde perguntas sobre categorias e serviços
- [ ] Aba **Analytics** → todos os **4 gráficos** aparecem lado a lado
- [ ] Aba **Analytics** → as **4 métricas** no topo exibem valores reais

---

## PASSO 5 — Commits finais

```bash
git checkout develop

# Chatbot
git add modules/chatbot.py
git commit -m "feat: implementa modulo de chatbot com deteccao de intencao e contexto de sessao"

# Correção dos gráficos
git add modules/analytics.py
git commit -m "fix: corrige exibicao dos 4 graficos no Streamlit com plt.close e backend Agg"

git push origin develop

# Merge final para main
git checkout main
git merge develop
git push origin main

# Tag de entrega
git tag -a v1.0.0 -m "Sprint 4 - Entrega final completa: chatbot + analytics corrigido"
git push origin v1.0.0
```

---

## Histórico de versões final

| Tag | Entrega |
|-----|---------|
| `v0.1.0` | Banco Oracle + dados simulados |
| `v0.2.0` | Random Forest — 91,84% acurácia |
| `v0.3.0` | Visão Computacional SVM |
| `v0.4.0` | *(placeholder — substituído por esta entrega)* |
| `v0.5.0` | Interface Streamlit completa |
| `v0.6.0` | Analytics + exportação CSV |
| `v0.7.0` | Documentação técnica + relatório analítico |
| **`v1.0.0`** | **Chatbot + correção dos gráficos — entrega final** |
