import requests
from bs4 import BeautifulSoup
import csv

# Создаем новый файл, чтобы не перезаписывать старый
with open('quotes_all.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Автор', 'Цитата'])
    
    # Запускаем цикл от 1 до 10 (число 11 не включается)
    for page in range(1, 11):
        # Подставляем номер страницы в ссылку через f-строку
        url = f'http://quotes.toscrape.com/page/{page}/'
        response = requests.get(url)
        
        # Разбираем HTML конкретной страницы
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        # Достаем текст и автора, как делали раньше
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            writer.writerow([author, text])
            
        print(f"Страница {page} успешно собрана!")

print("Готово! Все 100 цитат сохранены в quotes_all.csv")