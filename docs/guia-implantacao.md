# 🚀 Guia de Implantação — Tótem Inteligente FlexMedia

Guia completo de configuração do ambiente, conexão com Oracle e boas práticas de Git/GitHub para o projeto Challenge FlexMedia.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

| Ferramenta | Versão mínima | Download |
|-----------|--------------|---------|
| Python | 3.11+ | https://python.org |
| Git | 2.40+ | https://git-scm.com |
| VS Code (recomendado) | Qualquer | https://code.visualstudio.com |

---

## PARTE 1 — Configuração do Repositório Git

### 1.1 Criando o repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"New repository"** (botão verde no canto superior direito)
3. Preencha:
   - **Repository name:** `totem-flexmedia`
   - **Description:** `Tótem Inteligente FlexMedia — Challenge FIAP Sprint 4`
   - **Visibility:** `Private` ✅ (obrigatório conforme orientação da FIAP)
   - Marque **"Add a README file"**: ❌ (não marque — já temos o nosso)
4. Clique em **"Create repository"**

---

### 1.2 Configurando o Git localmente (primeira vez)

Abra o terminal e execute:

```bash
# Configure seu nome e e-mail (use o mesmo do GitHub)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Verificar se foi configurado corretamente
git config --global --list
```

---

### 1.3 Clonando o repositório vazio

```bash
# Clone o repositório que você criou no GitHub
git clone https://github.com/SEU_USUARIO/totem-flexmedia.git

# Entre na pasta
cd totem-flexmedia
```

---

### 1.4 Copiando os arquivos do projeto

Copie todos os arquivos entregues neste ZIP para dentro da pasta `totem-flexmedia/` que foi clonada.

A estrutura final deve ficar assim:

```
totem-flexmedia/
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
├── data/
│   └── gerar_dados.py
├── docs/
│   └── arquitetura.md
└── modules/
    ├── __init__.py
    └── db.py
```

---

### 1.5 Primeiro commit — estrutura base

```bash
# Verifica o status dos arquivos (quais serão commitados)
git status

# Adiciona todos os arquivos ao staging
git add .

# Cria o primeiro commit
git commit -m "feat: estrutura inicial do projeto e módulo de banco de dados"

# Envia para o GitHub
git push origin main
```

> ⚠️ **Atenção:** O arquivo `.env` (com suas senhas) está no `.gitignore` e **nunca será enviado ao GitHub**. Apenas o `.env.example` vai para o repositório.

---

## PARTE 2 — Configuração do Ambiente Python

### 2.1 Criando o ambiente virtual

```bash
# Cria o ambiente virtual dentro do projeto
python -m venv venv
```

Ativando o ambiente:

```bash
# Windows (Prompt de Comando)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

Você saberá que o ambiente está ativo quando o terminal mostrar `(venv)` no início da linha.

---

### 2.2 Instalando as dependências

```bash
# Com o ambiente virtual ativo
pip install -r requirements.txt

# Verificar se tudo foi instalado
pip list
```

---

## PARTE 3 — Configuração do Banco de Dados Oracle

### 3.1 Criando o arquivo .env

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Abra o arquivo `.env` no VS Code e preencha com suas credenciais da FIAP:

```env
ORACLE_USER=rm12345          # Seu RM sem "rm"
ORACLE_PASSWORD=DD/MM/AAAA   # Sua data de nascimento (formato padrão FIAP)
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

> 💡 **Dica:** As credenciais Oracle da FIAP geralmente seguem o padrão:
> - Usuário: `rmSEU_RM` (ex: `rm12345`)
> - Senha: data de nascimento no formato `DD/MM/AAAA`
> - DSN: confirme com seu professor o endereço exato do servidor

---

### 3.2 Testando a conexão

```bash
# Executa apenas o teste de conexão
python -c "from modules.db import get_connection; conn = get_connection(); print('Conexão OK!'); conn.close()"
```

Se aparecer `Conexão OK!`, está tudo certo. Caso contrário, verifique:
- ✅ Você está conectado à rede da FIAP (ou VPN se estiver em casa)
- ✅ As credenciais no `.env` estão corretas
- ✅ O ambiente virtual está ativo

---

### 3.3 Criando as tabelas e gerando os dados

```bash
# Cria as tabelas no Oracle e popula com dados simulados
python data/gerar_dados.py
```

A saída esperada é:

```
[DADOS] Criando tabelas (se não existirem)...
[DB] Tabela 'visitantes' criada com sucesso.
[DB] Tabela 'interacoes' criada com sucesso.
[DB] Tabela 'logs_sistema' criada com sucesso.
[DADOS] Gerando 150 visitantes...
  20/150 visitantes inseridos...
  40/150 visitantes inseridos...
  ...
[DADOS] Inserção concluída. Total de interações: ~550
[CSV] Dataset exportado para: data/dataset.csv
[OK] Dia 1 concluído. Banco populado e CSV gerado.
```

---

## PARTE 4 — Fluxo de Trabalho Git (Boas Práticas)

