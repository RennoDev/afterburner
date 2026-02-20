# Guia Básico do PyAutoGUI

Este guia apresenta os comandos essenciais do PyAutoGUI para automação de interface gráfica, focado no uso para controlar o MSI Afterburner.

## 📦 Importação

```python
import pyautogui
```

## 🖱️ Controle do Mouse

### Posição do Mouse

```python
# Obter posição atual do mouse
x, y = pyautogui.position()
print(f"Mouse está em X: {x}, Y: {y}")

# Obter tamanho da tela
largura, altura = pyautogui.size()
print(f"Resolução: {largura}x{altura}")
```

### Mover o Mouse

```python
# Mover para coordenadas absolutas
pyautogui.moveTo(100, 200)  # Move para x=100, y=200

# Mover relativo à posição atual
pyautogui.move(50, -30)  # Move 50px direita, 30px cima

# Mover com duração (animação suave)
pyautogui.moveTo(500, 500, duration=2)  # 2 segundos
```

### Cliques

```python
# Clique simples no local atual
pyautogui.click()

# Clique em coordenadas específicas
pyautogui.click(x=100, y=200)

# Clique duplo
pyautogui.doubleClick()

# Clique com botão direito
pyautogui.rightClick()

# Cliques múltiplos
pyautogui.click(clicks=3)  # Clica 3 vezes

# Segurar e soltar (drag)
pyautogui.mouseDown()  # Pressiona botão
pyautogui.mouseUp()    # Solta botão

# Arrastar
pyautogui.drag(100, 0, duration=1)  # Arrasta 100px para direita
```

## ⌨️ Controle do Teclado

### Digitar Texto

```python
# Digitar texto (com intervalo entre teclas)
pyautogui.write('Hello World!', interval=0.1)

# Pressionar uma tecla
pyautogui.press('enter')
pyautogui.press('esc')
pyautogui.press('tab')

# Pressionar múltiplas teclas em sequência
pyautogui.press(['left', 'left', 'down'])

# Segurar tecla
pyautogui.keyDown('shift')
pyautogui.press('a')
pyautogui.keyUp('shift')
```

### Atalhos

```python
# Combinações de teclas
pyautogui.hotkey('ctrl', 'c')  # Copiar
pyautogui.hotkey('ctrl', 'v')  # Colar
pyautogui.hotkey('alt', 'f4')  # Fechar janela
pyautogui.hotkey('ctrl', 'alt', 'del')  # Múltiplas teclas
```

### Teclas Especiais

```python
# Lista de teclas especiais disponíveis:
# 'enter', 'esc', 'tab', 'space', 'backspace', 'delete'
# 'up', 'down', 'left', 'right'
# 'pageup', 'pagedown', 'home', 'end'
# 'f1' até 'f12'
# 'volumeup', 'volumedown', 'volumemute'
# 'printscreen', 'insert', 'pause'
```

## 🖼️ Reconhecimento de Imagem

### Localizar Imagem na Tela

```python
# Encontrar coordenadas de uma imagem
location = pyautogui.locateOnScreen('botao.png')
if location:
    print(f"Encontrado em: {location}")
    # Retorna: Box(left=x, top=y, width=w, height=h)

# Obter centro da imagem
center = pyautogui.locateCenterOnScreen('botao.png')
if center:
    pyautogui.click(center)

# Localizar todas as ocorrências
locations = pyautogui.locateAllOnScreen('icone.png')
for loc in locations:
    print(loc)

# Com tolerância (confidence 0.0 a 1.0)
# Requer opencv-python
location = pyautogui.locateOnScreen('botao.png', confidence=0.8)
```

### Captura de Tela

```python
# Capturar tela inteira
screenshot = pyautogui.screenshot()
screenshot.save('tela.png')

# Capturar região específica (x, y, largura, altura)
screenshot = pyautogui.screenshot(region=(0, 0, 300, 400))

# Obter cor de um pixel
cor = pyautogui.pixel(100, 200)
print(cor)  # (R, G, B)

# Verificar se pixel corresponde a cor
if pyautogui.pixelMatchesColor(100, 200, (255, 0, 0)):
    print("Pixel é vermelho!")
```

## ⏱️ Controle de Tempo

