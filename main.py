import os
import time
import json
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request

BOT_TOKEN = "8637143257:AAG9KXTzc8ysoGyvaMFrXHRMzLdpXsnqIFc"
CHANNEL_ID = "@DEALLS_Hunter"
AMAZON_STORE_ID = "dealshunter2026eg-21"

# خادم ويب خفيف لإبقاء الخدمة نشطة على Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

def create_affiliate_link(original_link):
    clean_link = original_link.split('?')[0]
    return f"{clean_link}?tag={AMAZON_STORE_ID}"

def send_telegram_deal(title, old_price, new_price, raw_link):
    affiliate_link = create_affiliate_link(raw_link)
    discount = int(((old_price - new_price) / old_price) * 100) if old_price > new_price else 0
    
    message = f"""🔥 **تخفيض مميز بنسبة {discount}%!**

📦 **المنتج:** {title}
💰 **السعر قبل الخصم:** ~{old_price}~ جنيه
✅ **السعر الحالي:** {new_price} جنيه فقط!

🔗 **رابط الشراء المباشر:**
{affiliate_link}

📢 **قناة:** عروض وخصومات مصر
"""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with request.urlopen(req) as response:
            print(f"✅ تم نشر العرض: {title[:20]}...")
    except Exception as e:
        print("❌ خطأ إرسال:", e)

def bot_loop():
    while True:
        products = [
            {
                "title": "ماكينة حلاقة فيليبس متعددة الاستخدامات",
                "old_price": 1450,
                "new_price": 999,
                "link": "https://www.amazon.eg/dp/B08W8D1337"
            }
        ]
        
        for item in products:
            send_telegram_deal(item['title'], item['old_price'], item['new_price'], item['link'])
            time.sleep(10)
            
        time.sleep(3 * 3600)

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    bot_loop()
