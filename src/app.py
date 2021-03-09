import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import altair as alt
from vega_datasets import data
import numpy as np
import pandas as pd

alt.renderers.set_embed_options(actions=False)

# DATA

# ALl the player data for NBA
columns_to_skip = ['birth_year', 'birth_month', 'height','height_cm', 'weight', 'weight_kg', 'nationality', 'high_school', 'draft_round', 'draft_pick', 'draft_team']
player_data = pd.read_csv('https://github.com/naveen-chalasani/nba-analytics-heroku-app/raw/main/data/players_stats_by_season_full_details.csv', usecols = lambda x: x not in columns_to_skip)
player_data = player_data[player_data['League'] == 'NBA'].drop('League', axis = 1)
player_data['birth_date'] = pd.to_datetime(player_data['birth_date'], format='%b %d, %Y')
player_data['Season'] = pd.to_numeric(player_data['Season'].str.split(expand = True)[0])

# Data for Metrics / Key Performance Indicators
df_metrics = player_data[['Player', 'Stage', 'GP', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA']].copy()
df_metrics = df_metrics.groupby(['Player', 'Stage']).mean().reset_index().copy()
df_metrics['career_FG_%'] = round(df_metrics['FGM'] / df_metrics['FGA'] * 100, 2)
df_metrics['career_FT_%'] = round(df_metrics['FTM'] / df_metrics['FTA'] * 100, 2)
df_metrics['career_3PT_%'] = round(df_metrics['3PM'] / df_metrics['3PA'] * 100, 2)
df_metrics['Minutes_per_game'] = round(df_metrics['MIN'] / df_metrics['GP'], 2)
df_metrics.drop(['GP', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA'], axis = 1, inplace = True)

#  Data for Chart 1 
df_chart_1 = player_data[['Player', 'Season', 'Stage', 'GP', 'PTS', 'FGM', 'FTM', '3PM']].copy()
df_chart_1['PTS'] = df_chart_1['PTS'] / df_chart_1['GP']
df_chart_1['3 Point'] = (df_chart_1['3PM'] * 3) / df_chart_1['GP']
df_chart_1['FTM'] = df_chart_1['FTM'] / df_chart_1['GP']
df_chart_1.rename(columns={'FTM': 'Free throws'}, inplace = True)
df_chart_1['2 Point'] = df_chart_1['PTS'] - (df_chart_1['3 Point'] + df_chart_1['Free throws'])
df_chart_1.drop(['PTS', 'GP', 'FGM', '3PM'], axis = 1, inplace = True)
df_chart_1 = df_chart_1.melt(id_vars=['Player', 'Season', 'Stage'], var_name = 'Points_type', value_name = "Points_per_game").copy()
df_chart_1['Points_per_game'] = round(df_chart_1['Points_per_game'], 2)

# Data for Chart 2
df_chart_2 = player_data[['Player', 'Season', 'Stage', 'GP', 'AST']].copy()
df_chart_2['Assists_per_game'] = round(df_chart_2['AST'] / df_chart_2['GP'], 2)
df_chart_2.drop(['GP', 'AST'], axis = 1, inplace = True)

# Data for Chart 3
df_chart_3 = player_data[['Player', 'Season', 'Stage', 'GP', 'ORB', 'DRB']].copy()
df_chart_3['Offensive Rebounds'] = round(df_chart_3['ORB'] / df_chart_3['GP'], 2)
df_chart_3['Defensive Rebounds'] = round(df_chart_3['DRB'] / df_chart_3['GP'], 2)
df_chart_3.drop(['GP', 'ORB', 'DRB'], axis = 1, inplace = True)
df_chart_3 = df_chart_3.melt(id_vars=['Player', 'Season', 'Stage'], var_name = 'Rebound_type', value_name = "Rebounds_per_game").copy()

# Data for Chart 4
df_chart_4 = player_data[['Player', 'Season', 'Stage', 'GP', 'BLK', 'STL']].copy()
df_chart_4['Blocks'] = round(df_chart_4['BLK'] / df_chart_4['GP'], 2)
df_chart_4['Steals'] = round(df_chart_4['STL'] / df_chart_4['GP'], 2)
df_chart_4.drop(['GP', 'BLK', 'STL'], axis = 1, inplace = True)
df_chart_4 = df_chart_4.melt(id_vars=['Player', 'Season', 'Stage'], var_name = 'Blocks/Steals', value_name = "per_game").copy()

# Data for Chart 5
df_chart_5 = player_data[['Player', 'Season', 'Stage', 'GP', 'TOV', 'PF']].copy()
df_chart_5['Turnovers'] = round(df_chart_5['TOV'] / df_chart_5['GP'], 2)
df_chart_5['Fouls'] = round(df_chart_5['PF'] / df_chart_5['GP'], 2)
df_chart_5.drop(['GP', 'TOV', 'PF'], axis = 1, inplace = True)
df_chart_5 = df_chart_5.melt(id_vars=['Player', 'Season', 'Stage'], var_name = 'Turnovers/Fouls', value_name = "per_game").copy()

# Data for Chart 11 (chart 1 in second tab)
df_chart_11 = player_data[['Player', 'Season', 'Stage', 'FGM', 'FGA', '3PM', '3PA']].copy()
df_chart_11['2PA'] = df_chart_11['FGA'] - df_chart_11['3PA']
df_chart_11['2PM'] = df_chart_11['FGM'] - df_chart_11['3PM']
df_chart_11 = df_chart_11.groupby(['Player', 'Season', 'Stage']).mean().reset_index().copy()
df_chart_11['2PT_%'] = round(df_chart_11['2PM'] / df_chart_11['2PA'] * 100, 2)
df_chart_11['3PT_%'] = round(df_chart_11['3PM'] / df_chart_11['3PA'] * 100, 2)
df_chart_11['eFG_%'] = round(((df_chart_11['FGM'] + (0.5 * df_chart_11['3PM'])) / df_chart_11['FGA']) * 100, 2)
df_chart_11.drop(['FGM', 'FGA', '3PM', '3PA', '2PM', '2PA'], axis = 1, inplace = True)
df_chart_11 = df_chart_11.melt(id_vars=['Player', 'Season', 'Stage'], var_name = '2PT_3PT_eFG', value_name = "per_game").copy()

# Data for Chart 12
df_chart_12 = player_data[['Player', 'Season', 'Stage', 'GP', 'PTS', 'FGA', 'FTA']].copy()
df_chart_12 ['PTS'] = df_chart_12['PTS'] / df_chart_12['GP']
df_chart_12 ['FGA'] = df_chart_12['FGA'] / df_chart_12['GP']
df_chart_12 ['FTA'] = df_chart_12['FTA'] / df_chart_12['GP']
df_chart_12['True shooting attempts'] = df_chart_12['FGA'] + 0.44 * df_chart_12['FTA']
df_chart_12['True shooting percentage'] = round(df_chart_12['PTS'] / (2 * df_chart_12['True shooting attempts']) * 100, 2)
df_chart_12.drop(['GP', 'PTS', 'FGA', 'FTA', 'True shooting attempts'], axis = 1, inplace = True)

# Data for Chart 13 & 14
df_chart_13 = player_data[['Player', 'Season', 'Stage', 'GP', 'PTS', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'ORB', 'DRB', 'STL', 'AST', 'BLK', 'PF', 'TOV']].copy()
df_chart_13 ['PTS'] = df_chart_13['PTS'] / df_chart_13['GP']
df_chart_13 ['Minutes Played'] = round(df_chart_13['MIN'] / df_chart_13['GP'], 2)
df_chart_13 ['FGM'] = df_chart_13['FGM'] / df_chart_13['GP']
df_chart_13 ['FGA'] = df_chart_13['FGA'] / df_chart_13['GP']
df_chart_13 ['FTM'] = df_chart_13['FTM'] / df_chart_13['GP']
df_chart_13 ['FTA'] = df_chart_13['FTA'] / df_chart_13['GP']
df_chart_13 ['ORB'] = df_chart_13['ORB'] / df_chart_13['GP']
df_chart_13 ['DRB'] = df_chart_13['DRB'] / df_chart_13['GP']
df_chart_13 ['STL'] = df_chart_13['STL'] / df_chart_13['GP']
df_chart_13 ['AST'] = df_chart_13['AST'] / df_chart_13['GP']
df_chart_13 ['BLK'] = df_chart_13['BLK'] / df_chart_13['GP']
df_chart_13 ['PF'] = df_chart_13['PF'] / df_chart_13['GP']
df_chart_13 ['TOV'] = df_chart_13['TOV'] / df_chart_13['GP']
df_chart_13['Game Score'] = round(df_chart_13 ['PTS'] + 0.4 * df_chart_13 ['FGM'] - 0.7 * df_chart_13 ['FGA'] - 0.4 * (df_chart_13 ['FTA'] - df_chart_13 ['FTM']) + 0.7 * df_chart_13 ['ORB'] + 0.3 * df_chart_13 ['DRB'] + df_chart_13 ['STL'] + 0.7 * df_chart_13 ['AST'] + 0.7 * df_chart_13 ['BLK'] - 0.4 * df_chart_13 ['PF'] - df_chart_13 ['TOV'], 2)
df_chart_13.drop(['GP', 'PTS', 'MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'ORB', 'DRB', 'STL', 'AST', 'BLK', 'PF', 'TOV'], axis = 1, inplace = True)


# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# cards
first_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career FG%", className="card-title"),
            html.H5(id="card-01")
        ]
    ),
    color='info', inverse=True, style={'text-align': 'center'}
)

second_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career FT%", className="card-title"),
            html.H5(id="card-02")
        ]
    ),
    color='secondary', inverse=True, style={'text-align': 'center'}
)

