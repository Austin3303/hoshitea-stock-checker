import requests
import schedule
import time
import json

LINE_TOKEN = 'ใส่ Token ของคุณ'
USER_ID    = 'ใส่ User ID ของคุณ'

def send_line_message(message):
    requests.post(
        'https://api.line.me/v2/bot/message/push',
        headers={
            'Authorization': f'Bearer {LINE_TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            'to': USER_ID,
            'messages': [{'type': 'text', 'text': message}]
        }
    )

def check_stock():
    url = 'https://www.hoshitea.com/shop/item?category_id=5&pageno=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'ja,en;q=0.9'
    }
    
    try:
        res = requests.get(url, headers=headers)
        html = res.text
        
        # ดึง JSON จาก data-page
        import re
        match = re.search(r'data-page="([^"]+)"', html)
        if not match:
            print('ไม่พบข้อมูลสินค้า')
            return
        
        data = json.loads(match.group(1).replace('&quot;', '"').replace('&amp;', '&'))
        products = data['props']['products']
        
        back_in_stock = []
        for p in products:
            stock = p['product_classes'][0]['stock']
            unlimited = p['product_classes'][0]['stock_unlimited']
            if stock > 0 or unlimited == 1:
                name = p['name'].replace('【SOLD OUT】', '').strip()
                back_in_stock.append(name)
        
        if back_in_stock:
            msg = '🍵 มีสินค้ากลับมาแล้ว!\n\n'
            for i, name in enumerate(back_in_stock, 1):
                msg += f'{i}. {name}\n'
            msg += '\n🔗 https://www.hoshitea.com/shop/item?category_id=5&pageno=1'
            send_line_message(msg)
            print('แจ้งเตือนแล้ว:', back_in_stock)
        else:
            print('ยังหมดอยู่ทุกตัว')
    
    except Exception as e:
        print('Error:', e)

# รันทุก 1 ชั่วโมง
schedule.every(1).hours.do(check_stock)

# รันครั้งแรกทันที
check_stock()

while True:
    schedule.run_pending()
    time.sleep(60)
```

### ไฟล์ที่ 2: `requirements.txt`
```
requests
schedule
