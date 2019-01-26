import os
import requests

import arrow
from bs4 import BeautifulSoup
from flask import render_template


class HandlersManager:

    def __init__(self):
        self.__arguments = None

    def handle_intent(self, intent: str, **kwargs) -> callable:
        self.__arguments = kwargs

        if intent == 'mail':
            return self.__mail_request_handler()

        elif intent == 'news':
            return self.__news_request_handler()

        elif intent == 'weather':
            return self.__weather_request_handler()

        elif intent == 'call':
            return self.__call_request_handler()

        elif intent == 'search':
            return self.__search_request_handler()

        else:
            return self.__default_handler()

    def __default_handler(self):
        answer = self.__arguments.get('answer')

        return render_template('start.html', text=answer)

    def __mail_request_handler(self):
        answer = self.__arguments.get('answer')

        function = 'window.open("https://www.google.com/gmail/");'

        return render_template('mail.html', text=answer, function=function)

    def __news_request_handler(self):
        answer = self.__arguments.get('answer')
        params = self.__arguments.get('params')

        rss_url = 'https://www.tvn24.pl/najwazniejsze.xml'
        if params:
            try:
                geo_country = params['geo-country']
                if geo_country == 'Polska':
                    rss_url =\
                        'https://www.tvn24.pl/wiadomosci-z-kraju,3.xml'

            except KeyError as err:
                print(err)

        resp = requests.get(rss_url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, features="xml")
            output = HandlersManager.__tvn_soup_to_items(soup)
        else:
            output = "error"

        return render_template('news.html', tvn_news=output, text=answer)

    def __weather_request_handler(self):
        answer = self.__arguments.get('answer')
        params = self.__arguments.get('params')

        if params:
            try:
                city = params['miasto']
            except KeyError:
                city = 'Warsaw'
        api_key = os.environ.get('weather_api_key')

        if not api_key:
            return render_template('start.html', text=answer)

        current, forecast = HandlersManager.__get_weather_data(city, api_key)
        current_processed =\
            HandlersManager.__process_weather_current(current)
        forecast_processed = \
            HandlersManager.__process_weather_forecast(forecast)

        return render_template('weather.html', text=answer,
                               current=current_processed,
                               forecast=forecast_processed)

    def __call_request_handler(self):
        answer = self.__arguments.get('answer')
        params = self.__arguments.get('params')

        if params:
            try:
                name = params['given-name']
                mail = name.replace(" ", ".")
                mail += "@gmail_fake.com"

            except KeyError:
                mail = "krewny@krewny.pl"

        return render_template('hangouts.html', text=answer, mail=mail)

    def __search_request_handler(self):
        base_url = "http://www.google.com/search?q="

        answer = self.__arguments.get('answer')
        params = self.__arguments.get('params')

        if params:
            try:
                query = params['search-query']
                query_formatted = query.replace(" ", "+")
            except KeyError:
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
    def __convert_date(date_str: str, locale='pl_PL'):
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

    @staticmethod
    def __get_weather_data(city: str, api_key):
        base_url = 'http://api.openweathermap.org/data/2.5/'

        current_url = '{}{}?q={}&lang={}&units=metric&appid={}'\
            .format(base_url, 'weather', city, 'pl', api_key)

        forecast_url = '{}{}?q={}&lang={}&units=metric&appid={}'\
            .format(base_url, 'forecast', city, 'pl', api_key)

        try:
            current = requests.get(current_url).json()
            forecast = requests.get(forecast_url).json()

        except requests.exceptions.HTTPError:
            current = None
            forecast = None

        return current, forecast

    @staticmethod
    def __process_weather_current(weather_data: dict) -> dict:

        processed = {}
        try:
            icon_id = weather_data['weather'][0]['icon']
            processed['icon_url'] = 'http://openweathermap.org/img/w/{}.png'\
                .format(icon_id)
            processed['temp'] = weather_data['main']['temp']
            processed['description'] =\
                weather_data['weather'][0]['description']
        except KeyError:
            pass

        return processed

    @staticmethod
    def __process_weather_forecast(weather_data: dict) -> list:
        processed = []

        try:
            allowed_cnt = min(18, weather_data['cnt'])
            forecasts = weather_data['list'][4:allowed_cnt:4]

            for forecast in forecasts:
                forecast_data = {}

                date = arrow.get(forecast['dt_txt'],
                                 'YYYY-MM-DD HH:mm:ss')
                icon_id = forecast['weather'][0]['icon']

                forecast_data['date'] = date.format('DD MMM, H:mm',
                                                    locale="pl_PL")
                forecast_data['date_desc'] = date.humanize(locale='pl_PL')
                forecast_data['icon_url'] = 'http://openweathermap.org/img/w/{}.png'\
                    .format(icon_id)
                forecast_data['temp'] = forecast['main']['temp']
                forecast_data['description'] = forecast['weather'][0]['description']

                processed.append(forecast_data)

        except KeyError:
            pass

        return processed


