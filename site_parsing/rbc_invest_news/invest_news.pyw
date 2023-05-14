# -*- coding: utf-8 -*-
"""
Данный модуль представляет GUI для парсинга РБК Инвестиций.
При нажатии на заголовок новости открывается всплывающее окно с её текстом.
Как запускать из терминала:
    Windows - "start pythonw <путь_к_этому_файлу>"
    Linux - "nohup <путь_к_этому_файлу> &"
TODO: сделать кастомную полосу прокрутки у текста новости
TODO: добавить значок в трее или на панели задач
"""
import PySimpleGUI as sg
from rbc_parser import RBCParser


#  Переменные для GUI
BG_COLOR = "grey"
BUTTON_COLOR = "black"
CLOSE_BUTTON_TEXT = "Закрыть"

#  Парсим страницу РБК
rbc = RBCParser()
invest_news_titles = rbc.invest_news.keys()

#  Создаём окно, где каждый заголовок новости - кнопка,
#  и помимо этого есть отдельная кнопка для закрытия окна
sg.set_options(
    use_custom_titlebar=True,
    titlebar_background_color=BUTTON_COLOR,
    keep_on_top=True
)
layout = [
    [[sg.Button(el, button_color=BG_COLOR, mouseover_colors=BUTTON_COLOR)]
     for el in invest_news_titles],
    [sg.Button(CLOSE_BUTTON_TEXT, button_color=BUTTON_COLOR)]]
window = sg.Window(
    "Новости инвестиций РБК",
    layout,
    background_color=BG_COLOR,
    border_depth=20,
    alpha_channel=0.9,  # Прозрачность окна
    grab_anywhere=True
)


if __name__ == "__main__":
    #  Цикл для работы с окном
    while True:
        event, values = window.read()
        if event in invest_news_titles:
            sg.popup_scrolled(
                "\n\n".join(rbc.news_text(event)),
                title=event,
                background_color=BG_COLOR,
                button_color=BUTTON_COLOR,
                size=(100, 20),
                no_sizegrip=True,
                grab_anywhere=True
            )
        if event == CLOSE_BUTTON_TEXT or event == sg.WIN_CLOSED:
            break
    window.close()