third_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career 3-pt %", className="card-title"),
            html.H5(id="card-03")
        ]
    ),
    color='info', inverse=True, style={'text-align': 'center'}
)

fourth_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Avg Minutes per game", className="card-title"),
            html.H5(id="card-04")
        ]
    ),
    color='secondary', inverse=True, style={'text-align': 'center'}
)

fifth_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career FG%", className="card-title"),
            html.H5(id="card-05")
        ]
    ),
    color='info', inverse=True, style={'text-align': 'center'}
)

sixth_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career FT%", className="card-title"),
            html.H5(id="card-06")
        ]
    ),
    color='secondary', inverse=True, style={'text-align': 'center'}
)

seventh_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Career 3-pt %", className="card-title"),
            html.H5(id="card-07")
        ]
    ),
    color='info', inverse=True, style={'text-align': 'center'}
)

eighth_card = dbc.Card(
    dbc.CardBody(children=
        [
            html.P("Avg Minutes per game", className="card-title"),
            html.H5(id="card-08")
        ]
    ),
    color='secondary', inverse=True, style={'text-align': 'center'}
)


cards = dbc.Row(
    [
        dbc.Col(first_card, width=3), 
        dbc.Col(second_card, width=3),
        dbc.Col(third_card, width=3), 
        dbc.Col(fourth_card, width=3)
    ]
)

