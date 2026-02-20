from afterburner.logger import get_logger
from afterburner.utils.elements import wait_and_click

logger = get_logger(__name__)


def close_afterburner():
    """
    Fecha o MSI Afterburner.
    """
    try:
        logger.info("Iniciando fechamento do Afterburner")
        wait_and_click("minimizar.png", timeout=5)
        logger.info("Afterburner fechado com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao fechar Afterburner: {e}")
        return False


if __name__ == "__main__":
    close_afterburner()
