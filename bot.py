import telebot
from google import genai
from PIL import Image
import io

# তোমার নতুন Gemini Auth API Key বসানো হয়েছে
API_KEY = "AQ.Ab8RN6IM6DAeZFnQB7B6J8OC22s28B3YkU2x3zcBu4dsMkYWhA"
client = genai.Client(api_key=API_KEY)

# তোমার Telegram Token বসানো আছে
TELEGRAM_TOKEN = "9063727678:AAF_DWAWizkWS6Ku3-Jp21g91tdtmNY5zX0"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("✨👑 MASTER BOT AI (ULTRA VIP SPARKLE EDITION) IS RUNNING...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✨👑 *স্বাগতম! আমি 'Master Bot AI' (Ultra VIP)* 👑✨\n"
        "╔════════════════════╗\n"
        "🚀 আপনার যেকোনো ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট এখানে পাঠান।\n"
        "💎 আমি ক্যান্ডেলস্টিক প্যাটার্ন ও মার্কেট পাওয়ার গভীরভাবে স্ক্যান করে নিখুঁত সিগন্যাল দেব।\n"
        "╚════════════════════╝"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    wait_msg = (
        "⚡✨ *চার্ট স্ক্যানিং শুরু হয়েছে...* ✨⚡\n"
        "╔════════════════════╗\n"
        "🔍 AI ক্যান্ডেল ও সাপোর্ট-রেজিস্ট্যান্স মাপছে...\n"
        "⏳ দয়া করে মাত্র কয়েক সেকেন্ড অপেক্ষা করুন...\n"
        "╚════════════════════╝"
    )
    bot.reply_to(message, wait_msg, parse_mode='Markdown')
    
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(io.BytesIO(downloaded_file))
        
        trading_prompt = """
        তুমি একজন বিশ্বের সেরা প্রো-লেভেলের ফাইনান্সিয়াল মার্কেট এবং ক্যান্ডেলস্টিক চার্ট অ্যানালিস্ট। 
        প্রদত্ত চার্টের স্ক্রিনশটটি অত্যন্ত সূক্ষ্মভাবে পর্যবেক্ষণ করো। কোনো অনুমান বা ভুয়া তথ্য দেবে না।
        
        অ্যানালাইসিস করার নিয়মাবলী:
        ১. চার্টের বর্তমান ওভারঅল ট্রেন্ড এবং বায়ার-সেলারদের প্রকৃত শক্তি বিশ্লেষণ করো।
        ২. মার্কেট যদি অতিরিক্ত অস্থির বা অস্পষ্ট হয়, তবে স্পষ্টভাবে 'HOLD / NO TRADE' পরামর্শ দাও।

        সবকিছু বিশ্লেষণ করে কোনো বাড়তি কথা না লিখে শুধুমাত্র নিচের হুবহু উজ্জ্বল বক্স ফরম্যাটে বাংলায় উত্তর দাও:

        ✨👑 *MASTER BOT AI • ULTRA VIP* 👑✨
        ╔════════════════════╗
        🌟 *সিগন্যাল:* *[BUY / CALL 🟢⚡ অথবা SELL / PUT 🔴🔥 অথবা HOLD / NO TRADE 🟡⚠️ - চার্ট অনুযায়ী সঠিকটি লেখো]*
        💎 *অ্যাকুরেসি:* `[বাস্তবসম্মত শতাংশ লেখো, যেমন: ৯৪%]` 【[শতাংশ অনুযায়ী সবুজ বা লাল বক্স দাও, যেমন: 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜]】
        🔥 *মার্কেট পাওয়ার:* [চার্টের বর্তমান শক্তি লেখো, যেমন: অতি শক্তিশালী বায়ার 🚀 বা তীব্র সেলার চাপ 📉]
        ╚════════════════════╝

        🔮 *AI মার্কেট অ্যানালাইসিস:*
        > [চার্টের ট্রেন্ড, ক্যান্ডেল রিজেকশন এবং সাপোর্ট-রেজিস্ট্যান্স লেভেলের ওপর ভিত্তি করে ২-৩ লাইনে স্পষ্ট ও নিখুঁত ব্যাখ্যা দাও]

        🛡️ _নিরাপদ ট্রেডিংয়ের জন্য মানি ম্যানেজমেন্ট অনুসরণ করুন।_
        """
        
        # নতুন Google GenAI SDK দিয়ে AQ. কী ব্যবহার করে সিগন্যাল তৈরি
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[trading_prompt, img]
        )
        
        bot.reply_to(message, response.text, parse_mode='Markdown')
        
    except Exception as e:
        print("Error:", e)
        error_msg = (
            f"⚠️ *সতর্কতা: চার্টটি অ্যানালাইসিস করা সম্ভব হয়নি!*\n"
            f"কারণ: `{str(e)}`"
        )
        bot.reply_to(message, error_msg, parse_mode='Markdown')

if __name__ == "__main__":
    bot.polling(none_stop=True)
