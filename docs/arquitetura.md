# Documentação Técnica Final — Tótem Inteligente FlexMedia
**FIAP · Challenge Sprint 4 · 2025**

---

## 1. Visão Geral do Sistema

O Tótem Inteligente FlexMedia é uma solução digital interativa desenvolvida para ambientes de visitação — museus, centros culturais, eventos tecnológicos e espaços educacionais. O sistema combina coleta de dados, inteligência artificial e visualização analítica para oferecer uma experiência personalizada ao visitante e insights de engajamento ao gestor do espaço.

A solução foi construída ao longo de quatro sprints, evoluindo de um protótipo conceitual até uma aplicação funcional com modelos de IA treinados, interface web integrada e banco de dados em produção.

---

## 2. Arquitetura do Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                         │
│                     app.py  (Streamlit)                           │
│                                                                   │
│   🏠 Início │ 💬 Interagir │ 📷 Visão │ 📊 Analytics             │
└────────────────────────┬─────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────────┐
         │               │                   │
┌────────▼──────┐ ┌──────▼──────┐  ┌────────▼────────┐
│  chatbot.py   │ │  vision.py  │  │  analytics.py   │
│  (Diálogo)    │ │  (OpenCV)   │  │  (Pandas +      │
│               │ │  SVM        │  │   Matplotlib)   │
└────────┬──────┘ └──────┬──────┘  └────────┬────────┘
         │               │                   │
         └───────────────┼───────────────────┘
                         │
              ┌──────────▼──────────┐
              │   train_model.py    │
              │   Random Forest     │
              │   Classificador     │
              │   de Perfil         │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │       db.py         │
              │  python-oracledb    │
              └──────────┬──────────┘
                         │
         ┌───────────────────────────────┐
         │        ORACLE DATABASE        │
         │                               │
         │  visitantes                   │
         │  interacoes                   │
         │  logs_sistema                 │
         └───────────────────────────────┘
```

### Fluxo completo de dados

```
1. Visitante se cadastra no Tótem
        ↓
2. Interage via chatbot, menu, imagem ou busca
        ↓
3. Interação é registrada no Oracle (tabela interacoes)
        ↓
4. Modelo Random Forest classifica o perfil do visitante
        ↓
5. Modelo SVM classifica a imagem enviada (se houver)
        ↓
6. Analytics consolida métricas e gera gráficos de engajamento
        ↓
