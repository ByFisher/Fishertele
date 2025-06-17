from telethon import TelegramClient, functions, types
import asyncio
import os
import json
import sys
from collections import Counter

# Yapılandırma dosyası
CONFIG_FILE = "telegram_config.json"

# Varsayılan yapılandırma
DEFAULT_CONFIG = {
    "api_id": "",
    "api_hash": "",
    "message_limit": 1000,
    "user_limit": 20
}

def clear_screen():
    """Terminali temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Program başlığını gösterir"""
    clear_screen()
    print("=" * 50)
    print("TELEGRAM GRUP AKTİVİTE ANALİZİ".center(50))
    print("=" * 50)
    print()

def load_config():
    """Yapılandırma dosyasını yükler, yoksa varsayılanı kullanır"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Yapılandırmayı dosyaya kaydeder"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

async def get_active_users(group_name, config):
    """Gruptaki en aktif kullanıcıları bulur"""
    # Yapılandırmadan değerleri al
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    message_limit = config["message_limit"]
    user_limit = config["user_limit"]
    
    # API bilgileri kontrol et
    if not api_id or not api_hash:
        print("API bilgileri eksik! Lütfen önce yapılandırmayı tamamlayın.")
        return None
    
    # Oturum dosyası
    session_file = 'telegram_session'
    
    # TelegramClient oluştur
    client = TelegramClient(session_file, api_id, api_hash)
    
    try:
        # Bağlantı kur
        await client.start()
        
        if not await client.is_user_authorized():
            print("\nLütfen Telegram hesabınıza giriş yapın")
            phone = input("Telefon numaranızı girin (ülke kodu ile, örn: +90...): ")
            await client.send_code_request(phone)
            await client.sign_in(phone, input("Telegram'dan gelen kodu girin: "))
        
        # Grup bilgisini al
        try:
            entity = await client.get_entity(group_name)
        except ValueError:
            print(f"\nHata: '{group_name}' grubu bulunamadı. Gruba üye olduğunuzdan emin olun.")
            return None
        
        print(f"\n'{entity.title}' grubundaki mesajlar analiz ediliyor...")
        print(f"Son {message_limit} mesaj inceleniyor...")
        
        # Mesajları al
        messages = await client.get_messages(entity, limit=message_limit)
        
        # Mesaj gönderenleri say
        user_activity = Counter()
        
        for message in messages:
            if message.sender_id:
                user_activity[message.sender_id] += 1
        
        # En aktif kullanıcıları bul
        most_active = user_activity.most_common(user_limit)
        
        if not most_active:
            print("Hiç mesaj bulunamadı!")
            return None
        
        # Kullanıcı bilgilerini al
        print(f"En aktif {user_limit} kullanıcı tespit ediliyor...")
        active_users = []
        for user_id, count in most_active:
            try:
                user = await client.get_entity(user_id)
                username = user.username if user.username else f"Kullanıcı ID: {user_id}"
                active_users.append((username, count))
            except Exception as e:
                print(f"Kullanıcı bilgisi alınamadı (ID: {user_id}): {e}")
        
        return active_users
        
    finally:
        await client.disconnect()

async def analyze_group():
    """Grup analizi yapar"""
    print_header()
    config = load_config()
    
    group_name = input("Telegram grup adını veya bağlantısını girin: ")
    if not group_name:
        print("Grup adı boş olamaz!")
        input("\nDevam etmek için ENTER tuşuna basın...")
        return
    
    try:
        active_users = await get_active_users(group_name, config)
        
        if active_users:
            # Dosya adını sor
            default_filename = "aktif_kullanicilar.txt"
            filename = input(f"Sonuçların kaydedileceği dosya adı [{default_filename}]: ")
            if not filename:
                filename = default_filename
            
            # Sonuçları txt dosyasına kaydet
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Grup: {group_name} - En Aktif {config['user_limit']} Kullanıcı\n")
                file.write("-" * 50 + "\n")
                
                for i, (username, count) in enumerate(active_users, 1):
                    file.write(f"{i}. @{username} - {count} mesaj\n")
            
            print(f"\nAktif kullanıcılar '{filename}' dosyasına kaydedildi.")
            
            # Sonuçları ekranda göster
            print("\nEn aktif kullanıcılar:")
            print("-" * 30)
            for i, (username, count) in enumerate(active_users, 1):
                print(f"{i}. @{username} - {count} mesaj")
        
    except Exception as e:
        print(f"\nHata oluştu: {e}")
    
    input("\nDevam etmek için ENTER tuşuna basın...")

def configure_settings():
    """Yapılandırma ayarlarını düzenler"""
    config = load_config()
    
    while True:
        print_header()
        print("YAPILANDIRMA AYARLARI")
        print("-" * 50)
        print(f"1. API ID: {'*****' if config['api_id'] else 'Ayarlanmamış'}")
        print(f"2. API Hash: {'*****' if config['api_hash'] else 'Ayarlanmamış'}")
        print(f"3. İncelenecek mesaj sayısı: {config['message_limit']}")
        print(f"4. Listelenecek kullanıcı sayısı: {config['user_limit']}")
        print("5. Kaydet ve çık")
        print()
        
        choice = input("Seçiminiz (1-5): ")
        
        if choice == '1':
            config['api_id'] = input("API ID girin (https://my.telegram.org adresinden alabilirsiniz): ")
        elif choice == '2':
            config['api_hash'] = input("API Hash girin (https://my.telegram.org adresinden alabilirsiniz): ")
        elif choice == '3':
            try:
                limit = int(input(f"İncelenecek mesaj sayısı [{config['message_limit']}]: "))
                if limit > 0:
                    config['message_limit'] = limit
            except ValueError:
                print("Geçersiz değer! Sayı girmelisiniz.")
                input("Devam etmek için ENTER tuşuna basın...")
        elif choice == '4':
            try:
                limit = int(input(f"Listelenecek kullanıcı sayısı [{config['user_limit']}]: "))
                if limit > 0:
                    config['user_limit'] = limit
            except ValueError:
                print("Geçersiz değer! Sayı girmelisiniz.")
                input("Devam etmek için ENTER tuşuna basın...")
        elif choice == '5':
            save_config(config)
            print("Ayarlar kaydedildi!")
            break
        else:
            print("Geçersiz seçim!")
            input("Devam etmek için ENTER tuşuna basın...")

async def main_menu():
    """Ana menüyü gösterir"""
    while True:
        print_header()
        print("ANA MENÜ")
        print("-" * 50)
        print("1. Grup Analizi Yap")
        print("2. Ayarları Yapılandır")
        print("3. Çıkış")
        print()
        
        choice = input("Seçiminiz (1-3): ")
        
        if choice == '1':
            await analyze_group()
        elif choice == '2':
            configure_settings()
        elif choice == '3':
            print("\nProgram kapatılıyor...")
            break
        else:
            print("Geçersiz seçim!")
            input("Devam etmek için ENTER tuşuna basın...")

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"\nBeklenmeyen bir hata oluştu: {e}")
        input("Çıkmak için ENTER tuşuna basın...")