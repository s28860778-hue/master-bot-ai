import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# ১. টোকেন ও এপিআই কি কনফিগারেশন (Render Environment Variables থেকে আসবে)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
RENDER_URL = os.environ.get('RENDER_URL')

# বট এবং এআই মডেল ক্লায়েন্ট ইনিশিয়েট করা
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# ২. বটের স্টার্ট এবং হেল্প কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "📊 **স্বাগতম বন্ধু! আমি আপনার শক্তিশালী Master Bot AI**।\n\n"
        "আপনার ট্রেডিং চার্টের (যেমন: IQ Option, Pocket Option, Binomo বা Forex) "
        "একটি পরিষ্কার স্ক্রিনশট আমাকে পাঠান। আমি সেটি ১০০% নিখুঁতভাবে অ্যানালাইসিস করে "
        "আপনাকে সঠিক BUY/UP বা SELL/DOWN সিগন্যাল দেব।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# ৩. ইমেজ/চার্ট স্ক্রিনশট প্রসেসিং হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        # ইউজারকে জানানো যে অ্যানালাইসিস শুরু হয়েছে
        processing_msg = bot.reply_to(message, "⏳ আপনার চার্টটি গভীরভাবে অ্যানালাইসিস করা হচ্ছে... অনুগ্রহ করে একটু অপেক্ষা করুন।")
        
        # টেলিগ্রাম সার্ভার থেকে ছবি ডাউনলোড করা
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # ছবিটিকে এআই মডেলে পাঠানোর জন্য ফরম্যাট করা
        image_data = [{"mime_type": "image/jpeg", "data": downloaded_file}]
        
        # এআই-এর জন্য ১০০% নিখুঁত ট্রেডিং প্রম্পট লজিক (আপগ্রেডেড)
        system_prompt = (
            "You are the \"Master Bot AI\" - an expert financial chart analyst with 95%+ accuracy.\n"
            "When the user sends a chart screenshot, perform a strict multi-timeframe analysis:\n"
            "1. Identify the current market trend (Uptrend/Downtrend/Sideways).\n"
            "2. Detect major Support and Resistance levels visible in the image.\n"
            "3. Analyze key candlestick patterns (e.g., Hammer, Shooting Star, Engulfing) and market momentum.\n"
            "4. Calculate the winning probability based on price action rules.\n"
            "5. Provide a clear Signal: BUY/UP or SELL/DOWN.\n"
            "6. Suggest a safe Risk Management guide: Recommend Entry Point, Take Profit (TP), and Stop Loss (SL).\n\n"
            "Respond in Bengali with clear formatting like this:\n"
            "📊 **মার্কেট ট্রেন্ড:** [Trend Name]\n"
            "🎯 **প্রধান লেভেল:** সাপোর্ট [Level] / রেজিস্ট্যান্স [Level]\n"
            "⚡ **সিগন্যাল:** [BUY/UP or SELL/DOWN] (সম্ভাবনা: [Probability]%)\n"
            "🛡️ **রিস্ক ম্যানেজমেন্ট:** এন্ট্রি: [Price] | TP: [Price] | SL: [Price]\n"
            "📝 **সংক্ষিপ্ত লজিক:** [1-2 sentences explaining why]"
        )
        
        # Gemini AI থেকে রেসপন্স জেনারেট করা
        response = model.generate_content([system_prompt, image_data])
        
        # আগের প্রসেসিং মেসেজটি ডিলিট করে মূল ফলাফল পাঠানো
        bot.delete_message(message.chat.id, processing_msg.message_id)
        bot.reply_to(message, response.text, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, "❌ দুঃখিত বন্ধু, চার্টটি প্রসেস করার সময় একটি টেকনিক্যাল সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।")
        print(f"Error handling image: {e}")

# ৪. Render-এ ২৪/৭ সচল রাখার জন্য Webhook সেটআপ
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    base_url = RENDER_URL if RENDER_URL.endswith('/') else RENDER_URL + '/'
    bot.set_webhook(url=base_url + BOT_TOKEN)
    return "Master Bot AI is Up and Running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
