import telebot
import requests
import os
import time
import re

# Ambil token dari environment
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(TOKEN)

# ID grup yang diizinkan (opsional)
ALLOWED_GROUPS = os.environ.get("ALLOWED_GROUPS", "").split(",") if os.environ.get("ALLOWED_GROUPS") else None

# Kata terlarang (bisa ditambah)
BANNED_WORDS = ["spam", "scam", "judi", "porn", "bokep", "narkoba"]

@bot.message_handler(commands=['start'])
def sambutan(message):
    bot.reply_to(message, "🤖 *Bot Aktif!*\n\nSaya akan merespon otomatis di grup.\n\n📌 *Cara pakai:*\n• Mention: `@namabotmu pesan`\n• Reply ke pesan bot\n• /help untuk bantuan", parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def bantuan(message):
    bot.reply_to(message, """📖 *Panduan Bot*

🔹 *Perintah:*
• /start - Mulai bot
• /help - Bantuan ini
• /ping - Cek status

🔹 *Fitur:*
✅ Auto reply di grup & chat pribadi
✅ AI cerdas (Groq)
✅ Anti spam sederhana
✅ Khusus grup teknis

📌 *Cara pakai di grup:*
• Mention bot: `@namabotmu pertanyaan`
• Reply ke pesan bot: balas pesan bot

⚠️ *Kata terlarang:* spam, scam, judi, porn, bokep, narkoba
""", parse_mode="Markdown")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot aktif ✅")

# Cek kata terlarang
def contains_banned_words(text):
    if not text:
        return False
    text_lower = text.lower()
    for word in BANNED_WORDS:
        if word in text_lower:
            return True
    return False

# Fungsi auto reply
@bot.message_handler(func=lambda m: True)
def auto_reply(message):
    # Skip jika pesan kosong
    if not message.text:
        return
    
    # Cek izin grup (jika diatur)
    if ALLOWED_GROUPS and message.chat.type in ["group", "supergroup"]:
        if str(message.chat.id) not in ALLOWED_GROUPS:
            return
    
    # Cek kata terlarang
    if contains_banned_words(message.text):
        bot.reply_to(message, "⚠️ *Pesan Anda mengandung kata yang tidak diperbolehkan!*", parse_mode="Markdown")
        return
    
    # Di grup: hanya respon jika mention atau reply ke bot
    if message.chat.type in ["group", "supergroup"]:
        bot_username = bot.get_me().username
        # Cek mention @bot
        if f"@{bot_username}" not in message.text:
            # Cek reply ke pesan bot
            if not (message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id):
                return  # Abaikan
    
    # Indikator "sedang mengetik"
    bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # Panggil API Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # System prompt khusus teknis
        system_prompt = """Kamu adalah asisten AI untuk grup Telegram bertema teknis (Android modding, OpenWRT, Magisk, flashing ROM, custom ROM, root, dll). 

Aturan:
1. Jawab dengan bahasa Indonesia yang santai, jelas, dan akurat
2. Jika tidak tahu, katakan 'Saya belum tahu' jangan ngasal
3. Untuk pertanyaan non-teknis, jawab ramah tapi singkat
4. Jangan memberikan saran berbahaya (brick HP, dll)
5. Gunakan emoticon yang sesuai biar lebih friendly"""
        
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            jawaban = response.json()["choices"][0]["message"]["content"]
            # Batasi panjang
            if len(jawaban) > 4000:
                jawaban = jawaban[:4000] + "...\n\n📌 *Pesan dipotong karena terlalu panjang*"
            bot.reply_to(message, jawaban, parse_mode="Markdown")
        else:
            bot.reply_to(message, f"⚠️ *AI error.* Kode: {response.status_code}\nCoba lagi nanti.", parse_mode="Markdown")
            
    except requests.exceptions.Timeout:
        bot.reply_to(message, "⏰ *AI terlalu lama merespon.* Coba lagi nanti.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ *Error:* `{str(e)}`", parse_mode="Markdown")

# Jalankan bot
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 BOT AUTO REPLY TELEGRAM AKTIF!")
    print("=" * 50)
    print(f"✅ Bot: @{bot.get_me().username}")
    print(f"📱 Mode: Grup & Personal Chat")
    if ALLOWED_GROUPS:
        print(f"🔒 Hanya untuk grup: {ALLOWED_GROUPS}")
    else:
        print(f"🌍 Semua grup & chat pribadi diizinkan")
    print("=" * 50)
    print("🔄 Bot berjalan... Tekan Ctrl+C untuk berhenti")
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"⚠️ Error: {e}. Restart dalam 5 detik...")
            time.sleep(5)
