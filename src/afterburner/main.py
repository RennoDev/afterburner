"""
Entry point principal do Afterburner Controller.
Orquestra o workflow de abertura, configuração e fechamento do MSI Afterburner.
"""

import sys

from afterburner.config import settings
from afterburner.logger import get_logger
from afterburner.tasks.activateAB import activate_afterburner
from afterburner.tasks.closeAB import close_afterburner
from afterburner.tasks.openAB import open_afterburner

logger = get_logger(__name__)


def main():
    """
    Workflow principal: abre, configura e fecha o MSI Afterburner.
    """
    logger.info("=" * 60)
    logger.info(f"Iniciando {settings.app_name} v{settings.version}")
    logger.info("=" * 60)

    success = False
    afterburner_opened = False

    try:
        # Etapa 1: Abrir Afterburner
        logger.info("Etapa 1/3: Abrindo Afterburner...")
        if not open_afterburner():
            logger.error("Falha ao abrir Afterburner")
            return 1

        afterburner_opened = True
        logger.info("✓ Afterburner aberto com sucesso")

        # Etapa 2: Realizar ações
        logger.info("Etapa 2/3: Executando ações...")
        if not activate_afterburner():
            logger.error("Falha ao executar ações no Afterburner")
            return 2

        logger.info("✓ Ações executadas com sucesso")

        # Etapa 3: Fechar Afterburner
        logger.info("Etapa 3/3: Fechando Afterburner...")
        if not close_afterburner():
            logger.warning("Falha ao fechar Afterburner (pode já estar fechado)")
        else:
            logger.info("✓ Afterburner fechado com sucesso")

        success = True
        return 0

    except KeyboardInterrupt:
        logger.warning("Execução interrompida pelo usuário (Ctrl+C)")
        return 130

    except Exception as e:
        logger.error(f"Erro inesperado durante execução: {e}", exc_info=True)
        return 3

    finally:
        # Garantir fechamento se algo deu errado
        if not success and afterburner_opened:
            logger.info("Tentando fechar Afterburner após erro...")
            try:
                close_afterburner()
            except Exception as e:
                logger.error(f"Falha no fechamento de emergência: {e}")

        # Log final
        logger.info("=" * 60)
        if success:
            logger.info("Workflow concluído com sucesso! ✓")
        else:
            logger.error("Workflow concluído com erros ✗")
        logger.info("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
