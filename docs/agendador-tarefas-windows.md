# Configurar Afterburner no Agendador de Tarefas do Windows

Este guia ensina como configurar o projeto para executar automaticamente usando o Agendador de Tarefas do Windows (Task Scheduler).

## ⚠️ IMPORTANTE: Limitações do PyAutoGUI

Antes de configurar, entenda as **limitações críticas** da automação GUI:

❌ **NÃO FUNCIONA quando:**
- Tela está bloqueada (Win+L)
- Usuário não está logado
- Sessão RDP está minimizada/desconectada
- Computador em Sleep/Hibernação
- Monitor está desligado

✅ **FUNCIONA quando:**
- Usuário está logado e tela desbloqueada
- Computador totalmente ativo
- Monitor ligado e exibindo a área de trabalho

🔑 **ESSENCIAL para MSI Afterburner:**
- O Afterburner bloqueia automação se não tiver privilégios elevados
- **SEMPRE marque "Executar com privilégios mais altos"** no Agendador
- Sem isso, cliques dentro da janela do Afterburner serão ignorados

## 📋 Pré-requisitos

1. Projeto instalado e funcionando
2. Python e UV configurados
3. Caminho do projeto anotado (ex: `C:\Users\lucas\Documents\Projects\Python\afterburner`)
4. Caminho do UV anotado (geralmente: `C:\Users\[seu-usuario]\.cargo\bin\uv.exe`)

## 🚀 Método 1: Interface Gráfica do Agendador de Tarefas

### Passo 1: Abrir o Agendador de Tarefas

1. Pressione `Win + R`
2. Digite `taskschd.msc`
3. Pressione Enter

Ou pesquise por "Agendador de Tarefas" no menu Iniciar.

### Passo 2: Criar Nova Tarefa

1. No painel direito, clique em **"Criar Tarefa..."** (não "Criar Tarefa Básica")
2. Dê um nome à tarefa: `Afterburner Controller`
3. Adicione uma descrição: `Executa controle automático do MSI Afterburner`

### Passo 3: Configurar Geral

Na aba **Geral**:

- ✅ **Executar somente quando o usuário estiver conectado** (IMPORTANTE: PyAutoGUI precisa de sessão ativa)
- ✅ **Executar com privilégios mais altos** (🔴 OBRIGATÓRIO para MSI Afterburner!)
- ⚙️ **Configurar para**: Windows 10/11

> **⚠️ CRÍTICO**: Se não marcar "privilégios mais altos", o MSI Afterburner bloqueará todos os cliques!

### Passo 4: Configurar Disparadores (Triggers)

Na aba **Disparadores**, clique em **Novo**:

#### Opção A: Executar ao Iniciar o Sistema
```
Iniciar tarefa: Na inicialização
Atrasar tarefa por: 1 minuto
Repetir a tarefa a cada: (opcional)
Habilitado: ✅
```

#### Opção B: Executar em Horário Específico
```
Iniciar tarefa: Em um agendamento
Configurações: Diariamente
Hora de início: 08:00:00
Recorrência: 1 dia
Habilitado: ✅
```

#### Opção C: Executar ao Fazer Login
```
Iniciar tarefa: Ao fazer logon
Usuário específico: Seu usuário
Habilitado: ✅
```

### Passo 5: Configurar Ações

Na aba **Ações**, clique em **Novo**:

#### Opção A: Usando UV (Recomendado)
```
Ação: Iniciar um programa

Programa/script:
C:\Users\lucas\.cargo\bin\uv.exe

Adicionar argumentos:
run afterburner

Iniciar em:
C:\Users\lucas\Documents\Projects\Python\afterburner
```

#### Opção B: Usando Python do venv direto
```
Ação: Iniciar um programa

Programa/script:
C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe

Adicionar argumentos:
-m afterburner.main

Iniciar em:
C:\Users\lucas\Documents\Projects\Python\afterburner
```

**Importante**: Ajuste os caminhos conforme sua instalação!

### Passo 6: Configurar Condições

Na aba **Condições**:

- ⬜ **Desmarque** "Iniciar apenas se o computador estiver inativo" (PyAutoGUI precisa de acesso à tela)
- ⬜ **Desmarque** "Iniciar apenas se estiver na energia" (se for notebook)
- ⬜ **Desmarque** "Parar se alternar para bateria"
- ⬜ **Desmarque** "Ativar o computador para executar esta tarefa" (não acorda de sleep)

> **💡 Dica**: Para PyAutoGUI funcionar, o computador precisa estar totalmente ativo com sessão de usuário.

