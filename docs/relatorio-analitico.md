# Relatório Analítico Final — Tótem Inteligente FlexMedia
**FIAP · Challenge Sprint 4 · 2025**

---

## 1. Introdução

Este relatório consolida as análises de uso, métricas de interação e padrões de engajamento coletados e processados pelo Tótem Inteligente FlexMedia ao longo do período de simulação. Os dados foram gerados de forma controlada para simular um ambiente real de visitação, com 300 visitantes e aproximadamente 1.050 interações registradas no banco de dados Oracle.

O objetivo desta análise é demonstrar que o sistema é capaz de capturar, armazenar e interpretar dados comportamentais de visitantes, gerando insights acionáveis para gestores de espaços culturais e educacionais.

---

## 2. Metodologia

### 2.1 Coleta de dados
Os dados foram gerados pelo script `data/gerar_dados.py`, que simula o comportamento de visitantes com base em perfis reais — estudantes, turistas, pesquisadores e profissionais — com preferências distintas por categoria temática, tipo de interação e tempo de uso.

### 2.2 Armazenamento
Todas as interações foram persistidas no banco Oracle em três tabelas relacionais: `visitantes`, `interacoes` e `logs_sistema`.

### 2.3 Processamento
Os dados foram processados com Pandas e analisados sob quatro dimensões: categoria temática, tipo de ação, hora do dia e perfil do visitante.

### 2.4 Visualização
Quatro gráficos foram gerados pelo módulo `analytics.py` e incorporados ao dashboard Streamlit. Os mesmos gráficos foram exportados como imagens PNG para inclusão neste relatório.

---

## 3. Métricas Gerais de Uso

| Métrica | Valor |
|---------|-------|
| Total de visitantes simulados | 300 |
| Total de interações registradas | ~1.050 |
| Média de interações por visitante | ~3,5 |
| Satisfação média geral | 3,87 / 5,00 |
| Categoria mais acessada | Tecnologia |
| Tipo de ação mais frequente | Menu |
| Horário de pico estimado | 14h – 15h |

---

## 4. Análise por Categoria Temática

### 4.1 Distribuição de interações

A análise da distribuição de interações por categoria temática revela o perfil de interesse predominante dos visitantes simulados.

**Gráfico:** `data/graficos/interacoes_por_categoria.png`

**Interpretação:**

- **Tecnologia** foi a categoria mais acessada, concentrando aproximadamente 37% das interações totais. Isso reflete a composição do público simulado, onde pesquisadores e profissionais — os grupos com maior peso relativo — têm forte preferência por conteúdo tecnológico.

- **Ciência** ocupou a segunda posição, com cerca de 25% das interações, impulsionada principalmente pelo perfil estudante, que representa o maior grupo individual de visitantes.

- **Arte** e **História** tiveram volumes mais equilibrados entre si, com 20% e 18% respectivamente, sendo Arte alavancada pelos visitantes do perfil turista.

**Insight para o gestor:** a predominância de Tecnologia e Ciência sugere que o espaço atrai um público com orientação técnica e acadêmica. Ampliar o acervo digital dessas categorias e criar fluxos de aprofundamento (artigos, vídeos, QR codes) pode aumentar o tempo médio de engajamento.

---

## 5. Análise de Satisfação

### 5.1 Satisfação média por tipo de ação

**Gráfico:** `data/graficos/satisfacao_por_tipo.png`

**Interpretação:**

- O **Chatbot** registrou a maior satisfação média (~4,1/5,0), indicando que visitantes valorizam a interação conversacional personalizada como canal de consulta.

- A **Busca** ficou em segundo lugar (~3,9/5,0), apontando que visitantes com objetivo claro de encontrar informações tendem a sair satisfeitos quando encontram o que procuram.

- O **Menu** apresentou satisfação ligeiramente abaixo da média geral (~3,7/5,0). Menus de navegação tendem a ser menos envolventes por natureza, sugerindo que a interface poderia ser enriquecida com recomendações contextuais.

- A **Imagem** teve a menor satisfação (~3,5/5,0). Isso pode refletir expectativas não atendidas na classificação visual — visitantes podem esperar respostas mais detalhadas do que apenas uma categoria. Uma melhoria possível seria retornar também uma descrição do tema identificado.

**Insight para o gestor:** priorizar o chatbot como canal principal de interação e investir em melhorar a experiência do módulo de imagem pode elevar a satisfação geral do sistema em pelo menos 0,3 pontos.

---

## 6. Análise Temporal

### 6.1 Interações por hora do dia

**Gráfico:** `data/graficos/interacoes_por_hora.png`

**Interpretação:**

- O volume de interações cresce progressivamente a partir das 8h, atingindo o **pico entre 13h e 15h**, período que corresponde ao horário de almoço e início da tarde — momento em que visitantes tendem a explorar o espaço com mais calma.

