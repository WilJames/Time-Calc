from kivy.app import App

import re
from datetime import datetime
from datetime import timedelta
from time import time

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
# from kivy.uix.floatlayout import FloatLayout
# from kivy.properties import ObjectProperty

# from kivy.config import Config
Window.clearcolor = (.15, .15, .15, 1)
# Window.size = (720 / 2, 1280 / 2)

start_time = 0


def replace_scobs(string):
    string = string.replace(')(', ')*(')
    find = re.findall(r'\d+\(', string)
    for i in find:
        find1 = re.findall(r'\d+', i)
        string = re.sub(r"\d+\(", f'{find1[0]}*(', string, 1)
    find2 = re.findall(r'\)\d+', string)
    for i in find2:
        find1 = re.findall(r'\d+', i)
        string = re.sub(r"\)\d+", f')*{find1[0]}', string, 1)
    return string


def hours_to_min(string):
    string = string.replace('x', '*')
    string = re.sub(r"\d+\s[a-zA-Z]+\,\s", "", string)  # удаление дней
    string = re.sub(r"(^[\+\/\*\-\)]+|[\+\/\*\-\(]+$)", "", string)  # удаление любого лишнего знака перед и в конце
    string = replace_scobs(string)  # выставление умножения перед скобками
    time = re.findall(r"\d+:\d+", string)
    for i in time:
        a = i.split(':')
        b = int(a[0]) * 60 + int(a[1])
        string = re.sub(r"\d+:\d+", str(b), string, 1)
    try:
        minutes = eval(string)
        result = timedelta(minutes=minutes)
        result = re.sub(r"\.\d+$", "", str(result))
        result = result[:-3]
        return result
    except SyntaxError:
        return 'Ошибка записи'


class Interface(BoxLayout):
    def add_number(self, text):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        self.label.text += text

    def add_operation(self, text):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        elif self.label.text == '':
            pass
        else:
            self.label.text = re.sub(r"[\+\/x\-]$", "", self.label.text)
            self.label.text += text

    def result_clear(self):
        if self.label.text == '':
            pass
        else:
            self.label.text = ''

    def result_del(self):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        elif self.label.text == '':
            pass
        else:
            self.label.text = str(self.label.text[:-1])

    def cur_time(self):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        elif re.search(r"[\+\/x\-\)]$", self.label.text) or self.label.text == '':
            currentDT = datetime.now()
            self.label.text += currentDT.time().isoformat(timespec='minutes')
        else:
            pass

    def split_time(self):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        elif re.search(r"\d+$", self.label.text) and not re.search(r"\d+:\d+$", self.label.text):
            self.label.text += ':'
        else:
            pass

    def upkeys(self, state):
        if self.label.text == 'Ошибка записи':
            self.label.text = ''
        # print('My button <%s> state is <%s>' % (instance, value))
        if state == 'down':
            global start_time
            start_time = time()
        elif state == 'normal':
            end_time = round(time() - start_time)
            if end_time >= 1:
                self.label.text += ')'
            else:
                self.label.text += '('

    def calc_result(self):
        if self.label.text == '':
            pass
        elif self.label.text == 'Ошибка записи':
            self.label.text = ''
        else:
            result = hours_to_min(self.label.text)
            self.label.text = result


class CalcTimeApp(App):
    def build(self):
        return Interface()


if __name__ == "__main__":
    CalcTimeApp().run()
