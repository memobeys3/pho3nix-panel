from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database
import xray_manager
import uuid
import random
import os
import urllib.request

app = FastAPI(title="Xray VPN Management Panel")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/config")
def get_config():
    # Dinamik olarak sunucu IP'sini ve Reality Public Key'ini döndürür
    env_path = "/opt/xray-panel/.env"
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
            "is_active": u.is_active
        }
        for u in users
    ]

@app.post("/api/users")
def add_user(username: str, quota_gb: float = 0, db: Session = Depends(database.get_db)):
    existing_user = db.query(database.User).filter(database.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Basit port tahsisi
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
    # Xray loglarından veya API'sinden trafik güncellemesi için mock endpoint
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.used_bytes += added_bytes
    if user.quota_bytes > 0 and user.used_bytes >= user.quota_bytes:
        user.is_active = False
    
    db.commit()
    
    if not user.is_active:
        xray_manager.apply_config(db) # Kotayı aşan kullanıcıyı konfigürasyondan düş
        
    return {"message": "Traffic updated"}
