# Documentação Técnica — Tótem Inteligente FlexMedia

## 1. Visão Geral

O Tótem Inteligente FlexMedia é um sistema digital interativo projetado para ambientes de visitação (museus, centros culturais, eventos tecnológicos). Ele combina coleta de dados, inteligência artificial e visualização analítica para oferecer uma experiência personalizada ao visitante e insights de engajamento ao gestor do espaço.

---

## 2. Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   INTERFACE (Streamlit)                  │
│         Chatbot │ Classificador │ Visão │ Analytics      │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼──────┐ ┌─────▼──────┐ ┌────▼───────┐
    │  chatbot.py │ │ vision.py  │ │analytics.py│
    │  (Diálogo) │ │  (OpenCV)  │ │ (Pandas)   │
    └─────┬──────┘ └─────┬──────┘ └────┬───────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
                  ┌──────▼──────┐
                  │    db.py    │
                  │  (OracleDB) │
                  └──────┬──────┘
                         │
              ┌───────────────────────┐
              │   ORACLE DATABASE     │
              │  visitantes           │
              │  interacoes           │
              │  logs_sistema         │
              └───────────────────────┘
```

---

## 3. Banco de Dados

### Tecnologia
Oracle Database — acessado via biblioteca `python-oracledb` em modo **thin** (sem necessidade do Oracle Instant Client instalado).

### Tabelas

#### `visitantes`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único |
| nome | VARCHAR2(100) | Nome do visitante |
| perfil | VARCHAR2(50) | estudante / turista / pesquisador / profissional |
| idade_faixa | VARCHAR2(20) | jovem / adulto / idoso |
| criado_em | TIMESTAMP | Data/hora de registro |

#### `interacoes`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único |
| visitante_id | NUMBER (FK) | Referência ao visitante |
| tipo_acao | VARCHAR2(50) | chatbot / imagem / menu / busca |
| categoria | VARCHAR2(50) | arte / ciencia / historia / tecnologia |
| duracao_seg | NUMBER(5) | Tempo de interação em segundos |
| satisfacao | NUMBER(1) | Avaliação de 1 a 5 |
| registrado_em | TIMESTAMP | Data/hora da interação |

#### `logs_sistema`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | NUMBER (PK) | Identificador único |
| modulo | VARCHAR2(50) | Módulo que gerou o log |
| evento | VARCHAR2(200) | Descrição do evento |
| nivel | VARCHAR2(10) | INFO / WARN / ERROR |
| registrado_em | TIMESTAMP | Data/hora do log |

---

## 4. Módulos

### `modules/db.py`
Gerencia a conexão com o Oracle e expõe funções CRUD para os demais módulos. Usa variáveis de ambiente para as credenciais (arquivo `.env`).

### `modules/chatbot.py`
Implementa o fluxo de diálogo do tótem. Processa a entrada de texto do visitante, classifica a intenção e retorna uma resposta contextualizada sobre o ambiente visitado.

### `modules/vision.py`
Processa imagens capturadas ou enviadas pelo visitante. Utiliza OpenCV para pré-processamento e um classificador treinado para identificar categorias visuais.

### `modules/analytics.py`
Consulta o banco de dados e gera visualizações analíticas com Pandas, Matplotlib e Seaborn: frequência por categoria, satisfação média, uso ao longo do tempo.

### `models/train_model.py`
Treina um classificador (Random Forest) sobre o dataset de interações para prever o perfil do visitante com base no comportamento de uso.

---

## 5. Fluxo de Dados

```
1. Visitante interage com o Tótem (texto, imagem ou menu)
        ↓
2. Ação é processada pelo módulo correspondente
        ↓
3. Interação é registrada no Oracle (tabela interacoes)
        ↓
4. Classificador prediz perfil e categoria de interesse
        ↓
5. Dashboard de Analytics consolida métricas de engajamento
```

---

## 6. Tecnologias e Justificativas

| Tecnologia | Justificativa |
|-----------|---------------|
| Python 3.11 | Ecossistema rico para IA e dados |
| Oracle DB | Banco robusto para dados transacionais |
| python-oracledb | Driver oficial Oracle, modo thin sem instalação extra |
| Streamlit | Prototipagem rápida de interfaces web em Python |
| Scikit-learn | Biblioteca consolidada para ML clássico |
| OpenCV | Processamento de imagem em tempo real |
| Pandas/Seaborn | Análise e visualização de dados |
| Faker | Geração de dados realistas para simulação |
