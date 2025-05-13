import logging
import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

# Nível de log vindo do env (default INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Formato comum para todos os handlers
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Handler para arquivo rotativo
file_handler = RotatingFileHandler(
    filename="security_audit.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Handler para console (docker logs)
console_handler = StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configuração raiz
logging.basicConfig(level=LOG_LEVEL, handlers=[file_handler, console_handler])


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)