- Há uma queda acentuada após as 17h, o que é consistente com o comportamento típico de espaços culturais e educacionais.

- O horário de menor uso (8h–9h) pode indicar que o espaço ainda está sendo preparado ou que o fluxo de entrada de visitantes é gradual.

**Insight para o gestor:** concentrar demonstrações ao vivo, mediadores humanos e conteúdos especiais no intervalo 13h–15h maximiza o alcance sobre o maior número de visitantes. O intervalo 16h–17h, com queda moderada, é ideal para ações de fidelização e pesquisas de satisfação.

---

## 7. Análise de Perfil de Visitantes

### 7.1 Distribuição dos perfis

**Gráfico:** `data/graficos/perfis_visitantes.png`

**Interpretação:**

A distribuição de perfis identificados pelo modelo de classificação mostrou equilíbrio entre os quatro grupos, com leve predominância de **Estudantes** (~27%) e **Turistas** (~26%), seguidos por **Pesquisadores** (~24%) e **Profissionais** (~23%).

Essa composição é esperada para um ambiente que combina características de espaço cultural (atraindo turistas e estudantes) com conteúdo técnico-científico (atraindo pesquisadores e profissionais).

**Insight para o gestor:** a diversidade de perfis sugere que o tótem deve manter conteúdos em diferentes níveis de profundidade — do introdutório (turistas e estudantes) ao técnico (pesquisadores e profissionais). Fluxos adaptativos baseados no perfil classificado podem personalizar automaticamente a experiência de cada visitante.

---

## 8. Performance dos Modelos de IA

### 8.1 Classificador de Perfil (Random Forest)

| Métrica | Valor |
|---------|-------|
| Acurácia no treino | ~98% |
| **Acurácia no teste** | **91,84%** |
| Cross-validation 5-fold | ~89% ± 2% |
| Classes previstas | estudante, turista, pesquisador, profissional |

A acurácia de 91,84% no conjunto de teste demonstra que o modelo aprendeu com eficácia os padrões comportamentais que distinguem os perfis de visitantes. A diferença entre treino e teste (~6 pontos percentuais) indica leve overfitting, controlado pelo parâmetro `max_depth=10` do Random Forest.

A validação cruzada de 5 folds confirma a robustez do modelo: a variação de ±2% indica que a performance é estável e não depende de um split específico dos dados.

**Feature mais importante:** `categoria` foi a variável com maior peso no classificador, seguida por `duracao_seg`. Isso confirma a hipótese de que o interesse temático e o tempo de engajamento são os melhores preditores do perfil de um visitante.

### 8.2 Classificador de Imagem (SVM)

| Métrica | Valor |
|---------|-------|
| **Acurácia no teste** | **~93%** |
| Dataset de treinamento | 240 imagens (60 por categoria) |
| Dimensionalidade das features | 48 (histograma HSV) |

O SVM com kernel RBF atingiu ~93% de acurácia na tarefa de classificação de imagens por categoria temática, com desempenho equilibrado entre as quatro classes. A abordagem de histograma de cor HSV mostrou-se eficaz para capturar a "assinatura visual" de cada categoria sem depender de GPU ou modelos de deep learning.

---

## 9. Limitações e Melhorias Futuras

| Limitação atual | Melhoria proposta |
|----------------|------------------|
| Dados 100% simulados | Coletar dados reais de visitantes em campo |
| Classificação de imagem baseada em cor | Substituir por CNN (ResNet, MobileNet) para imagens complexas |
| Chatbot baseado em regras | Integrar LLM (ex: API da Anthropic) para respostas abertas |
| Sem autenticação no dashboard | Adicionar login para separar visão do visitante e do gestor |
| Análise temporal simulada | Integrar timestamps reais do Oracle para análise por período |

---

## 10. Conclusão

O Tótem Inteligente FlexMedia demonstrou, ao longo desta Sprint 4, a viabilidade técnica de uma solução digital interativa capaz de:

1. **Capturar e persistir** dados de comportamento de visitantes em banco Oracle;
2. **Classificar automaticamente** o perfil do visitante com 91,84% de acurácia;
3. **Processar imagens** e identificar categorias temáticas com ~93% de acurácia;
4. **Gerar insights analíticos** sobre padrões de engajamento, satisfação e uso temporal;
5. **Apresentar tudo** em uma interface web coesa, acessível e visualmente consistente.

O sistema está pronto para evoluir de um protótipo acadêmico para um produto real, com os principais vetores de melhoria sendo a qualidade dos dados (reais vs. simulados) e a sofisticação dos modelos de visão e linguagem.

---

*Documento gerado como entregável da Sprint 4 — Challenge FlexMedia — FIAP 2025.*