cards_tab2 = dbc.Row(
    [
        dbc.Col(fifth_card, width=3), 
        dbc.Col(sixth_card, width=3),
        dbc.Col(seventh_card, width=3), 
        dbc.Col(eighth_card, width=3)
    ]
)
# dropdowns
first_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='player-widget',
            #style={'width': '250px'},
            value='Kobe Bryant',  # REQUIRED to show the plot on the first page load
            options=[{'label': player, 'value': player} for player in player_data['Player'].unique()])
    ],
    style={"width": "100%"}
)

second_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='stage-widget',
            #style={'width': '250px'},
            value='Regular_Season',  # REQUIRED to show the plot on the first page load
            options=[{'label': Stage, 'value': Stage} for Stage in player_data['Stage'].unique()])
    ],
    style={"width": "100%"}
)

dropdowns = dbc.Row(
    [
        dbc.Col(first_dropdown, width=3), 
        dbc.Col(second_dropdown, width=3),
        dbc.Col(html.H5(''), width=6)
    ]
)

third_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='player-widget-2',
            #style={'width': '250px'},
            value='Kobe Bryant',  # REQUIRED to show the plot on the first page load
            options=[{'label': player, 'value': player} for player in player_data['Player'].unique()])
    ],
    style={"width": "100%"}
)

fourth_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='stage-widget-2',
            #style={'width': '250px'},
            value='Regular_Season',  # REQUIRED to show the plot on the first page load
            options=[{'label': Stage, 'value': Stage} for Stage in player_data['Stage'].unique()])
    ],
    style={"width": "100%"}
)

dropdowns2 = dbc.Row(
    [
        dbc.Col(third_dropdown, width=3), 
        dbc.Col(fourth_dropdown, width=3),
        dbc.Col(html.H5(''), width=6)
    ]
)

tab1_content = html.Div(
    [
        dropdowns,
        html.Br(),
        cards,
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id='chart-1',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '345px', 'height': '300px'}), width = 4),
                dbc.Col(
                    html.Iframe(
                        id='chart-2',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '345px', 'height': '300px'}), width = 4),
                dbc.Col(
                    html.Iframe(
                        id='chart-3',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '345px', 'height': '300px'}), width = 4)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id='chart-4',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6),
                dbc.Col(
                    html.Iframe(
                        id='chart-5',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6)
            ]
        ),
    ]
)

