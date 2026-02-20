# Afterburner Controller

Projeto de automação para controlar o MSI Afterburner através de interface gráfica, utilizando boas práticas de arquitetura e ferramentas modernas do ecossistema Python.

## ⚠️ IMPORTANTE - Requisitos de Execução

### 🔴 CRÍTICO: O MSI Afterburner bloqueia automação sem privilégios elevados

O MSI Afterburner possui proteções de segurança que **bloqueiam cliques automatizados** se o script não for executado como administrador. Isso acontece porque:

- O Afterburner controla hardware (GPU, voltagem, clocks)
- Possui proteções anti-tamper em nível kernel
- Requer privilégios elevados para aceitar automação

**✅ SOLUÇÃO: Execute SEMPRE como Administrador**
```powershell
# PowerShell como Administrador (clique direito → "Executar como Administrador")
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner
```

**Sintoma sem admin**: O script roda, mas o mouse não clica dentro da janela do Afterburner.

### 📺 Limitações do PyAutoGUI

❌ **NÃO funciona quando:**
- Tela está bloqueada (Win+L)
- Usuário não está logado
- Sessão RDP está minimizada/desconectada
- Computador em Sleep/Hibernação
- Monitor desligado

✅ **FUNCIONA quando:**
- Usuário está logado com tela desbloqueada
- Computador totalmente ativo
- Monitor ligado e exibindo área de trabalho
- **Script executado como Administrador** (para MSI Afterburner)

## 📋 Sobre o Projeto

Este projeto foi desenvolvido para automatizar a interação com o MSI Afterburner, permitindo abrir o aplicativo, realizar configurações através de cliques automatizados e fechá-lo de forma programática. Apesar da simplicidade do objetivo, o projeto serve como template de arquitetura robusta e escalável.

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular e organizada, priorizando:

- **Separação de Responsabilidades**: Cada módulo tem uma função específica e bem definida
- **Configuração Centralizada**: Uso do Dynaconf para gerenciamento de configurações
- **Logging Estruturado**: Sistema de logs com rotação automática
- **Gestão de Dependências Moderna**: Uso do UV como gerenciador de pacotes

### Estrutura de Diretórios

```
afterburner/
├── config/                    # Configurações do projeto
│   ├── settings.toml         # Configurações principais
│   └── .secrets.toml         # Credenciais (não versionado)
├── docs/                      # Documentação
│   ├── pyautogui-guia-basico.md
│   ├── agendador-tarefas-windows.md
│   └── git-comandos-basicos.md
├── elements/                  # Elementos UI capturados (screenshots)
│   └── README.md             # Instruções de uso
├── log/                       # Arquivos de log
│   └── afterburner.log
├── src/
│   └── afterburner/           # Pacote principal
│       ├── __init__.py
│       ├── config.py          # Configuração do Dynaconf
│       ├── logger.py          # Sistema de logging
│       ├── main.py            # Entry point
│       ├── utils/             # Utilitários
│       │   └── elements.py    # Detecção e interação com elementos UI
│       └── tasks/             # Módulos de tarefas
│           ├── openAB.py      # Abre o Afterburner
│           ├── activateAB.py  # Realiza ações no Afterburner
│           └── closeAB.py     # Fecha o Afterburner
├── pyproject.toml             # Configuração do projeto e dependências
├── uv.lock                    # Lock file do UV
└── README.md
```

## 🛠️ Stack Tecnológica

### Core
- **Python 3.14+**: Linguagem base do projeto
- **UV**: Gerenciador de pacotes e ambiente virtual ultra-rápido

### Bibliotecas Principais
- **Dynaconf**: Gerenciamento de configurações com suporte a múltiplos ambientes
- **PyAutoGUI**: Automação de interface gráfica (mouse e teclado)
- **Pillow**: Backend para screenshots e manipulação de imagens (requerido pelo PyAutoGUI)
- **OpenCV-Python**: Melhora a detecção de elementos com confidence e acelera busca por imagens

### Padrões e Práticas
- **TOML**: Formato de configuração legível e estruturado
- **Logging com Rotação**: Logs organizados com controle de tamanho
- **Ambientes Múltiplos**: Configurações específicas para development/production