```python
import time

# Pausa simples
time.sleep(1)  # Aguarda 1 segundo

# Pausa do PyAutoGUI (recomendado)
pyautogui.sleep(1)

# Definir pausa automática entre comandos
pyautogui.PAUSE = 0.5  # 0.5 segundos entre cada comando
```

## 🛡️ Segurança

### Fail-Safe

```python
# Ativar fail-safe (padrão: True)
# Move mouse para canto superior esquerdo para abortar
pyautogui.FAILSAFE = True

# Desativar (cuidado!)
pyautogui.FAILSAFE = False
```

### Validação de Coordenadas

```python
# Verificar se coordenadas estão dentro da tela
x, y = 1000, 500
if pyautogui.onScreen(x, y):
    pyautogui.click(x, y)
else:
    print("Coordenadas fora da tela!")
```

## 📋 Caixas de Mensagem

```python
# Alerta simples
pyautogui.alert('Operação concluída!', 'Sucesso')

# Confirmar (OK/Cancel)
resposta = pyautogui.confirm('Deseja continuar?', 'Confirmação')
if resposta == 'OK':
    print("Usuário confirmou")

# Prompt de texto
nome = pyautogui.prompt('Digite seu nome:')

# Senha
senha = pyautogui.password('Digite sua senha:')
```

## 🎯 Exemplo Prático: Interagir com MSI Afterburner

```python
import pyautogui
import time

# Configuração
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

# 1. Descobrir posição de um botão (executar uma vez)
print("Mova o mouse para o botão desejado...")
time.sleep(3)
x, y = pyautogui.position()
print(f"Posição do botão: ({x}, {y})")

# 2. Clicar no botão descoberto
pyautogui.click(x, y)

# 3. Usar imagem como referência (mais confiável)
botao_location = pyautogui.locateCenterOnScreen('botao_apply.png')
if botao_location:
    pyautogui.click(botao_location)
else:
    print("Botão não encontrado na tela")

# 4. Sequência de ações
pyautogui.click(100, 200)  # Clique em um campo
time.sleep(0.5)
pyautogui.write('85')  # Digita valor
time.sleep(0.5)
pyautogui.press('tab')  # Navega para próximo campo
pyautogui.click(300, 400)  # Clica em aplicar
```

## 🔍 Dicas para Descobrir Coordenadas

### Método 1: Script de Posição

```python
import pyautogui
import time

print("Você tem 5 segundos para posicionar o mouse...")
time.sleep(5)
print(f"Posição: {pyautogui.position()}")
```

### Método 2: Loop de Monitoramento

```python
import pyautogui

print("Pressione Ctrl+C para parar")
print("Mova o mouse para ver coordenadas em tempo real:")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x:4d} Y: {y:4d}", end='\r')
        pyautogui.sleep(0.1)
except KeyboardInterrupt:
    print("\nCaptura finalizada!")
```

### Método 3: Capturar Região

```python
import pyautogui

# Captura uma região e salva para análise
pyautogui.screenshot('regiao.png', region=(0, 0, 800, 600))
print("Região capturada! Abra 'regiao.png' para analisar")
```

## ⚠️ Considerações Importantes

1. **Resolução da Tela**: Coordenadas são específicas da resolução. Se mudar resolução, precisa recalibrar.

2. **Escalamento do Windows**: Em telas com DPI alto, pode ser necessário ajustar coordenadas.

3. **Performance**: Usar `locateOnScreen()` é lento. Use com moderação ou em regiões específicas.

4. **Fail-Safe**: Sempre deixe ativado durante desenvolvimento. Mova mouse para canto para abortar.

5. **Delays**: Sempre adicione `time.sleep()` entre ações importantes para dar tempo do sistema responder.

6. **Janela Ativa**: Certifique-se que a janela do Afterburner está em foco antes de enviar comandos.

## 📚 Recursos Adicionais

- [Documentação Oficial do PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Cheat Sheet](https://pyautogui.readthedocs.io/en/latest/quickstart.html)
- Para usar `confidence` em `locateOnScreen()`, instale: `uv add opencv-python`

---

**Dica Pro**: Sempre teste seus scripts com pausas longas primeiro, depois reduza gradualmente para otimizar.
