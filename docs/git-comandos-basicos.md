# Comandos Git - GitHub e GitLab

Guia de referência rápida para inicializar, conectar e gerenciar repositórios Git no GitHub e GitLab.

## 📦 Inicializar Repositório Local

### Novo Projeto

```bash
# Inicializar repositório Git
git init

# Configurar nome e email (se ainda não configurou globalmente)
git config user.name "Seu Nome"
git config user.email "seu.email@example.com"

# Adicionar todos os arquivos
git add .

# Criar commit inicial
git commit -m "Initial commit"
```

### Projeto Existente (Clone)

```bash
# GitHub
git clone https://github.com/usuario/repositorio.git

# GitLab
git clone https://gitlab.com/usuario/repositorio.git

# Entrar na pasta
cd repositorio
```

## 🌐 Conectar ao GitHub

### Método 1: HTTPS (Recomendado para iniciantes)

```bash
# Adicionar remote
git remote add origin https://github.com/USUARIO/REPOSITORIO.git

# Verificar remote
git remote -v

# Renomear branch para main
git branch -M main

# Push inicial (com tracking)
git push -u origin main
```

### Método 2: SSH (Mais seguro, sem senha)

**Pré-requisito:** Configurar chave SSH no GitHub

```bash
# Adicionar remote via SSH
git remote add origin git@github.com:USUARIO/REPOSITORIO.git

# Renomear branch e push
git branch -M main
git push -u origin main
```

### Criar Repositório Direto pelo GitHub CLI

```bash
# Instalar GitHub CLI
winget install --id GitHub.cli

# Autenticar
gh auth login

# Criar repositório público e fazer push
gh repo create REPOSITORIO --public --source=. --push

# Ou privado
gh repo create REPOSITORIO --private --source=. --push
```

## 🦊 Conectar ao GitLab

### Método 1: HTTPS

```bash
# Adicionar remote
git remote add origin https://gitlab.com/USUARIO/REPOSITORIO.git

# Renomear branch para main
git branch -M main

# Push inicial
git push -u origin main
```

### Método 2: SSH

**Pré-requisito:** Configurar chave SSH no GitLab

```bash
# Adicionar remote via SSH
git remote add origin git@gitlab.com:USUARIO/REPOSITORIO.git

# Renomear branch e push
git branch -M main
git push -u origin main
```

### Criar Repositório pelo GitLab CLI

```bash
# Instalar GitLab CLI
# Windows (via Scoop)
scoop install glab

# Autenticar
glab auth login

# Criar repositório e push
glab repo create REPOSITORIO --public --defaultBranch main
git push -u origin main
```

## 🔄 Gerenciar Múltiplos Remotes (GitHub + GitLab)

```bash
# Adicionar GitHub como 'origin'
git remote add origin https://github.com/USUARIO/REPO.git

# Adicionar GitLab como 'gitlab'
git remote add gitlab https://gitlab.com/USUARIO/REPO.git

# Ver todos os remotes
git remote -v

# Push para ambos
git push origin main
git push gitlab main

# Ou criar um remote que faz push para ambos
git remote set-url --add --push origin https://github.com/USUARIO/REPO.git
git remote set-url --add --push origin https://gitlab.com/USUARIO/REPO.git

# Agora 'git push origin main' envia para os dois!
```

## 📤 Workflow Completo - Subir para Main

### Primeira Vez (Setup Inicial)

```bash
# 1. Inicializar e commit inicial
git init
git add .
git commit -m "Initial commit"

# 2. Conectar ao remote (GitHub ou GitLab)
git remote add origin https://github.com/USUARIO/REPO.git

# 3. Renomear branch para main
git branch -M main

# 4. Push com tracking
git push -u origin main
```

### Workflow Diário

```bash
# 1. Ver status
git status

# 2. Adicionar arquivos modificados
git add .                    # Todos os arquivos
git add arquivo.py          # Arquivo específico
git add src/                # Diretório específico

# 3. Commit
git commit -m "Descrição das mudanças"

# 4. Push para main
git push

# Ou especificando (se não usou -u antes)
git push origin main
```

### Workflow com Branches

```bash
# 1. Criar e mudar para nova branch
git checkout -b feature/nova-funcionalidade

# 2. Fazer alterações e commit
git add .
git commit -m "Add nova funcionalidade"

# 3. Push da branch
git push -u origin feature/nova-funcionalidade

# 4. Merge na main (via Pull Request/Merge Request)
# Ou localmente:
git checkout main
git merge feature/nova-funcionalidade
git push

# 5. Deletar branch (opcional)
git branch -d feature/nova-funcionalidade
git push origin --delete feature/nova-funcionalidade
```

## 🔍 Comandos de Consulta

```bash
# Ver status atual
git status

# Ver histórico de commits
git log
git log --oneline              # Formato compacto
git log --graph --oneline      # Com gráfico

# Ver diferenças não commitadas
git diff

# Ver diferenças commitadas
git diff HEAD~1 HEAD

# Ver remotes configurados
git remote -v

# Ver branches
git branch                     # Locais
git branch -r                  # Remotas
git branch -a                  # Todas
```

## 🔧 Comandos de Configuração

