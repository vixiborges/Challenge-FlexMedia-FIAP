FIAP - Faculdade de Informática e Administração Paulista
FIAP - Faculdade de Informática e Admnistração Paulista


Flexmedia - Sprint final

👨‍🎓 Integrantes:
Gustavo Borges Marinho Peres

📜 Descrição
Totem interativo para museus, exposições, e eventos sociais, desenvolvido utilizando Python e SQL, e interface com Streamlit, o totem permite que o usuário interaja via chatbot, buscando informações sobre o evento. Além disso também foi treinado um modelo para previsão e classificação de interações, identificando o possível perfil do usuário. Também foi desenvolvido um módulo de visão computacional, onde, a partir de imagens geradas, é possível identificar o tema do objeto. para finalizar, temos uma tela de analytics, com os principais indicadores, gráficos e o registro das últimas interações.

📁 Estrutura de pastas
Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

data: Nesta pasta ficarão os arquivos gerados, como as imagens para o módulo de visão computacional.

models: Aqui estão os arquivos relacionados ao treinamento do modelo de classificação de usuários.

modules: Aqui estão os módulos presentes na aplicação (analytics, chatbot, db e vision)

README.md: arquivo que serve como guia e explicação geral sobre o projeto.

🔧 Como executar o código
Crie e ative o ambiente virtual (python -m venv venv e venv\Scripts\activate) e instale as bibliotecas e dependencias (pip install -r requirements.txt).

Passo 1
    Inicializar o banco e gerar dados > python data/gerar_dados.py

Passo 2
    Treinar modelo de IA > python models/train_model.py

Passo 3
    Rodar a aplicação > streamlit run app.py

🗃 Histórico de lançamentos
0.4.0 - 17/04/2026 Fix analytics e adição do chatbot
0.3.0 - 16/04/2026 Refinamento e alterações no estilo da aplicação
0.2.0 - 13/04/2026 Repopulação das tabelas, treinamento do modelo e módulo de visão computacional
0.1.0 - 08/04/2026 Commit inicial
📋 Licença

MODELO GIT FIAP por Fiap está licenciado sobre Attribution 4.0 International.