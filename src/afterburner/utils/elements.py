import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

from afterburner.config import ROOT_DIR, settings
from afterburner.logger import get_logger

logger = get_logger(__name__)

# Diretório de elementos UI
ELEMENTS_DIR = ROOT_DIR / "elements"


# ============================================================================
# Funções de Alto Nível (para uso nas tasks)
# ============================================================================


def wait_and_click(element_name: str, timeout: float | None) -> bool:
    """
    Aguarda um elemento aparecer e clica nele.

    Args:
        element_name: Nome do arquivo do elemento
        timeout: Tempo máximo de espera

    Returns:
        True se encontrou e clicou, False caso contrário
    """
    location = wait_element(element_name, timeout)

    if location:
        logger.info(f"Clicando em '{element_name}' após aguardar")

        if settings.actions.human_simulation:
            duration = settings.actions.mouse_duration
        else:
            duration = 0

        pyautogui.moveTo(location[0], location[1], duration=duration)
        pyautogui.click()

        time.sleep(settings.actions.global_wait)
        return True

    return False


def click_element(element_name: str, clicks: int = 1) -> bool:
    """
    Localiza e clica no centro de um elemento.

    Args:
        element_name: Nome do arquivo do elemento
        clicks: Número de cliques

    Returns:
        True se encontrou e clicou, False caso contrário
    """
    location = find_element(element_name)

    if location:
        logger.info(f"Clicando em '{element_name}' na posição {location}")

        if settings.actions.human_simulation:
            duration = settings.actions.mouse_duration
        else:
            duration = 0

        pyautogui.moveTo(location[0], location[1], duration=duration)
        pyautogui.click(clicks=clicks)

        time.sleep(settings.actions.global_wait)
        return True

    logger.warning(f"Elemento '{element_name}' não encontrado para clicar")
    return False


# ============================================================================
# Funções de Nível Intermediário
# ============================================================================


def wait_element(
    element_name: str, timeout: Optional[float] = None
) -> Optional[Tuple[int, int]]:
    """
    Aguarda um elemento aparecer na tela.

    Args:
        element_name: Nome do arquivo do elemento
        timeout: Tempo máximo de espera

    Returns:
        Tupla (x, y) com coordenadas do centro ou None se timeout
    """
    if timeout is None:
        timeout = settings.actions.wait_timeout

    logger.info(f"Aguardando elemento '{element_name}' (timeout={timeout}s)")
    end_time = time.time() + timeout

    while time.time() < end_time:
        location = find_element(element_name)
        if location:
            logger.info(f"Elemento '{element_name}' encontrado")
            return location

        time.sleep(settings.actions.check_interval)

    logger.warning(f"Timeout ao aguardar elemento '{element_name}'")
    return None


def find_element(element_name: str) -> Optional[Tuple[int, int]]:
    """
    Localiza um elemento na tela e retorna o centro.

    Args:
        element_name: Nome do arquivo do elemento (ex: 'apply_button.png')

    Returns:
        Tupla (x, y) com coordenadas do centro ou None se não encontrado
    """
    element_path = _get_element_path(element_name)

    if not element_path.exists():
        logger.error(f"Elemento não encontrado: {element_path}")
        return None

    try:
        location = pyautogui.locateCenterOnScreen(
            str(element_path),
            confidence=settings.actions.confidence,
            grayscale=settings.actions.grayscale,
        )

        if location:
            logger.debug(f"Elemento '{element_name}' encontrado em: {location}")

        return location

    except Exception as e:
        logger.error(f"Erro ao buscar elemento '{element_name}': {e}")
        return None


# ============================================================================
# Funções Auxiliares Internas
# ============================================================================


def _get_element_path(element_name: str) -> Path:
    """Retorna o caminho completo para um elemento."""
    return ELEMENTS_DIR / element_name


# ============================================================================
# Inicialização
# ============================================================================


def setup():
    """Inicializa configurações do PyAutoGUI."""
    pyautogui.FAILSAFE = settings.actions.use_failsafe
    pyautogui.PAUSE = settings.actions.pause_between_actions

    ELEMENTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"PyAutoGUI configurado - Fail-Safe: {pyautogui.FAILSAFE}")
    logger.debug(f"Diretório de elementos: {ELEMENTS_DIR}")


# Inicializar automaticamente
setup()
