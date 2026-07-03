import json
import os
import subprocess
from sqlalchemy.orm import Session
import database

CONFIG_PATH = "/etc/xray/config.json"
ENV_PATH = "/opt/xray-panel/.env"

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

    # Eğer hiç kullanıcı yoksa Xray servisinin çökmemesi için dummy inbound
    if not inbounds:
        inbounds.append({
            "listen": "127.0.0.1",
            "port": 10000,
            "protocol": "dokodemo-door",
            "settings": {"network": "tcp,udp"},
            "tag": "dummy_in"
        })

    config = {
        "log": {"loglevel": "warning"},
        "inbounds": inbounds,
        "outbounds": [{"protocol": "freedom", "tag": "direct"}],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": []
        }
    }
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
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
