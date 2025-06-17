# Telegram Grup Aktivite Analizi

Bu proje, Telegram gruplarındaki en aktif kullanıcıları tespit eden ve kullanıcı adlarını bir metin dosyasına kaydeden basit bir Python uygulamasıdır.

## Özellikler

- Belirtilen Telegram grubundaki mesajları analiz eder
- En aktif kullanıcıları tespit eder ve sıralar
- Sonuçları hem ekranda gösterir hem de metin dosyasına kaydeder
- Kullanıcı dostu terminal arayüzü
- Özelleştirilebilir yapılandırma ayarları:
  - İncelenecek mesaj sayısı
  - Listelenecek kullanıcı sayısı

## Ekran Görüntüleri

tele.avif

## Kurulum

1. Projeyi klonlayın:
```
git clone https://github.com/kullaniciadi/telegram-grup-analizi.git
cd telegram-grup-analizi
```

2. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```

3. Telegram API bilgilerinizi alın:
   - https://my.telegram.org adresine gidin
   - Giriş yapın ve "API Development tools" bölümüne gidin
   - Yeni bir uygulama oluşturun ve API ID ve API Hash bilgilerinizi alın

## Kullanım

1. Programı çalıştırın:
```
python telegram_active_users.py
```

2. İlk kullanımda "Ayarları Yapılandır" seçeneğini seçerek API bilgilerinizi girin

3. "Grup Analizi Yap" seçeneğini seçin ve analiz etmek istediğiniz grubun adını veya bağlantısını girin

4. Program analizi tamamladıktan sonra sonuçları hem ekranda gösterecek hem de bir metin dosyasına kaydedecektir

## Teknik Detaylar

- Telethon kütüphanesi kullanılarak Telegram API ile iletişim kurulur
- Asenkron programlama ile verimli çalışma sağlanır
- Yapılandırma ayarları JSON dosyasında saklanır
- Kullanıcı oturum bilgileri yerel olarak saklanır

## Gereksinimler

- Python 3.6 veya üzeri
- Telethon 1.28.5

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Sorularınız veya önerileriniz için GitHub üzerinden issue açabilir veya pull request gönderebilirsiniz.
