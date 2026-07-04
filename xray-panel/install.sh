#!/bin/bash
set -e

PANEL_DIR="/opt/pho3nix-panel"

echo "========================================="
echo "   🦊 Pho3nix Panel Installer"
echo "========================================="

echo "[1/6] Sistem paketleri güncelleniyor..."
apt-get update && apt-get upgrade -y

echo "[2/6] Python ve araçlar kuruluyor..."
apt-get install -y python3 python3-pip python3-venv curl jq git

echo "[3/6] Xray-Core kuruluyor..."
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

echo "[4/6] Panel ortamı hazırlanıyor..."
mkdir -p $PANEL_DIR/templates
mkdir -p /var/log/xray

cp requirements.txt database.py xray_manager.py main.py telegram_bot.py $PANEL_DIR/ 2>/dev/null || echo "Warning: Python dosyaları kopyalanamadı."
cp -r templates/* $PANEL_DIR/templates/ 2>/dev/null || echo "Warning: Template dosyaları kopyalanamadı."

cd $PANEL_DIR

echo "Reality anahtarları üretiliyor..."
KEYS=$(xray x25519)
PRIVATE_KEY=$(echo "$KEYS" | grep "Private" | awk '{print $3}')
PUBLIC_KEY=$(echo "$KEYS" | grep "Public" | awk '{print $3}')

echo "REALITY_PRIVATE=$PRIVATE_KEY" > .env
echo "REALITY_PUBLIC=$PUBLIC_KEY" >> .env

# Telegram bot kurulumu
read -p "Telegram bot token'ınız var mı? (y/n): " HAS_BOT
if [ "$HAS_BOT" = "y" ]; then
    read -p "Bot token: " BOT_TOKEN
    read -p "Admin Telegram ID'leri (virgülle ayırın): " ADMIN_IDS
    echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" >> .env
    echo "TELEGRAM_ADMIN_IDS=$ADMIN_IDS" >> .env
fi

echo "Python bağımlılıkları kuruluyor..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[5/6] Systemd servisleri oluşturuluyor..."
cat <<EOF > /etc/systemd/system/pho3nix-panel.service
[Unit]
Description=Pho3nix VPN Management Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PANEL_DIR
Environment="PATH=$PANEL_DIR/venv/bin"
ExecStart=$PANEL_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

if [ "$HAS_BOT" = "y" ]; then
cat <<EOF > /etc/systemd/system/pho3nix-bot.service
[Unit]
Description=Pho3nix Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PANEL_DIR
Environment="PATH=$PANEL_DIR/venv/bin"
ExecStart=$PANEL_DIR/venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
fi

echo "[6/6] Servisler başlatılıyor..."
systemctl daemon-reload
systemctl enable xray
systemctl start xray
systemctl enable pho3nix-panel
systemctl start pho3nix-panel

if [ "$HAS_BOT" = "y" ]; then
    systemctl enable pho3nix-bot
    systemctl start pho3nix-bot
fi

sleep 2
curl -s http://127.0.0.1:8000/api/users > /dev/null

echo "========================================="
echo "   ✅ Kurulum Tamamlandı!"
echo "========================================="
echo "Panel: http://$(curl -s ifconfig.me):8000"
echo "Reality Public Key: $PUBLIC_KEY"
if [ "$HAS_BOT" = "y" ]; then
    echo "Telegram Bot: Aktif"
fi
echo "========================================="
