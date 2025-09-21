# layout.py
# Создание layout приложения
from dash import dcc, html

def create_layout(role_stats):
    """Создание layout приложения"""
    return html.Div([
        # Шапка дашборда
        html.Div([
            html.H1("USER DASH", style={
                'color': 'white', 'margin': '0', 'fontSize': '2.5em', 'fontWeight': 'bold'
            }),
            html.P("Найди свою идеальную профессию и узнай всё о карьерных возможностях", style={
                'color': '#ecf0f1', 'margin': '0', 'fontSize': '1.1em'
            })
        ], style={
            'backgroundColor': '#338feb', 'padding': '20px 40px',
            'borderBottom': '3px solid #3498db'
        }),
        
        # Основной контент
        html.Div([
            # Блок выбора профессии
            html.Div([
                html.Div([
                    html.H3("Выберите профессию для анализа", style={
                        'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'
                    }),
                    dcc.Dropdown(
                        id='profession-selector',
                        options=[{'label': f"{role} ({count} чел.)", 'value': role} 
                                for role, count in zip(role_stats['role'], role_stats['count'])] if not role_stats.empty else [],
                        placeholder='Выберите профессию...',
                        style={'marginBottom': '20px', 'maxWidth': '600px', 'margin': '0 auto'}
                    ),
                    
                    html.Div(id='profession-summary', style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'textAlign': 'center',
                        'maxWidth': '800px',
                        'margin': '0 auto'
                    })
                ], style={'width': '100%'})
            ], style={'margin': '20px 0', 'textAlign': 'center'}),
            
            # Статистика выбранной профессии
            html.Div([
                html.H3("Статистика профессии", style={
                    'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'
                })
            ], style={'margin': '20px 0'}),
            
            html.Div([
                # Опыт работы
                html.Div([
                    dcc.Graph(id='experience-distribution')
                ], className='graph-container'),
                
                # Образование
                html.Div([
                    dcc.Graph(id='education-distribution')
                ], className='graph-container'),
                
                # Университеты
                html.Div([
                    dcc.Graph(id='university-distribution')
                ], className='graph-container'),
                
                # Навыки
                html.Div([
                    dcc.Graph(id='skills-distribution')
                ], className='graph-container'),
                
                # Зарплатные ожидания
                html.Div([
                    dcc.Graph(id='salary-expectations')
                ], className='graph-container'),
                
                # Карьерные предпочтения
                html.Div([
                    dcc.Graph(id='career-preferences')
                ], className='graph-container')
            ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'margin': '20px 0'}),
            
            # Рекомендации
            html.Div([
                html.H3("Рекомендации для развития", style={
                    'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'
                }),
                html.Div(id='career-recommendations', style={
                    'backgroundColor': 'white',
                    'padding': '25px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'maxWidth': '1000px',
                    'margin': '0 auto'
                })
            ], style={'margin': '20px 0', 'textAlign': 'center'}),
            
            # Сравнение с другими профессиями
            html.Div([
                html.H3("Сравнение с другими профессиями", style={
                    'color': '#2c3e50', 'marginBottom': '20px', 'textAlign': 'center'
                }),
                dcc.Dropdown(
                    id='compare-selector',
                    options=[{'label': role, 'value': role} for role in role_stats['role']] if not role_stats.empty else [],
                    placeholder='Выберите профессии для сравнения...',
                    multi=True,
                    style={'marginBottom': '20px', 'maxWidth': '600px', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Graph(id='comparison-chart')
                ], className='graph-container', style={'maxWidth': '1000px', 'margin': '0 auto'})
            ], style={'margin': '30px 0', 'textAlign': 'center'})
            
        ], style={
            'padding': '20px', 
            'backgroundColor': '#f0f8ff',
            'minHeight': '100vh'
        })
    ])