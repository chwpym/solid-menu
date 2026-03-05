"""
Serviço de Backup Automático e Manual do banco de dados SQLite.
"""

import os
import shutil
import logging
from datetime import datetime
from threading import Thread
import time
import schedule

from config import DATABASE_URL, BACKUP_DIR, BACKUP_HORA

logger = logging.getLogger(__name__)


def parse_db_path() -> str:
    """Extrai o caminho absoluto do arquivo sqlite a partir da DATABASE_URL."""
    # sqlite:///caminho/para/banco.db -> caminho/para/banco.db
    if DATABASE_URL.startswith("sqlite:///"):
        return DATABASE_URL.replace("sqlite:///", "")
    return ""


def executar_backup_manual() -> tuple[bool, str]:
    """Copia o arquivo do SQLite para a pasta de backups com timestamp."""
    db_path = parse_db_path()
    if not db_path or not os.path.exists(db_path):
        return False, "Arquivo de banco de dados não encontrado."

    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = os.path.join(BACKUP_DIR, f"backup_{timestamp}.db")

        # Como é um monolito local de baixo tráfego de madrugada, um copy2
        # do SQLite geralmente é suficiente. Se houver concorrência alta,
        # seria melhor usar a API de backup do SQLite em Python.
        shutil.copy2(db_path, destino)
        logger.info(f"Backup concluído com sucesso: {destino}")
        return True, str(destino)
    except Exception as e:
        logger.error(f"Erro ao realizar backup: {e}")
        return False, str(e)


def _rotina_backup_diario():
    logger.info("Iniciando rotina de backup diário automático...")
    sucesso, msg = executar_backup_manual()
    if sucesso:
        limpar_backups_antigos(dias_retes=30)


def limpar_backups_antigos(dias_retes: int = 30):
    """Remove arquivos de backup mais antigos que 'dias_retes'."""
    try:
        agora = time.time()
        for arquivo in os.listdir(BACKUP_DIR):
            caminho_completo = os.path.join(BACKUP_DIR, arquivo)
            if os.path.isfile(caminho_completo):
                idade_dias = (agora - os.path.getmtime(caminho_completo)) / (24 * 3600)
                if idade_dias > dias_retes:
                    os.remove(caminho_completo)
                    logger.info(f"Backup antigo removido: {arquivo}")
    except Exception as e:
        logger.error(f"Erro ao limpar backups antigos: {e}")


def _scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(60)


def iniciar_agendador_background():
    """Inicia thread do schedule rodando em background no FastAPI."""
    horario_formatado = f"{BACKUP_HORA:02d}:00"
    schedule.every().day.at(horario_formatado).do(_rotina_backup_diario)

    thread = Thread(target=_scheduler_loop, daemon=True)
    thread.start()
    logger.info(
        f"Serviço de backup automático agendado para {horario_formatado} diariamente."
    )
