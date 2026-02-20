import pyautogui

from afterburner.logger import get_logger
from afterburner.utils.elements import wait_and_click

logger = get_logger(__name__)


def activate_afterburner():
    """
    Realiza ações/configurações no MSI Afterburner já aberto.
    """
    try:
        logger.info("Iniciando ações no Afterburner")
        # time.sleep(5)  # Pequena pausa para garantir que a janela esteja ativa
        # x, y = pyautogui.position()
        # logger.info(f"Posição atual do mouse: ({x}, {y})")
        pyautogui.click(1134, 460)
        wait_and_click("apply.png", timeout=5)
        logger.info("Ações no Afterburner concluídas")
        return True

    except Exception as e:
        logger.error(f"Erro ao ativar Afterburner: {e}")
        return False


if __name__ == "__main__":
    activate_afterburner()
