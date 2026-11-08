import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# ১. সরাসরি টোকেন ও এপিআই কি কনফিগারেশন (১০০% নিখুঁত কানেকশন)
BOT_TOKEN = "9063727678:AAH5f6ivj7MXs-fd1AZjXg1N4LeKIxYrTRc"
GEMINI_API_KEY = "AQ.Ab8RN6JkZ3d9KKIqTIG0f4vlqJhdDtRU1jhzPniSLHsmz_lOMw"
RENDER_URL = "https://master-bot-ai.onrender.com"

# বট ও জেমিনি এআই সক্রিয় করা
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# জেমিনি মডেল কনফিগারেশন
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "max_output_tokens": 1000,
}

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config=generation_config
)

app = Flask(__name__)

# @bot.message_handler(commands=['start', 'help'])
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **MASTER BOT AI v2.0 (PRO-UPGRADED)** 📊\n\n"
        "আমি এখন আগের চেয়ে **দ্বিগুণ শক্তিশালী এবং প্রাতিষ্ঠানিক মানের এআই অ্যানালাইটিক্স** প্রযুক্তিতে চালিত!\n\n"
        "আপনার যেকোনো ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট পাঠান। আমি সিগন্যাল প্রদান করব।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# চার্ট ইমেজ অ্যানালিসিস হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        # প্রসেসিং মেসেজ পাঠানো
        processing_msg = bot.reply_to(message, "⏳ **Master Bot AI আপনার চার্টটি গভীরভাবে অ্যানালাইসিস করছে...**")
        
        # ছবি ডাউনলোড করা
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # জেমিনির জন্য ইমেজ ডাটা ফরম্যাট করা
        image_data = {"mime_type": "image/jpeg", "data": downloaded_file}
        
        # জেমিনির জন্য প্রফেশনাল ট্রেডিং প্রম্পট (আপনার আগের স্টাইল অনুযায়ী)
        system_prompt = (
            "You are 'Master Bot AI Pro v2.0' - a chart analyst. Respond ONLY in Bengali:\n\n"
            "📈 **মার্কেট স্ট্রাকচার:** [Trend]\n"
            "🎯 **প্রাতিষ্ঠানিক এসএনডিআর জোন:** ডিমান্ড: [Price] | সাপ্লাই: [Price]\n"
            "⚡ **মাস্টার সিগন্যাল:** BUY/UP or SELL/DOWN (উইন রেট: [Probability]%)\n"
            "🛡️ **স্মার্ট রিস্ক ম্যানেজমেন্ট:** এন্ট্রি: [Price] | TP: [Price] | SL: [Price]\n"
            "🧠 **এডভান্সড ট্রেডিং লজিক:** [Provide 2 detailed sentences in Bengali explaining the chart movement]"
        )
        
        # জেমিনি এআই থেকে রেসপন্স জেনারেট করা
        response = model.generate_content([system_prompt, image_data])
        
        # আগের প্রসেসিং মেসেজটি ডিলিট করা
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        # অ্যানালিসিস রেজাল্ট টেলিগ্রামে পাঠানো
        bot.reply_to(message, response.text, parse_mode='Markdown')
        
    except Exception as e:
        # কোনো ত্রুটি হলে তা টেলিগ্রামে দেখানো
        bot.reply_to(message, f"❌ কারিগরি ত্রুটি! Error Details: {str(e)}")

# Webhook রুট সমূহ (আপনার আগের কোডের নিখুঁত রুট লজিক)
@app.route('/webhook', methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid Content-Type", 400

@app.route("/")
def webhook():
    bot.remove_webhook()
    base_url = RENDER_URL.strip().rstrip('/')
    clean_url = f"{base_url}/webhook"
    bot.set_webhook(url=clean_url)
    return f"🟢 Master Bot AI Pro v2.0 is Up and Running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
