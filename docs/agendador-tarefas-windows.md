# Configurar Afterburner no Agendador de Tarefas do Windows

Este guia ensina como configurar o projeto para executar automaticamente usando o Agendador de Tarefas do Windows (Task Scheduler).

## 📋 Pré-requisitos

1. Projeto instalado e funcionando
2. Python e UV configurados
3. Caminho do projeto anotado (ex: `C:\Users\lucas\Documents\Projects\Python\afterburner`)

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

- ✅ **Executar estando o usuário conectado ou não**
- ✅ **Executar com privilégios mais altos** (se necessário)
- ⚙️ **Configurar para**: Windows 10/11

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

```
Ação: Iniciar um programa

Programa/script:
C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe

Adicionar argumentos:
-m afterburner.main

Iniciar em (opcional):
C:\Users\lucas\Documents\Projects\Python\afterburner
```

**Importante**: Ajuste os caminhos conforme sua instalação!

### Passo 6: Configurar Condições

Na aba **Condições**:

- ⬜ Iniciar a tarefa apenas se o computador estiver inativo por...
- ✅ Iniciar a tarefa apenas se o computador estiver conectado à energia (se relevante)
- ⬜ Parar se o computador alternar para bateria

### Passo 7: Configurar Configurações

Na aba **Configurações**:

- ⬜ Permitir que a tarefa seja executada sob demanda
- ✅ Executar tarefa assim que possível após uma hora agendada ter sido perdida
- ⬜ Se a tarefa falhar, reiniciar a cada: 1 minuto / Tentar reiniciar até: 3 vezes
- ⬜ Parar a tarefa se ela for executada por mais de: 1 hora
- ✅ Se a tarefa em execução não terminar quando solicitado, forçar sua interrupção

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
$pythonExe = "$projectPath\.venv\Scripts\python.exe"
$arguments = "-m afterburner.main"

# Criar ação
$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument $arguments `
    -WorkingDirectory $projectPath

# Criar disparador (exemplo: diário às 8h)
$trigger = New-ScheduledTaskTrigger -Daily -At 8am

# Ou disparador ao iniciar o sistema:
# $trigger = New-ScheduledTaskTrigger -AtStartup

# Ou disparador ao fazer login:
# $trigger = New-ScheduledTaskTrigger -AtLogOn

# Configurações principais
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType S4U `
    -RunLevel Limited

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

```powershell
# Criar tarefa que executa diariamente às 8h
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc daily /st 08:00 /rl limited

# Executar na inicialização do sistema
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc onstart /delay 0001:00 /rl limited

# Executar ao fazer login
schtasks /create /tn "Afterburner Controller" `
    /tr "C:\Users\lucas\Documents\Projects\Python\afterburner\.venv\Scripts\python.exe -m afterburner.main" `
    /sc onlogon /rl limited
```

## 🔧 Troubleshooting

### Problema: Tarefa não executa

**Verificar:**
1. Caminhos estão corretos (python.exe e projeto)
2. Ambiente virtual ativado corretamente
3. Permissões do usuário
4. Logs do Agendador: Biblioteca do Agendador → Histórico

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
```

## 🔒 Executar com Privilégios Elevados

Se precisa executar como Administrador:

1. No Agendador, marque **"Executar com privilégios mais altos"**
2. Ou via PowerShell:
```powershell
Register-ScheduledTask `
    -TaskName "Afterburner Controller" `
    -Action $action `
    -Trigger $trigger `
    -Principal (New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest) `
    -Settings $settings
```

## 📧 Enviar Email em Caso de Falha (Opcional)

Configure ação adicional para enviar email se tarefa falhar:

1. Aba **Ações** → **Novo**
2. Ação: **Enviar um email**
3. Configure servidor SMTP e destinatários

**Nota**: Este recurso foi descontinuado no Windows 10/11. Use script PowerShell customizado.

## 🌐 Variáveis de Ambiente

Se seu projeto depende de variáveis de ambiente:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-Command `"& { `$env:AFTERBURNER_ENV='production'; cd 'C:\path\to\project'; .\.venv\Scripts\python.exe -m afterburner.main }`""
```

## ✅ Checklist Final

- [ ] Caminhos absolutos verificados
- [ ] Ambiente virtual correto
- [ ] Permissões adequadas
- [ ] Disparador configurado
- [ ] Tarefa testada manualmente
- [ ] Logs sendo gerados corretamente
- [ ] Histórico habilitado no Agendador

## 📚 Recursos Adicionais

- [Documentação do Task Scheduler](https://docs.microsoft.com/pt-br/windows/win32/taskschd/task-scheduler-start-page)
- [ScheduledTask PowerShell Module](https://docs.microsoft.com/pt-br/powershell/module/scheduledtasks/)
- [Schtasks Command Reference](https://docs.microsoft.com/pt-br/windows-server/administration/windows-commands/schtasks)

---

**Dica**: Sempre teste a tarefa manualmente antes de deixar agendada para garantir que tudo funciona corretamente!
