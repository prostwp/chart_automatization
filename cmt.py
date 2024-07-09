# import requests
# from datetime import datetime, timedelta
#
# def get_daily_price_change_percentage(symbol, api_key):
#     # URL для запроса данных о валютной паре
#     url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&apikey={api_key}'
#     response = requests.get(url)
#     data = response.json()
#
#     # Получаем текущую дату
#     current_date = datetime.now().strftime('%Y-%m-%d')
#
#     try:
#         time_series = data['Time Series FX (Daily)']
#
#         # Данные за сегодня
#         today_data = time_series[current_date]
#         today_open = float(today_data['1. open'])
#         today_close = float(today_data['4. close'])
#
#         # Рассчитываем изменение в процентах
#         change_percentage = ((today_close - today_open) / today_open) * 100
#         return change_percentage
#
#     except KeyError:
#         return "Данные за текущий день недоступны или недоступны."
#
# # Пример использования функции
# api_key = 'SP5UT4AK12FE7ZEQ'
# symbol = 'EURUSD'
# percentage_change = get_daily_price_change_percentage(symbol, api_key)
# if isinstance(percentage_change, float):
#     print(f'Изменение цены за сегодня: {percentage_change:.2f}%')
# else:
#     print('Не удалось получить данные.')
import webbrowser

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "https://docs.python.org/"

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url)