# Elementos UI

Pasta para armazenar capturas de elementos da interface do MSI Afterburner.

## 📸 Como Usar

### 1. Capturar Elementos

```python
import pyautogui

# Capturar região específica
pyautogui.screenshot('elements/apply_button.png', region=(x, y, width, height))
```

### 2. Usar nas Tasks

```python
from afterburner.utils.images import click_element, wait_and_click

# Clicar direto
click_element('apply_button.png')

# Aguardar e clicar
wait_and_click('settings_icon.png', timeout=5)
```

## 💡 Dicas

- Capture apenas o elemento necessário (botão, ícone, etc)
- Use nomes descritivos: `apply_button.png`, `settings_icon.png`
- Formato PNG recomendado
- Recorte com precisão para melhor detecção

## ⚙️ Configurações

Ajuste em `config/settings.toml`:

```toml
[default.actions]
confidence = 0.8        # Precisão da detecção (0.7-0.9)
grayscale = true        # Busca em escala de cinza (mais rápido)
wait_timeout = 10.0     # Tempo máximo de espera
```
