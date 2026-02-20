from afterburner.logger import get_logger
from afterburner.utils.elements import wait_and_click, wait_element

logger = get_logger(__name__)


def open_afterburner():
    """
    Abre o MSI Afterburner através da busca do Windows e aguarda a janela estar pronta.
    """
    try:
        logger.info("Abrindo Afterburner...")

        wait_and_click("segundoPlano.png", timeout=5)
        wait_and_click("afterburnerIcon.png", timeout=5)
        wait_element("afterburner.png", timeout=5)

        if not wait_element("afterburner.png", timeout=10):
            logger.error("Janela do Afterburner não detectada")
            return False

        logger.info("Afterburner aberto")
        return True
    except Exception as e:
        logger.error(f"Erro ao abrir Afterburner: {e}")
        return False


if __name__ == "__main__":
    open_afterburner()