```bash
# Configuração global (para todos os projetos)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Configuração local (só para este projeto)
git config user.name "Outro Nome"
git config user.email "outro@email.com"

# Ver configurações
git config --list
git config user.name
git config user.email

# Configurar editor padrão
git config --global core.editor "code --wait"  # VS Code

# Configurar line endings (Windows)
git config --global core.autocrlf true

# Salvar credenciais HTTPS
git config --global credential.helper store
```

## 🛠️ Comandos Úteis

### Desfazer Mudanças

```bash
# Desfazer mudanças não commitadas em arquivo
git checkout -- arquivo.py

# Desfazer todos os arquivos não commitados
git checkout -- .

# Remover arquivo do stage (antes do commit)
git reset HEAD arquivo.py

# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Desfazer último commit (descarta alterações)
git reset --hard HEAD~1

# Reverter commit específico (cria novo commit)
git revert <commit-hash>
```

### Atualizar do Remote

```bash
# Buscar mudanças (não aplica)
git fetch origin

# Buscar e aplicar (merge)
git pull origin main

# Ou apenas
git pull

# Pull com rebase (história linear)
git pull --rebase
```

### Gerenciar Remotes

```bash
# Adicionar remote
git remote add nome-remote URL

# Remover remote
git remote remove nome-remote

# Renomear remote
git remote rename antigo novo

# Alterar URL do remote
git remote set-url origin NOVA_URL

# Ver detalhes de um remote
git remote show origin
```

### Stash (Guardar Temporariamente)

```bash
# Guardar mudanças não commitadas
git stash

# Guardar com mensagem
git stash save "Mensagem descritiva"

# Listar stashes
git stash list

# Aplicar último stash
git stash apply

# Aplicar e remover último stash
git stash pop

# Aplicar stash específico
git stash apply stash@{0}

# Remover stash
git stash drop stash@{0}

# Limpar todos os stashes
git stash clear
```

### Tags

```bash
# Criar tag
git tag v1.0.0

# Criar tag anotada
git tag -a v1.0.0 -m "Versão 1.0.0"

# Listar tags
git tag

# Push tag específica
git push origin v1.0.0

# Push todas as tags
git push origin --tags

# Deletar tag local
git tag -d v1.0.0

# Deletar tag remota
git push origin --delete v1.0.0
```

## 📋 .gitignore Essencial

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/

# Virtual Environment
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Secrets
.env
.secrets.*
*.key
*.pem

# Logs
*.log
log/

# Testing
.pytest_cache/
.coverage
htmlcov/
```

## 🔐 Configurar SSH (GitHub/GitLab)

### Gerar Chave SSH

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu.email@example.com"

# Ou RSA (se ed25519 não disponível)
ssh-keygen -t rsa -b 4096 -C "seu.email@example.com"

# Salvar em: C:\Users\SEU_USUARIO\.ssh\id_ed25519
# Senha: (opcional, mas recomendado)

# Iniciar ssh-agent
Get-Service ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent

# Adicionar chave ao ssh-agent
ssh-add C:\Users\SEU_USUARIO\.ssh\id_ed25519
```

### Adicionar Chave Pública ao GitHub

1. Copiar chave pública:
```bash
Get-Content C:\Users\SEU_USUARIO\.ssh\id_ed25519.pub | Set-Clipboard
```

2. GitHub → Settings → SSH and GPG keys → New SSH key
3. Cole a chave e salve

### Adicionar Chave Pública ao GitLab

1. Mesmo processo de copiar:
```bash
Get-Content C:\Users\SEU_USUARIO\.ssh\id_ed25519.pub | Set-Clipboard
```

2. GitLab → Preferences → SSH Keys
3. Cole a chave e salve

### Testar Conexão

```bash
# GitHub
ssh -T git@github.com

# GitLab
ssh -T git@gitlab.com
```

## 📊 Aliases Úteis

```bash
# Criar aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'

# Usar aliases
git st           # = git status
git co main      # = git checkout main
git visual       # = git log --graph --oneline --all
```

## 🚨 Troubleshooting

### "fatal: refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

### Alterar último commit (mensagem ou arquivos)

```bash
# Alterar mensagem do último commit
git commit --amend -m "Nova mensagem"

# Adicionar arquivo esquecido ao último commit
git add arquivo-esquecido.py
git commit --amend --no-edit
```

### Push rejeitado (remote ahead)

```bash
# Opção 1: Pull e merge
git pull origin main
git push origin main

# Opção 2: Force push (cuidado!)
git push --force origin main

# Opção 3: Force push mais seguro
git push --force-with-lease origin main
```

### Remover arquivo do histórico (arquivo grande/sensível)

```bash
# Usando filter-branch (legado)
git filter-branch --tree-filter 'rm -f arquivo-grande.zip' HEAD

# Ou usar BFG Repo-Cleaner (recomendado)
# Baixe de: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files arquivo-grande.zip
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## 📚 Recursos Adicionais

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitLab Docs](https://docs.gitlab.com/)
- [Oh My Git! (jogo para aprender Git)](https://ohmygit.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Dica**: Pratique os comandos em um repositório de teste antes de usar em projetos importantes!