## 📦 Instalação

### Pré-requisitos

- Python 3.14 ou superior
- MSI Afterburner instalado
- UV instalado ([instruções](https://github.com/astral-sh/uv))

### Setup

1. **Clone o repositório**
```powershell
git clone <url-do-repositorio>
cd afterburner
```

2. **Instale as dependências com UV**
```powershell
uv sync

# Dependências automáticas incluem:
# - dynaconf (configurações)
# - pyautogui (automação GUI)
# - opencv-python (detecção de imagens melhorada)
# - pillow (backend para screenshots do PyAutoGUI)
```

3. **Configure o settings.toml**

Edite `config/settings.toml` e ajuste o caminho do executável:
```toml
[default.afterburner]
executable_path = "C:\\Program Files (x86)\\MSI Afterburner\\MSIAfterburner.exe"
```

4. **Capture elementos UI necessários**

Capture screenshots dos elementos que o script precisa clicar e salve em `elements/`:
- `segundoPlano.png` - Ícone de busca do Windows
- `afterburnerIcon.png` - Ícone do Afterburner na busca
- `afterburner.png` - Janela do Afterburner
- `profile.png` - Botão de perfil
- `apply.png` - Botão aplicar
- `minimizar.png` - Botão minimizar

Consulte [elements/README.md](elements/README.md) para instruções de captura.

5. **Execute o projeto COMO ADMINISTRADOR**

```powershell
# PowerShell como Administrador (obrigatório para MSI Afterburner!)
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner
```

Ou ative o ambiente virtual manualmente:
```powershell
# PowerShell como Administrador
.venv\Scripts\Activate.ps1
python -m afterburner.main
```

> **⚠️ CRÍTICO**: Sem privilégios de administrador, o MSI Afterburner bloqueará todos os cliques!

## ⚙️ Configuração

### Arquivo settings.toml

O arquivo `config/settings.toml` centraliza todas as configurações:

```toml
[default]
app_name = "Afterburner Controller"
debug = false

[default.afterburner]
executable_path = "..."      # Caminho do MSI Afterburner
startup_timeout = 5          # Tempo de espera para inicialização
action_delay = 0.5           # Delay entre ações
max_retries = 3              # Tentativas de retry

[default.logging]
enabled = true
log_level = "INFO"          # DEBUG, INFO, WARNING, ERROR
log_file = "afterburner.log"
max_bytes = 10485760        # 10MB
backup_count = 5            # Manter 5 backups

[default.actions]
global_wait = 1.0            # Espera padrão entre ações (segundos)
human_simulation = true      # Movimentos mais naturais
mouse_duration = 0.3         # Duração do movimento do mouse
confidence = 0.8             # Precisão detecção de elementos (0.7-0.9)
grayscale = true             # Busca em escala de cinza (mais rápido)

[development]
debug = true

[development.logging]
log_level = "DEBUG"
```

### Múltiplos Ambientes

Alterne entre ambientes usando variável de ambiente:

```powershell
# Development (verbose logging)
$env:AFTERBURNER_ENV = "development"
uv run afterburner

# Production (minimal logging)
$env:AFTERBURNER_ENV = "production"
uv run afterburner
```

### Secrets

Para dados sensíveis, crie `config/.secrets.toml` (não versionado):

```toml
[default]
api_key = "sua-chave-secreta"
```

## 🚀 Uso

### Execução Manual

**⚠️ SEMPRE execute como Administrador para o MSI Afterburner aceitar automação:**

```powershell
# Abra PowerShell como Administrador (clique direito → "Executar como Administrador")

# Via UV (recomendado)
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner

# Via ambiente virtual
.venv\Scripts\python.exe -m afterburner.main
```

**Teste rápido de privilégios:**
```powershell
# Se esse comando funcionar corretamente, seus privilégios estão OK
[Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent() | 
    Select-Object -ExpandProperty IsInRole[Security.Principal.WindowsBuiltInRole]::Administrator
# Retorno: True = Admin | False = Sem privilégios
```

### Agendamento Automático

O projeto pode ser agendado no Windows Task Scheduler para execução automática.

**🔴 OBRIGATÓRIO**: Configure a tarefa com **"Executar com privilégios mais altos"** ou os cliques serão bloqueados!

Consulte a [documentação completa](docs/agendador-tarefas-windows.md) para instruções detalhadas.

**Exemplo rápido (COM PRIVILÉGIOS ELEVADOS):**
```powershell
# Usando UV (recomendado)
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc daily /st 08:00 `
    /rl highest /f

# Usando Python direto
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\path\to\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc daily /st 08:00 `
    /rl highest /f
```

> **Nota**: O parâmetro `/rl highest` garante privilégios elevados. Sem ele, o MSI Afterburner bloqueará a automação.

**⚠️ Limitação importante**: O Task Scheduler só funciona quando o usuário está logado com tela desbloqueada (requisito do PyAutoGUI).

## 📝 Desenvolvimento

### Estrutura dos Módulos

#### config.py
Configuração do Dynaconf com caminhos absolutos e suporte a ambientes:
```python
from afterburner.config import settings

print(settings.afterburner.executable_path)
print(settings.logging.log_level)
```

#### logger.py
Sistema de logging centralizado:
```python
from afterburner.logger import get_logger

logger = get_logger(__name__)
logger.info("Mensagem de log")
```

#### utils/elements.py
Utilitários para detecção e interação com elementos UI:
```python
from afterburner.utils.elements import click_element, wait_and_click

# Clicar em um elemento
click_element('apply_button.png')

# Aguardar e clicar
wait_and_click('settings_icon.png', timeout=5)
```

**Organização hierárquica:**
- `wait_and_click()` - Alto nível: aguarda e clica
- `click_element()` - Alto nível: localiza e clica
- `wait_element()` - Médio nível: aguarda elemento aparecer
- `find_element()` - Médio nível: localiza centro do elemento
- `_get_element_path()` - Interno: constrói caminho do elemento
- `setup()` - Inicialização: configura PyAutoGUI

#### tasks/
Módulos independentes para cada etapa do processo:
- `openAB.py`: Responsável por abrir o MSI Afterburner
- `activateAB.py`: Executa ações/cliques na interface
- `closeAB.py`: Fecha o aplicativo de forma segura

### Adicionando Novas Tasks

1. Crie um novo arquivo em `src/afterburner/tasks/`
2. Importe a configuração, logger e utilitários:
```python
from afterburner.config import settings
from afterburner.logger import get_logger
from afterburner.utils.elements import click_element, wait_and_click

logger = get_logger(__name__)

def minha_task():
    logger.info("Executando minha task")
    
    # Interagir com elementos UI
    if wait_and_click('botao.png', timeout=5):
        logger.info("Botão clicado com sucesso")
    else:
        logger.error("Elemento não encontrado")
        return False
    
    return True
```

3. Importe e execute no `main.py`

### Capturando Elementos UI

O projeto usa detecção de imagens para localizar elementos na tela:

1. **Capture o elemento** (botão, ícone, etc):
```python
import pyautogui

# Capturar região específica
pyautogui.screenshot('elements/apply_button.png', region=(x, y, width, height))
```

2. **Use nas tasks**:
```python
from afterburner.utils.images import click_element

click_element('apply_button.png')
```

**Dicas:**
- Capture apenas o elemento necessário (botão, ícone)
- Use nomes descritivos: `apply_button.png`, `settings_icon.png`
- Formato PNG recomendado
- Os elementos ficam em `elements/`
- Evite capturar elementos com texto que pode mudar
- Prefira ícones e botões que permanecem visualmente consistentes

**Ferramenta de captura recomendada:**
```python
import pyautogui
import time

# Dá 5 segundos para posicionar o mouse
time.sleep(5)
x, y = pyautogui.position()
print(f"Posição: {x}, {y}")

# Capturar região 100x50 a partir da posição
pyautogui.screenshot('elements/meu_elemento.png', region=(x, y, 100, 50))
```

Consulte [o guia do PyAutoGUI](docs/pyautogui-guia-basico.md) para mais detalhes.

## 🔍 Logging e Debugging

### Visualizar Logs

```powershell
# Logs em tempo real
Get-Content log\afterburner.log -Wait -Tail 20

# Últimas 50 linhas
Get-Content log\afterburner.log -Tail 50
```

### Debug Mode

Ative o modo debug para logging detalhado:

```powershell
$env:AFTERBURNER_ENV = "development"
uv run afterburner
```

Ou temporariamente em `settings.toml`:
```toml
[default]
debug = true

[default.logging]
log_level = "DEBUG"
```

## 🛡️ Fail-Safe

O PyAutoGUI possui um mecanismo de segurança embutido:

- **Fail-Safe ativado por padrão**: Mova o mouse para o **canto superior esquerdo** da tela para abortar a execução imediatamente
- Configurado em `src/afterburner/utils/elements.py` na função `setup()`
- Lança exceção `pyautogui.FailSafeException` quando ativado
- **Recomendação**: Sempre mantenha ativado para poder abortar em emergências

```python
# Em utils/elements.py
pyautogui.FAILSAFE = True  # Padrão do projeto
```

**Como usar:**
1. Script começa a executar
2. Se algo der errado, **mova o mouse rapidamente para o canto superior esquerdo**
3. Script para imediatamente com exceção

## 📚 Documentação Adicional

- [Guia Básico do PyAutoGUI](docs/pyautogui-guia-basico.md) - Comandos essenciais para automação
- [Agendador de Tarefas do Windows](docs/agendador-tarefas-windows.md) - Como automatizar a execução
- [Comandos Git](docs/git-comandos-basicos.md) - Comandos Git para GitHub/GitLab
- [Elementos UI](elements/README.md) - Como capturar e usar elementos

## 🔧 Troubleshooting

### 🔴 Problema CRÍTICO: "Mouse não clica dentro do MSI Afterburner"

**Sintoma:** O script executa, move o mouse, mas não clica nos botões do Afterburner.

**Causa:** Falta de privilégios elevados. O MSI Afterburner bloqueia automação de processos sem privilégios administrativos.

**Solução:**
```powershell
# Abra PowerShell como Administrador (clique direito → "Executar como Administrador")
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner
```

**Para Task Scheduler:**
1. Abra a tarefa no Agendador
2. Aba **Geral** → ✅ Marque **"Executar com privilégios mais altos"**
3. Salve e teste novamente

### Problema: "Script executa mas nada acontece na tela"

**Causas possíveis:**
- ❌ Tela bloqueada (Win+L) - PyAutoGUI **NÃO** funciona com tela bloqueada
- ❌ Sessão RDP minimizada/desconectada
- ❌ Usuário não está logado
- ❌ Monitor desligado

**Solução:** PyAutoGUI requer sessão ativa, desbloqueada, com monitor ligado. Não há workaround.

### Problema: "Janela UAC aparece e script para"

**Causa:** O Windows mostra janela de Controle de Conta de Usuário que bloqueia automação por segurança.

**Solução:**
1. Use o executável direto em vez da busca do Windows
2. Configure o MSI Afterburner para não pedir confirmação UAC:
   - Clique direito no atalho → Propriedades → Compatibilidade
   - Desmarque "Executar como administrador"
3. Execute o script como administrador (recomendado)

### Problema: "Executable não encontrado"
- Verifique o caminho em `config/settings.toml`
- Use caminho absoluto completo
- Certifique-se que o MSI Afterburner está instalado
- Caminhos válidos:
  - `C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe`
  - `C:\Users\[usuario]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\MSI Afterburner\MSI Afterburner.lnk`

### Problema: "Elemento não encontrado"
- Recapture o elemento na resolução atual
- Ajuste `confidence` no `settings.toml` (reduzir para ~0.7)
- Verifique se o elemento está visível na tela
- Certifique-se que a janela do Afterburner está em foco
- Teste com diferentes valores de `grayscale` (true/false)
- Verifique se capturou apenas o elemento (sem muito background)

### Problema: "Detecção muito lenta"
- Instale opencv-python: `uv add opencv-python`
- Mantenha `grayscale = true` no settings.toml
- Capture elementos menores (apenas o necessário)
- Aumente timeout se necessário

### Problema: "Import error"
- Certifique-se que o ambiente virtual está ativado
- Execute `uv sync` para reinstalar dependências
- Verifique se está executando do diretório raiz do projeto
- Confirme que Python 3.14+ está instalado

## 🎯 Princípios de Design

Este projeto foi estruturado seguindo princípios de engenharia de software:

1. **Configuração Externa**: Nenhum valor hardcoded, tudo em `settings.toml`
2. **Logging Apropriado**: Rastreabilidade de execução e erros
3. **Modularização**: Cada task é independente e reutilizável
4. **Gerenciamento Moderno**: UV para velocidade e confiabilidade
5. **Documentação**: Código auto-explicativo + docs complementares
6. **Organização Hierárquica**: Funções organizadas por nível de abstração (alto → médio → interno)

## 💡 Lições Aprendidas

### Automação GUI em Windows

1. **Privilégios são cruciais**: Aplicações que controlam hardware (como MSI Afterburner) bloqueiam automação sem privilégios elevados
2. **UAC é intransponível**: Janelas UAC do Windows não aceitam automação por design de segurança
3. **PyAutoGUI tem limitações**: Requer sessão ativa, tela desbloqueada, monitor ligado - não funciona em background
4. **Detecção por imagem vs coordenadas**: Coordenadas falham em aplicações protegidas; detecção por imagem é mais confiável
5. **Fail-Safe é essencial**: Sempre mantenha um mecanismo de emergência (mouse no canto da tela)

### Boas Práticas Descobertas

- Use `subprocess.Popen` com `shell=True` para abrir executáveis
- Prefira detectar elementos por imagem (mais robusto que coordenadas fixas)
- Configure timeouts generosos para permitir intervenção manual (ex: clicar no UAC)
- Logs detalhados são vitais para debugging de automação GUI
- Teste como Admin antes de configurar no Task Scheduler

### Alternativas ao PyAutoGUI

Para casos onde PyAutoGUI é limitado:
- **pywinauto**: Interação nativa com janelas Windows (mais robusto)
- **win32api**: Cliques de baixo nível usando Windows API
- **AutoHotkey**: Script nativo Windows com menos restrições
- **MSI Afterburner SDK**: API oficial (se disponível)

## 🔐 Considerações de Segurança

- ⚠️ Executar como Administrador concede privilégios elevados
- ⚠️ Scripts automatizados podem ser explorados se modificados
- ✅ Mantenha o código fonte seguro e versionado
- ✅ Use `.secrets.toml` para dados sensíveis (não commitado)
- ✅ Revise mudanças antes de executar com privilégios elevados

## 🤝 Contribuindo

Este é um projeto de uso pessoal, mas serve como template para projetos similares. Sinta-se livre para adaptar a arquitetura para suas necessidades.

## 📝 Resumo de Comandos Essenciais

```powershell
# Setup inicial
git clone <url-do-repositorio>
cd afterburner
uv sync

# Executar (SEMPRE COMO ADMIN!)
# PowerShell → Clique direito → "Executar como Administrador"
uv run afterburner

# Verificar logs
Get-Content log\afterburner.log -Tail 50

# Testar detecção de elementos
uv run python -c "import pyautogui; print(pyautogui.locateCenterOnScreen('elements/apply.png'))"

# Agendador de Tarefas (COM PRIVILÉGIOS ELEVADOS)
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc daily /st 08:00 /rl highest /f

# Verificar se está rodando como Admin
[Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent() | 
    Select-Object -ExpandProperty IsInRole[Security.Principal.WindowsBuiltInRole]::Administrator
```

## 🚨 Checklist Antes de Executar

- [ ] PowerShell aberto **como Administrador**
- [ ] Usuário logado com **tela desbloqueada**
- [ ] MSI Afterburner instalado
- [ ] Elementos UI capturados em `elements/`
- [ ] `config/settings.toml` configurado com caminho do executável
- [ ] Dependências instaladas (`uv sync`)
- [ ] Monitor ligado e visível

## 📄 Licença

Este projeto é de uso pessoal.

---

**Autor**: Lucas  
**Versão**: 0.1.0  
**Python**: 3.14+