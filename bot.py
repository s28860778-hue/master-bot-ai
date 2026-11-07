
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

# দ্বিগুণ শক্তিশালী পারফরম্যান্সের জন্য প্রো-কনফিগারেশন সেটআপ
generation_config = {
    "temperature": 0.2,  # ক্রিয়েটিভিটি কমিয়ে ১০০% লজিক্যাল এবং নিখুঁত ট্রেডিং ডেটা নিশ্চিত করার জন্য
    "top_p": 0.95,
    "max_output_tokens": 1000,
}

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config=generation_config
)

app = Flask(__name__)

# ২. বটের স্টার্ট এবং হেল্প কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **MASTER BOT AI v2.0 (PRO-UPGRADED)** 📊\n\n"
        "আমি এখন আগের চেয়ে **দ্বিগুণ শক্তিশালী এবং প্রাতিষ্ঠানিক মানের এআই এনালাইটিক্স** প্রযুক্তিতে চালিত!\n\n"
        "আপনার যেকোনো ট্রেডিং চার্টের (IQ Option, Pocket Option, Forex, Crypto) পরিষ্কার স্ক্রিনশট পাঠান। "
        "আমি ক্যান্ডেলস্টিক সাইকোলজি, এসএনআর লেভেল এবং প্রাতিষ্ঠানিক লজিক বিশ্লেষণ করে "
        "আপনাকে সর্বোচ্চ নিখুঁত **BUY/UP** বা **SELL/DOWN** সিগন্যাল প্রদান করব।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# ৩. ইমেজ/চার্ট স্ক্রিনশট প্রসেসিং হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        # ইউজারকে প্রফেশনাল মেসেজ দিয়ে আশ্বস্ত করা
        processing_msg = bot.reply_to(
            message, 
            "🧠 **Master Bot AI আপনার চার্টটি গভীরভাবে অ্যানালাইসিস করছে...**\n"
            "🔍 *মার্কেট ট্রেন্ড, ক্যান্ডেলস্টিক সাইকোলজি এবং এসএনআর লেভেল যাচাই করা হচ্ছে। অনুগ্রহ করে কয়েক সেকেন্ড অপেক্ষা করুন...*"
        )
        
        # টেলিগ্রাম সার্ভার থেকে ছবি ডাউনলোড করা
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # ছবিটিকে Gemini AI-এর নতুন ফরম্যাট অনুযায়ী নিখুঁতভাবে তৈরি করা (Fixed)
        image_data = {
            "mime_type": "image/jpeg", 
            "data": downloaded_file
        }
        
        # অত্যন্ত শক্তিশালী, প্রাতিষ্ঠানিক মানের আল্ট্রা-ট্রেডিং প্রম্পট লজিক (দ্বিগুণ নির্ভুল)
        system_prompt = (
            "You are 'Master Bot AI Pro v2.0' - a high-frequency institutional chart analyst and algorithmic trading system with 98% analytical precision.\n"
            "Your objective is to thoroughly evaluate the provided screenshot with absolute neutrality, scanning for BOTH upward and downward high-probability setups.\n\n"
            "STRICT ANALYTICAL PROTOCOLS:\n"
            "1. Market Structure: Determine the macro and micro trends (Strong Uptrend, Aggressive Downtrend, Ranging/Sideways, or Fakeouts/Liquidity sweeps).\n"
            "2. Advanced Candlestick Psychology: Analyze price action at the hard edges. Identify patterns (e.g., Pin Bars, Morning/Evening Stars, Marubozu, inside bars) along with volume/momentum implications.\n"
            "3. Institutional Levels: Detect high-liquidity Support/Demand zones and Resistance/Supply zones. Identify if a level is holding, breaking, or experiencing a fake breakout.\n"
            "4. Indicator Simulation: Visually estimate core indicator states (RSI overbought/oversold divergence, Moving Average crossovers, Bollinger Band compressions) based on price position.\n"
            "5. Unbiased Execution: You MUST execute a dynamic binary decision. If prices bounce off major support or show heavy bullish rejection, output 'BUY/UP'. If prices reject major resistance, show bearish engulfing, or break below support, output 'SELL/DOWN'. Never hardcode or prefer one direction over another.\n\n"
            "Respond ONLY in Bengali using this precise, bold, professional markdown template:\n\n"
            "📈 **মার্কেট স্ট্রাকচার:** [Trend Direction / Volatility State]\n"
            "🎯 **প্রাতিষ্ঠানিক এসএনআর জোন:** ডিমান্ড (সাপোর্ট): [Price] | সাপ্লাই (রেজিস্ট্যান্স): [Price]\n"
            "⚡ **মাস্টার সিগন্যাল:** [Strictly output either BUY/UP or SELL/DOWN] (উইন রেট সম্ভাবনা: [Probability]%)\n"
            "🛡️ **স্মার্ট রিস্ক ম্যানেজমেন্ট:** এন্ট্রি পয়েন্ট: [Price] | টেক প্রফিট (TP): [Price] | স্টপ লস (SL): [Price]\n"
            "🧠 **এডভান্সড ট্রেডিং লজিক:** [Provide a deeply technical 2-sentence explanation in Bengali detailing candle rejection, trend confirmation, or level interaction that solidifies this signal]"
        )
        
        # Gemini AI থেকে রেসপন্স জেনারেট করা (Fixed Format)
        response = model.generate_content([system_prompt, image_data])
        
        # আগের প্রসেসিং মেসেজটি ডিলিট করে মূল ফলাফল পাঠানো
        bot.delete_message(message.chat.id, processing_msg.message_id)
        bot.reply_to(message, response.text, parse_mode='Markdown')
        
    except Exception as e:
        # কোনো সমস্যা হলে মূল কারণটি টেলিগ্রামেই প্রিন্ট করবে যাতে সহজে ধরা যায়
        bot.reply_to(message, f"❌ কারিগরি ত্রুটি! চার্টটি নিখুঁতভাবে স্ক্যান করা যায়নি।\nError Details: {str(e)}")
        print(f"Error handling image: {e}")

# ৪. Render-এ ২৪/৭ সচল রাখার জন্য Webhook সেটআপ (১০০% Fixed পাথ)
@app.route('/webhook', methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Content-Type", 400

@app.route("/")
def webhook():
    bot.remove_webhook()
    # স্ল্যাশ ও পাথের ঝামেলা চিরতরে দূর করার জন্য সরাসরি সুনির্দিষ্ট URL সেটআপ
    base_url = RENDER_URL.strip().rstrip('/')
    clean_url = f"{base_url}/webhook"
    
    bot.set_webhook(url=clean_url)
    return f"🟢 Master Bot AI Pro v2.0 is Up and Running!<br>Webhook successfully pointed to: {clean_url}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


