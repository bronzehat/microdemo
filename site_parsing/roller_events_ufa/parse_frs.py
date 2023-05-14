# -*- coding: utf-8 -*-
"""
В этом модуле представлен парсер объявлений с сайта
Федерации Роллер Спорта (Уфа)
"""
import re
from datetime import date, datetime
from requests_html import HTMLSession


# URL сайта ФРС
FRS_EVENTS_URL = "http://xn--80akranlerj.xn--p1ai/sample-page/" \
                 "%D0%BC%D0%B5%D1%80%D0%BE%D0%BF%D1%80%D0%B8%D1%8F%D1%82%D0%B8%D1%8F/"


class FRSParser:
    """
    Класс для парсинга сайта ФРС
    """

    def __init__(self):
        self.session = HTMLSession()
        self.response = self.session.get(FRS_EVENTS_URL)
        self.today = date.today()
        self.months = dict(zip(
            range(1, 12),
            ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
             "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")))
        self.css_locator = ".elementor-widget-container"

    def get_month_by_date(self, next_month=False):
        """
        Получаем фразу для парсинга событий месяца,
        исходя из текущего месяца и года
        :param next_month: если True, ответ будет для следующего
        месяца
        :return: фраза вида "Январь 1973"
        """
        month_number = date.today().month
        if next_month:
            month_number += 1
        return ' '.join([self.months[month_number], str(date.today().year)])

    def is_future_event(self, event):
        """
        Проверяем, не прошло ли событие на данный момент
        :param event: строка события с датой и описанием
        :return: Trye, если событие будущее
        """
        # Получаем даты
        event_date = event.split(" —", 1)[0]
        # Если дата не одна, а промежуток, берём только первую
        if re.search("\d{1,2}.\d{2}.\d{4}-\d{1,2}.\d{2}.\d{4}", event_date):
            event_date = event_date.split("-")[0]
        # Если строка не парсится как дата, выведи её, как есть
        try:
            event_date = datetime.strptime(event_date, '%d.%m.%Y').date()
        except ValueError:
            return True
        return True if event_date > self.today else False

    def get_current_year_events(self):
        """
        Получаем все события на текущий год
        :return:
        """
        this_year_events = [
            i for i in self.response.html.find(self.css_locator)
            if f"Календарь мероприятий {date.today().year}" in i.text]
        return this_year_events

    def filter_events(self, content, month):
        """
        Фильтруем события по дате:
        - удаляем все события, которые не начинаются с даты
        или выражения из get_month_by_date()
        - удаляем события, которые уже прошли
        :param content: текст с событиями
        :param month: выражение вида "Январь 1973"
        :return:
        """
        # Делаем копию списка, чтобы итерироваться и
        # одновременно удалять ненужные элементы
        for event in content[:]:
            if event[0].isalpha():
                # Если строка начинается не с даты и не с выражения типа
                # "Месяц Год" - скорее всего, поставили ненужный перенос
                # строки. Добавляем её к предыдущему элементу.
                if not event.startswith(month):
                    content[content.index(event)-1] += ". " + event
                    content.remove(event)
            elif not self.is_future_event(event):
                # Если событие прошло или уже началось - удаляем
                content.remove(event)
        # Сортируем результат, т.к. события могут идти не по порядку
        content.sort()
        return content

    def get_events_by_month(self, month):
        """
        Получаем все события для заданного месяца
        :param month: выражение вида "Январь 1973"
        :return: все события за данный месяц
        """
        # Берём только события за нужный месяц и
        # удаляем ненужные символы из вывода
        month_events = [
            i.text.replace('\xa0', '')
            for i in self.response.html.find(self.css_locator)
            if f"{month}" in i.text]
        if month_events:
            return month_events[0].splitlines()[1:]

    def get_future_month_events(self):
        """
        Получаем события для следующего месяца, если
        прошло больше половины текущего месяца
        :return:
        """
        if self.today.day > 15:
            month = self.get_month_by_date(next_month=True)
            content = self.get_events_by_month(month)
            filtered_content = self.filter_events(content, month)
            return '\n\n'.join(filtered_content)

    def get_current_month_events(self):
        """
        Получаем события для текущего месяца
        :return:
        """
        month = self.get_month_by_date()
        content = self.get_events_by_month(month)
        filtered_content = self.filter_events(content, month)
        return '\n\n'.join(filtered_content)