### 4.1 Estratégia de branches

Nunca trabalhe direto na branch `main`. Use a seguinte estrutura:

```
main          ← versão estável, só recebe merges aprovados
└── develop   ← branch de desenvolvimento contínuo
    ├── feature/banco-de-dados
    ├── feature/modelo-ia
    ├── feature/visao-computacional
    ├── feature/chatbot
    └── feature/analytics
```

Criando a branch de desenvolvimento:

```bash
git checkout -b develop
git push origin develop
```

Criando uma branch para cada funcionalidade:

```bash
# Exemplo: trabalhando no módulo de IA
git checkout develop
git checkout -b feature/modelo-ia
```

---

### 4.2 Padrão de commits (Conventional Commits)

Use prefixos padronizados para mensagens de commit. Isso facilita a leitura do histórico e impressiona avaliadores:

| Prefixo | Quando usar | Exemplo |
|---------|------------|---------|
| `feat:` | Nova funcionalidade | `feat: adiciona classificador de perfil de visitante` |
| `fix:` | Correção de bug | `fix: corrige erro de conexão com Oracle` |
| `docs:` | Documentação | `docs: atualiza README com instruções de instalação` |
| `refactor:` | Refatoração sem mudar comportamento | `refactor: extrai lógica de conexão para função separada` |
| `test:` | Adição de testes | `test: adiciona teste de inserção no banco` |
| `chore:` | Tarefas de manutenção | `chore: atualiza dependências do requirements.txt` |

```bash
# Exemplos de commits bem escritos
git commit -m "feat: cria tabelas visitantes, interacoes e logs_sistema no Oracle"
git commit -m "feat: implementa geração de 150 visitantes simulados com Faker"
git commit -m "docs: adiciona documentação técnica da arquitetura"
```

---

### 4.3 Ciclo diário de trabalho

```bash
# 1. Sempre comece atualizando sua branch
git checkout develop
git pull origin develop

# 2. Crie ou mude para a branch da funcionalidade
git checkout feature/nome-da-feature

# 3. Faça suas alterações e commite com frequência
git add .
git commit -m "feat: descreva o que foi feito"

# 4. Ao terminar a feature, integre ao develop
git checkout develop
git merge feature/nome-da-feature
git push origin develop

# 5. Quando o projeto estiver estável, suba para a main
git checkout main
git merge develop
git push origin main
```

---

### 4.4 Adicionando colaboradores ao repositório

1. No GitHub, vá em **Settings → Collaborators**
2. Clique em **"Add people"**
3. Busque pelo nome ou e-mail do seu colega de grupo
4. Selecione a permissão **"Write"**

---

### 4.5 Protegendo a branch main (boa prática)

1. No GitHub, vá em **Settings → Branches**
2. Clique em **"Add branch protection rule"**
3. Em "Branch name pattern", digite `main`
4. Marque **"Require a pull request before merging"**
5. Clique em **"Create"**

Isso impede que alguém suba código quebrado direto na main.

---

## PARTE 5 — Estrutura de Commits por Sprint

Para organizar o histórico do projeto, use tags para marcar cada entrega:

```bash
# Ao final do Dia 1
git tag -a v0.1.0 -m "Sprint 4 - Dia 1: Banco de dados e dados simulados"
git push origin v0.1.0

# Ao final do Dia 2
git tag -a v0.2.0 -m "Sprint 4 - Dia 2: Modelo de classificação IA"
git push origin v0.2.0

# Entrega final
git tag -a v1.0.0 -m "Sprint 4 - Entrega final: Sistema completo"
git push origin v1.0.0
```

---

## PARTE 6 — Checklist de Entrega Final

Antes de entregar o link do repositório, verifique:

- [ ] O repositório está como **Private** no GitHub
- [ ] O arquivo `.env` **não está** no repositório (apenas `.env.example`)
- [ ] O `README.md` está completo com instruções de instalação
- [ ] Todos os commits seguem o padrão `tipo: descrição`
- [ ] O código está organizado em branches (`main`, `develop`, `feature/*`)
- [ ] A tag `v1.0.0` foi criada e enviada
- [ ] A documentação técnica está em `docs/arquitetura.md`
- [ ] Os professores foram adicionados como colaboradores (se necessário)

---

## ❓ Problemas Comuns

**Erro: `ORA-01017: invalid username/password`**
→ Verifique as credenciais no `.env`. Lembre-se que a FIAP pode usar `rm` minúsculo antes do número.

**Erro: `DPY-6001: cannot connect to database`**
→ Você precisa estar na rede da FIAP ou usar a VPN. Conecte-se e tente novamente.

**Erro: `ModuleNotFoundError`**
→ O ambiente virtual não está ativo. Execute `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac).

**Git pede usuário e senha a cada push**
→ Configure autenticação via token:
```bash
git remote set-url origin https://SEU_TOKEN@github.com/SEU_USUARIO/totem-flexmedia.git
```
Gere o token em: GitHub → Settings → Developer settings → Personal access tokens.
