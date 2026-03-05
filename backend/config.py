"""
Configurações centrais do sistema de restaurante.
Lidas de variáveis de ambiente ou valores padrão.
"""

import os
from pathlib import Path

# Diretório base do backend
BASE_DIR = Path(__file__).parent

# Banco de dados
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/restaurante.db"

# Segurança JWT
SECRET_KEY = os.getenv(
    "SECRET_KEY", "restaurante-local-first-secret-key-mude-em-producao"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12  # 12 horas

# Servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Backup automático
BACKUP_DIR = BASE_DIR / "data" / "backups"
BACKUP_HORA = 3  # 3h da manhã

# Versão do sistema
VERSION = "1.0.0"
SYSTEM_NAME = "SolidMenu"
