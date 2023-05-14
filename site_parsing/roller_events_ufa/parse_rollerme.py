# -*- coding: utf-8 -*-
"""
В этом модуле представлен парсер объявлений с сайта
роллер школы RollerMe (Уфа)
"""
import re
from datetime import datetime, date
from requests_html import HTMLSession

ROLLERME_EVENTS_URL = "https://roller-me.ru/activity.html"
ANNOUNCE_AGE_IN_DAYS = 14
ANNOUNCE_CSS_SELECTOR = ".post-item-description"


class RollermeParser:

    def __init__(self):
        self.session = HTMLSession()
        self.response = self.session.get(ROLLERME_EVENTS_URL)

    def get_all_announces(self):
        return self.response.html.find(ANNOUNCE_CSS_SELECTOR)

    @staticmethod
    def is_fresh_announce(announce):
        now = date.today()
        publication_date = announce.text.split('\n', 1)[0]
        publication_date = datetime.strptime(publication_date, '%d-%m-%Y').date()
        return True if (now - publication_date).days < ANNOUNCE_AGE_IN_DAYS else False

    def get_fresh_announces(self):
        announces = dict()
        for announce in self.get_all_announces():
            if self.is_fresh_announce(announce):
                # Отфильтровываем объявления о прошедших событиях
                if not re.search('[П|п]рошли|[Б|б]ыли', announce.text):
                    for url in announce.absolute_links:
                        event_page = self.session.get(url)
                        event_title = event_page.html.find(".heading-text")[0].text
                        event_info = event_page.html.find(ANNOUNCE_CSS_SELECTOR)[0].text
                        event_schedule = event_page.html.find(".card")[0].text
                        announces[event_title] = (event_info, event_schedule, url)
        return announces
