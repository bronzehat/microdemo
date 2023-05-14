# -*- coding: utf-8 -*-
"""
В этом модуле представлен парсер новостей с РБК Инвестиций
"""
import re
from requests_html import HTMLSession


RBC_INVEST_URL = "https://quote.rbc.ru"
EXCLUDE_ARTICLE_PATTERNS = [re.compile("\n.*,.*"),
                            re.compile("Фото:"),
                            re.compile("^$"),
                            ]


class RBCParser:
    """
    Класс для парсинга новостей инвестиций с сайта РБК
    """
    def __init__(self):
        self.session = HTMLSession()
        self.response = self.session.get(RBC_INVEST_URL)

    @property
    def invest_news(self):
        """
        Представляем новости и ссылки на их подробный текст в виде словаря.
        Ключ - заголовок статьи, время публикации и количество комментов.
        Значение - ссылка на статью.
        """
        all_news = self.response.html.find('.news-feed .news-feed__item')
        return {i.text: url
                for i in all_news for url in i.links
                if i.text and RBC_INVEST_URL in url
                }

    def news_text(self, title):
        """
        :param title: заголовок новости
        :return: очищенный текст новости
        """
        text_response = self.session.get(self.invest_news[title])
        news_text = [i.text.replace(u'\xa0', u' ')
                     for i in text_response.html.find("div.article__text > p")
                     if not any(re.search(exp, i.text) for exp in EXCLUDE_ARTICLE_PATTERNS)]
        return news_text
