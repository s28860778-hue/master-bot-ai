import os
import io
import base64
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from PIL import Image

# ১. তোমার আসল Gemini Auth Key (AQ. ফরম্যাট)
API_KEY = "AQ.Ab8RN6LXI4O8pk20QnFMamJQEP0A-9-zgaT6WaxcdJCxQqXKaw"

# ২. তোমার নতুন Telegram Token (@master_bot_ai_2026_bot)
TELEGRAM_TOKEN = "9063727678:AAG1Tj7cNmH4jUWHrfLvyfrKARmMhZIGDOg"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Render-এর Port Timeout সমস্যা সমাধানের জন্য ছোট ওয়েব সার্ভার
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Master Bot AI is Live!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

print("✨👑 MASTER BOT AI (ULTRA VIP SPARKLE EDITION) IS RUNNING...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨👑 *স্বাগতম! আমি 'Master Bot AI' (Ultra VIP)* 👑✨\n"
        "╔══════════════════════════╗\n"
        "📌 আপনার যেকোনো ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট এখানে পাঠান।\n"
        "🔍 আমি ক্যান্ডেলস্টিক প্যাটার্ন ও মার্কেট পাওয়ার গভীরভাবে স্ক্যান করে নির্ভুল বিশ্লেষণ দেব।\n"
        "╚══════════════════════════╝"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    wait_msg = (
        "⚡✨ *চার্ট স্ক্যানিং শুরু হয়েছে...* ✨⚡\n"
        "╔══════════════════════════╗\n"
        "🔍 AI ক্যান্ডেল ও সাপোর্ট-রেজিস্ট্যান্স মাপছে...\n"
        "⏳ দয়া করে মাত্র কয়েক সেকেন্ড অপেক্ষা করুন...\n"
        "╚══════════════════════════╝"
    )
    bot.reply_to(message, wait_msg, parse_mode='Markdown')

    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # দ্রুত প্রসেসিংয়ের জন্য ছবি অপ্টিমাইজ ও Base64 রূপান্তর
        img = Image.open(io.BytesIO(downloaded_file))
        img.thumbnail((1024, 1024))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        trading_prompt = """
তুমি একজন বিশ্বের সেরা প্রো-লেভেলের ফাইন্যান্সিয়াল মার্কেট এবং ক্যান্ডেলস্টিক চার্ট অ্যানালিস্ট।
প্রদত্ত চার্টের স্ক্রিনশটটি অত্যন্ত সূক্ষ্মভাবে পর্যবেক্ষণ করো। কোনো অনুমান বা ভুয়া তথ্য দেবে না।

অ্যানালাইসিস করার নিয়মাবলী:
১. চার্টের বর্তমান ওভারঅল ট্রেন্ড এবং বায়ার-সেলারদের প্রকৃত শক্তি বিশ্লেষণ করো।
২. মার্কেট যদি অতিরিক্ত অস্থির বা অস্পষ্ট হয়, তবে স্পষ্টভাবে 'HOLD / NO TRADE ⏸️' সাজেস্ট করো।

সবকিছু বিশ্লেষণ করে কোনো বাড়তি কথা না লিখে শুধুমাত্র নিচের হুবহু উজ্জ্বল ফরম্যাটে উত্তর দাও:

✨👑 *MASTER BOT AI • ULTRA VIP* 👑✨
╔══════════════════════════╗
🌟 *সিগন্যাল:* *[BUY / CALL 🟢⚡ অথবা SELL / PUT 🔴🔥 অথবা HOLD / NO TRADE ⏸️]*
💎 *অ্যাকুরেসি:* `[বাস্তবসম্মত শতাংশ লেখো, যেমন: ৯৪%]` `[শতাংশ অনুযায়ী বার দাও, যেমন: 🟩🟩🟩🟩⬜]`
🔥 *মার্কেট পাওয়ার:* `[চার্টের বর্তমান শক্তি লেখো, যেমন: অতি শক্তিশালী বায়ার চাপ / শক্তিশালী সেলার চাপ]`
╚══════════════════════════╝

🔮 *AI মার্কেট অ্যানালাইসিস:*
> [চার্টের ট্রেন্ড, ক্যান্ডেল রিজেকশন এবং সাপোর্ট-রেজিস্ট্যান্স লেভেলের ওপর ভিত্তি করে ২-৩ লাইনের সংক্ষিপ্ত ও নিখুঁত ব্যাখ্যা লেখো]

🛡️ _নিরাপদ ট্রেডিংয়ের জন্য মানি ম্যানেজমেন্ট অনুসরণ করুন।_
"""

        # সঠিক এবং সম্পূর্ণ REST API URL
        api_url = "https://googleapis.com"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }
        data = {
            "contents": [{
                "parts": [
                    {"text": trading_prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }]
        }

        res = requests.post(api_url, headers=headers, json=data, timeout=30)
        res_json = res.json()

        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            reply_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
            bot.reply_to(message, reply_text, parse_mode='Markdown')
        else:
            error_detail = res_json.get("error", {}).get("message", str(res_json))
            bot.reply_to(message, f"⚠️ *সতর্কতা: API এরর!*\nকারণ: `{error_detail}`", parse_mode='Markdown')

    except Exception as e:
        print("Error:", e)
        error_msg = (
            f"⚠️ *সতর্কতা: চার্টটি অ্যানালাইসিস করা সম্ভব হয়নি!*\n"
            f"কারণ: `{str(e)}`"
        )
        bot.reply_to(message, error_msg, parse_mode='Markdown')

if __name__ == "__main__":
    bot.polling(none_stop=True)
