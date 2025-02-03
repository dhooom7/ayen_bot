import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# بيانات تسجيل الدخول
LOGIN_URL = "https://inspector.ayen.app"  # ✅ رابط تسجيل الدخول الجديد
REQUESTS_URL = "https://inspector.ayen.app/available-orders/"  # ✅ رابط الطلبات الجديد

EMAIL = "Sale73Li8@gmail.com"
PASSWORD = "19961416Al"

# بيانات تيليجرام
TELEGRAM_BOT_TOKEN = "7753822380:AAEOJHdbI-lGKbJv0QzaSJ0RdzW0aQs4Y5k"
CHAT_ID = "5225767276"

# إنشاء كائن البوت
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# تسجيل الدخول إلى الموقع
session = requests.Session()
login_data = {"email": EMAIL, "password": PASSWORD}
response = session.post(LOGIN_URL, data=login_data)

if response.status_code == 200:
    print("✅ تم تسجيل الدخول بنجاح!")
else:
    print("❌ فشل تسجيل الدخول! تحقق من بياناتك.")
    exit()

def check_new_requests():
    response = session.get(REQUESTS_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # تعديل بناءً على HTML الصفحة
    requests_list = soup.find_all("div", class_="order-item")  # تأكد من أن الكلاس صحيح

    new_requests = []
    for request in requests_list:
        new_requests.append(request.text.strip())

    return new_requests

def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# تشغيل البوت كل دقيقة
while True:
    new_requests = check_new_requests()
    if new_requests:
        message = "🚀 طلب جديد في Ayen:\n\n" + "\n".join(new_requests)
        send_telegram_message(message)
    else:
        print("🔍 لا توجد طلبات جديدة.")
    
    time.sleep(60)
