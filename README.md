# 🖥️ Tótem Inteligente FlexMedia

Sistema interativo inteligente para ambientes de visitação, desenvolvido como projeto Challenge da FIAP em parceria com a FlexMedia.

---

## 🏗️ Arquitetura

```
totem-flexmedia/
├── app.py                  # Interface principal (Streamlit)
├── data/
│   ├── gerar_dados.py      # Geração de dados simulados
│   ├── dataset.csv         # Dataset exportado (gerado automaticamente)
│   └── imagens/            # Dataset de imagens para visão computacional
├── models/
│   ├── train_model.py      # Treinamento do classificador
│   └── model.pkl           # Modelo salvo (gerado automaticamente)
├── modules/
│   ├── db.py               # Conexão e CRUD Oracle
│   ├── vision.py           # Processamento de imagem (OpenCV)
│   ├── chatbot.py          # Lógica de diálogo do tótem
│   └── analytics.py        # Métricas e gráficos de engajamento
├── docs/
│   └── arquitetura.md      # Documentação técnica
├── .env.example            # Template de variáveis de ambiente
└── requirements.txt
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/totem-flexmedia.git
cd totem-flexmedia
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as credenciais Oracle
```bash
cp .env.example .env
```
Edite o `.env` com suas credenciais:
```
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

---

## 🚀 Como Executar

### Passo 1 — Inicializar banco e gerar dados
```bash
python data/gerar_dados.py
```
Isso vai:
- Criar as tabelas no Oracle (`visitantes`, `interacoes`, `logs_sistema`)
- Inserir 150 visitantes simulados com interações
- Exportar `data/dataset.csv` para treinamento do modelo

### Passo 2 — Treinar o modelo de IA
```bash
python models/train_model.py
```

### Passo 3 — Rodar a aplicação
```bash
streamlit run app.py
```

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Interface | Streamlit |
| Banco de Dados | Oracle (via python-oracledb) |
| Machine Learning | Scikit-learn |
| Visão Computacional | OpenCV + Pillow |
| Análise de Dados | Pandas + Matplotlib + Seaborn |
| Geração de dados | Faker |

---

## 👥 Equipe

- Nome 1
- Nome 2

**FIAP — Challenge FlexMedia — Sprint 4**
