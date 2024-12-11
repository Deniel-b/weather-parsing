import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def get_weather_data(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    days = []
    temperatures = []

    _days = soup.find_all("span", class_="hdr__inner")
    _table = soup.find_all("span", class_="text text_block text_bold_medium margin_bottom_10")

    for day in _days:
        days.append(day.text.strip())

    temp_values = []
    for temp in _table:
        temp_values.append(temp.text.strip())

    for i in range(0, len(temp_values), 4):
        day_temps = list(map(lambda x: int(x.replace("+", "").replace("\u2212", "-").replace("\u00b0", "")), temp_values[i:i+4]))
        temperatures.append(day_temps)

    return days, temperatures

def plot_weather(days, temperatures):
    times_of_day = ['ночь', 'утро', 'день', 'вечер']

    plt.figure(figsize=(12, 6))

    for i, time in enumerate(times_of_day):
        temps_at_time = [temps[i] for temps in temperatures]
        plt.plot(days, temps_at_time, label=f"{time}")

    plt.title("Прогноз погоды на 14 дней")
    plt.xlabel("Дни")
    plt.ylabel("Температура, °C")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = "https://pogoda.mail.ru/prognoz/arzamas/14dney/"
    days, temperatures = get_weather_data(url)
    plot_weather(days, temperatures)
