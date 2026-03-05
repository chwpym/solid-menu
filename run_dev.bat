@echo off
echo ===================================================
echo Iniciando Servidor de Desenvolvimento - Restaurante
echo ===================================================

echo.
echo [1/3] Verificando ambiente virtual (venv)...
if not exist "venv\" (
    echo Criando novo ambiente virtual...
    python -m venv venv
)

echo.
echo [2/3] Ativando ambiente e instalando dependencias (se necessario)...
call venv\Scripts\activate.bat
pip install -r backend\requirements.txt

echo.
echo [3/3] Iniciando o backend FastAPI (com Auto-Reload)...
echo.
echo Acesse o Swagger UI (Docs) em: http://localhost:8000/docs
echo Para parar o servidor, pressione CTRL+C várias vezes.
echo.
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
