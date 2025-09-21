# callbacks.py
# Callback функции для обработки взаимодействий
from dash import Input, Output, callback, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from user_config import RECOMMENDATIONS_MAP, DEFAULT_RECOMMENDATIONS, SALARY_RANGES

def register_callbacks(app, merged_data, skill_counts):
    """Регистрация callback функций"""
    
    @app.callback(
        [Output('profession-summary', 'children'),
         Output('experience-distribution', 'figure'),
         Output('education-distribution', 'figure'),
         Output('university-distribution', 'figure'),
         Output('skills-distribution', 'figure'),
         Output('salary-expectations', 'figure'),
         Output('career-preferences', 'figure'),
         Output('career-recommendations', 'children'),
         Output('comparison-chart', 'figure')],
        [Input('profession-selector', 'value'),
         Input('compare-selector', 'value')]
    )
    def update_dashboard(selected_profession, compare_professions):
        if merged_data.empty:
            return get_empty_state()
        
        if not selected_profession:
            return get_default_state()
        
        # Фильтруем данные по выбранной профессии
        profession_data = merged_data[merged_data['role'] == selected_profession]
        
        # Сводка по профессии
        summary = create_profession_summary(selected_profession, profession_data)
        
        # Графики
        exp_fig = create_experience_chart(profession_data)
        edu_fig = create_education_chart(profession_data)
        uni_fig = create_university_chart(profession_data)
        skills_fig = create_skills_chart(skill_counts)
        salary_fig = create_salary_chart(selected_profession)
        career_fig = create_career_chart(profession_data)
        
        # Рекомендации
        recommendations = create_recommendations(selected_profession)
        
        # График сравнения
        compare_fig = create_comparison_chart(selected_profession, compare_professions, merged_data)
        
        return summary, exp_fig, edu_fig, uni_fig, skills_fig, salary_fig, career_fig, recommendations, compare_fig

def get_empty_state():
    """Состояние при отсутствии данных"""
    empty_fig = go.Figure().update_layout(
        plot_bgcolor='white', 
        paper_bgcolor='rgba(0,0,0,0)',
        title='Данные не загружены. Проверьте подключение к БД.'
    )
    
    summary = html.P("Не удалось подключиться к базе данных. Проверьте настройки подключения.", 
                    style={'color': '#e74c3c', 'fontSize': '16px'})
    
    recommendations = html.Div([
        html.P("Ошибка подключения:", style={'fontWeight': 'bold', 'color': '#2c3e50'}),
        html.P("Проверьте параметры подключения к PostgreSQL", style={'margin': '5px 0', 'color': '#34495e'})
    ])
    
    return summary, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, recommendations, empty_fig

def get_default_state():
    """Состояние по умолчанию (профессия не выбрана)"""
    empty_fig = go.Figure().update_layout(
        plot_bgcolor='white', 
        paper_bgcolor='rgba(0,0,0,0)',
        title='Выберите профессию для анализа'
    )
    
    summary = html.P("Выберите профессию из списка выше чтобы увидеть детальную статистику", 
                    style={'color': '#7f8c8d', 'fontSize': '16px'})
    
    recommendations = html.Div([
        html.P("Чтобы начать анализ:", style={'fontWeight': 'bold', 'color': '#2c3e50'}),
        html.Div([
            html.P("Выберите профессию из выпадающего списка", style={'margin': '5px 0', 'color': '#34495e'}),
            html.P("Изучите статистику и требования", style={'margin': '5px 0', 'color': '#34495e'}),
            html.P("Посмотрите рекомендации для развития", style={'margin': '5px 0', 'color': '#34495e'})
        ])
    ])
    
    return summary, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, recommendations, empty_fig

def create_profession_summary(selected_profession, profession_data):
    """Создание сводки по профессии"""
    from dash import html
    
    total_people = len(profession_data)
    avg_experience = profession_data['experiance'].mean() if not profession_data.empty else 0
    common_education = profession_data['level'].mode()[0] if not profession_data.empty and not profession_data['level'].mode().empty else 'Нет данных'
    
    return html.Div([
        html.H4(f"Профессия: {selected_profession}", style={'color': '#2c3e50', 'marginBottom': '15px'}),
        html.Div([
            html.Div([
                html.P(f"Всего специалистов", style={'fontWeight': 'bold', 'margin': '0'}),
                html.P(f"{total_people}", style={'fontSize': '24px', 'color': '#3498db', 'margin': '5px 0'})
            ], style={'display': 'inline-block', 'margin': '0 20px'}),
            html.Div([
                html.P(f"Средний опыт", style={'fontWeight': 'bold', 'margin': '0'}),
                html.P(f"{avg_experience:.1f} лет", style={'fontSize': '24px', 'color': '#e74c3c', 'margin': '5px 0'})
            ], style={'display': 'inline-block', 'margin': '0 20px'}),
            html.Div([
                html.P(f"Уровень образования", style={'fontWeight': 'bold', 'margin': '0'}),
                html.P(f"{common_education}", style={'fontSize': '18px', 'color': '#27ae60', 'margin': '5px 0'})
            ], style={'display': 'inline-block', 'margin': '0 20px'})
        ], style={'textAlign': 'center'})
    ])

