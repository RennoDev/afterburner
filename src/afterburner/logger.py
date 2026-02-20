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

    # Define o nível de log com fallback
    log_level_str = getattr(settings.logging, "log_level", "INFO")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Formato do log com fallback
    log_format = getattr(
        settings.logging,
        "log_format",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    formatter = logging.Formatter(log_format)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo (se logging estiver habilitado)
    if getattr(settings.logging, "enabled", True):
        # Cria o diretório de logs se não existir
        log_dir = ROOT_DIR / getattr(settings.logging, "log_dir", "log")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / getattr(settings.logging, "log_file", "afterburner.log")

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=getattr(settings.logging, "max_bytes", 10485760),
            backupCount=getattr(settings.logging, "backup_count", 5),
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
