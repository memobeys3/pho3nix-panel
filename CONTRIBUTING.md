# 🤝 Katkıda Bulunma Rehberi

Xray Panel'e katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, katkı sürecini kolaylaştırmak için hazırlanmıştır.

## 📋 İçindekiler

- [Nasıl Katkıda Bulunabilirim?](#nasıl-katkıda-bulunabilirim)
- [Geliştirme Ortamı](#geliştirme-ortamı)
- [Kod Standartları](#kod-standartları)
- [Pull Request Süreci](#pull-request-süreci)
- [Hata Raporlama](#hata-raporlama)
- [Özellik Önerileri](#özellik-önerileri)

## Nasıl Katkıda Bulunabilirim?

1. **Hata düzeltmeleri**: Bulduğunuz hataları düzeltin
2. **Yeni özellikler**: Projeye yeni özellikler ekleyin
3. **Dokümantasyon**: README ve kod yorumlarını iyileştirin
4. **Test yazımı**: Test coverage'ı artırın
5. **Çeviri**: Dokümantasyonu diğer dillere çevirin

## Geliştirme Ortamı

### 1. Repository'yi forklayın ve klonlayın

```bash
git clone https://github.com/username/xray-panel.git
cd xray-panel
```

### 2. Sanal ortam oluşturun

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. Geliştirme modunda çalıştırın

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Kod Standartları

### Python

- **PEP 8** standartlarına uyun
- Type hints kullanın
- Docstring'ler yazın (Google style)
- Fonksiyonlar tek bir iş yapmalı

```python
# ✅ İyi
def add_user(username: str, quota_gb: float, db: Session) -> User:
    """
    Yeni kullanıcı ekler.
    
    Args:
        username: Kullanıcı adı
        quota_gb: Kota (GB cinsinden, 0 sınırsız)
        db: Veritabanı session'ı
    
    Returns:
        User: Oluşturulan kullanıcı objesi
    
    Raises:
        HTTPException: Kullanıcı adı zaten varsa
    """
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=username, quota_bytes=int(quota_gb * 1024**3))
    db.add(new_user)
    db.commit()
    return new_user

# ❌ Kötü
def adduser(u, q, d):
    e = d.query(User).filter(User.username == u).first()
    if e:
        raise HTTPException(status_code=400, detail="Username already exists")
    n = User(username=u, quota_bytes=int(q * 1024**3))
    d.add(n)
    d.commit()
    return n
```

### JavaScript

- Modern ES6+ syntax kullanın
- Async/await tercih edin
- Hata yönetimi yapın

```javascript
// ✅ İyi
async function fetchUsers() {
    try {
        const response = await fetch('/api/users');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json();
        return users;
    } catch (error) {
        console.error('Failed to fetch users:', error);
        throw error;
    }
}

// ❌ Kötü
function fetchUsers() {
    fetch('/api/users').then(r => r.json()).then(u => u);
}
```

### HTML/CSS

- Tailwind CSS kullanın
- Semantic HTML yazın
- Accessibility (a11y) standartlarına uyun

## Pull Request Süreci

### 1. Branch oluşturun

```bash
git checkout -b feature/yenil-ozellik
# veya
git checkout -b fix/hata-duzeltme
```

### 2. Değişikliklerinizi yapın

- Kod standartlarına uyun
- Test yazın (mümkünse)
- Dokümantasyon güncelleyin

### 3. Commit mesajları

```bash
# ✅ İyi
git commit -m "feat: add user quota management"
git commit -m "fix: correct traffic calculation bug"
git commit -m "docs: update README with installation steps"

# ❌ Kötü
git commit -m "update"
git commit -m "fix stuff"
```

**Commit tipi önekleri:**
- `feat:` Yeni özellik
- `fix:` Hata düzeltmesi
- `docs:` Dokümantasyon değişikliği
- `style:` Kod formatı (mantık değişikliği yok)
- `refactor:` Kod yeniden düzenleme
- `test:` Test ekleme/düzeltme
- `chore:` Bakım işleri

### 4. Push ve PR oluşturun

```bash
git push origin feature/yeni-ozellik
```

GitHub'da Pull Request oluşturun ve şunları ekleyin:

- **Ne değiştirdiniz?** (kısa açıklama)
- **Neden değiştirdiniz?** (problem/özellik açıklaması)
- **Nasıl test ettiniz?** (test adımları)
- **Ekran görüntüleri** (UI değişikliği varsa)

### 5. Code Review

- Reviewer yorumlarını bekleyin
- Gerekli değişiklikleri yapın
- Onay aldıktan sonra merge edilir

## Hata Raporlama

Hata bildirirken şunları ekleyin:

### Hata Şablonu

```markdown
**Hata Açıklaması**
Kısa ve net hata açıklaması.

**Tekrarlama Adımları**
1. '...' adımına git
2. '...' tıkla
3. '...' komutunu çalıştır
4. Hatayı gör

**Beklenen Davranış**
Ne olmasını bekliyordunuz?

**Gerçek Davranış**
Aslında ne oldu?

**Ekran Görüntüleri**
Mümkünse ekran görüntüsü ekleyin.

**Ortam Bilgileri**
- OS: [örn. Ubuntu 22.04]
- Python: [örn. 3.10.12]
- Xray-Core: [örn. 1.8.0]
- Tarayıcı: [örn. Chrome 120]

**Ek Bilgiler**
Başka bir bilgi varsa ekleyin.
```

## Özellik Önerileri

Yeni özellik önerirken:

1. **Problemi tanımlayın**: Bu özellik hangi problemi çözüyor?
2. **Kullanım senaryosu**: Nasıl kullanılacak?
3. **Alternatifler**: Başka çözümler var mı?
4. **Ek bilgiler**: Mockup, diagram, referanslar

## 📜 Lisans

Katkılarınız MIT lisansı altında lisanslanacaktır. Katkıda bulunarak, katkılarınızın bu lisans altında dağıtılmasını kabul etmiş olursunuz.

## ❓ Sorularınız mı var?

- Issue açın
- Tartışma (Discussion) başlatın
- Kod yorumlarında sorun

---

**Katkılarınız için teşekkürler! 🎉**
