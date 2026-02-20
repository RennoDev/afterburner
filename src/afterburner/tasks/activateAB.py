import pyautogui

from afterburner.logger import get_logger
from afterburner.utils.elements import wait_and_click

logger = get_logger(__name__)


def activate_afterburner():
    """
    Realiza ações/configurações no MSI Afterburner já aberto.
    """
    try:
        logger.info("Ativando Afterburner...")
        pyautogui.click(1134, 460)
        wait_and_click("apply.png", timeout=5)
        logger.info("Afterburner ativado com sucesso")
        return True

    except Exception as e:
        logger.error(f"Erro ao ativar Afterburner: {e}")
        return False


if __name__ == "__main__":
    activate_afterburner()
