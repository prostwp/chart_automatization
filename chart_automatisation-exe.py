from chart_automatisation import ChartAutomation
import os
from chart_keys import keys
import webbrowser
import subprocess
from pynput.keyboard import Controller, Key
import requests
from command_v_handler import VKeyHandler
from datetime import datetime, timedelta
try:
    import pyautogui
except AssertionError:
    pass
import time

file_path = 'C:\\Users\\dkarnachev\\Downloads\\chart_pasted_text.txt'
keyboard = Controller()

def write_pattern_trend(trend):
    if " ".join(chart.chart_name) == "Pennant" and chart.direction == 'buy':
        write(keys[trend][0], enter=False)
    elif " ".join(chart.chart_name) == "Pennant" and chart.direction == 'sell':
        write(keys[trend][1], enter=False)

    if " ".join(chart.chart_name) == "Flag" and chart.direction == 'buy':
        write(keys[trend][0], enter=False)
    elif " ".join(chart.chart_name) == "Flag" and chart.direction == 'sell':
        write(keys[trend][1], enter=False)

    if " ".join(chart.chart_name) == "Double Top" and chart.direction == 'sell':
        write(keys[trend][0], enter=False)

    if " ".join(chart.chart_name) == "Double Bottom" and chart.direction == 'buy':
        write(keys[trend][1], enter=False)

    if " ".join(chart.chart_name) == "Head and Shoulders" and chart.direction == 'sell':
        write(keys[trend][0], enter=False)
    elif " ".join(chart.chart_name) == "Head and Shoulders" and chart.direction == 'buy':
        write(keys[trend][1], enter=False)

    if " ".join(chart.chart_name) == "Rectangle" and chart.direction == 'sell':
        write(keys[trend][2], enter=False)
    elif " ".join(chart.chart_name) == "Rectangle" and chart.direction == 'buy':
        write(keys[trend][2], enter=False)

    if " ".join(chart.chart_name) == "Triangle" and chart.direction == 'sell':
        write(keys[trend][2], enter=False)
    elif " ".join(chart.chart_name) == "Triangle" and chart.direction == 'buy':
        write(keys[trend][2], enter=False)

    if " ".join(chart.chart_name) == "Wedge" and chart.direction == 'buy':
        write(keys[trend][1], enter=False)
    elif " ".join(chart.chart_name) == "Wedge" and chart.direction == 'sell':
        write(keys[trend][0], enter=False)





def write(text, interval=0.00001, enter=True):
    global keyboard
    for i in text:
        keyboard.press(i)
        keyboard.release(i)
        time.sleep(interval)
    if enter:
        pyautogui.press('enter')
    else:
        pyautogui.press('space')
    print(f"Write {text}")


def toggle_bold():
    keyboard.press(Key.ctrl)
    keyboard.press('b')
    keyboard.release('b')
    keyboard.release(Key.ctrl)


def write_with_rebound():
    global chart

    write(keys["display_pattern"][0].replace("Wedge", " ".join(chart.chart_name)))

    if chart.direction == "sell":
        write(keys["sell_rebound"][0].replace("Wedge", " ".join(chart.chart_name)))

    elif chart.direction == 'buy':
        write(keys["buy_rebound"][0].replace("Wedge", " ".join(chart.chart_name)))


def write_for_double_bottom_top(neckline_status):
    write(keys["display_pattern"][0].replace("Wedge", " ".join(chart.chart_name)), enter=False)

    if chart.chart_name[1] == "Top":
        write(keys["drop_rise"][0])
        if neckline_status:
            write(keys["neckline"][0])

    elif chart.chart_name[1] == "Bottom":
        write(keys["drop_rise"][1])
        if neckline_status:
            write(keys["neckline"][1])


def write_head_and_shoulders():
    write(keys["display_pattern"][0].replace("Wedge", " ".join(chart.chart_name)))
    if chart.direction == 'buy':
        write(keys["neckline"][1])
    elif chart.direction == 'sell':
        write(keys["neckline"][0])


while True:
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:

        chart = ChartAutomation()
        decoded_json = chart.decoding(file_path)
        chart.find_data_state_and_timeframe()
        print(chart.timeframe)
        drawing_data = decoded_json['panels'][0]['drawings']
        for drawing in drawing_data:
            chart.defining_the_pattern_name(drawing)
            chart.define_direction(drawing)
        print(" ".join(chart.chart_name))
        print(len(" ".join(chart.chart_name)))
        # chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

        if decoded_json:
            url = 'https://cp.octafeed.com/panel/overview-posts/create'
            webbrowser.open_new_tab(url)

            time.sleep(5)

            # toggle_bold()

            pyautogui.press('enter')

            toggle_bold()

            write(keys["general_outlook"][0])

            if chart.timeframe == 1 or chart.timeframe == 5 and chart.chart_name[0]:
                write_pattern_trend("local_trend")
            else:
                write_pattern_trend("global_trend")

            if chart.chart_name[0] in ("Pennant", "Wedge", "Flag", "Rectangle", "Triangle"):
                write_with_rebound()
            elif chart.chart_name[0] in "Double":
                write_for_double_bottom_top(chart.neckline_flag)
            elif chart.chart_name[0] in "Head":
                write_head_and_shoulders()

            with open("news.txt", "r") as content:
                try:
                    with open("news.txt", 'r') as file:
                        content = file.readlines()
                    if content and len(content) == 2:
                        file_time = datetime.strptime(content[1], '%H:%M').time()
                        current_time = datetime.now()
                        threshold_time = datetime.combine(current_time.date(), file_time)
                        time_difference = threshold_time - current_time
                        toggle_bold()
                        write(keys["fundamental_factors"][0])
                        # toggle_bold()
                        if time_difference > timedelta(hours=1):
                            write(content[0])
                        elif timedelta(0) <= time_difference <= timedelta(hours=1):
                            write(content[0].replace("hour", "minute"))
                        else:
                            with open("news.txt", 'w') as file:
                                pass
                    else:
                        write(keys["no_news"][0])
                except FileNotFoundError:
                    print("File not found.")
            today = datetime.today()
            if today.weekday() == 4:
                write(keys["friday"][0])


            print(chart.data_state)
            subprocess.run(
                ["node", "puppeteer_script.js", f"{chart.direction}", f"{chart.timeframe}", f"{chart.data_state}",
                 f"{" ".join(chart.chart_name)}"])
        os.remove(file_path)
