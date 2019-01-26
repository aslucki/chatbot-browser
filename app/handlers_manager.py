from datetime import datetime
import requests

from bs4 import BeautifulSoup
from flask import render_template


class HandlersManager:

    @staticmethod
    def handle_intent(intent: str, answer=None, query=None) -> callable:
        if intent == 'mail':
            return HandlersManager.__mail_request_handler(answer)

        elif intent == 'news':
            return HandlersManager.__news_request_handler(answer)

        elif intent == 'weather':
            return HandlersManager.__weather_request_handler(answer)

        elif intent == 'call':
            return HandlersManager.__call_request_handler(answer)

        elif intent == 'search':
            return HandlersManager.__search_request_handler(answer, query)

        else:
            return HandlersManager.__default_handler(answer)

    @staticmethod
    def __default_handler(answer):
        return render_template('start.html', text=answer)

    @staticmethod
    def __mail_request_handler(answer):

        function = 'window.open("https://www.google.com/gmail/");'

        return render_template('mail.html', text=answer, function=function)

    @staticmethod
    def __news_request_handler(answer):

        resp = requests.get('https://www.tvn24.pl/najwazniejsze.xml')
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, features="xml")
            output = HandlersManager.__tvn_soup_to_items(soup)
        else:
            pass

        return render_template('news.html', tvn_news=output, text=answer)

    @staticmethod
    def __weather_request_handler(answer):

        return render_template('weather.html', text=answer)

    @staticmethod
    def __call_request_handler(answer):
        return render_template('hangouts.html', text=answer)

    @staticmethod
    def __search_request_handler(answer, query):

        base_url = "http://www.google.com/search?q="
        query_formated = query.replace(" ", "+")

        function = 'window.open(\"{}\");'.format(base_url+query_formated)

        return render_template('search.html', text=answer, function=function)

    @staticmethod
    def __tvn_soup_to_items(soup: BeautifulSoup) -> list:
        output = []
        for item in soup.findAll('item'):

            title = item.find('title').contents[0]
            if title.replace(" ", "") == "" or title == "<![CDATA[ ]]>":
                continue

            date = item.find('pubDate').contents[0]
            converted_date = datetime\
                .strptime(date, '%a, %d %b %y %H:%M:%S %z')\
                .strftime('%A, %d %B %Y, godzina: %H:%M')

            item_dict = dict()
            item_dict['title'] = title
            item_dict['description'] = item.find('description').contents[0]
            item_dict['link'] = item.find('link').contents[0]
            item_dict['date'] = converted_date
            output.append(item_dict)

        return output
