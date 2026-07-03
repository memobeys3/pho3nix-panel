#!/bin/bash
set -e

PANEL_DIR="/opt/xray-panel"

echo "========================================="
echo "   Xray VPN Management Panel Installer"
echo "========================================="

echo "[1/5] Updating system packages..."
apt-get update && apt-get upgrade -y

echo "[2/5] Installing Python and essential tools..."
apt-get install -y python3 python3-pip python3-venv curl jq git

echo "[3/5] Installing Xray-Core..."
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

echo "[4/5] Setting up Panel environment and keys..."
mkdir -p $PANEL_DIR/templates

# Dosyaları kopyala (Script'in projenin kök dizininde çalıştığı varsayılmıştır)
cp requirements.txt database.py xray_manager.py main.py $PANEL_DIR/ 2>/dev/null || echo "Warning: Python dosyaları kopyalanamadı."
cp -r templates/* $PANEL_DIR/templates/ 2>/dev/null || echo "Warning: Template dosyaları kopyalanamadı."

cd $PANEL_DIR

# Reality Protokolü için X25519 Anahtar Çifti Üretimi
echo "Generating Xray Reality Keys..."
KEYS=$(xray x25519)
PRIVATE_KEY=$(echo "$KEYS" | grep "Private" | awk '{print $3}')
PUBLIC_KEY=$(echo "$KEYS" | grep "Public" | awk '{print $3}')

echo "REALITY_PRIVATE=$PRIVATE_KEY" > .env
echo "REALITY_PUBLIC=$PUBLIC_KEY" >> .env
echo "Keys saved to .env"

echo "Installing Python dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[5/5] Configuring Systemd Services..."
cat <<EOF > /etc/systemd/system/xray-panel.service
[Unit]
Description=Xray VPN Management Panel
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

systemctl daemon-reload
systemctl enable xray
systemctl start xray
systemctl enable xray-panel
systemctl start xray-panel

# İlk konfigürasyonu üretmek için API'yi tetikle (Opsiyonel ama sağlıklı başlangıç için)
sleep 2
curl -s http://127.0.0.1:8000/api/users > /dev/null

echo "========================================="
echo "   Installation Complete!"
echo "========================================="
echo "Access your panel at: http://$(curl -s ifconfig.me):8000"
echo "Public Key for Reality (Share with clients): $PUBLIC_KEY"
echo "Short ID: 0123456789abcdef"
echo "========================================="
