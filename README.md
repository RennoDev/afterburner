# Afterburner Controller

Projeto de automação para controlar o MSI Afterburner através de interface gráfica, utilizando boas práticas de arquitetura e ferramentas modernas do ecossistema Python.

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
│   └── agendador-tarefas-windows.md
├── log/                       # Arquivos de log
│   └── afterburner.log
├── src/
│   └── afterburner/           # Pacote principal
│       ├── __init__.py
│       ├── config.py          # Configuração do Dynaconf
│       ├── logger.py          # Sistema de logging
│       ├── main.py            # Entry point
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
```

3. **Configure o settings.toml**

Edite `config/settings.toml` e ajuste o caminho do executável:
```toml
[default.afterburner]
executable_path = "C:\\Program Files (x86)\\MSI Afterburner\\MSIAfterburner.exe"
```

4. **Execute o projeto**
```powershell
uv run afterburner
```

Ou ative o ambiente virtual manualmente:
```powershell
.venv\Scripts\Activate.ps1
python -m afterburner.main
```

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

```powershell
# Via UV
uv run afterburner

# Via ambiente virtual
.venv\Scripts\python.exe -m afterburner.main
```

### Agendamento Automático

O projeto pode ser agendado no Windows Task Scheduler para execução automática.

Consulte a [documentação completa](docs/agendador-tarefas-windows.md) para instruções detalhadas.

**Exemplo rápido:**
```powershell
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\path\to\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc daily /st 08:00
```

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

#### tasks/
Módulos independentes para cada etapa do processo:
- `openAB.py`: Responsável por abrir o MSI Afterburner
- `activateAB.py`: Executa ações/cliques na interface
- `closeAB.py`: Fecha o aplicativo de forma segura

### Adicionando Novas Tasks

1. Crie um novo arquivo em `src/afterburner/tasks/`
2. Importe a configuração e logger:
```python
from afterburner.config import settings
from afterburner.logger import get_logger

logger = get_logger(__name__)

def minha_task():
    logger.info("Executando minha task")
    # Sua lógica aqui
```

3. Importe e execute no `main.py`

### Testando Coordenadas

Use o script auxiliar para descobrir coordenadas de botões:

```python
import pyautogui
import time

print("Mova o mouse para o botão em 5 segundos...")
time.sleep(5)
print(f"Coordenadas: {pyautogui.position()}")
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

- **Fail-Safe ativado por padrão**: Mova o mouse para o canto superior esquerdo da tela para abortar a execução
- Configurável via `settings.toml`:
```toml
[default.actions]
use_failsafe = true
```

## 📚 Documentação Adicional

- [Guia Básico do PyAutoGUI](docs/pyautogui-guia-basico.md) - Comandos essenciais para automação
- [Agendador de Tarefas do Windows](docs/agendador-tarefas-windows.md) - Como automatizar a execução

## 🔧 Troubleshooting

### Problema: "Executable não encontrado"
- Verifique o caminho em `config/settings.toml`
- Use caminho absoluto completo
- Certifique-se que o MSI Afterburner está instalado

### Problema: "Cliques não funcionam"
- Coordenadas podem estar incorretas para sua resolução
- Execute o script de descoberta de coordenadas
- Verifique se a janela do Afterburner está visível e em foco

### Problema: "Import error"
- Certifique-se que o ambiente virtual está ativado
- Execute `uv sync` para reinstalar dependências
- Verifique se está executando do diretório raiz do projeto

## 🎯 Princípios de Design

Este projeto foi estruturado seguindo princípios de engenharia de software:

1. **Configuração Externa**: Nenhum valor hardcoded, tudo em `settings.toml`
2. **Logging Apropriado**: Rastreabilidade de execução e erros
3. **Modularização**: Cada task é independente e reutilizável
4. **Gerenciamento Moderno**: UV para velocidade e confiabilidade
5. **Documentação**: Código auto-explicativo + docs complementares

## 🤝 Contribuindo

Este é um projeto de uso pessoal, mas serve como template para projetos similares. Sinta-se livre para adaptar a arquitetura para suas necessidades.

## 📄 Licença

Este projeto é de uso pessoal.

---

**Autor**: Lucas  
**Versão**: 0.1.0  
**Python**: 3.14+