### Passo 7: Configurar Configurações

Na aba **Configurações**:

- ✅ **Marque** "Permitir que a tarefa seja executada sob demanda" (para testes)
- ✅ **Marque** "Executar tarefa assim que possível após uma hora agendada ter sido perdida"
- ⬜ Se a tarefa falhar, reiniciar a cada: 1 minuto / Tentar reiniciar até: 3 vezes
- ✅ **Marque** "Parar a tarefa se ela for executada por mais de": **5 minutos** (segurança)
- ✅ **Marque** "Se a tarefa em execução não terminar quando solicitado, forçar sua interrupção"

> **⚠️ Atenção**: Defina timeout curto (5-10 min) para evitar processos travados.

### Passo 8: Salvar e Testar

1. Clique em **OK**
2. Digite sua senha do Windows se solicitado
3. Encontre a tarefa na lista
4. Clique com botão direito → **Executar** para testar

## 💻 Método 2: PowerShell (Automático)

Crie um script PowerShell para registrar a tarefa automaticamente:

```powershell
# Salve como: register-task.ps1

# Configurações
$taskName = "Afterburner Controller"
$taskDescription = "Executa controle automático do MSI Afterburner"
$projectPath = "C:\Users\lucas\Documents\Projects\Python\afterburner"

# Opção A: Usando UV (recomendado)
$uvExe = "C:\Users\$env:USERNAME\.cargo\bin\uv.exe"
$arguments = "run afterburner"

# Opção B: Usando Python direto
# $uvExe = "$projectPath\.venv\Scripts\python.exe"
# $arguments = "-m afterburner.main"

# Criar ação
$action = New-ScheduledTaskAction `
    -Execute $uvExe `
    -Argument $arguments `
    -WorkingDirectory $projectPath

# Criar disparador (exemplo: diário às 8h)
$trigger = New-ScheduledTaskTrigger -Daily -At 8am

# Ou disparador ao iniciar o sistema:
# $trigger = New-ScheduledTaskTrigger -AtStartup

# Ou disparador ao fazer login:
# $trigger = New-ScheduledTaskTrigger -AtLogOn

# Configurações principais (COM PRIVILÉGIOS ELEVADOS - OBRIGATÓRIO!)
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

# Configurações adicionais
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Registrar tarefa
Register-ScheduledTask `
    -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Force

Write-Host "✅ Tarefa '$taskName' registrada com sucesso!"
```

### Executar o Script PowerShell

```powershell
# Executar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\register-task.ps1
```

## 📝 Método 3: Comando Direto (schtasks)

### Usando UV (Recomendado):

```powershell
# Criar tarefa que executa diariamente às 8h (COM PRIVILÉGIOS ELEVADOS)
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc daily /st 08:00 /rl highest `
    /f

# Executar na inicialização do sistema
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc onstart /delay 0001:00 /rl highest `
    /f

# Executar ao fazer login
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc onlogon /rl highest `
    /f
```

### Usando Python diretamente:

```powershell
# Criar tarefa que executa diariamente às 8h
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc daily /st 08:00 /rl highest

# Executar na inicialização do sistema
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc onstart /delay 0001:00 /rl highest

# Executar ao fazer login
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc onlogon /rl highest
```

> **⚠️ IMPORTANTE**: O parâmetro `/rl highest` é OBRIGATÓRIO para o MSI Afterburner!

## 🔧 Troubleshooting

### Problema: Mouse não clica dentro do MSI Afterburner

**Causa**: Falta de privilégios elevados

**Solução:**
1. Abra a tarefa no Agendador
2. Aba **Geral** → ✅ Marque **"Executar com privilégios mais altos"**
3. **Segurança** → Configure para RunLevel = Highest
4. Salve e teste novamente

**Teste manual:**
```powershell
# PowerShell como Administrador
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner
```

### Problema: Tarefa executa mas nada acontece na tela

**Causas possíveis:**
- ❌ Tela está bloqueada (Win+L)
- ❌ Sessão RDP desconectada
- ❌ Usuário não está logado
- ❌ Monitor desligado

**Solução:**
- PyAutoGUI **REQUER** sessão ativa e desbloqueada
- Configure a tarefa para **"Executar somente quando usuário estiver conectado"**
- Mantenha o computador desbloqueado durante a execução

### Problema: Tarefa não executa

**Verificar:**
1. Caminhos estão corretos (uv.exe ou python.exe e projeto)
2. "Executar com privilégios mais altos" MARCADO
3. "Executar somente quando usuário estiver conectado" MARCADO
4. Permissões do usuário
5. Logs do Agendador: Biblioteca do Agendador → Histórico

**Visualizar histórico:**
```powershell
Get-ScheduledTask -TaskName "Afterburner Controller" | Get-ScheduledTaskInfo
```

### Problema: Tarefa executa mas falha

**Verificar logs do projeto:**
```powershell
Get-Content C:\Users\lucas\Documents\Projects\Python\afterburner\log\afterburner.log -Tail 50
```

**Testar execução manual:**
```powershell
cd C:\Users\lucas\Documents\Projects\Python\afterburner
.\.venv\Scripts\python.exe -m afterburner.main
```

### Problema: "O sistema não pode encontrar o arquivo especificado"

Certifique-se de usar caminhos absolutos completos, não relativos.

**Correto:**
```
C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe
```

**Incorreto:**
```
.venv\Scripts\python.exe
python.exe
```

## 🎯 Exemplos de Agendamentos Comuns

### Executar uma vez por dia
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
```

