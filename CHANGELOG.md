# Değişiklik Günlüğü

Bu projenin tüm önemli değişiklikleri bu dosyada belgelenmiştir.

Format [Keep a Changelog](https://keepachangelog.com/) standardına dayanmaktadır.

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

[1.0.0]: https://github.com/username/xray-panel/releases/tag/v1.0.0
[0.1.0]: https://github.com/username/xray-panel/releases/tag/v0.1.0
