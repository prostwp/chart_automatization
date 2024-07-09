import base64
import json
import os
import webbrowser
import subprocess
import time

# import pyautogui
import re
import requests


class ChartAutomation:
    def __init__(self):
        self.timeframe = 0
        self.dict_sup_res = {'Support': [], 'Resistance': []}
        self.direction = ''
        self.data_state = ''
        self.broke_flag = [1]
        self.chart_name = ''
        self.neckline_flag = None
        self.content = ''

    def get_price_change_percentage(self, symbol, api_key):
        # Получаем данные о валютной паре за текущий день
        url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        # Получаем текущую дату
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Получаем данные за текущий и предыдущий день
        try:
            today_data = data['Time Series FX (Daily)'][current_date]
            today_open = float(today_data['1. open'])
            today_close = float(today_data['4. close'])

            # Рассчитываем изменение в процентах
            change_percentage = ((today_close - today_open) / today_open) * 100
            return change_percentage
        except KeyError:
            return "Данные за текущий день еще недоступны."

    def defining_the_pattern_name(self, draw_element):
        self._error_handler(draw_element, dict)
        if draw_element['toolType'] == 'text':
            splited_draw_el = draw_element['settings']['text'].split()
            if splited_draw_el[0] == "Neckline":
                self.neckline_flag = True
            if splited_draw_el[0] in ("Pennant", "Wedge", "Flag", "Double", "Head", "Rectangle", "Triangle"):
                self.chart_name = splited_draw_el


    def define_direction(self, draw_element):
        if draw_element['toolType'] == 'arrow_line':
            if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
                self.direction = "sell"
            elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
                self.direction = "buy"
            else:
                raise Exception("Direction did not found")

    def find_data_state_and_timeframe(self):
        try:
            data_state_match = re.search(r'data-symbol="([A-Z]{6})"', self.content)
            timeframe_match = re.search(r'data-timeframe="(60|300|900|1800|3600)"', self.content)
            if data_state_match and timeframe_match:
                currency_pair = data_state_match.group(1)
                self.data_state = currency_pair

                currency_timeframe = timeframe_match.group(1)
                print(currency_timeframe)
                self.timeframe = int(currency_timeframe) / 60
                print(self.timeframe)
            else:
                raise ValueError("Валютная пара или таймфрейм не найдены в файле")
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")


    def decoding(self, file_path):
        try:
            # Открываем исходный файл для чтения
            with open(file_path, 'r') as file:
                self.content = file.read()

            # Извлекаем Base64 строку изображения
            base64_str_index = self.content.find("base64,") + len("base64,")
            base64_str_end_index = self.content.find('"', base64_str_index)
            base64_image_str = self.content[base64_str_index:base64_str_end_index]

            # Декодируем Base64 строку изображения в бинарные данные
            image_data = base64.b64decode(base64_image_str)

            # Сохраняем бинарные данные в файл
            # self.png_wtirer(image_data)

            # Извлекаем и декодируем строку состояния
            data_state_index = self.content.find('data-state="') + len('data-state="')
            data_state_end_index = self.content.find('"', data_state_index)
            data_state_str = self.content[data_state_index:data_state_end_index]

            # Декодируем строку состояния из Base64
            data_state = base64.b64decode(data_state_str).decode('utf-8')
            json_data_state = json.loads(data_state)

            # Сохраняем декодированные данные состояния в файл
            # with open('decoded_state.json', 'w') as state_file:
            #     state_file.write(data_state)

            print("Файлы успешно декодированы и сохранены.")
            return json_data_state
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")


    def png_wtirer(self, data):
        with open('decoded_image.png', 'wb') as image_file:
            image_file.write(data)

    def _error_handler(self, data, expected_type):
        if not isinstance(data, expected_type) or not data:
            raise TypeError(f"Provided data: {data} is not of type {expected_type.__name__} or is empty")

# tmp = ChartAutomation()
# tmp.decoding('/Users/dkarnachev/Downloads/pasted_text.txt')
# tmp.find_data_state_and_timeframe()
# tmp.defining_the_pattern_name()
# print("1".join(tmp.chart_name))
