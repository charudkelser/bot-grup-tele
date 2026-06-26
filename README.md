# 🤖 Bot Auto Reply Telegram

Bot Telegram dengan AI (Groq) untuk auto reply di grup.

## Fitur
- ✅ Auto reply di grup & chat pribadi
- ✅ AI cerdas dengan Groq
- ✅ Anti spam sederhana
- ✅ Khusus grup teknis (Android modding, OpenWRT, Magisk, dll)

## Cara Deploy
1. Clone repo ini
2. Install dependency: `pip install -r requirements.txt`
3. Set environment variables:
   - `TELEGRAM_TOKEN` = Token dari @BotFather
   - `GROQ_API_KEY` = API Key dari Groq
   - `ALLOWED_GROUPS` = ID grup (opsional)
4. Jalankan: `python bot.py`

## Cara Pakai di Grup
- Mention bot: `@namabotmu pertanyaan`
- Reply ke pesan bot

## License
MIT
