import requests
from pprint import pprint
from bs4 import BeautifulSoup


def get_weather_data(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    _header = soup.find_all("h1", class_="hdr__inner")
    _days = soup.find_all("span", class_="hdr__inner")
    time = soup.find_all("span", class_="text text_block text_bold_normal text_fixed margin_bottom_10")
    _table = soup.find_all("span", class_="text text_block text_bold_medium margin_bottom_10")
    _tmp_one = []
    _tmp_table = []
    _tmp_time = []
    for i in range(len(_table)):
        if i != 0:
            if i % 4 == 0:
                _tmp_table.append(_tmp_one)
                _tmp_one = []
            _tmp_one.append(_table[i].text)
        else:
            _tmp_one.append(_table[i].text)

    _days.pop(-1)
    _tmp_one = []
    for i in range(len(time)):
        if i != 0:
            if i % 4 == 0:
                _tmp_time.append(_tmp_one)
                _tmp_one = []
            _tmp_one.append(time[i].text)
        else:
            _tmp_one.append(time[i].text)

    for i in range(len(_header)):
        print(_header[i].text)
        for n in range(len(_days)):
            print(_days[n].text)
            print(" ".join(_tmp_time[n]))
            print(" ".join(_tmp_table[n]))

get_weather_data("https://pogoda.mail.ru/prognoz/arzamas/14dney/")