tab2_content = html.Div(
    [
        dropdowns2,
        html.Br(),
        cards_tab2,
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id='chart-11',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6),
                dbc.Col(
                    html.Iframe(
                        id='chart-12',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id='chart-13',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6),
                dbc.Col(
                    html.Iframe(
                        id='chart-14',
                        style={'border-width': '1', 'border-color': '#DCDCDC', 'width': '530px', 'height': '300px'}), width = 6)
            ]
        ),
    ]
)

tab3_content = html.Div(
    [
        #dropdowns,
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div("Trend 1 - Placeholder")),
                dbc.Col(html.Div("Trend 2 - Placeholder")),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div("Trend 3 - Placeholder")),
                dbc.Col(html.Div("Trend 4 - Placeholder")),
            ]
        ),
    ]
)

tabs = html.Div(
    [
        html.H2("NBA Analytics Dashboard"),
        dbc.Tabs(
            [
                dbc.Tab(children=[
                    html.Br(),
                    tab1_content
                    ],
                    label="Player stats",
                    style={"padding": "10px"},
                    label_style={"color": "#4682B4", "font-weight": "bold", "font-size": "larger", "background-color": "#f4f6f6"},
                    active_label_style={"color": "#DC143C", "font-weight": "bold", "font-size": "larger", "background-color": "#FFEFD5"}
                ),
                dbc.Tab(children=[
                    html.Br(),
                    tab2_content
                    ],
                    label="Advanced Analytics",
                    style={"padding": "10px"},
                    label_style={"color": "#4682B4", "font-weight": "bold", "font-size": "larger", "background-color": "#f4f6f6"},
                    active_label_style={"color": "#DC143C", "font-weight": "bold", "font-size": "larger", "background-color": "#FFEFD5"}
                ),
                dbc.Tab(children=[
                    html.Br(),
                    tab3_content
                    ],
                    label="NBA trends",
                    style={"padding": "10px"},
                    label_style={"color": "#4682B4", "font-weight": "bold", "font-size": "larger", "background-color": "#f4f6f6"},
                    active_label_style={"color": "#DC143C", "font-weight": "bold", "font-size": "larger", "background-color": "#FFEFD5"}
                )
            ]
        ),
    ]
)


app.layout = html.Div(
    [
        dbc.Container(
            [
                html.Br(),
                tabs
            ]
        ),
    ]
)

# Set up callbacks/backend

