import os
import threading
import sys
import webbrowser
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Imports Internos ---
from config import BASE_DIR, PORT, SYSTEM_NAME
from database import init_db
from services.backup import iniciar_agendador_background

# Import de todos os routers
from routers.auth import router as router_auth
from routers.usuarios import router as router_user
from routers.cardapio import router as router_cardapio
from routers.cadastros import router as router_cadastros
from routers.estoque import router as router_estoque
from routers.pedidos import router as router_pedidos
from routers.financeiro import router as router_financeiro
from routers.sistema import router as router_sistema

# Cria app principal
app = FastAPI(
    title=SYSTEM_NAME,
    description="Backend API do SolidMenu - Sistema Local-First",
    version="1.0.0",
)

# CORS (Permite PWAs acessarem a rede local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar em prd para os IPs da rede local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as Rotas
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_cardapio)
app.include_router(router_cadastros)
app.include_router(router_estoque)
app.include_router(router_pedidos)
app.include_router(router_financeiro)
app.include_router(router_sistema)


# Setup estáticos silencioso
def mount_directory(path: Path, url: str):
    path.mkdir(parents=True, exist_ok=True)
    app.mount(url, StaticFiles(directory=str(path), html=True), name=path.name)


mount_directory(BASE_DIR / "static" / "admin", "/admin")
mount_directory(BASE_DIR / "static" / "garcom", "/pwa-garcom")
mount_directory(BASE_DIR / "static" / "entregador", "/pwa-entregador")
mount_directory(BASE_DIR / "static" / "producao", "/tela-producao")


# ----------------------------------------------------
# Eventos de Startup
# ----------------------------------------------------
@app.on_event("startup")
def startup_event():
    # Inicializa banco e popula admin
    init_db()
    # Inicia serviço de backup thread
    iniciar_agendador_background()


# ----------------------------------------------------
# Pystray Integrado no __main__
# ----------------------------------------------------
def start_tray_icon():
    import pystray
    from PIL import Image, ImageDraw

    # Desenho simples de um quadrado verde para o icone (poderia carregar .ico)
    icon_image = Image.new("RGB", (64, 64), color="white")
    d = ImageDraw.Draw(icon_image)
    d.rectangle([16, 16, 48, 48], fill="green")

    def on_open_admin(icon, item):
        webbrowser.open(f"http://localhost:{PORT}/admin/")

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)  # Encerra o uvicorn também à força

    menu = (
        pystray.MenuItem("Abrir Painel Admin", on_open_admin),
        pystray.MenuItem("Sair do Sistema", on_quit),
    )

    tray_icon = pystray.Icon(
        "restaurante_sys", icon_image, title=SYSTEM_NAME, menu=menu
    )
    tray_icon.run()


if __name__ == "__main__":
    import uvicorn

    # Em ambiente Windows com pyinstaller, esconderemos a janela via flags,
    # rodando FastAPI em background e o tray icon travando o thread principal.

    # Thread do FastAPI
    server_thread = threading.Thread(
        target=uvicorn.run,
        args=("main:app",),
        kwargs={"host": "0.0.0.0", "port": PORT, "log_level": "info"},
        daemon=True,
    )
    server_thread.start()

    # Main thread fica com o Pystray
    start_tray_icon()
