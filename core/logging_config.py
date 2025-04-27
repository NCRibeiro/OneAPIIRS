# logging_config.py

import logging

# Configuração básica do logger
logging.basicConfig(
    filename='security_audit.log',  # Arquivo de log
    level=logging.INFO,  # Nível de log: INFO, WARNING, ERROR, etc.
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato dos logs
)

# Função para obter o logger configurado
def get_logger():
    return logging.getLogger(__name__)
