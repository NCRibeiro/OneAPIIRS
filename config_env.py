# config_env.py

import os
from configparser import ConfigParser

# Verifica se o arquivo de configuração existe
if os.path.exists("config_env.ini"):
    # Interpolação desativada para evitar conflitos com formatos de logging ou tokens
    config = ConfigParser(interpolation=None)
    config.read("config_env.ini")

    # Itera pelas seções e adiciona ao os.environ
    for section in config.sections():
        for key, value in config.items(section):
            os.environ[key.upper()] = value  # Upper garante compatibilidade com Pydantic
