# app.py
# hr_dashboard_app.py
import dash
from hr_data_processing import DataProcessor
from hr_layout import create_layout
from hr_callbacks import register_callbacks

def create_dash_hr_app(flask_app):
    # Инициализация обработчика данных
    data_processor = DataProcessor()

    # Создание Dash приложения с правильным порядком параметров
    app = dash.Dash(
        name='dashboard_hr',  # Уникальное имя должно быть первым
        server=flask_app,
        url_base_pathname='/dash_hr/',
        assets_folder='assets'
    )

    # Установка layout
    app.layout = create_layout(data_processor)

    # Регистрация callback функций
    register_callbacks(app, data_processor)

    return app