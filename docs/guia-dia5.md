# 📘 Guia de Implantação — Dia 5: Interface Streamlit

## O que foi desenvolvido hoje

O arquivo `app.py` é a interface principal do Tótem — ele integra todos os módulos
desenvolvidos nos dias anteriores em uma aplicação web com 4 abas funcionais.

| Aba | O que faz | Módulos integrados |
|-----|-----------|-------------------|
| 🏠 Início | Apresentação e cadastro do visitante | `db.py` |
| 💬 Interagir | Chatbot e classificador de perfil | `chatbot.py` + `train_model.py` |
| 📷 Visão | Upload e classificação de imagem | `vision.py` |
| 📊 Analytics | Métricas, gráficos e tabela de interações | `analytics.py` + `db.py` |

---

## Pré-requisitos

Antes de rodar o app, certifique-se que todos os passos anteriores foram concluídos:

```bash
# Verificar arquivos necessários
ls data/dataset.csv            # ✅ Dia 1
ls models/model.pkl            # ✅ Dia 2
ls models/encoders.pkl         # ✅ Dia 2
ls models/vision_model.pkl     # ✅ Dia 3
```

Se algum arquivo estiver faltando, execute:

```bash
python data/gerar_dados.py          # regera dataset e popula banco
python models/train_model.py        # retreina classificador de perfil
python modules/vision.py            # regera imagens e treina modelo de visão
```

---

## PASSO 1 — Copiar o arquivo para o projeto

Copie `app.py` deste ZIP para a **raiz** do projeto (`totem-flexmedia/`).

---

## PASSO 2 — Rodar a aplicação

```bash
# Na raiz do projeto, com o ambiente virtual ativo
streamlit run app.py
```

O Streamlit abrirá automaticamente no navegador em:
```
http://localhost:8501
```

### Saída esperada no terminal:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## PASSO 3 — Testar cada aba

### Aba Início
1. Digite seu nome no campo de identificação
2. Selecione sua faixa etária
3. Clique em **"Entrar no Tótem →"**
4. Verifique se aparece o card verde **"✓ Sessão ativa"**

### Aba Interagir — Chatbot
1. Após se cadastrar, vá para a aba **Interagir**
2. O assistente virtual deve enviar uma mensagem de boas-vindas automaticamente
3. Digite uma pergunta (ex: "O que tem de arte aqui?") e pressione **→**
4. Verifique se a resposta aparece corretamente

### Aba Interagir — Classificador de Perfil
1. Selecione tipo de ação, categoria, duração e satisfação
2. Clique em **"Classificar Perfil"**
3. Verifique se aparece o perfil previsto com as barras de probabilidade

### Aba Visão
1. Clique em **"Selecione uma imagem"** e escolha qualquer foto
2. Clique em **"Classificar Imagem →"**
3. Verifique se aparece a categoria identificada com o badge colorido

### Aba Analytics
1. Verifique se as 4 métricas no topo aparecem com valores reais
2. Verifique se os 4 gráficos são renderizados corretamente
3. Verifique se a tabela de interações recentes está populada

---

## PASSO 4 — Resolução de problemas comuns

**App abre mas as abas mostram erros de módulo:**
```bash
# Verifique se o ambiente virtual está ativo
which python   # deve apontar para venv/

# Reinstale as dependências
pip install -r requirements.txt
```

**Erro "Módulo de banco indisponível":**
- Verifique as credenciais no `.env`
- Confirme que está conectado à rede da FIAP ou VPN

**Gráficos não aparecem na aba Analytics:**
```bash
# Verifique se o módulo analytics.py existe
ls modules/analytics.py

# Rode o dia 6 para criar este módulo
```

**Imagem não classifica:**
```bash
# Verifique se o modelo de visão existe
ls models/vision_model.pkl

# Se não existir, execute:
python modules/vision.py
```

---

## PASSO 5 — Commitar no GitHub

```bash
git checkout develop
git checkout -b feature/interface-streamlit

# Adiciona o app principal
git add app.py
git add docs/guia-dia5.md

git commit -m "feat: implementa interface Streamlit com 4 abas integradas ao sistema"

git push origin feature/interface-streamlit
```

---

## PASSO 6 — Pull Request no GitHub

1. Acesse o repositório no GitHub
2. Clique em **"Compare & pull request"**
3. Preencha:
   - **Title:** `feat: interface Streamlit principal`
   - **Description:**
     ```
     ## O que foi feito
     - Interface com 4 abas: Início, Interagir, Visão, Analytics
     - Integração completa com db.py, chatbot.py, vision.py, train_model.py
     - Cadastro de visitante com persistência no Oracle
     - Chatbot com histórico de conversa por sessão
     - Classificador de perfil com barras de probabilidade
     - Upload e classificação de imagem com badges por categoria
     - Painel de analytics com 4 métricas e 4 gráficos
     - Design dark com tipografia Syne + DM Sans
     ```
4. Clique em **"Merge pull request"**

---

## PASSO 7 — Tag de versão

```bash
git checkout develop
git pull origin develop

git tag -a v0.5.0 -m "Sprint 4 - Dia 5: Interface Streamlit completa integrada"
git push origin v0.5.0
```

---

## Estrutura atualizada do projeto

```
totem-flexmedia/
├── app.py                          ✅ Dia 5  ← NOVO (raiz do projeto)
├── data/
│   ├── gerar_dados.py              ✅ Dia 1
│   └── dataset.csv                 ✅ Dia 1 (gerado)
├── models/
│   ├── train_model.py              ✅ Dia 2
│   ├── model.pkl                   ✅ Dia 2 (gerado)
│   ├── encoders.pkl                ✅ Dia 2 (gerado)
│   ├── vision_model.pkl            ✅ Dia 3 (gerado)
│   ├── confusion_matrix.png        ✅ Dia 2 (gerado)
│   └── feature_importance.png      ✅ Dia 2 (gerado)
├── modules/
│   ├── db.py                       ✅ Dia 1
│   ├── vision.py                   ✅ Dia 3
│   ├── chatbot.py                  ✅ Dia 4
│   └── __init__.py                 ✅ Dia 1
├── docs/
│   ├── arquitetura.md              ✅ Dia 1
│   ├── guia-implantacao.md         ✅ Dia 1
│   ├── guia-dia2.md                ✅ Dia 2
│   ├── correcao-acuracia.md        ✅ Dia 2
│   ├── guia-dia3.md                ✅ Dia 3
│   ├── guia-dia4.md                ✅ Dia 4
│   └── guia-dia5.md                ✅ Dia 5  ← NOVO
└── ...
```

> **Próximo passo — Dia 6:** módulo `modules/analytics.py` com os 4 gráficos
> de engajamento que a aba Analytics já está preparada para receber.
