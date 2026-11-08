
import telebot
from google import genai
from PIL import Image
import io

# ১. আপনার সঠিক টোকেন এবং আসল API Key বসান
TOKEN = '9063727678:AAH5f6ivj7MXs-fdiAZjXg1n4LEKixYrTRc'  # টেলিগ্রাম বটের টোকেন
API_KEY = 'YOUR_ACTUAL_GEMINI_API_KEY' # আপনার আসল AIzaSy... এপিআই কি

# ২. বট ও জেমিনাই ক্লায়েন্ট চালু করা
bot = telebot.TeleBot(TOKEN)
client = genai.Client(api_key=API_KEY)

# চার্ট অ্যানালিসিসের জন্য শক্তিশালী প্রম্পট
PROMPT = (
    "You are an expert financial market analyst. Analyze this market chart screenshot carefully. "
    "Provide a detailed analysis in Bengali. You must include:\n"
    "1. Market Trend (Upward, Downward, or Sideways)\n"
    "2. Key Support and Resistance levels visible\n"
    "3. Clear Trading Signal: Give a bold **BUY** or **SELL / DOWN** signal with proper technical reasons based on price action or indicators shown.\n"
    "Keep the language professional, encouraging, and easy to understand for Bengali traders."
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমি আপনার AI বাংলা স্ক্যানার বট। আপনার যেকোনো মার্কেট চার্টের স্ক্রিনশট এখানে পাঠান, আমি সেটির টেকনিক্যাল অ্যানালিসিস এবং বাই/সেল সিগন্যাল তৈরি করে দেবো।")

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        bot.reply_to(message, "আপনার চার্টটি পেয়েছি। আমি এটি গভীরভাবে অ্যানালিসিস করছি, দয়া করে একটু অপেক্ষা করুন...")
        
        # টেলিগ্রাম থেকে ছবি ডাউনলোড করা
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # ছবিটিকে PIL Image-এ কনভার্ট করা
        image = Image.open(io.BytesIO(downloaded_file))
        
        # Gemini 1.5 Flash মডেলের মাধ্যমে রেসপন্স তৈরি
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=
        )
        
        # ইউজারকে ফলাফল পাঠানো
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, f"দুঃখিত বন্ধু, চার্টটি প্রসেস করার সময় একটি সমস্যা হয়েছে। এরর: {str(e)}")

# বট রানিং রাখা
if __name__ == '__main__':
    print("AI বাংলা স্ক্যানার বট চালু হয়েছে...")
    bot.infinity_polling()
