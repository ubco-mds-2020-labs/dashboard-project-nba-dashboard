import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import altair as alt
from vega_datasets import data
import numpy as np
import pandas as pd


# Read in global data / setup dummy data
record = np.arange(1, 65, 1)
players = ['Player 1', 'Player 1', 'Player 1', 'Player 1', 'Player 2', 'Player 2', 'Player 2', 'Player 2', 'Player 3', 'Player 3', 'Player 3', 'Player 3', 'Player 4', 'Player 4', 'Player 4', 'Player 4'] * 4
years = [2000, 2001, 2002, 2003] * 16
points = np.random.randint(7, 31, 64)
player_data = pd.DataFrame({'Player': players, 'Year': years, 'Points': points}, index=record)

record = np.arange(1, 33, 1)
teams = ['Team 1', 'Team 1', 'Team 1', 'Team 1', 'Team 1', 'Team 1', 'Team 1', 'Team 1', 'Team 2', 'Team 2', 'Team 2', 'Team 2', 'Team 2', 'Team 2', 'Team 2', 'Team 2', 'Team 3', 'Team 3', 'Team 3', 'Team 3', 'Team 3', 'Team 3', 'Team 3', 'Team 3', 'Team 4', 'Team 4', 'Team 4', 'Team 4', 'Team 4', 'Team 4', 'Team 4', 'Team 4']
years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007] * 4
wins = np.random.randint(25, 65, 32)
team_data = pd.DataFrame({'Team': teams, 'Year': years, 'Wins': wins}, index=record)

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

tab1_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('NBA Rank: 37')),
                        color='warning', style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Salary: $12,345,678')),
                        color='info', inverse=True, style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Years in NBA: 7')),
                        color='warning', style={'text-align': 'center'}))
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('All-Star appearances: 3')),
                        color='info', inverse=True, style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Offense Efficiency Rating: 87.4%')),
                        color='warning', style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Defense Efficiency Rating: 72.9%')),
                        color='info', inverse=True, style={'text-align': 'center'}))
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                    html.H5('Filter data'),
                    dcc.Dropdown(
                        id='player-widget',
                        style={'width': '340px'},
                        value='Player 1',  # REQUIRED to show the plot on the first page load
                        options=[{'label': player, 'value': player} for player in player_data['Player'].unique()]),
                    dcc.Dropdown(
                        id='year-widget',
                        style={'width': '340px'},
                        value='2000',  # REQUIRED to show the plot on the first page load
                        options=[{'label': year, 'value': year} for year in player_data['Year'].unique()])
                    ]
                ),
                dbc.Col(
                    [
                    html.Iframe(
                        id='bar-chart',
                        style={'border-width': '1', 'width': '717px', 'height': '400px'})
                    ]
                )
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div("Chart 2 - Placeholder")),
                dbc.Col(html.Div("Chart 3 - Placeholder")),
            ]
        ),
    ]
)

tab2_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('NBA Rank : 7')),
                        color='warning', style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Total Wins in season: 54')),
                        color='info', inverse=True, style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Total Losses in season: 20')),
                        color='warning', style={'text-align': 'center'}))
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Home games win%: 80%')),
                        color='info', inverse=True, style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Offense Efficiency Ranking: 5')),
                        color='warning', style={'text-align': 'center'})),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Defense Efficiency Ranking: 11')),
                        color='info', inverse=True, style={'text-align': 'center'}))
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                    html.H5('Select a Team'),
                    dcc.Dropdown(
                        id='team-widget',
                        style={'width': '340px'},
                        #value='Team 2',  # REQUIRED to show the plot on the first page load
                        options=[{'label': team, 'value': team} for team in team_data['Team'].unique()])
                    ]
                ),
                dbc.Col(
                    [
                    html.Iframe(
                        id='bar-chart-2',
                        style={'border-width': '1', 'width': '717px', 'height': '400px'})
                    ]
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div("Chart 2 - Placeholder")),
                dbc.Col(html.Div("Chart 3 - Placeholder")),
            ]
        ),
    ]
)

tab3_content = html.Div(
    [
        html.Br(),
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
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(children=[
                    html.Br(),
                    html.H4("This is tab for Individual Player stats"),
                    html.Br(),
                    tab1_content
                    ],
                    label="Player stats",
                    style={"padding": "10px"},
                ),
                dbc.Tab(children=[
                    html.Br(),
                    html.H4("This is tab for Team statistics"),
                    html.Br(),
                    tab2_content
                    ],
                    label="Team stats",
                    style={"padding": "10px"},
                ),
                dbc.Tab(children=[
                    html.Br(),
                    html.H4("This is tab for NBA trends"),
                    html.Br(),
                    tab3_content
                    ],
                    label="NBA trends",
                    style={"padding": "10px"},
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
@app.callback(
    Output('bar-chart', 'srcDoc'),
    Input('player-widget', 'value'),
    Input('year-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(player_data[(player_data.Player == xcol) & (player_data.Year == int(ycol))]).mark_bar().encode(
        x=alt.X('Points', bin = True),
        y='count()'
        ).properties(title='Histogram of points scored')
    return chart.to_html()

@app.callback(
    Output('bar-chart-2', 'srcDoc'),
    Input('team-widget', 'value'))
def plot_altair(selected_team):
    chart = alt.Chart(team_data[team_data.Team == selected_team]).mark_bar().encode(
        y=alt.Y('Year:O'),
        x=alt.X('Wins')
        ).properties(title='Number of wins by Year')
    return chart.to_html()

if __name__ == "__main__":
    app.run_server(debug=True)