### Executar várias vezes ao dia
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 8am
$trigger.Repetition = (New-ScheduledTaskTrigger -Once -At 8am -RepetitionInterval (New-TimeSpan -Hours 4)).Repetition
# Executa às 8h, 12h, 16h, 20h
```

### Executar de hora em hora
```powershell
$trigger = New-ScheduledTaskTrigger -Once -At 12am -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Hours 23)
```

### Executar só em dias úteis
```powershell
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 8am
```

### Executar ao iniciar + repetir a cada 30 minutos
```powershell
$trigger = New-ScheduledTaskTrigger -AtStartup -RepetitionInterval (New-TimeSpan -Minutes 30)
```

## 📊 Gerenciar Tarefas Existentes

### Listar todas as tarefas
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Afterburner*"}
```

### Ver status da tarefa
```powershell
Get-ScheduledTask -TaskName "Afterburner Controller"
```

### Executar tarefa manualmente
```powershell
Start-ScheduledTask -TaskName "Afterburner Controller"
```

### Desabilitar tarefa
```powershell
Disable-ScheduledTask -TaskName "Afterburner Controller"
```

### Habilitar tarefa
```powershell
Enable-ScheduledTask -TaskName "Afterburner Controller"
```

### Remover tarefa
```powershell
Unregister-ScheduledTask -TaskName "Afterburner Controller" -Confirm:$false
```

### Ver histórico de execuções
```powershell
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" |
    Where-Object {$_.Message -like "*Afterburner Controller*"} |
    Select-Object TimeCreated, Message -First 10
```

## 🛠️ Script Auxiliar: Criar Wrapper Batch

Crie um arquivo `.bat` para facilitar a execução:

### Usando UV (Recomendado):

```batch
@echo off
REM Salve como: run-afterburner.bat

cd /d "C:\Users\lucas\Documents\Projects\Python\afterburner"

REM Usando UV
"C:\Users\lucas\.cargo\bin\uv.exe" run afterburner

REM Redirecionar output para arquivo (opcional)
REM "C:\Users\lucas\.cargo\bin\uv.exe" run afterburner >> "log\execution.log" 2>&1

exit /b %ERRORLEVEL%
```

### Usando Python direto:

```batch
@echo off
REM Salve como: run-afterburner.bat

cd /d "C:\Users\lucas\Documents\Projects\Python\afterburner"
".venv\Scripts\python.exe" -m afterburner.main

REM Redirecionar output para arquivo (opcional)
REM ".venv\Scripts\python.exe" -m afterburner.main >> "log\execution.log" 2>&1

exit /b %ERRORLEVEL%
```

Depois use o `.bat` no Agendador:
```
Programa/script: C:\Users\lucas\Documents\Projects\Python\afterburner\run-afterburner.bat
✅ Executar com privilégios mais altos (OBRIGATÓRIO!)
```

## 🔒 Executar com Privilégios Elevados (ESSENCIAL)

### Por que é necessário?

O MSI Afterburner **bloqueia automação** sem privilégios administrativos porque:
- Controla hardware (GPU, voltagem, clocks)
- Tem proteções anti-tamper
- Roda em modo kernel-level

### Configuração no Agendador (Interface Gráfica):

1. Abra a tarefa criada
2. Aba **Geral** → ✅ **"Executar com privilégios mais altos"**
3. Clique OK e digite sua senha de administrador

### Configuração via PowerShell:

```powershell
# Com privilégios elevados (Highest)
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName "Afterburner Controller" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Force
```

### Configuração via schtasks:

