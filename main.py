import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

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

def predict_temperatures(temperatures):
    times_of_day = ['ночь', 'утро', 'день', 'вечер']
    predictions = []

    for i in range(4):
        temps = [temp[i] for temp in temperatures]
        days = np.arange(len(temps)).reshape(-1, 1)
        model = LinearRegression()
        model.fit(days, temps)
        future_days = np.arange(len(temps), len(temps) + 3).reshape(-1, 1)
        predicted_temps = model.predict(future_days).tolist()
        predictions.append(predicted_temps)

    return predictions

def plot_weather(days, temperatures, predicted_days, predicted_temperatures):
    times_of_day = ['ночь', 'утро', 'день', 'вечер']

    plt.figure(figsize=(12, 6))

    extended_days = days + predicted_days

    for i, time in enumerate(times_of_day):
        temps_at_time = [temps[i] for temps in temperatures]
        plt.plot(days, temps_at_time, label=f"{time}")

        future_temps = predicted_temperatures[i]
        future_x = extended_days[len(days):]
        plt.plot(future_x, future_temps, linestyle="--", label=f"{time} (прогноз)")

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

    predicted_days = [f"День {len(days) + i + 1}" for i in range(3)]
    predicted_temperatures = predict_temperatures(temperatures)

    plot_weather(days, temperatures, predicted_days, predicted_temperatures)
