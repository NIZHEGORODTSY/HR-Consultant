# app.py
import dash
from data_processing import DataProcessor
from layout import create_layout
from callbacks import register_callbacks


def create_dash_app(flask_app):
    # Инициализация обработчика данных
    data_processor = DataProcessor()

    # Создание Dash приложения
    app = dash.Dash(__name__, server=flask_app, update_title='/dash/', assets_folder='assets')

    # Установка layout
    app.layout = create_layout(data_processor)

    # Регистрация callback функций
    register_callbacks(app, data_processor)

    # Запуск приложения
    return app