7. Dashboard exibe KPIs, gráficos e tabela de interações recentes
```

---

## 3. Banco de Dados Oracle

### Tecnologia e conexão

O banco utiliza **Oracle Database** acessado via biblioteca `python-oracledb` em modo **thin** — sem necessidade de instalar o Oracle Instant Client na máquina. As credenciais são carregadas de variáveis de ambiente via `python-dotenv`, garantindo que nenhuma senha seja exposta no código-fonte ou no repositório.

### Modelo de dados

#### Tabela `visitantes`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único gerado automaticamente |
| nome | VARCHAR2(100) | Nome do visitante |
| perfil | VARCHAR2(50) | estudante / turista / pesquisador / profissional |
| idade_faixa | VARCHAR2(20) | jovem / adulto / idoso |
| criado_em | TIMESTAMP | Data e hora de registro |

#### Tabela `interacoes`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único |
| visitante_id | NUMBER (FK) | Referência a `visitantes.id` |
| tipo_acao | VARCHAR2(50) | chatbot / imagem / menu / busca |
| categoria | VARCHAR2(50) | arte / ciencia / historia / tecnologia |
| duracao_seg | NUMBER(5) | Tempo de interação em segundos |
| satisfacao | NUMBER(1) | Avaliação de 1 a 5 |
| registrado_em | TIMESTAMP | Data e hora da interação |

#### Tabela `logs_sistema`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único |
| modulo | VARCHAR2(50) | Módulo que gerou o evento |
| evento | VARCHAR2(200) | Descrição do evento |
| nivel | VARCHAR2(10) | INFO / WARN / ERROR |
| registrado_em | TIMESTAMP | Data e hora do log |

---

## 4. Módulos do Sistema

### `modules/db.py` — Persistência de dados
Gerencia a conexão com o Oracle e expõe funções CRUD para todos os módulos da aplicação. Implementa o padrão de abrir e fechar a conexão a cada operação, evitando conexões ociosas no servidor da FIAP.

### `modules/chatbot.py` — Interação conversacional
Implementa o fluxo de diálogo do tótem. Processa a entrada de texto do visitante, identifica a intenção (consulta de conteúdo, navegação, ajuda) e retorna respostas contextualizadas sobre o ambiente visitado. Mantém um contexto de sessão para respostas coerentes ao longo da conversa.

### `modules/vision.py` — Visão Computacional
Pipeline completo de classificação de imagens:
1. Geração de dataset simulado com paletas de cor por categoria
2. Extração de features via histograma HSV (48 dimensões)
3. Treinamento de SVM com kernel RBF
4. Classificação em tempo real de imagens enviadas pelo visitante

### `modules/analytics.py` — Análise de engajamento
Consulta o banco Oracle, transforma os dados em DataFrames Pandas e gera quatro gráficos de engajamento com tema escuro consistente com a interface. Exporta relatório consolidado em CSV para uso na documentação final.

### `models/train_model.py` — Classificador de perfil
Pipeline de Machine Learning que treina um Random Forest sobre os dados de interação para prever o perfil do visitante. Inclui pré-processamento, divisão treino/teste, validação cruzada e persistência do modelo em arquivo `.pkl`.

---

## 5. Modelos de Inteligência Artificial

### Classificador de Perfil de Visitante

| Atributo | Detalhe |
|----------|---------|
| Algoritmo | Random Forest Classifier |
| Biblioteca | scikit-learn 1.4.1 |
| Features de entrada | tipo_acao, categoria, duracao_seg, satisfacao, idade_faixa |
| Target | perfil (estudante / turista / pesquisador / profissional) |
| Divisão | 80% treino / 20% teste (estratificada) |
| Avaliação | Acurácia, F1-score, Cross-validation 5-fold |
| **Acurácia no teste** | **91,84%** |
| Persistência | `models/model.pkl` + `models/encoders.pkl` |

**Justificativa do algoritmo:** o Random Forest foi escolhido por sua robustez com dados tabulares mistos, resistência a overfitting via ensemble de árvores e geração nativa de importância de features — útil para interpretar quais variáveis mais influenciam o perfil do visitante.

### Classificador de Imagem (Visão Computacional)

| Atributo | Detalhe |
|----------|---------|
| Algoritmo | SVM com kernel RBF |
| Biblioteca | scikit-learn + OpenCV 4.9 |
| Features de entrada | Histograma HSV — 48 dimensões (3 canais × 16 bins) |
| Target | categoria (arte / ciencia / historia / tecnologia) |
| Dataset | 240 imagens sintéticas (60 por categoria) |
| **Acurácia no teste** | **~93%** |
| Persistência | `models/vision_model.pkl` |

**Justificativa do algoritmo:** o SVM com kernel RBF foi preferido ao Random Forest para este problema porque lida melhor com features de histograma de alta dimensionalidade, encontrando fronteiras de decisão não-lineares entre as assinaturas de cor de cada categoria.

---

## 6. Tecnologias Utilizadas

| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|--------------|
| Interface | Streamlit | 1.32.0 | Prototipagem rápida de dashboards em Python |
| Banco de dados | Oracle Database | — | Robusto, transacional, disponível na FIAP |
| Driver Oracle | python-oracledb | 2.1.2 | Modo thin, sem Instant Client |
| Machine Learning | scikit-learn | 1.4.1 | Biblioteca consolidada para ML clássico |
| Visão Computacional | OpenCV | 4.9.0 | Processamento de imagem em tempo real |
| Análise de dados | Pandas | 2.2.1 | Manipulação de DataFrames |
| Visualização | Matplotlib + Seaborn | 3.8.3 / 0.13.2 | Gráficos analíticos com tema customizado |
| Geração de dados | Faker | 24.3.0 | Dados simulados realistas em português |
| Persistência de modelos | Joblib | 1.3.2 | Serialização eficiente de objetos scikit-learn |
| Variáveis de ambiente | python-dotenv | 1.0.1 | Segurança das credenciais |

---

## 7. Segurança e Boas Práticas

- **Credenciais protegidas:** todas as senhas e DSN do Oracle ficam no arquivo `.env`, que está no `.gitignore` e nunca é enviado ao repositório. O repositório contém apenas o `.env.example` com campos vazios.
- **Repositório privado:** o projeto foi mantido como repositório privado no GitHub, conforme orientação da FIAP para projetos Challenge.
- **Dados simulados:** nenhum dado pessoal real foi utilizado. Os visitantes foram gerados com a biblioteca Faker.
- **Modelos não versionados:** os arquivos `.pkl` estão no `.gitignore`, pois são gerados localmente. Isso evita o versionamento de binários grandes e garante que o modelo seja sempre retreinado com os dados mais recentes.

---

## 8. Estrutura Final do Repositório

```
totem-flexmedia/
├── app.py                          Interface principal Streamlit
├── requirements.txt                Dependências do projeto
├── .env.example                    Template de variáveis de ambiente
├── .gitignore                      Arquivos ignorados pelo Git
├── README.md                       Guia de instalação e execução
│
├── data/
│   ├── gerar_dados.py              Geração de dados simulados + população do Oracle
│   └── dataset.csv                 Dataset exportado (gerado localmente)
│
├── models/
│   ├── train_model.py              Pipeline de ML — Random Forest
│   ├── confusion_matrix.png        Matriz de confusão do classificador
│   └── feature_importance.png      Importância das features
│
├── modules/
│   ├── __init__.py
│   ├── db.py                       Conexão Oracle + CRUD
│   ├── chatbot.py                  Lógica de diálogo
│   ├── vision.py                   Visão computacional (SVM + OpenCV)
│   └── analytics.py                Métricas e gráficos de engajamento
│
└── docs/
    ├── arquitetura.md              Este documento
    ├── guia-implantacao.md         Setup do ambiente e Git
    ├── guia-dia2.md                Treinamento do modelo
    ├── correcao-acuracia.md        Diagnóstico e correção da acurácia
    ├── guia-dia3.md                Visão computacional
    ├── guia-dia4.md                Chatbot
    ├── guia-dia5.md                Interface Streamlit
    ├── guia-dia6.md                Analytics
    └── relatorio-analitico.md      Relatório analítico final
```
