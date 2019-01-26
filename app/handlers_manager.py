import requests

import arrow
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
            output = "error"

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

        if query:
            query_formatted = query.replace(" ", "+")
        else:
            query_formatted = ""

        function = 'window.open(\"{}\");'.format(base_url+query_formatted)

        return render_template('search.html', text=answer, function=function)

    @staticmethod
    def __tvn_soup_to_items(soup: BeautifulSoup) -> list:

        output = []
        for item in soup.findAll('item'):

            title = item.find('title').contents[0]
            if title.replace(" ", "") == "" or title == "<![CDATA[ ]]>":
                continue

            date_str = item.find('pubDate').contents[0]
            converted_date = HandlersManager.__convert_date(date_str,
                                                            locale='pl_PL')

            item_dict = dict()
            item_dict['title'] = title
            item_dict['description'] = item.find('description').contents[0]
            item_dict['link'] = item.find('link').contents[0]
            item_dict['date'] = converted_date
            output.append(item_dict)

        return output


    @staticmethod
    def __convert_date(date_str:str, locale='pl_PL'):
        try:
            date_obj = arrow.get(date_str,
                                 'ddd, DD MMM YY HH:mm:ss Z')
            description = date_obj.humanize(locale=locale)
            converted_date = date_obj \
                .format('dddd, D MMMM YYYY, H:mm', locale=locale)

            converted_date += ' ({}) '.format(description)
        except arrow.parser.ParserError:
            converted_date = date_str

        return converted_date

