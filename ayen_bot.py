import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# بيانات تسجيل الدخول
LOGIN_URL = "https://inspector.ayen.com.sa/login"  # تأكد من صحة الرابط
REQUESTS_URL = "https://inspector.ayen.com.sa/requests"

EMAIL = "Sale73Li8@gmail.com"
PASSWORD = "19961416Al"

# بيانات تيليجرام
TELEGRAM_BOT_TOKEN = "7753822380"
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
    requests_list = soup.find_all("div", class_="request-item")  # عدل هذا بناءً على كود HTML

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
    
    time.sleep(60)  # الفحص كل دقيقة
