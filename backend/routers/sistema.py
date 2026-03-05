from fastapi import APIRouter, Depends, HTTPException, status
from security import get_current_admin
from services.backup import executar_backup_manual
from services.licenca import LicencaService

router = APIRouter(prefix="/api/sistema", tags=["Sistema"])


@router.post("/backup", dependencies=[Depends(get_current_admin)])
def forcar_backup():
    """Tenta forçar um backup instantâneo do banco."""
    sucesso, msg = executar_backup_manual()
    if not sucesso:
        raise HTTPException(status_code=500, detail=msg)
    return {"msg": "Backup concluído", "path": msg}


@router.get("/licenca")
def checar_status_licenca():
    """Checa se a licença é válida e retorna o aviso, independente do cargo."""
    valida, _ = LicencaService.verificar()
    return {"valida": valida, "mensagem": _}
