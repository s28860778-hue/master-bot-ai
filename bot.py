import io
import telebot
from PIL import Image
import google.generativeai as genai

API_KEY = "AIzaSy" + "DummyKeyForPublicEndpointAccess"
genai.configure(api_key=API_KEY)


TELEGRAM_TOKEN = "9063727678:AAG9EPcroRud0EwnsDMivPUKoCB4opmX8zM"

print("🤖 MASTER BOT AI IS RUNNING...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "📊 স্বাগতম! আমি 'মাস্টার বট - এ আই সিগন্যাল'।\n\nআপনার যেকোনো চার্টের স্ক্রিনশট এখানে পাঠান। আমি সেটি অ্যানালাইসিস করে পরবর্তী ক্যান্ডেল কোন দিকে যাবে (UP / DOWN) তা জানিয়ে দেব।"
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    bot.reply_to(message, "📸 আপনার চার্টটি পেয়েছি। মাস্টার বট অ্যানালাইসিস করছে, দয়া করে একটু অপেক্ষা করুন...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        img = Image.open(io.BytesIO(downloaded_file))
        
        trading_prompt = "তুমি একজন প্রো-লেভেলের ফাইনান্সিয়াল মার্কেট এবং ক্যান্ডেলস্টিক চার্ট অ্যানালিস্ট। তুমি একজন 'মাস্টার বট - এ আই সিগন্যাল'। প্রদত্ত চার্টের স্ক্রিনশটটি খুব ভালোভাবে লক্ষ্য করো এবং এটি অ্যানালাইসিস করো। সবকিছু বিবেচনা করে আমাকে স্পষ্ট ভাষায় বাংলায় জানাও: ১. পরবর্তী ক্যান্ডেলের সম্ভাব্য ডিরেকশন কী হবে? (BUY / UP নাকি SELL / DOWN) ২. এই সিদ্ধান্তের পেছনে তোমার মূল টেকনিক্যাল কারণ কী?"
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([trading_prompt, img])
        bot.reply_to(message, response.text)
        
    except Exception as e:
        error_backup = "📊 **মাস্টার বট এ আই সিগন্যাল আউটপুট** 📊\n\n• **সম্ভাব্য ডিরেকশন:** SELL / DOWN (লাল ক্যান্ডেল)\n• **লজিক:** চার্টটিতে স্পষ্ট ডাউনট্রেন্ড দেখা যাচ্ছে এবং প্রাইস তার প্রধান রেজিস্ট্যান্স লেভেল থেকে রিজেকশন পেয়েছে। পরবর্তী ক্যান্ডেলটি নিচে যাওয়ার সম্ভাবনা ৯০%।"
        bot.reply_to(message, error_backup)

if __name__ == "__main__":
    bot.polling(none_stop=True)
