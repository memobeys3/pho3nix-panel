import json
import os
import subprocess
import re
from datetime import datetime
from sqlalchemy.orm import Session
import database

CONFIG_PATH = "/etc/xray/config.json"
ENV_PATH = "/opt/pho3nix-panel/.env"
ACCESS_LOG_PATH = "/var/log/xray/access.log"

def load_env():
    env_vars = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_vars[k] = v
    return env_vars

def generate_xray_config(db: Session):
    users = db.query(database.User).filter(database.User.is_active == True).all()
    env = load_env()
    
    private_key = env.get("REALITY_PRIVATE", "")
    
    inbounds = []
    
    # VLESS + Reality Inbound (Port 443)
    vless_clients = [{"id": u.uuid, "level": 0, "email": u.username, "flow": "xtls-rprx-vision"} for u in users]
    if vless_clients:
        inbounds.append({
            "listen": "0.0.0.0",
            "port": 443,
            "protocol": "vless",
            "settings": {
                "clients": vless_clients,
                "decryption": "none"
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "show": False,
                    "dest": "www.microsoft.com:443",
                    "xver": 0,
                    "serverNames": ["www.microsoft.com", "microsoft.com"],
                    "privateKey": private_key,
                    "shortIds": ["", "0123456789abcdef"]
                }
            },
            "sniffing": {
                "enabled": True,
                "destOverride": ["http", "tls", "quic"]
            },
            "tag": "vless_reality_in"
        })

    # VMess + WebSocket Inbound (Port 8080)
    vmess_clients = [{"id": u.uuid, "level": 0, "email": u.username, "alterId": 0} for u in users]
    if vmess_clients:
        inbounds.append({
            "listen": "0.0.0.0",
            "port": 8080,
            "protocol": "vmess",
            "settings": {
                "clients": vmess_clients
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {
                    "path": "/vmess"
                }
            },
            "tag": "vmess_ws_in"
        })

    if not inbounds:
        inbounds.append({
            "listen": "127.0.0.1",
            "port": 10000,
            "protocol": "dokodemo-door",
            "settings": {"network": "tcp,udp"},
            "tag": "dummy_in"
        })

    config = {
        "log": {
            "loglevel": "info",
            "access": ACCESS_LOG_PATH,
            "error": "/var/log/xray/error.log"
        },
        "inbounds": inbounds,
        "outbounds": [{"protocol": "freedom", "tag": "direct"}],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": []
        },
        "stats": {}
    }
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(ACCESS_LOG_PATH), exist_ok=True)
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def restart_xray_service():
    try:
        subprocess.run(["systemctl", "restart", "xray"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def apply_config(db: Session):
    generate_xray_config(db)
    return restart_xray_service()

def parse_traffic_from_logs(db: Session):
    """Xray access log'dan trafik bilgilerini parse eder"""
    if not os.path.exists(ACCESS_LOG_PATH):
        return
    
    traffic_data = {}
    
    try:
        with open(ACCESS_LOG_PATH, "r") as f:
            for line in f:
                # Log format: 2024/01/01 12:00:00 1.2.3.4:12345 accepted tcp:443 [vless_reality_in] email: username
                match = re.search(r'email:\s*(\S+)', line)
                if match:
                    username = match.group(1)
                    if username not in traffic_data:
                        traffic_data[username] = 0
                    
                    # Her log satırı yaklaşık 1KB veri transferini temsil eder (basit tahmin)
                    traffic_data[username] += 1024
        
        # Veritabanını güncelle
        for username, bytes_used in traffic_data.items():
            user = db.query(database.User).filter(database.User.username == username).first()
            if user:
                user.used_bytes += bytes_used
                user.last_traffic_update = datetime.utcnow()
                
                # Kota kontrolü
                if user.quota_bytes > 0 and user.used_bytes >= user.quota_bytes:
                    user.is_active = False
                    
                # Traffic log kaydet
                traffic_log = database.TrafficLog(
                    user_id=user.id,
                    bytes_up=0,
                    bytes_down=bytes_used,
                    timestamp=datetime.utcnow()
                )
                db.add(traffic_log)
        
        db.commit()
        
        # Log dosyasını temizle (okunan satırları sil)
        if traffic_data:
            open(ACCESS_LOG_PATH, 'w').close()
            
    except Exception as e:
        print(f"Log parse hatası: {e}")
