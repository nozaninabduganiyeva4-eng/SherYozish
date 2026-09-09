# ✍️ She'r Yozuvchi AI Telegram Bot

Foydalanuvchi yuborgan istalgan so'z yoki mavzuga moslab qisqa, qofiyalangan va go'zal original o'zbekcha to'rtliklar to'qib beruvchi Telegram bot.

---

## ✨ Imkoniyatlari

- 🎯 **Ixtiyoriy mavzuda she'r to'qish:** Foydalanuvchi xohlagan so'zini yuborishi mumkin (*Ona, Bahor, Muhabbat, Dasturlash, Toshkent, Do'stlik...*).
- 🤖 **Zamonaviy AI (OpenAI GPT-4o-mini):** Adabiy o'zbek tilida, ritm va qofiyaga ega to'rtliklar yaratadi.
- 🔁 **«Yana boshqa she'r» tugmasi:** Bir xil mavzuda yangi variantlarni osongina qayta to'qish.
- ⚡ **Tezkor va asinxron:** Eng so'nggi `aiogram 3.x` kutubxonasiga asoslangan.
- 📱 **Tayyor mavzular:** Bahor, Muhabbat, Ona, Do'stlik, Vatan, Yomg'ir kabi tezkor tanlov tugmalari.

---

## 📁 Loyiha Strukturasi

```
SherYozish/
├── poem_bot.py           # Botning asosiy kodi
├── requirements.txt      # Kerakli Python kutubxonalari
├── .env.example          # Muhit o'zgaruvchilari namunasi
├── .gitignore            # Git uchun e'tiborsiz qoldiriladigan fayllar
├── start_bot.bat         # Windows uchun 1-bosishda ishga tushiruvchi fayl
└── README.md             # Loyiha qo'llanmasi
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Repozitoriyni yuklab olish (Clone)
```bash
git clone https://github.com/nozaninabduganiyeva4-eng/SherYozish.git
cd SherYozish
```

### 2. Virtual muhit yaratish va kutubxonalarni o'rnatish
```bash
# Virtual muhit yaratish
python -m venv venv

# Virtual muhitni faollashtirish (Windows):
.\venv\Scripts\activate

# Kutubxonalarni o'rnatish:
pip install -r requirements.txt
```

### 3. `.env` faylini sozlash
`.env.example` faylidan nusxa olib `.env` nomli fayl yarating:
```env
BOT_TOKEN=bu_yerga_bot_father_tokeningiz
OPENAI_API_KEY=bu_yerga_openai_api_kalitingiz
```

- **BOT_TOKEN**: [@BotFather](https://t.me/BotFather) dan olinadi.
- **OPENAI_API_KEY**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys) sahifasidan olinadi.

### 4. Botni ishga tushirish

**Windows foydalanuvchilari uchun:**
`start_bot.bat` fayliga ikki marta bosing.

**Terminal orqali:**
```bash
python poem_bot.py
```

---

## 🛠 Texnologiyalar
- **Python 3.10+**
- **aiogram 3.x**
- **OpenAI API (GPT-4o-mini)**
- **python-dotenv**