```powershell
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\.cargo\bin\uv.exe run afterburner" `
    /sc daily /st 08:00 `
    /rl highest `
    /ru "%USERNAME%" /f
```

> **⚠️ CRÍTICO**: Sem `/rl highest`, os cliques dentro do Afterburner serão ignorados!

## 🌐 Variáveis de Ambiente

Se seu projeto depende de variáveis de ambiente personalizadas:

### Usando UV:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-Command `"& { `$env:AFTERBURNER_ENV='production'; cd 'C:\Users\lucas\Documents\Projects\Python\afterburner'; & 'C:\Users\lucas\.cargo\bin\uv.exe' run afterburner }`"" `
    -WorkingDirectory "C:\Users\lucas\Documents\Projects\Python\afterburner"
```

### Usando Python direto:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-Command `"& { `$env:AFTERBURNER_ENV='production'; cd 'C:\path\to\project'; .\.venv\Scripts\python.exe -m afterburner.main }`""
```

**Nota**: O projeto usa Dynaconf, então você pode trocar ambientes via variável `AFTERBURNER_ENV`:
- `AFTERBURNER_ENV=default` (padrão)
- `AFTERBURNER_ENV=development`
- `AFTERBURNER_ENV=production`

## ✅ Checklist Final

- [ ] Caminhos absolutos verificados (UV ou Python)
- [ ] **"Executar com privilégios mais altos" MARCADO** 🔴 CRÍTICO
- [ ] **"Executar somente quando usuário estiver conectado" MARCADO**
- [ ] Condições ajustadas (sem bloqueios de inatividade/bateria)
- [ ] Disparador configurado corretamente
- [ ] Tarefa testada manualmente (com PowerShell como Admin)
- [ ] Logs sendo gerados corretamente
- [ ] Histórico habilitado no Agendador
- [ ] Computador ficará desbloqueado durante execução
- [ ] Timeout definido (5-10 minutos recomendado)

## 🎯 Resumo de Configuração Ideal

```
✅ Geral:
   - Executar somente quando usuário estiver conectado
   - ✅ Executar com privilégios mais altos (OBRIGATÓRIO!)
   - Configurar para: Windows 10/11

✅ Ações:
   - Programa: C:\Users\[usuario]\.cargo\bin\uv.exe
   - Argumentos: run afterburner
   - Iniciar em: C:\Users\[usuario]\...\afterburner

✅ Condições:
   - ❌ DESMARCADO: Todas as opções de inatividade/bateria

✅ Configurações:
   - ✅ Permitir execução sob demanda
   - ✅ Timeout de 5-10 minutos
```

## 📚 Recursos Adicionais

- [Documentação do Task Scheduler](https://docs.microsoft.com/pt-br/windows/win32/taskschd/task-scheduler-start-page)
- [ScheduledTask PowerShell Module](https://docs.microsoft.com/pt-br/powershell/module/scheduledtasks/)
- [Schtasks Command Reference](https://docs.microsoft.com/pt-br/windows-server/administration/windows-commands/schtasks)

---

## 🔴 AVISOS CRÍTICOS

### MSI Afterburner bloqueia automação sem privilégios

O MSI Afterburner executa com proteções que **bloqueiam cliques de automação** se o script não tiver privilégios elevados. Isso acontece porque:

1. O Afterburner controla hardware (GPU/overclock)
2. Tem proteções de segurança contra manipulação não autorizada
3. Funciona em modo kernel-level em alguns casos

**Sintoma**: O script executa, mas mouse não clica dentro da janela do Afterburner.

**Solução**: `RunLevel = Highest` (Executar com privilégios mais altos)

### PyAutoGUI precisa de sessão ativa

Diferente de scripts CLI/API que podem rodar em background, PyAutoGUI:
- Precisa **capturar a tela** para localizar elementos
- Precisa **mover o mouse** e **simular cliques**
- Não funciona em sessões desconectadas ou bloqueadas

**💡 Dica para uso 24/7**: Se precisar executar sem estar logado, considere:
- Usar API do Afterburner (MSI Afterburner SDK)
- AutoHotkey com backend Windows nativo
- VNC/RDP mantendo sessão ativa (não recomendado)

---

**Dica**: Sempre teste a tarefa manualmente **como Administrador** antes de deixar agendada para garantir que tudo funciona corretamente!

**Teste rápido:**
```powershell
# PowerShell como ADMINISTRADOR
cd C:\Users\lucas\Documents\Projects\Python\afterburner
uv run afterburner
```

Se funcionar no terminal como admin mas não no Agendador, revise as configurações acima.
