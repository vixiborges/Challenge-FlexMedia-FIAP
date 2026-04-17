<p align="center">
<a href="https://www.fiap.com.br/">
  <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%">
</a>
</p>

<br>

# Tótem Inteligente FlexMedia

https://youtu.be/DibpSJPr88k

## Grupo FlexMedia — Challenge Sprint 4

### 👨‍🎓 Integrantes:

Gustavo Borges Marinho Peres

## 📜 Descrição

O **Tótem Inteligente FlexMedia** é uma solução digital interativa desenvolvida para ambientes de visitação — museus, centros culturais, eventos tecnológicos e espaços educacionais. 

A solução combina quatro grandes pilares tecnológicos. O primeiro é a **coleta e persistência de dados**, em que todas as interações dos visitantes são registradas em um banco de dados, estruturado em três tabelas relacionais: `visitantes`, `interacoes` e `logs_sistema`. Cada registro captura o tipo de ação realizada, a categoria temática acessada, o tempo de engajamento e a avaliação de satisfação do visitante.

O segundo pilar é a **Inteligência Artificial aplicada à classificação de perfil**. Um modelo Random Forest foi treinado sobre os dados de interação para prever, em tempo real, o perfil de cada visitante — estudante, turista, pesquisador ou profissional. O modelo atingiu **91,84% de acurácia** no conjunto de teste.

O terceiro pilar é a **Visão Computacional**. O sistema é capaz de receber imagens enviadas pelo visitante e classificá-las em uma das quatro categorias temáticas do tótem (Arte, Ciência, História ou Tecnologia). A classificação utiliza um modelo SVM com kernel RBF treinado sobre features de histograma de cor no espaço HSV, sem dependência de GPU ou modelos de deep learning, atingindo aproximadamente **93% de acurácia**.

O quarto pilar é a **interação conversacional**, implementada por meio de um módulo de chatbot com detecção de intenção por expressões regulares. O assistente virtual do tótem responde perguntas sobre as exposições, horários, ingressos, acessibilidade, alimentação e serviços do espaço, mantendo contexto de sessão entre os turnos da conversa.

Toda a solução é apresentada em uma **interface web construída com Streamlit**, organizada em quatro abas: Início (cadastro do visitante), Interagir (chatbot e classificador de perfil), Visão (upload e classificação de imagem) e Analytics (painel de métricas e gráficos de engajamento). O painel analítico exibe quatro visualizações — interações por categoria, satisfação por tipo de ação, volume por hora do dia e distribuição de perfis de visitantes — além de um conjunto de KPIs para o gestor do espaço.

## 📁 Estrutura de pastas

```
totem-flexmedia/
│

├── data/                     Imagens e elementos não-estruturados do repositório
│
├── docs/                     Documentação do projeto
│   ├── arquitetura.md          Documentação técnica da arquitetura do sistema
│   ├── relatorio-analitico.md  Relatório analítico final com interpretação dos dados
│  
|
├── data/
│   └── gerar_dados.py      Geração de dados simulados e exportação CSV
├── models/
│   └── train_model.py      Pipeline de ML — Random Forest
|── modules/
│   ├── db.py               Conexão Oracle e funções CRUD
│   ├── chatbot.py          Módulo de diálogo e detecção de intenção
│   ├── vision.py           Visão computacional — SVM + OpenCV
│   └── analytics.py        Métricas e gráficos de engajamento
│
├── app.py                      Interface Streamlit
├── .env.example                Template de variáveis de ambiente
├── .gitignore                  Arquivos ignorados pelo Git
├── requirements.txt            Dependências do projeto
└── README.md                   Este arquivo
```

---

## 🔧 Como executar o código

### Pré-requisitos

| Ferramenta | Versão mínima | Download |
|-----------|--------------|---------|
| Python | 3.11+ | https://python.org |
| Git | 2.40+ | https://git-scm.com |
| Acesso ao Oracle FIAP | — | Credenciais fornecidas pela instituição |

---

### Fase 1 — Configurar o ambiente virtual

# Criar o ambiente virtual
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

---

### Fase 3 — Configurar as credenciais Oracle

```bash
# Copie o template
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais da FIAP:

```env
ORACLE_USER=rmSEU_RM
ORACLE_PASSWORD=SUA_SENHA
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

### Fase 4 — Inicializar o banco e gerar os dados

```bash
# Cria as tabelas no Oracle e popula com dados simulados
python data/gerar_dados.py
```

---

### Fase 5 — Treinar os modelos de IA

```bash
# Classificador de perfil (Random Forest)
python models/train_model.py

# Modelo de visão computacional (SVM)
python modules/vision.py
```

---

### Fase 6 — Executar a aplicação

```bash
streamlit run app.py
```

## 🗃 Histórico de lançamentos

* **1.0.0** — Entrega final: chatbot + correção dos gráficos de analytics
* **0.6.0** — Módulo de analytics com 4 gráficos e exportação CSV
* **0.5.0** — Interface Streamlit completa com 4 abas integradas
* **0.4.0** — Módulo de chatbot com detecção de intenção e contexto de sessão
* **0.3.0** — Visão computacional com SVM e histograma HSV (~93% acurácia)
* **0.2.0** — Modelo Random Forest para classificação de perfil (91,84% acurácia)
* **0.1.0** — Estrutura inicial, banco Oracle e geração de dados simulados

---

## 📋 Licença

**Tótem Inteligente FlexMedia** por **Grupo FlexMedia — FIAP** está licenciado sobre
[Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
