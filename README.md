# ⚡ Xray VPN Management Panel

Modern, web tabanlı Xray-Core yönetim paneli. VLESS + Reality ve VMess protokollerini destekler, kullanıcı ve kota yönetimi sağlar.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![Xray-Core](https://img.shields.io/badge/Xray-Core-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-purple.svg)

## 🎯 Özellikler

- ✅ **VLESS + Reality** desteği (en güncel ve tespit edilmesi zor protokol)
- ✅ **VMess + WebSocket** desteği
- ✅ Web tabanlı kullanıcı yönetimi
- ✅ Kota ve trafik takibi
- ✅ Otomatik QR kod üretimi
- ✅ `vless://` ve `vmess://` bağlantı linki üretimi
- ✅ Karanlık tema (Dark Mode) arayüz
- ✅ Otomatik X25519 anahtar çifti üretimi
- ✅ Systemd servis entegrasyonu
- ✅ SQLite veritabanı
- ✅ Modern REST API
- ✅ Responsive tasarım

## 📋 Gereksinimler

- Ubuntu/Debian tabanlı Linux sunucu (20.04+)
- Python 3.8+
- Root veya sudo yetkisi
- Açık portlar: 443 (VLESS), 8080 (VMess), 8000 (Panel)

## 🚀 Kurulum

### Otomatik Kurulum (Önerilen)

```bash
# Projeyi klonlayın
git clone https://github.com/username/xray-panel.git
cd xray-panel

# Kurulum betiğini çalıştırın
chmod +x install.sh
sudo ./install.sh
```

Kurulum tamamlandığında:
- Panel `http://SUNUCU_IP:8000` adresinde çalışır
- Reality Public Key terminalde gösterilir (istemcilerle paylaşın)
- Xray servisi otomatik başlar

### Manuel Kurulum

```bash
# 1. Sistem güncelleme
sudo apt-get update && sudo apt-get upgrade -y

# 2. Python ve bağımlılıklar
sudo apt-get install -y python3 python3-pip python3-venv curl jq git

# 3. Xray-Core kurulumu
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# 4. Proje dizini oluştur
sudo mkdir -p /opt/xray-panel
cd /opt/xray-panel

# 5. Dosyaları kopyala (proje dizininden)
sudo cp /path/to/xray-panel/* .
sudo cp -r /path/to/xray-panel/templates .

# 6. Python sanal ortam
sudo python3 -m venv venv
sudo source venv/bin/activate
sudo pip install -r requirements.txt

# 7. Reality anahtarları üret
KEYS=$(xray x25519)
PRIVATE_KEY=$(echo "$KEYS" | grep "Private" | awk '{print $3}')
PUBLIC_KEY=$(echo "$KEYS" | grep "Public" | awk '{print $3}')

echo "REALITY_PRIVATE=$PRIVATE_KEY" | sudo tee .env
echo "REALITY_PUBLIC=$PUBLIC_KEY" | sudo tee -a .env

# 8. Systemd servisi oluştur
sudo cat <<EOF > /etc/systemd/system/xray-panel.service
[Unit]
Description=Xray VPN Management Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/xray-panel
Environment="PATH=/opt/xray-panel/venv/bin"
ExecStart=/opt/xray-panel/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 9. Servisleri başlat
sudo systemctl daemon-reload
sudo systemctl enable xray
sudo systemctl start xray
sudo systemctl enable xray-panel
sudo systemctl start xray-panel
```

## 📖 Kullanım

### Web Arayüzü

1. Tarayıcınızda `http://SUNUCU_IP:8000` adresine gidin
2. "Add New User" bölümünden kullanıcı ekleyin
3. Kullanıcı listesinden "QR" butonuna tıklayarak bağlantı kodunu alın
4. "Copy VLESS Link" veya "Copy VMess Link" ile bağlantıyı kopyalayın

### İstemci Ayarları

#### VLESS + Reality (Önerilen)

```
Protocol: VLESS
Address: SUNUCU_IP
Port: 443
UUID: (panelden alınan UUID)
Flow: xtls-rprx-vision
Security: reality
SNI: www.microsoft.com
Public Key: (install.sh çıktısındaki Public Key)
Short ID: 0123456789abcdef
Fingerprint: chrome
```

#### VMess + WebSocket

```
Protocol: VMess
Address: SUNUCU_IP
Port: 8080
UUID: (panelden alınan UUID)
Alter ID: 0
Security: auto
Network: ws
WebSocket Path: /vmess
```

## 🔒 Güvenlik

### Firewall Ayarları

```bash
# UFW ile portları açın
sudo ufw allow 443/tcp  # VLESS Reality
sudo ufw allow 8080/tcp # VMess WebSocket
sudo ufw allow 8000/tcp # Panel (opsiyonel, reverse proxy kullanın)
sudo ufw allow 22/tcp   # SSH
sudo ufw enable
```

### Production Önerileri

- ⚠️ **Panel portunu (8000) public internet'e açmayın**
- ✅ Nginx reverse proxy kullanın (HTTPS ile)
- ✅ Temel kimlik doğrulama ekleyin (HTTP Basic Auth)
- ✅ Fail2ban kurun
- ✅ Düzenli yedekleme alın (`/opt/xray-panel/xray_panel.db`)

### Nginx Reverse Proxy Örneği

```nginx
server {
    listen 80;
    server_name panel.domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📡 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/users` | Tüm kullanıcıları listele |
| POST | `/api/users?username=xxx&quota_gb=10` | Yeni kullanıcı ekle |
| DELETE | `/api/users/{id}` | Kullanıcı sil |
| POST | `/api/traffic/update?user_id=1&added_bytes=1000` | Trafik güncelle |
| GET | `/api/config` | Sunucu konfigürasyonunu al |

### API Örnekleri

```bash
# Kullanıcıları listele
curl http://localhost:8000/api/users

# Yeni kullanıcı ekle
curl -X POST "http://localhost:8000/api/users?username=ahmet&quota_gb=50"

# Kullanıcı sil
curl -X DELETE http://localhost:8000/api/users/1

# Sunucu bilgilerini al
curl http://localhost:8000/api/config
```

## 🔧 Dosya Yapısı

```
/opt/xray-panel/
├── requirements.txt      # Python bağımlılıkları
├── install.sh            # Otomatik kurulum betiği
├── database.py           # SQLAlchemy ORM
├── xray_manager.py       # Xray config yönetimi
├── main.py               # FastAPI uygulaması
├── xray_panel.db         # SQLite veritabanı
├── .env                  # Reality anahtarları (GİZLİ)
├── venv/                 # Python sanal ortamı
└── templates/
    └── index.html        # Web arayüzü

/etc/xray/
└── config.json           # Xray-Core konfigürasyonu (otomatik üretilir)
```

## 🐛 Sorun Giderme

### Panel açılmıyor

```bash
# Servis durumunu kontrol edin
sudo systemctl status xray-panel

# Logları inceleyin
sudo journalctl -u xray-panel -f
```

### Xray servisi başlamıyor

```bash
# Xray servisi kontrol
sudo systemctl status xray

# Config dosyasını doğrulayın
sudo xray run -test -config /etc/xray/config.json

# Logları kontrol edin
sudo journalctl -u xray -f
```

### Kullanıcılar bağlanamıyor

1. Reality Public Key'in doğru olduğundan emin olun
2. Firewall portlarının açık olduğunu kontrol edin
3. SNI değerini kontrol edin (www.microsoft.com)
4. UUID'nin doğru kopyalandığından emin olun

### Kota aşıldı ama kullanıcı hala bağlı

```bash
# Manuel olarak config'i yenileyin
cd /opt/xray-panel
sudo source venv/bin/activate
python -c "import database, xray_manager; db = next(database.get_db()); xray_manager.apply_config(db)"
```

## 📊 Veritabanı Yedekleme

```bash
# Manuel yedekleme
cp /opt/xray-panel/xray_panel.db /opt/xray-panel/backups/backup-$(date +%Y%m%d).db

# Otomatik yedekleme (crontab)
crontab -e
# Her gün saat 03:00'te yedekle
0 3 * * * cp /opt/xray-panel/xray_panel.db /opt/xray-panel/backups/backup-$(date +\%Y\%m\%d).db
```

## 📝 Değişiklik Günlüğü

### v1.0.0 (2026-07-04)
- ✨ İlk sürüm
- 🎉 VLESS + Reality desteği
- 🎉 VMess + WebSocket desteği
- 🎉 Web arayüzü
- 🎉 Kullanıcı ve kota yönetimi
- 🎉 QR kod ve bağlantı linki üretimi

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

### Geliştirme Ortamı

```bash
git clone https://github.com/username/xray-panel.git
cd xray-panel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## ⚠️ Sorumluluk Reddi

Bu yazılım yalnızca eğitim ve araştırma amaçlıdır. Kullanıcılar yerel yasalara uymakla yükümlüdür. Geliştiriciler, bu yazılımın kullanımından doğabilecek herhangi bir yasal sorumluğu kabul etmez.

## 🙏 Teşekkürler

- [Xray-Core](https://github.com/XTLS/Xray-core) - Güçlü proxy çekirdeği
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [QRCode.js](https://github.com/davidshimjs/qrcodejs) - QR kod üretimi

## 📞 İletişim

- **Issues**: [GitHub Issues](https://github.com/username/xray-panel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/username/xray-panel/discussions)

## 🌟 Yıldız Geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=username/xray-panel&type=Date)](https://star-history.com/#username/xray-panel&Date)

---

<p align="center">
  <strong>Made with ❤️ by the community</strong><br>
  <sub>Eğer bu proje işinize yaradıysa ⭐ vermeyi unutmayın!</sub>
</p>


