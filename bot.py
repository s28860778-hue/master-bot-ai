
import io
import os
import telebot
from google import genai
from google.genai import types

# ১. আপনার সরবরাহকৃত সঠিক টোকেন এবং জেমিনির আসল চাবি কাঠি
BOT_TOKEN = '9063727678:AAG9EPcroRud0EwnsDMivPuKoCB4opmX8zM'
GEMINI_API_KEY = 'AQ.Ab8RN6JtHwO4tIwEVkslAc_kC-pSFjfYtSFI06ySUBBNo9RssA'

# বট এবং জেমিনি এআই ক্লায়েন্ট সেটআপ
bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# চার্ট অ্যানালিসিসের জন্য শক্তিশালী প্রম্পট
PROMPT = (
    "You are an expert financial market analyst. Analyze this market chart screenshot. "
    "Provide a detailed analysis in Bengali. You must include:\n"
    "1. Market Trend (Upward, Downward, or Sideways)\n"
    "2. Key Support and Resistance levels visible\n"
    "3. Clear Trading Signal: Give a bold **BUY** or **SELL** or **HOLD** signal based on technical indicators.\n"
    "Keep the language professional, encouraging, and easy to understand in Bengali."
)

# /start এবং /help কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 হ্যালো! আমি আপনার **AI বাংলা স্ক্যানার** বট।\n\n"
        "📈 মার্কেটের যেকোনো চার্ট বা স্ক্রিনশট আমাকে এখানে পাঠান। "
        "আমি সেটি নিখুঁতভাবে স্ক্যান করে আপনাকে বাংলায় সম্পূর্ণ অ্যানালিসিস বুঝিয়ে দেব।"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# স্ক্রিনশট/ছবি পাওয়ার পর প্রসেস করার মূল হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_market_screenshot(message):
    try:
        # ইউজারকে প্রসেসিং স্ট্যাটাস জানানো
        status_msg = bot.reply_to(message, "⏳ আপনার স্ক্রিনশটটি পেয়েছি। আমি এটি অ্যানালিসিস করছি, দয়া করে একটু অপেক্ষা করুন...")

        # টেলিগ্রাম সার্ভার থেকে ছবি ডাউনলোড করার প্রক্রিয়া
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # জেমিনি এআই-এর জন্য ইমেজ পার্ট তৈরি করা
        image_part = types.Part.from_bytes(
            data=downloaded_file,
            mime_type="image/jpeg"
        )

        # লেটেস্ট জেমিনি মডেল ব্যবহার করে ছবি অ্যানালিসিস
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, PROMPT]
        )

        # সফলভাবে অ্যানালিসিস সম্পন্ন হলে আগের মেসেজটি আপডেট করে পাঠানো
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text=f"📊 **মার্কেট অ্যানালিসিস রেজাল্ট:**\n\n{response.text}",
            parse_mode='Markdown'
        )
    except Exception as e:
        # কোনো কারণে এরর আসলে তা সুন্দরভাবে হ্যান্ডেল করা
        bot.reply_to(message, f"❌ দুঃখিত বন্ধু, চাটটি প্রসেস করার সময় একটি সমস্যা হয়েছে। এরর: {str(e)}")

# বটটি রান করা
if __name__ == "__main__":
    print("🤖 AI বাংলা স্ক্যানার বটটি চালু হয়েছে...")
    bot.infinity_polling()
