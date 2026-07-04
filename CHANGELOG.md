# Değişiklik Günlüğü

Bu projenin tüm önemli değişiklikleri bu dosyada belgelenmiştir.

Format [Keep a Changelog](https://keepachangelog.com/) standardına dayanmaktadır.

## [1.1.0] - 2026-07-04

### Eklenenler
- ✨ **Abonelik Sistemi** (`/sub/{username}` endpoint'i)
  - Base64 encoded çoklu protokol desteği (VLESS + VMess)
  - v2rayNG, Streisand, Hiddify uygulamalarıyla tam uyumlu
  - Kullanıcı silinince otomatik devre dışı
  - Kota bitince otomatik engelleme
  - Custom HTTP header'lar (X-Sub-User, X-Sub-Quota, X-Sub-Used)

- 🤖 **Telegram Bot Entegrasyonu**
  - `/start` - Bot hakkında bilgi
  - `/add <isim> <kota>` - Kullanıcı ekleme
  - `/delete <isim>` - Kullanıcı silme
  - `/list` - Tüm kullanıcıları listeleme
  - `/status` - Sistem durumu görüntüleme
  - `/sub <isim>` - Abonelik linki alma
  - Admin ID tabanlı yetkilendirme
  - Systemd servisi olarak otomatik başlatma

- 📊 **Canlı Trafik İzleme**
  - Xray access log parsing (`/var/log/xray/access.log`)
  - `/api/traffic/live` endpoint'i
  - Her 5 dakikada otomatik trafik güncelleme (APScheduler)
  - Dashboard'da 10 saniyede bir canlı yenileme
  - TrafficLog tablosu (detaylı trafik kayıtları)
  - Son güncelleme zamanı gösterimi

- 🎨 **Dashboard İyileştirmeleri**
  - "Son Güncelleme" istatistik kartı
  - Canlı izleme göstergesi (yeşil nokta animasyonu)
  - Mor tema vurguları
  - Türkçe arayüz

### Değişenler
- `requirements.txt` güncellendi:
  - `python-telegram-bot==20.7` eklendi
  - `httpx==0.27.0` eklendi
  - `apscheduler==3.10.4` eklendi
  - `python-multipart==0.0.9` eklendi
  - `base58==2.1.1` eklendi

- `database.py` güncellendi:
  - `TrafficLog` tablosu eklendi
  - `User.last_traffic_update` alanı eklendi

- `xray_manager.py` güncellendi:
  - `parse_traffic_from_logs()` fonksiyonu eklendi
  - Xray config'e `stats` ve `log` bölümleri eklendi
  - Access log parsing ve kota kontrolü

- `main.py` güncellendi:
  - `/api/traffic/live` endpoint eklendi
  - `/sub/{username}` endpoint eklendi
  - APScheduler ile periyodik trafik güncelleme
  - Background task yönetimi

- `install.sh` güncellendi:
  - Telegram bot kurulum seçeneği eklendi
  - `/var/log/xray/` dizini oluşturma
  - `pho3nix-bot.service` systemd servisi

### Teknik Detaylar
- FastAPI lifespan event'leri ile scheduler yönetimi
- SQLAlchemy session yönetimi iyileştirildi
- Telegram bot async/await pattern'leri
- Base64 encoding/decoding for subscription links
- Regex-based log parsing

### Güvenlik
- Telegram bot admin ID doğrulaması
- Access log dosyası otomatik temizleme
- Kota aşımında otomatik kullanıcı engelleme

## [1.0.0] - 2026-07-04

### Eklenenler
- İlk kararlı sürüm
- VLESS + Reality protokol desteği
- VMess + WebSocket protokol desteği
- Web tabanlı kullanıcı yönetim arayüzü
- SQLite veritabanı entegrasyonu
- Otomatik kullanıcı ekleme/silme
- Kota yönetimi (GB bazlı)
- Trafik kullanımı takibi
- Otomatik QR kod üretimi
- vless:// bağlantı linki üretimi
- vmess:// bağlantı linki üretimi
- Karanlık tema (Dark Mode) arayüz
- Otomatik X25519 anahtar çifti üretimi
- Systemd servis entegrasyonu
- FastAPI tabanlı REST API
- Tailwind CSS ile modern UI
- Responsive tasarım (mobil uyumlu)
- Otomatik kurulum betiği (install.sh)
- API endpoint'leri:
  - GET /api/users - Kullanıcı listeleme
  - POST /api/users - Kullanıcı ekleme
  - DELETE /api/users/{id} - Kullanıcı silme
  - POST /api/traffic/update - Trafik güncelleme
  - GET /api/config - Sunucu konfigürasyonu

### Teknik Detaylar
- Python 3.8+ desteği
- FastAPI 0.111+
- SQLAlchemy 2.0+
- Uvicorn ASGI sunucusu
- Xray-Core 1.8+ entegrasyonu
- Jinja2 template engine
- QRCode.js kütüphanesi

### Güvenlik
- Reality protokolü ile gelişmiş gizlilik
- Otomatik anahtar üretimi
- Kota aşımında otomatik kullanıcı engelleme
- Temiz kod mimarisi

### Dokümantasyon
- Kapsamlı README.md
- Kurulum rehberi
- API dokümantasyonu
- Sorun giderme kılavuzu
- Katkıda bulunma rehberi
- MIT Lisansı

## [0.1.0] - 2026-06-20

### Eklenenler
- İlk geliştirme sürümü
- Temel Xray entegrasyonu
- Basit kullanıcı yönetimi
- CLI arayüzü

---

## Versiyonlama

Bu proje [Semantic Versioning](https://semver.org/) kullanmaktadır.

- **MAJOR** (X.0.0): Geriye uyumsuz API değişikliklikleri
- **MINOR** (0.X.0): Geriye uyumlu yeni özellikler
- **PATCH** (0.0.X): Geriye uyumlu hata düzeltmeleri

[1.1.0]: https://github.com/memobeys3/pho3nix-panel/releases/tag/v1.1.0
[1.0.0]: https://github.com/memobeys3/pho3nix-panel/releases/tag/v1.0.0
[0.1.0]: https://github.com/memobeys3/pho3nix-panel/releases/tag/v0.1.0