def create_experience_chart(profession_data):
    """График распределения опыта"""
    if not profession_data.empty:
        fig = px.histogram(profession_data, x='experiance', 
                          title='Распределение опыта работы',
                          nbins=8, 
                          color_discrete_sequence=['#3498db'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return create_empty_chart('Нет данных для отображения')

def create_education_chart(profession_data):
    """График образования"""
    if not profession_data.empty:
        edu_data = profession_data['level'].value_counts().reset_index()
        edu_data.columns = ['level', 'count']
        fig = px.pie(edu_data, values='count', names='level',
                    title='Уровень образования',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return create_empty_chart('Нет данных для отображения')

def create_university_chart(profession_data):
    """График университетов"""
    if not profession_data.empty:
        uni_data = profession_data['university'].value_counts().reset_index()
        uni_data.columns = ['university', 'count']
        fig = px.bar(uni_data.head(6), x='university', y='count',
                    title='Топ университетов',
                    color='count', 
                    color_continuous_scale='blues')
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return create_empty_chart('Нет данных для отображения')

def create_skills_chart(skill_counts):
    """График навыков"""
    if not skill_counts.empty:
        fig = px.bar(skill_counts.head(8), x='skill', y='count',
                   title='Топ востребованных навыков',
                   color='count', 
                   color_continuous_scale='purples')
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return create_empty_chart('Нет данных для отображения')

def create_salary_chart(selected_profession):
    """График зарплатных ожиданий"""
    salary_data = pd.DataFrame({
        'Опыт': ['0-2 года', '3-5 лет', '6-10 лет', '10+ лет'],
        'Зарплата': SALARY_RANGES.get(selected_profession, [50000, 80000, 120000, 180000])
    })
    
    fig = px.bar(salary_data, x='Опыт', y='Зарплата',
               title='Зарплатные ожидания',
               color='Зарплата', 
               color_continuous_scale='teal')
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(tickprefix='₽', tickformat=',.0f')
    return fig

def create_career_chart(profession_data):
    """График карьерных предпочтений"""
    if not profession_data.empty:
        career_data = profession_data['description'].value_counts().reset_index()
        career_data.columns = ['preference', 'count']
        fig = px.bar(career_data, x='preference', y='count',
                   title='Карьерные предпочтения',
                   color='count', 
                   color_continuous_scale='oranges')
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return create_empty_chart('Нет данных для отображения')

def create_recommendations(selected_profession):
    """Создание рекомендаций"""
    from dash import html
    
    rec_list = RECOMMENDATIONS_MAP.get(selected_profession, DEFAULT_RECOMMENDATIONS)
    return html.Div([
        html.H5("Рекомендации для развития:", style={'color': '#2c3e50', 'marginBottom': '15px'}),
        html.Div([
            html.P(item, style={
                'margin': '10px 0', 
                'color': '#34495e', 
                'paddingLeft': '0',
                'borderLeft': 'none',
                'listStyleType': 'none'
            }) for item in rec_list
        ])
    ])

def create_comparison_chart(selected_profession, compare_professions, merged_data):
    """График сравнения профессий"""
    if compare_professions and not merged_data.empty:
        compare_data = merged_data[merged_data['role'].isin([selected_profession] + compare_professions)]
        if not compare_data.empty:
            fig = px.box(compare_data, x='role', y='experiance', 
                        title='Сравнение опыта работы',
                        color='role')
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
            return fig
        else:
            return create_empty_chart('Нет данных для сравнения')
    else:
        return create_empty_chart('Выберите профессии для сравнения')

def create_empty_chart(title):
    """Создание пустого графика"""
    return go.Figure().update_layout(
        plot_bgcolor='white', 
        paper_bgcolor='rgba(0,0,0,0)',
        title=title
    )