import logging
import sys
from logging.handlers import RotatingFileHandler

from afterburner.config import ROOT_DIR, settings


def get_logger(name: str | None) -> logging.Logger:
    """Retorna um logger configurado com base nas settings do projeto."""
    # Se não for passado um nome, usa __name__ do módulo chamador
    if name is None:
        name = __name__

    logger = logging.getLogger(name)

    # Se o logger já foi configurado, retorna ele
    if logger.handlers:
        return logger

    # Define o nível de log
    log_level = getattr(logging, settings.logging.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Formato do log
    formatter = logging.Formatter(settings.logging.log_format)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo (se logging estiver habilitado)
    if settings.logging.enabled:
        # Cria o diretório de logs se não existir
        log_dir = ROOT_DIR / settings.logging.log_dir
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / settings.logging.log_file

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=settings.logging.max_bytes,
            backupCount=settings.logging.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
