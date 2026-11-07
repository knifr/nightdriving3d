import os
import threading
from aiohttp import web

async def _handle(request):
    return web.Response(text="Night Drive 3D bot is alive 🚗💨")

def _run_server():
    app = web.Application()
    app.router.add_get("/", _handle)
    app.router.add_get("/health", _handle)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port, print=None)

def keep_alive():
    """Запускает aiohttp-сервер в фоне."""
    t = threading.Thread(target=_run_server, daemon=True)
    t.start()
