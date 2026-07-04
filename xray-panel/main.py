from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database
import xray_manager
import uuid
import random
import os
import urllib.request
import base64
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

app = FastAPI(title="Pho3nix Panel")
templates = Jinja2Templates(directory="templates")

# Scheduler - Periyodik trafik güncelleme
scheduler = AsyncIOScheduler()

def update_traffic_periodically():
    """Her 5 dakikada bir trafiği güncelle"""
    db = next(database.get_db())
    try:
        xray_manager.parse_traffic_from_logs(db)
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(update_traffic_periodically, 'interval', minutes=5)
    scheduler.start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/config")
def get_config():
    env_path = "/opt/pho3nix-panel/.env"
    public_key = ""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("REALITY_PUBLIC="):
                    public_key = line.strip().split("=", 1)[1]
    
    try:
        ip = urllib.request.urlopen('https://ifconfig.me', timeout=3).read().decode('utf8')
    except:
        ip = "YOUR_SERVER_IP"

    return {
        "public_key": public_key,
        "server_ip": ip,
        "sni": "www.microsoft.com",
        "short_id": "0123456789abcdef"
    }

@app.get("/api/users")
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(database.User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "uuid": u.uuid,
            "port": u.port,
            "quota_bytes": u.quota_bytes,
            "used_bytes": u.used_bytes,
            "is_active": u.is_active,
            "last_update": u.last_traffic_update.isoformat() if u.last_traffic_update else None
        }
        for u in users
    ]

@app.post("/api/users")
def add_user(username: str, quota_gb: float = 0, db: Session = Depends(database.get_db)):
    existing_user = db.query(database.User).filter(database.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    port = random.randint(10000, 60000)
    
    new_user = database.User(
        username=username,
        uuid=str(uuid.uuid4()),
        port=port,
        quota_bytes=int(quota_gb * 1024 * 1024 * 1024),
        used_bytes=0,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    xray_manager.apply_config(db)
    
    return {"message": "User added successfully", "uuid": new_user.uuid}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    xray_manager.apply_config(db)
    
    return {"message": "User deleted successfully"}

@app.post("/api/traffic/update")
def update_traffic(user_id: int, added_bytes: int, db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.used_bytes += added_bytes
    if user.quota_bytes > 0 and user.used_bytes >= user.quota_bytes:
        user.is_active = False
    
    db.commit()
    
    if not user.is_active:
        xray_manager.apply_config(db)
        
    return {"message": "Traffic updated"}

@app.get("/api/traffic/live")
def get_live_traffic(db: Session = Depends(database.get_db)):
    """Canlı trafik verilerini döndür"""
    users = db.query(database.User).all()
    return {
        "users": [
            {
                "username": u.username,
                "used_bytes": u.used_bytes,
                "quota_bytes": u.quota_bytes,
                "is_active": u.is_active,
                "last_update": u.last_traffic_update.isoformat() if u.last_traffic_update else None
            }
            for u in users
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/sub/{username}")
def get_subscription(username: str, request: Request, db: Session = Depends(database.get_db)):
    """Abonelik linki - Tüm protokolleri base64 encoded döndürür"""
    user = db.query(database.User).filter(database.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        return PlainTextResponse("Hesabınızın süresi dolmuş veya engellenmiş.", status_code=403)
    
    # Sunucu bilgilerini al
    env_path = "/opt/pho3nix-panel/.env"
    public_key = ""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("REALITY_PUBLIC="):
                    public_key = line.strip().split("=", 1)[1]
    
    try:
        server_ip = urllib.request.urlopen('https://ifconfig.me', timeout=3).read().decode('utf8')
    except:
        server_ip = request.client.host if request.client else "localhost"
    
    # VLESS link oluştur
    vless_params = {
        "type": "tcp",
        "security": "reality",
        "pbk": public_key,
        "sni": "www.microsoft.com",
        "fp": "chrome",
        "sid": "0123456789abcdef",
        "flow": "xtls-rprx-vision"
    }
    vless_link = f"vless://{user.uuid}@{server_ip}:443?{'&'.join([f'{k}={v}' for k,v in vless_params.items()])}#{username}-VLESS"
    
    # VMess link oluştur
    vmess_config = {
        "v": "2",
        "ps": f"{username}-VMess",
        "add": server_ip,
        "port": "8080",
        "id": user.uuid,
        "aid": "0",
        "net": "ws",
        "type": "none",
        "host": "",
        "path": "/vmess",
        "tls": ""
    }
    import json
    vmess_link = "vmess://" + base64.b64encode(json.dumps(vmess_config).encode()).decode()
    
    # Tüm linkleri birleştir ve base64 encode et
    all_links = f"{vless_link}\n{vmess_link}"
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return PlainTextResponse(
        content=encoded,
        headers={
            "Content-Type": "text/plain",
            "Content-Disposition": "inline",
            "X-Sub-User": username,
            "X-Sub-Quota": str(user.quota_bytes),
            "X-Sub-Used": str(user.used_bytes)
        }
    )