# metrics
@app.callback(
    Output(component_id="card-01", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_FG(player, stage):
    career_FG = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_FG_%'].iloc[0]
    return (str(career_FG) + ' %')

@app.callback(
    Output(component_id="card-02", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_FT(player, stage):
    career_FT = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_FT_%'].iloc[0]
    return (str(career_FT) + ' %')

@app.callback(
    Output(component_id="card-03", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_3PT(player, stage):
    career_3PT = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_3PT_%'].iloc[0]
    return (str(career_3PT) + ' %')

@app.callback(
    Output(component_id="card-04", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_minutes(player, stage):
    avg_minutes = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['Minutes_per_game'].iloc[0]
    return str(avg_minutes) + ' minutes'

@app.callback(
    Output(component_id="card-05", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_FG(player, stage):
    career_FG = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_FG_%'].iloc[0]
    return (str(career_FG) + ' %')

@app.callback(
    Output(component_id="card-06", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_FT(player, stage):
    career_FT = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_FT_%'].iloc[0]
    return (str(career_FT) + ' %')

@app.callback(
    Output(component_id="card-07", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_3PT(player, stage):
    career_3PT = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['career_3PT_%'].iloc[0]
    return (str(career_3PT) + ' %')

@app.callback(
    Output(component_id="card-08", component_property="children"), 
    Input("player-widget", "value"),
    Input('stage-widget', 'value'))
def metric_minutes(player, stage):
    avg_minutes = df_metrics[(df_metrics['Player'] == player) & (df_metrics['Stage'] == stage)]['Minutes_per_game'].iloc[0]
    return str(avg_minutes) + ' minutes'

# tab 1
@app.callback(
    Output('chart-1', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('stage-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_1[(df_chart_1['Player'] == xcol) & (df_chart_1['Stage'] == ycol)]).mark_bar().encode(
        y = alt.Y('sum(Points_per_game)', title = 'Points'),
        x = alt.X('Season:O'), 
        color = alt.Color('Points_type', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Season', 'Points_type', 'Points_per_game']
        ).properties(title='Average Points by Season', width=240, height = 160)
    return chart.to_html()

@app.callback(
    Output('chart-2', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('stage-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_2[(df_chart_2['Player'] == xcol) & (df_chart_2['Stage'] == ycol)]).mark_line().encode(
        y = alt.Y('Assists_per_game', title = 'Assists', scale=alt.Scale(zero=False)),
        x = alt.X('Season:O'),
        tooltip=['Player', 'Stage', 'Season', 'Assists_per_game']
        ).properties(title='Average Assists by Season', width=240, height = 200)
    return chart.to_html()

@app.callback(
    Output('chart-3', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('stage-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_3[(df_chart_3['Player'] == xcol) & (df_chart_3['Stage'] == ycol)]).mark_bar().encode(
        y = alt.Y('sum(Rebounds_per_game)', title = 'Rebounds'),
        x = alt.X('Season:O'), 
        color = alt.Color('Rebound_type', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Season', 'Rebound_type', 'Rebounds_per_game']
        ).properties(title='Average Rebounds by Season', width=240, height = 160)
    return chart.to_html()

@app.callback(
    Output('chart-4', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('stage-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_4[(df_chart_4['Player'] == xcol) & (df_chart_4['Stage'] == ycol)]).mark_line().encode(
        y = alt.Y('per_game', title = 'Count'),
        x = alt.X('Season:O'),
        color = alt.Color('Blocks/Steals', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Season', 'Blocks/Steals', 'per_game']
        ).properties(title='Average Blocks & Steals by Season', width=430, height = 160)
    return chart.to_html()

@app.callback(
    Output('chart-5', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('stage-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_5[(df_chart_5['Player'] == xcol) & (df_chart_5['Stage'] == ycol)]).mark_line().encode(
        y = alt.Y('per_game', title = 'Count'),
        x = alt.X('Season:O'),
        color = alt.Color('Turnovers/Fouls', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Season', 'Turnovers/Fouls', 'per_game']
        ).properties(title='Average Turnovers & Fouls by Season', width=430, height = 160)
    return chart.to_html()

# tab 2
@app.callback(
    Output('chart-11', 'srcDoc'),
    Input('player-widget-2', 'value'),
    Input('stage-widget-2', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_11[(df_chart_11['Player'] == xcol) & (df_chart_11['Stage'] == ycol)]).mark_line().encode(
        y = alt.Y('per_game', title = 'Shooting Percentage', scale=alt.Scale(zero=False)),
        x = alt.X('Season:O'),
        color = alt.Color('2PT_3PT_eFG', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Season', '2PT_3PT_eFG', 'per_game']
        ).properties(title='Average Shooting Percentages by Season', width=430, height = 160)
    return chart.to_html()

@app.callback(
    Output('chart-12', 'srcDoc'),
    Input('player-widget-2', 'value'),
    Input('stage-widget-2', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_12[(df_chart_12['Player'] == xcol) & (df_chart_12['Stage'] == ycol)]).mark_bar().encode(
        y = alt.Y('True shooting percentage', title = 'True Shooting Percentage', scale=alt.Scale(zero=False)),
        x = alt.X('Season:O'),
        tooltip=['Player', 'Stage', 'Season', 'True shooting percentage']
        ).properties(title='True Shooting Percentage by Season', width=430, height = 190)
    return chart.to_html()

@app.callback(
    Output('chart-13', 'srcDoc'),
    Input('player-widget-2', 'value'),
    Input('stage-widget-2', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_13[(df_chart_13['Player'] == xcol) & (df_chart_13['Stage'] == ycol)]).mark_bar().encode(
        y = alt.Y('Game Score', title = 'Game Score', scale=alt.Scale(zero=False)),
        x = alt.X('Season:O'),
        tooltip=['Player', 'Stage', 'Season', 'Game Score']
        ).properties(title='Player Productivity by Season', width=430, height = 190)
    return chart.to_html()

@app.callback(
    Output('chart-14', 'srcDoc'),
    Input('player-widget-2', 'value'),
    Input('stage-widget-2', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(df_chart_13[df_chart_13['Player'] == xcol]).mark_circle(size=60).encode(
        x = alt.X('Minutes Played', scale=alt.Scale(zero=False)),
        y = alt.Y('Game Score', scale=alt.Scale(zero=False)),
        color = alt.Color('Stage', legend = alt.Legend(orient = 'bottom', title = "")),
        tooltip=['Player', 'Stage', 'Minutes Played', 'Game Score']
        ).properties(title='Player Productivity by Minutes Played', width=430, height = 160)
    return chart.to_html()

if __name__ == "__main__":
    app.run_server(debug=True)