import requests
import json
import re
import os
import time
import random

LINE_TOKEN = os.environ['LINE_TOKEN']
USER_ID = os.environ['USER_ID']

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
    time.sleep(random.uniform(1, 5))
    
    url = 'https://www.hoshitea.com/shop/item?category_id=40025&pageno=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'ja,en;q=0.9'
    }
    
    res = requests.get(url, headers=headers)
    match = re.search(r'data-page="([^"]+)"', res.text)
    if not match:
        print('ไม่พบข้อมูล')
        return
    
    data = json.loads(match.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    products = data['props']['products']
    
    print(f'พบสินค้าทั้งหมด {len(products)} รายการ')
    for p in products:
        stock = p['product_classes'][0]['stock']
        unlimited = p['product_classes'][0]['stock_unlimited']
        print(f"- {p['name'][:30]} | stock: {stock} | unlimited: {unlimited}")
    
    back_in_stock = []
    for p in products:
        stock = p['product_classes'][0]['stock']
        unlimited = p['product_classes'][0]['stock_unlimited']
        if stock >= 0 or unlimited == 1:
            name = p['name'].replace('SOLD OUT', '').strip()
            back_in_stock.append(name)
    
    if back_in_stock:
        msg = '🍵 มีสินค้ากลับมาแล้ว!\n\n'
        for i, name in enumerate(back_in_stock, 1):
            msg += f'{i}. {name}\n'
        msg += '\n🔗 https://www.hoshitea.com/shop/item?category_id=40025&pageno=1'
        send_line_message(msg)
        print('แจ้งเตือนแล้ว!')
    else:
        print('ยังหมดอยู่ทุกตัว')

check_stock()
