import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import keep_alive

# بيانات تسجيل الدخول
LOGIN_URL = "https://inspector.ayen.com.sa/login"  # تأكد من صحة الرابط
REQUESTS_URL = "https://inspector.ayen.com.sa/requests"  # رابط صفحة الطلبات
EMAIL_SENDER = "Sale73Li8@gmail.com"  # ضع بريدك هنا
EMAIL_PASSWORD = "19961416Al"  # استخدم كلمة مرور التطبيق إذا كنت تستخدم Gmail
EMAIL_RECEIVER = "Sale73Li8@gmail.com"  # البريد الذي ستصله التنبيهات

# تسجيل الدخول
session = requests.Session()
login_data = {"email": "Sale73Li8@gmail.com", "password": "19961416Al"}
response = session.post(LOGIN_URL, data=login_data)

if response.status_code == 200:
    print("تم تسجيل الدخول بنجاح!")
else:
    print("فشل تسجيل الدخول! تحقق من بياناتك.")
    exit()

def check_new_requests():
    response = session.get(REQUESTS_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    requests_list = soup.find_all("div", class_="request-item")  # عدل هذا حسب HTML الموقع
    
    new_requests = []
    for request in requests_list:
        new_requests.append(request.text.strip())
    
    return new_requests

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("تم إرسال الإشعار بالبريد الإلكتروني!")
    except Exception as e:
        print("خطأ أثناء إرسال البريد:", e)

# تشغيل البوت كل 5 دقائق
while True:
    new_requests = check_new_requests()
    if new_requests:
        send_email("طلب جديد!", "\n".join(new_requests))
    else:
        print("لا توجد طلبات جديدة.")
    
    time.sleep(60)  # فحص الموقع كل 5 دقائق
    
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Ayen Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()
