# user_dashboard_app.py
import dash
from dash import html
from user_database import load_data_from_db, get_empty_dataframes, explore_database_structure
from user_layout import create_layout
from user_callbacks import register_callbacks

def create_dash_user_app(flask_app):
    explore_database_structure()

    # Загружаем данные
    users, skills, roles, educations, career_preferences, merged_data, skill_counts, role_stats = load_data_from_db()

    # Проверяем, что данные загрузились
    if users is None:
        users, skills, roles, educations, career_preferences, merged_data, skill_counts, role_stats = get_empty_dataframes()

    print(f"Загружено пользователей: {len(users)}")
    print(f"Загружено навыков: {len(skills)}")
    print(f"Загружено ролей: {len(roles)}")
    print(f"Загружено образований: {len(educations)}")
    print(f"Загружено карьерных предпочтений: {len(career_preferences)}")
    print(f"Объединенных данных: {len(merged_data)}")

    if not merged_data.empty:
        print("Колонки в объединенных данных:", merged_data.columns.tolist())

    # Создаем экземпляр Dash приложения с правильным порядком параметров
    app = dash.Dash(
        name='dashboard_user',  # Уникальное имя должно быть первым
        server=flask_app,
        url_base_pathname='/dash_user/'
    )

    # Устанавливаем layout
    app.layout = create_layout(role_stats)

    # Регистрация callback функций
    register_callbacks(app, merged_data, skill_counts)

    # HTML шаблон с CSS стилями
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>USER DASH</title>
            {%favicon%}
            {%css%}
            <style>
                .metric-card {
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 10px;
                    min-width: 200px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    flex: 1;
                }
                
                .graph-container {
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .filter-container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .data-table {
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .data-table th {
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }
                
                .data-table td {
                    padding: 10px;
                    border-bottom: 1px solid #e0e0e0;
                }
                
                .data-table tr:hover {
                    background-color: 'white';
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    return app