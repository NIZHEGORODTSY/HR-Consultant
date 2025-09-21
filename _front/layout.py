# layout.py
from dash import dcc, html
from datetime import datetime
from data_processing import DataProcessor


def create_layout(data_processor):
    """Создание layout дашборда"""
    # Получаем данные для графиков
    skill_counts = data_processor.get_skill_counts()
    role_stats = data_processor.get_role_stats()
    education_stats = data_processor.get_education_stats()
    university_stats = data_processor.get_university_stats()
    role_university = data_processor.get_role_university_crosstab()
    career_pref_stats = data_processor.get_career_pref_stats()
    speciality_stats = data_processor.get_speciality_stats()
    sunburst_data = data_processor.get_sunburst_data()

    return html.Div([
        # Шапка дашборда
        html.Div([
            html.H1("HR Analytics Dashboard", style={
                'color': 'white', 'margin': '0', 'fontSize': '2.5em', 'fontWeight': 'bold'
            }),
            html.P("Комплексный анализ компетенций и карьерных траекторий", style={
                'color': '#ecf0f1', 'margin': '0', 'fontSize': '1.1em'
            }),
            html.P(f"Данные обновлены: {datetime.now().strftime('%Y-%m-%d %H:%M')}", style={
                'color': '#ecf0f1', 'margin': '10px 0 0 0', 'fontSize': '0.9em'
            })
        ], style={
            'backgroundColor': "#338feb", 'padding': '20px 40px',
            'borderBottom': '3px solid #3498db'
        }),

        # Основной контент
        html.Div([
            # Статистика в карточках
            create_metrics_cards(data_processor),

            # Графики
            create_charts(
                university_stats, role_university, role_stats, education_stats,
                skill_counts, data_processor.roles, career_pref_stats, speciality_stats, sunburst_data
            ),

            # Фильтры для данных
            create_filters(data_processor),

            # Таблица с данными
            html.Div([
                html.H4("Данные сотрудников", style={'color': '#2c3e50', 'marginBottom': '15px'}),
                html.Div(id='data-table')
            ], style={'margin': '30px 0'})

        ], style={
            'padding': '20px',
            'backgroundColor': '#f0f8ff',
            'minHeight': '100vh'
        })
    ])


def create_metrics_cards(data_processor):
    """Создание карточек с метриками"""
    skill_counts = data_processor.get_skill_counts()
    university_stats = data_processor.get_university_stats()

    return html.Div([
        html.Div([
            html.H4("Всего сотрудников", style={'color': '#2c3e50'}),
            html.H2(f"{len(data_processor.users)}", style={'color': '#27ae60', 'fontSize': '2.5em'})
        ], className='metric-card'),

        html.Div([
            html.H4("Уникальных навыков", style={'color': '#2c3e50'}),
            html.H2(f"{skill_counts['skill'].nunique() if not skill_counts.empty else 0}",
                    style={'color': '#3498db', 'fontSize': '2.5em'})
        ], className='metric-card'),

        # html.Div([
        #    html.H4("Средний опыт", style={'color': '#2c3e50'}),
        #    html.H2(f"{data_processor.roles['experience'].mean():.1f if not data_processor.roles.empty and 'experience' in data_processor.roles.columns else 0} лет", 
        #           style={'color': '#e74c3c', 'fontSize': '2.5em'})
        # ], className='metric-card'),

        html.Div([
            html.H4("Университетов", style={'color': '#2c3e50'}),
            html.H2(f"{university_stats['university'].nunique() if not university_stats.empty else 0}",
                    style={'color': '#9b59b6', 'fontSize': '2.5em'})
        ], className='metric-card')
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px 0', 'flexWrap': 'wrap'})


def create_charts(university_stats, role_university, role_stats, education_stats,
                  skill_counts, roles, career_pref_stats, speciality_stats, sunburst_data):
    """Создание графиков"""
    import plotly.express as px

    return html.Div([
        # Первая строка графиков
        html.Div([
            html.Div([
                dcc.Graph(
                    id='university-chart',
                    figure=px.bar(university_stats, x='university', y='count',
                                  title='Распределение по университетам',
                                  color='count', color_continuous_scale='blues')
                    .update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
                    if not university_stats.empty else {}
                )
            ], className='graph-container'),

            html.Div([
                dcc.Graph(
                    id='role-university-chart',
                    figure=px.imshow(role_university,
                                     title='Профессии vs Университеты',
                                     color_continuous_scale='blues')
                    .update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
                    if not role_university.empty else {}
                )
            ], className='graph-container')
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'margin': '20px 0'}),

        # Остальные строки графиков (аналогично)
        # ... (остальной код создания графиков)

    ])


def create_filters(data_processor):
    """Создание фильтров"""
    return html.Div([
        html.H4("Фильтры данных", style={'color': '#2c3e50', 'marginBottom': '15px'}),
        html.Div([
            dcc.Dropdown(
                id='role-filter',
                options=[{'label': role, 'value': role} for role in
                         (data_processor.roles['role'].unique() if not data_processor.roles.empty else [])],
                placeholder='Фильтр по профессии',
                multi=True,
                style={'marginBottom': '10px'}
            ),
            dcc.Dropdown(
                id='university-filter',
                options=[{'label': uni, 'value': uni} for uni in (
                    data_processor.educations['university'].unique() if not data_processor.educations.empty else [])],
                placeholder='Фильтр по университету',
                multi=True,
                style={'marginBottom': '10px'}
            ),
            dcc.Dropdown(
                id='experience-filter',
                options=[
                    {'label': 'До 3 лет', 'value': '0-3'},
                    {'label': '3-5 лет', 'value': '3-5'},
                    {'label': '5-10 лет', 'value': '5-10'},
                    {'label': '10+ лет', 'value': '10+'}
                ],
                placeholder='Фильтр по опыту работы',
                multi=True
            )
        ])
    ], className='filter-container')
