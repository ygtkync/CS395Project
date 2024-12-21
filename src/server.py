import asyncio
import json
import pathlib
import ssl
import subprocess
import psutil
import time
from aiohttp import web


async def hello(request):
    text = "Hello"
    return web.Response(text=text)


async def monitor(request):
    path = pathlib.Path(__file__).parents[0].joinpath("monitor.html")
    print("Serving {path}".format(path=path))
    return web.FileResponse(path)


async def get_system_stats(sort_by="cpu"):

    processes = get_top_processes(sort_by)
    stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "load_avg": psutil.getloadavg(),
        "uptime": format_uptime(),
        "process_summary": get_process_summary(),
        "processes": processes,
        "logged_in_users": get_logged_in_users(),
        "last_10_users": get_last_10_users(),
        "system_logs": get_system_logs(),
    }
    return stats

def get_top_processes(sort_by):

    key = {
        "cpu": "cpu_percent",
        "memory": "memory_percent",
        "pid": "pid",
    }.get(sort_by, "cpu_percent")
    processes = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            continue
    return sorted(processes, key=lambda x: x[key] or 0, reverse=True)[:15]

def get_process_summary():

    processes = list(psutil.process_iter())
    states = {"running": 0, "sleeping": 0, "stopped": 0, "zombie": 0}
    for p in processes:
        try:
            states[p.status()] += 1
        except:
            pass
    return {"total": len(processes), "states": states}

def get_logged_in_users():

    return [user.name for user in psutil.users()]

def get_last_10_users():

    try:
        cmd = "last -n 10"
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result.split("\n")
    except:
        return ["Son kullanıcı bilgisi alınamıyor."]

def get_system_logs():
    """Son 50 sistem logunu getir."""
    try:
        with open("/var/log/system.log", "r") as f:
            return f.readlines()[-50:]
    except:
        return ["Sistem logları alınamıyor."]

def format_uptime():
    """Çalışma süresini oku."""
    uptime_seconds = int(time.time() - psutil.boot_time())
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} saat, {minutes} dakika"


async def send_stats(request):
    """Send system stats to WebSocket client."""
    print("Client connected")
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text and msg.data == "stats":
            data = await get_system_stats()
            response = ["stats", data]
            await ws.send_str(json.dumps(response))
        elif msg.type == web.WSMsgType.binary:
            # Ignore binary messages
            continue
        elif msg.type == web.WSMsgType.close:
            break

    return ws


def create_ssl_context():
    """Create SSL context for secure WebSocket connection."""
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert_file = pathlib.Path(__file__).parents[1].joinpath("cert/localhost.crt")
    key_file = pathlib.Path(__file__).parents[1].joinpath("cert/localhost.key")
    ssl_context.load_cert_chain(cert_file, key_file)
    return ssl_context


def run():
    """Start WebSocket server."""
    ssl_context = create_ssl_context()
    app = web.Application()
    app.add_routes(
        [
            web.get("/ws", send_stats),
            web.get("/monitor", monitor),
            web.get("/hello", hello),
        ]
    )
    web.run_app(app, port=8765, ssl_context=ssl_context)


if __name__ == "__main__":
    print("Server started at wss://localhost:8765")
    run()