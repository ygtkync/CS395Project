import asyncio
import base64
import json
import pathlib
import ssl
import subprocess
import time

import psutil
from aiohttp import web

# Handles the root route
async def hello(request):
    return web.Response(text="Hello")

# Handles the /monitor route with authentication
async def monitor(request):
    auth_header = request.headers.get("Authorization", "")
    if not check_authentication(auth_header):
        return web.Response(
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Safe Zone"'},
            text="Unauthorized: Please enter your username and password."
        )

    path = pathlib.Path(__file__).parents[0].joinpath("monitor.html")
    return web.FileResponse(path)

# Validates user credentials
def check_authentication(auth_header):
    if not auth_header.startswith("Basic "):
        return False
    try:
        encoded_credentials = auth_header.split(" ", 1)[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)

        # Secure user information
        valid_users = {
            "admin": "password",
            "yigit": "123456",
            "deneme": "deneme",
            "elayadi": "654321"
        }

        return valid_users.get(username) == password
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

# Handles WebSocket communication
async def send_stats(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text and msg.data == "stats":
            data = await get_system_stats()
            response = ["stats", data]
            await ws.send_str(json.dumps(response))
        elif msg.type == web.WSMsgType.close:
            break

    return ws

# Gathers system statistics
async def get_system_stats(sort_by="cpu"):
    processes = get_top_processes(sort_by)
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "load_avg": psutil.getloadavg(),
        "uptime": format_uptime(),
        "logged_in_users": get_logged_in_users(),
        "last_10_users": get_last_10_users(),
        "system_logs": get_system_logs(),
        "process_summary": get_process_summary(),
        "processes": processes,
    }

# Retrieves top processes sorted by specified key
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

# Summarizes process states
def get_process_summary():
    processes = list(psutil.process_iter())
    states = {"running": 0, "sleeping": 0, "stopped": 0, "zombie": 0}
    for p in processes:
        try:
            states[p.status()] += 1
        except Exception:
            continue
    return {"total": len(processes), "states": states}

# Retrieves logged-in users
def get_logged_in_users():
    return [user.name for user in psutil.users()]

# Retrieves the last 10 logged-in users
def get_last_10_users():
    try:
        result = subprocess.check_output("last -n 10", shell=True, text=True)
        return result.split("\n")
    except subprocess.SubprocessError:
        return ["Unable to obtain user information."]

# Retrieves the last 50 lines of the system log
def get_system_logs():
    try:
        with open("/var/log/syslog", "r") as f:
            return f.readlines()[-50:]
    except Exception:
        return ["System logs cannot be retrieved."]

# Formats system uptime
def format_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} hours, {minutes} minutes"

# Creates SSL context for secure connections
def create_ssl_context():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert_file = pathlib.Path(__file__).parents[1].joinpath("cert/localhost.crt")
    key_file = pathlib.Path(__file__).parents[1].joinpath("cert/localhost.key")
    ssl_context.load_cert_chain(cert_file, key_file)
    return ssl_context

# Runs the web server
def run():
    ssl_context = create_ssl_context()
    app = web.Application()
    app.add_routes([
        web.get("/ws", send_stats),
        web.get("/monitor", monitor),
        web.get("/hello", hello),
    ])
    web.run_app(app, port=8765, ssl_context=ssl_context)



if __name__ == "__main__":
    print("Server started at wss://localhost:8765")
    run()