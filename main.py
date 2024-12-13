import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.linear_model import LinearRegression
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go


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
        day_temps = list(
            map(lambda x: int(x.replace("+", "").replace("\u2212", "-").replace("\u00b0", "")), temp_values[i:i + 4]))
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


def create_dash_app():
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Button("Получить данные", id="fetch-data-button", n_clicks=0),
        dcc.Graph(id="weather-graph"),
        html.Div(id="hidden-data", style={"display": "none"})
    ])

    @app.callback(
        Output("weather-graph", "figure"),
        Input("fetch-data-button", "n_clicks"),
        prevent_initial_call=True
    )
    def update_graph(n_clicks):
        url = "https://pogoda.mail.ru/prognoz/arzamas/14dney/"
        days, temperatures = get_weather_data(url)

        predicted_days = [f"День {len(days) + i + 1}" for i in range(3)]
        predicted_temperatures = predict_temperatures(temperatures)

        times_of_day = ['ночь', 'утро', 'день', 'вечер']
        colors = ['blue', 'orange', 'green', 'red']

        fig = go.Figure()

        extended_days = days + predicted_days

        for i, (time, color) in enumerate(zip(times_of_day, colors)):
            temps_at_time = [temps[i] for temps in temperatures]
            future_temps = predicted_temperatures[i]

            # Сплошные линии для фактических данных
            fig.add_trace(go.Scatter(
                x=days,
                y=temps_at_time,
                mode='lines',
                name=f"{time}",
                line=dict(color=color)
            ))

            # Пунктирные линии для прогнозируемых данных
            future_x = extended_days[len(days):]
            fig.add_trace(go.Scatter(
                x=future_x,
                y=future_temps,
                mode='lines',
                name=f"{time} (прогноз)",
                line=dict(color=color, dash='dash')
            ))

            # Пунктирные соединяющие линии
            if len(days) > 0 and len(future_x) > 0:
                fig.add_trace(go.Scatter(
                    x=[days[-1], future_x[0]],
                    y=[temps_at_time[-1], future_temps[0]],
                    mode='lines',
                    line=dict(color=color, dash='dash'),
                    showlegend=False
                ))

        fig.update_layout(
            title="Прогноз погоды на 14 дней",
            xaxis_title="Дни",
            yaxis_title="Температура, °C",
            legend_title="Время суток",
            template="plotly_white"
        )

        return fig

    return app


if __name__ == "__main__":
    app = create_dash_app()
    app.run_server(debug=True)
