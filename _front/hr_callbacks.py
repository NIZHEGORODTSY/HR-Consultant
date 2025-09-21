# callbacks.py
from dash import Input, Output, html
from hr_data_processing import DataProcessor
import pandas as pd


def register_callbacks(app, data_processor):
    """Регистрация callback функций"""

    @app.callback(
        Output('data-table', 'children'),
        [Input('role-filter', 'value'),
         Input('university-filter', 'value'),
         Input('experience-filter', 'value')]
    )
    def update_table(selected_roles, selected_universities, selected_experience):
        filtered_data = data_processor.get_filtered_data(selected_roles, selected_universities, selected_experience)

        if filtered_data.empty:
            return html.Div("Нет данных для отображения", style={'color': 'red', 'padding': '20px'})

        return html.Table([
            html.Thead(html.Tr([
                html.Th('ФИО'), html.Th('Должность'), html.Th('Опыт'),
                html.Th('Образование'), html.Th('Университет'), html.Th('Специальность')
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(row['full_name']),
                    html.Td(row.get('role', 'Н/Д')),
                    html.Td(f"{row.get('experience', 'Н/Д')} лет" if pd.notna(row.get('experience')) else 'Н/Д'),
                    html.Td(row.get('level', 'Н/Д')),
                    html.Td(row.get('university', 'Н/Д')),
                    html.Td(row.get('speciality', 'Н/Д'))
                ]) for _, row in filtered_data.head(20).iterrows()
            ])
        ], className='data-table')
