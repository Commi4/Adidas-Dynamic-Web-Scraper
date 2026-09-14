import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv
import requests
import re

print("Запускаем браузер...")
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

url = 'https://www.adidas.cz/muzi-tenisky'
driver.get(url)

print("Ждем загрузки первого экрана...")
time.sleep(4)

print("Пробуем закрыть баннер с куки...")
try:
    cookie_btn = driver.find_element(By.ID, 'glass-gdpr-default-consent-accept-button')
    driver.execute_script("arguments[0].click();", cookie_btn)
    print("Куки приняты!")
except:
    pass

FILE_NAME = 'adidas_shoes.csv'

with open(FILE_NAME, 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Название', 'Цена (Kč)'])
    
    current_page = 1
    total_saved = 0
    
    while True:
        print(f"\n--- Парсим страницу {current_page} ---")
        
        # Медленный и надежный скролл, чтобы сайт успевал отрисовывать цены
        for i in range(10):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(0.5) 
            
        cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="plp-product-card"]')
        
        page_saved = 0
        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, '[data-testid="product-card-title"]').get_attribute('textContent')
            except:
                title = ''
                
            price = ''
            try:
                raw_price = card.find_element(By.CSS_SELECTOR, '[data-testid="main-price"]').get_attribute('textContent')
                price = re.sub(r'[^\d,]', '', raw_price)
            except:
                price = ''
                
           # Записываем товар, если у него есть хотя бы название
            if title != '':
                # Если цена пустая (товар распродан), пишем статус. Иначе - пишем саму цену.
                final_price = price if price != '' else 'Нет в наличии'
                
                writer.writerow([title, final_price])
                page_saved += 1
                total_saved += 1
                
        print(f"Собрано {page_saved} валидных товаров. Всего в базе: {total_saved}")
        
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="pagination-next-button"]')
            driver.execute_script("arguments[0].click();", next_button)
            print("Переходим на следующую страницу...")
            current_page += 1
            time.sleep(5) 
        except:
            print("\nКнопка 'Další' не найдена. Конец каталога достигнут!")
            break 

print(f"\nУспех! Всего собрано товаров: {total_saved}")

try:
    driver.quit()
except:
    pass

# ==========================================
# БЛОК ОТПРАВКИ ФАЙЛА В TELEGRAM
# ==========================================
print("\nПодготавливаем отправку файла в Telegram...")
TOKEN = "8993965523:AAGdx30tAy3pmj0DIWM0e55x2s9yBuTgIOg"
CHAT_ID = "718047090" 

url_tg = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

try:
    with open(FILE_NAME, 'rb') as file_to_send:
        response = requests.post(url_tg, data={'chat_id': CHAT_ID}, files={'document': file_to_send})

    if response.status_code == 200:
        print("✅ Файл успешно доставлен в твой Telegram!")
    else:
        print("❌ Ошибка отправки:", response.text)
except Exception as e:
    print("❌ Не удалось отправить файл. Ошибка:", e)