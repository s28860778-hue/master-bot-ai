import os
import io
import time
import base64
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

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

print("MASTER BOT AI IS RUNNING...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨ *স্বাগতম! আমি Master Bot AI* ✨\n\n"
        "📊 আপনার যেকোনো ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট এখানে পাঠান।\n"
        "🔍 আমি ক্যান্ডেলস্টিক প্যাটার্ন ও সাপোর্ট-রেজিস্ট্যান্স বিশ্লেষণ করে আপনাকে সিগন্যাল দেব।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    wait_msg = (
        "⚡✨ *চার্ট স্ক্যানিং শুরু হয়েছে...* ✨⚡\n\n"
        "🔮 AI ক্যান্ডেল ও সাপোর্ট-রেজিস্ট্যান্স মাপছে...\n"
        "⏳ দয়া করে কয়েক সেকেন্ড অপেক্ষা করুন..."
    )
    bot.reply_to(message, wait_msg, parse_mode='Markdown')
    try:
        largest_photo = message.photo[-1]
        file_info = bot.get_file(largest_photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        img = Image.open(io.BytesIO(downloaded_file))
        img.thumbnail((900, 900))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        trading_prompt = """
তুমি একজন অভিজ্ঞ প্রো-লেভেলের প্রাইস-অ্যাকশন এবং ক্যান্ডেলস্টিক চার্ট অ্যানালিস্ট।
প্রদত্ত চার্টের স্ক্রিনশটটি অত্যন্ত সূক্ষ্মভাবে পর্যবেক্ষণ করো। কোনো অনুমান বা ভুয়া তথ্য দেবে না।

অ্যানালাইসিস করার নিয়মাবলি:
১. চার্টের বর্তমান ওভারঅল ট্রেন্ড এবং বায়ার-সেলারদের প্রকৃত শক্তি বিশ্লেষণ করো।
২. মার্কেট যদি অতিরিক্ত অস্থির বা অস্পষ্ট হয়, তবে স্পষ্টভাবে 'HOLD / NO TRADE' সাজেস্ট করো।

সবকিছু বিশ্লেষণ করে কেবল মাত্র নিচের ফরম্যাটে উত্তর দাও:

⚡ *MASTER BOT AI SIGNAL* ⚡

🎯 *সিগন্যাল:* *[BUY / CALL অথবা SELL / PUT অথবা HOLD / NO TRADE]*
📊 *অ্যাকুরেসি:* *[সম্ভাব্যতা শতাংশ লেখো, যেমন: ৮৫%]*
⏱️ *মার্কেট টাইম:* *[চার্টের টাইমফ্রেম বুঝে লেখো, যেমন: ১-৩ মিনিট]*

🔍 *AI চার্ট অ্যানালাইসিস:*
> [চার্টের ট্রেন্ড, ক্যান্ডেল রিজেকশন এবং সাপোর্ট-রেজিস্ট্যান্স লেভেলের ওপর ভিত্তি করে ২-৩ লাইনের সংক্ষিপ্ত ব্যাখ্যা]

⚠️ _বিঃদ্রঃ নিজস্ব ঝুঁকি ব্যবস্থাপনা (Risk Management) মেনে ট্রেড করুন।_
"""

        models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
        reply_text = None
        last_error = ""

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

        for model_name in models:
            try:
                api_url = f"https://googleapis.com{model_name}:generateContent"
                res = requests.post(api_url, headers=headers, json=data, timeout=30)
                res_json = res.json()

                if "candidates" in res_json and len(res_json["candidates"]) > 0:
                    candidate = res_json["candidates"][0]
                    parts = candidate.get("content", {}).get("parts", [])
                    if len(parts) > 0 and "text" in parts[0]:
                        reply_text = parts[0]["text"]
                        break
                else:
                    last_error = res_json.get("error", {}).get("message", str(res_json))
                    time.sleep(1)
            except Exception as req_err:
                last_error = str(req_err)
                time.sleep(1)

        if reply_text:
            bot.reply_to(message, reply_text, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"⚠️ *সতর্কতা: API এরর!*\nকারণ: `{last_error}`", parse_mode='Markdown')

    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, f"⚠️ *সতর্কতা: চার্টটি অ্যানালাইসিস করা সম্ভব হয়নি!*\nকারণ: `{e}`", parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
