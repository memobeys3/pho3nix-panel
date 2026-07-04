# 🦊 Pho3nix Panel

Modern, web tabanlı Xray-Core yönetim paneli. VLESS + Reality ve VMess protokollerini destekler, kullanıcı ve kota yönetimi sağlar.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![Xray-Core](https://img.shields.io/badge/Xray-Core-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-1.1.0-purple.svg)

## 🎯 Özellikler

- ✅ **VLESS + Reality** desteği (en güncel ve tespit edilmesi zor protokol)
- ✅ **VMess + WebSocket** desteği
- ✅ **Abonelik Sistemi** (v2rayNG, Streisand, Hiddify uyumlu)
- ✅ **Telegram Bot Entegrasyonu** (mobilden yönetim)
- ✅ **Canlı Trafik İzleme** (gerçek zamanlı kullanım takibi)
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
git clone https://github.com/memobeys3/pho3nix-panel.git
cd pho3nix-panel

# Kurulum betiğini çalıştırın
chmod +x install.sh
sudo ./install.sh
```

Kurulum sırasında Telegram bot kurulumu isteyecektir. Eğer bot kullanmak istiyorsanız:
1. [@BotFather](https://t.me/BotFather)'dan yeni bot oluşturun ve token'ı alın
2. Kendi Telegram ID'nizi öğrenin ([@userinfobot](https://t.me/userinfobot) kullanabilirsiniz)
3. Kurulum sırasında bu bilgileri girin

Kurulum tamamlandığında:
- Panel `http://SUNUCU_IP:8000` adresinde çalışır
- Reality Public Key terminalde gösterilir (istemcilerle paylaşın)
- Xray servisi ve Telegram bot (isteğe bağlı) otomatik başlar

## 📖 Kullanım

### Web Arayüzü

1. Tarayıcınızda `http://SUNUCU_IP:8000` adresine gidin
2. "Yeni Kullanıcı Ekle" bölümünden kullanıcı ekleyin
3. Kullanıcı listesinden "QR" butonuna tıklayarak bağlantı kodunu alın
4. **Abonelik Linkini Kopyala** butonu ile tek linkle tüm protokolleri alın

### 📱 Abonelik Sistemi (Subscription Link)

**En kolay yöntem!** Kullanıcıya tek bir link verirsiniz, tüm uygulamalar otomatik olarak sunucuları çeker.

**Abonelik Linki Formatı:**
```
http://SUNUCU_IP:8000/sub/KULLANICI_ADI
```

**Örnek:**
```
http://123.45.67.89:8000/sub/ahmet
```

#### Kullanıcı Uygulamalarına Ekleme:

**v2rayNG (Android):**
1. Uygulamayı açın
2. Sağ üstteki **"+"** butonuna tıklayın
3. **"İçe aktar"** veya **"Import from clipboard"** seçin
4. Abonelik linkini yapıştırın
5. **"Abonelik güncelle"** butonuna tıklayın

**Streisand (iOS):**
1. Uygulamayı açın
2. **"+"** butonuna tıklayın
3. **"Abonelik ekle"** seçin
4. Link yapıştırın ve kaydedin
5. Abonelik kartına tıklayarak güncelleyin

**Hiddify (Android/iOS/Desktop):**
1. Uygulamayı açın
2. **"Profil ekle"** butonuna tıklayın
3. **"Abonelik URL'sinden ekle"** seçin
4. Linki yapıştırın
5. Otomatik olarak tüm sunucular eklenecek

**Avantajları:**
- ✅ Tek linkle tüm protokoller (VLESS + VMess)
- ✅ Kullanıcı silinince otomatik devre dışı
- ✅ Kota bitince otomatik engelleme
- ✅ Sunucu değişikliğinde yeniden kurulum gerekmez

### 🤖 Telegram Bot Kullanımı

BotFather'dan oluşturduğunuz bota mesaj atarak paneli yönetebilirsiniz.

**Mevcut Komutlar:**

```
/start - Bot hakkında bilgi ve komut listesi
/add <kullanıcı_adı> <kota_gb> - Yeni kullanıcı ekle
/delete <kullanıcı_adı> - Kullanıcı sil
/list - Tüm kullanıcıları listele
/status - Sistem durumu (kullanıcı sayısı, trafik)
/sub <kullanıcı_adı> - Abonelik linkini al
```

**Örnek Kullanım:**

```
/add ahmet 50
→ 50 GB kotalı "ahmet" kullanıcısı oluşturur

/list
→ Tüm kullanıcıları ve kota durumlarını gösterir

/sub ahmet
→ Ahmet'in abonelik linkini gönderir

/delete ahmet
→ Ahmet kullanıcısını siler
```

**Güvenlik:** Bot sadece `.env` dosyasında tanımlı admin ID'lerine yanıt verir. Yetkisiz kullanıcılar botu kullanamaz.

### 📊 Canlı Trafik İzleme

Dashboard'da **her 10 saniyede bir** otomatik olarak güncellenen trafik verileri:

- **Toplam Kullanıcı:** Sistemdeki tüm kullanıcı sayısı
- **Aktif Bağlantı:** Kota aşmamış kullanıcılar
- **Toplam Trafik:** Tüm kullanıcıların harcadığı veri
- **Son Güncelleme:** Trafik verisinin en son ne zaman güncellendiği

Xray access log dosyası (`/var/log/xray/access.log`) her 5 dakikada bir parse edilerek veritabanı güncellenir.

### İstemci Ayarları (Manuel Kurulum)

Abonelik linki kullanmıyorsanız, manuel olarak da bağlanabilirsiniz:

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
- ✅ Düzenli yedekleme alın (`/opt/pho3nix-panel/pho3nix_panel.db`)
- ✅ Telegram bot admin ID'lerini güvenli tutun

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
| GET | `/api/traffic/live` | Canlı trafik verilerini al |
| GET | `/api/config` | Sunucu konfigürasyonunu al |
| GET | `/sub/{username}` | Abonelik linki (base64 encoded) |

### API Örnekleri

```bash
# Kullanıcıları listele
curl http://localhost:8000/api/users

# Yeni kullanıcı ekle
curl -X POST "http://localhost:8000/api/users?username=ahmet&quota_gb=50"

# Kullanıcı sil
curl -X DELETE http://localhost:8000/api/users/1

# Canlı trafik verisi al
curl http://localhost:8000/api/traffic/live

# Abonelik linkini al (v2rayNG için)
curl http://localhost:8000/sub/ahmet

# Sunucu bilgilerini al
curl http://localhost:8000/api/config
```

## 🔧 Dosya Yapısı

```
/opt/pho3nix-panel/
├── requirements.txt      # Python bağımlılıkları
├── install.sh            # Otomatik kurulum betiği
├── database.py           # SQLAlchemy ORM
├── xray_manager.py       # Xray config yönetimi
├── main.py               # FastAPI uygulaması
├── telegram_bot.py       # Telegram bot entegrasyonu
├── pho3nix_panel.db      # SQLite veritabanı
├── .env                  # Reality ve Telegram anahtarları (GİZLİ)
├── venv/                 # Python sanal ortamı
└── templates/
    └── index.html        # Web arayüzü

/etc/xray/
└── config.json           # Xray-Core konfigürasyonu (otomatik üretilir)

/var/log/xray/
├── access.log            # Xray erişim logları (trafik izleme için)
└── error.log             # Xray hata logları
```

## 🐛 Sorun Giderme

### Panel açılmıyor

```bash
# Servis durumunu kontrol edin
sudo systemctl status pho3nix-panel

# Logları inceleyin
sudo journalctl -u pho3nix-panel -f
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

### Telegram bot çalışmıyor

```bash
# Bot servis durumu
sudo systemctl status pho3nix-bot

# Bot logları
sudo journalctl -u pho3nix-bot -f

# .env dosyasını kontrol edin
cat /opt/pho3nix-panel/.env | grep TELEGRAM
```

**Sık karşılaşılan bot sorunları:**
- ❌ Bot token yanlış → BotFather'dan yeni token alın
- ❌ Admin ID yanlış → [@userinfobot](https://t.me/userinfobot) ile ID'nizi öğrenin
- ❌ Bot yanıt vermiyor → `/start` komutu ile başlayın

### Kullanıcılar bağlanamıyor

1. Reality Public Key'in doğru olduğundan emin olun
2. Firewall portlarının açık olduğunu kontrol edin
3. SNI değerini kontrol edin (www.microsoft.com)
4. UUID'nin doğru kopyalandığından emin olun
5. Abonelik linkini tekrar güncelleyin

### Kota aşıldı ama kullanıcı hala bağlı

```bash
# Manuel olarak config'i yenileyin
cd /opt/pho3nix-panel
sudo source venv/bin/activate
python -c "import database, xray_manager; db = next(database.get_db()); xray_manager.apply_config(db)"
```

### Trafik verisi güncellenmiyor

```bash
# Access log dosyasını kontrol edin
sudo tail -f /var/log/xray/access.log

# Manuel trafik güncelleme tetikle
curl http://localhost:8000/api/traffic/live
```

## 📊 Veritabanı Yedekleme

```bash
# Manuel yedekleme
cp /opt/pho3nix-panel/pho3nix_panel.db /opt/pho3nix-panel/backups/backup-$(date +%Y%m%d).db

# Otomatik yedekleme (crontab)
crontab -e
# Her gün saat 03:00'te yedekle
0 3 * * * cp /opt/pho3nix-panel/pho3nix_panel.db /opt/pho3nix-panel/backups/backup-$(date +\%Y\%m\%d).db
```

## 📝 Değişiklik Günlüğü

### v1.1.0 (2026-07-04)
- ✨ **Abonelik Sistemi** - Tek linkle tüm protokoller
- 🤖 **Telegram Bot** - Mobilden tam yönetim
- 📊 **Canlı Trafik İzleme** - Gerçek zamanlı kullanım takibi
- 🎨 Dashboard'a "Son Güncelleme" kartı eklendi
- 📝 TrafficLog tablosu eklendi (detaylı trafik kayıtları)

### v1.0.0 (2026-07-04)
- ✨ İlk sürüm
- 🎉 VLESS + Reality desteği
- 🎉 VMess + WebSocket desteği
- 🎉 Web arayüzü
- 🎉 Kullanıcı ve kota yönetimi
- 🎉 QR kod ve bağlantı linki üretimi

Detaylı değişiklik günlüğü için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request açabilirsiniz.

### Geliştirme Ortamı

```bash
git clone https://github.com/memobeys3/pho3nix-panel.git
cd pho3nix-panel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## ⚠️ Sorumluluk Reddi

Bu yazılım yalnızca eğitim ve araştırma amaçlıdır. Kullanıcılar yerel yasalara uymakla yükümlüdür. Geliştiriciler, bu yazılımın kullanımından doğabilecek herhangi bir yasal sorumluğu kabul etmez.

## 🙏 Teşekkürler

- [Xray-Core](https://github.com/XTLS/Xray-core) - Güçlü proxy çekirdeği
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram bot framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [QRCode.js](https://github.com/davidshimjs/qrcodejs) - QR kod üretimi

## 📞 İletişim

- **Issues**: [GitHub Issues](https://github.com/memobeys3/pho3nix-panel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/memobeys3/pho3nix-panel/discussions)

## 🌟 Yıldız Geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=memobeys3/pho3nix-panel&type=Date)](https://star-history.com/#memobeys3/pho3nix-panel&Date)

---

<p align="center">
  <strong>Made with ❤️ by memobeys3</strong><br>
  <sub>Eğer bu proje işinize yaradıysa ⭐ vermeyi unutmayın!</sub>
</p>
