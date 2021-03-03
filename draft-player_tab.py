import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import altair as alt
import plotly.express as px
from vega_datasets import data
import numpy as np
import pandas as pd

# DELETE**************************************************************
# Read in global data / setup dummy data
record = np.arange(1, 65, 1)
players = [
    "Player 1",
    "Player 1",
    "Player 1",
    "Player 1",
    "Player 2",
    "Player 2",
    "Player 2",
    "Player 2",
    "Player 3",
    "Player 3",
    "Player 3",
    "Player 3",
    "Player 4",
    "Player 4",
    "Player 4",
    "Player 4",
] * 4
years = [2000, 2001, 2002, 2003] * 16
points = np.random.randint(7, 31, 64)
player_data = pd.DataFrame(
    {"Player": players, "Year": years, "Points": points}, index=record
)

record = np.arange(1, 33, 1)
teams = [
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 1",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 2",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 3",
    "Team 4",
    "Team 4",
    "Team 4",
    "Team 4",
    "Team 4",
    "Team 4",
    "Team 4",
    "Team 4",
]
years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007] * 4
wins = np.random.randint(25, 65, 32)
team_data = pd.DataFrame({"Team": teams, "Year": years, "Wins": wins}, index=record)
# **************************************************************************************

# Read in global data / setup dummy data
raw_data = pd.read_csv("players_stats_by_season_full_details.csv")

# Filter for NBA data
nba_data = raw_data[raw_data["League"] == "NBA"]

# Convert Columns to numeric
nba_data.loc[:, "GP":"PTS"].apply(pd.to_numeric, errors="coerce", axis=1)

# Insert columns for points and reounds per game
nba_data.insert(
    22, "REB_per_game", (nba_data.loc[:, "REB"] / nba_data.loc[:, "GP"]), True
)
nba_data.insert(
    23, "PTS_per_game", (nba_data.loc[:, "PTS"] / nba_data.loc[:, "GP"]), True
)

# Create new plot to plot FGM based on type
nba_2pointer = nba_data.copy()
nba_2pointer["FG_type"] = "2 pointer"
nba_2pointer["throws_made"] = nba_2pointer["FGM"] - nba_2pointer["3PM"]
nba_3pointer = nba_data.copy()
nba_3pointer["FG_type"] = "3 pointer"
nba_3pointer["throws_made"] = nba_3pointer["3PM"]
nba_FG_data = nba_2pointer.append(nba_3pointer)


# Setup app and layout/frontend
app = dash.Dash(__name__)

server = app.server

tab1_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="player-widget",
                            style={"width": "340px"},
                            value="Player",  # REQUIRED to show the plot on the first page load
                            options=[
                                {"label": player, "value": player}
                                for player in nba_data["Player"].unique()
                            ],
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.H6(
                                id="output-1",
                                children=[
                                    "Draft team: ",
                                    html.P(id="draft_team_card", children=""),
                                ],
                            )
                        ),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Salary: $12,345,678")),
                        color="warning",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Years in NBA: 7")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Years in NBA: 7")),
                        color="warning",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("All-Star appearances: 3")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Offense Efficiency Rating: 87.4%")),
                        color="warning",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Years in NBA: 7")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Defense Efficiency Rating: 72.9%")),
                        color="warning",
                        inverse=True,
                        style={
                            "text-align": "center",
                            # "width": "280px",
                            # "height": "80px",
                        },
                    )
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Iframe(
                            id="bar-chart-1-1",
                            style={
                                "border-width": "0",
                                "width": "317px",
                                "height": "440px",
                            },
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="bar-chart-1-2",
                            style={
                                "border-width": "0",
                                "width": "318px",
                                "height": "440px",
                            },
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="bar-chart-1-3",
                            style={
                                "border-width": "0",
                                "width": "395px",
                                "height": "440px",
                            },
                        )
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Iframe(
                            # html.Div(
                            # [
                            # dcc.Graph(
                            id="bar-chart-1-4",
                            # figure={},
                            # clickData=None,
                            # hoverData=None,
                            # config={
                            #     'staticplot':False,
                            #     'scrollZoom':True,
                            #     'doubleClick':'reset',
                            #    'showTips':True,
                            #     'displayModeBar':False,
                            #     'watermark':True
                            # }
                            style={
                                "border-width": "0",
                                "width": "900px",
                                "height": "550px",
                            },
                            # )
                            # ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            dbc.Card(
                                dbc.CardBody(html.H5("NBA Rank: 37")),
                                color="warning",
                                style={"text-align": "center"},
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Card(
                                dbc.CardBody(html.H5("NBA Rank: 37")),
                                color="warning",
                                style={"text-align": "center"},
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Card(
                                dbc.CardBody(html.H5("NBA Rank: 37")),
                                color="warning",
                                style={"text-align": "center"},
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Card(
                                dbc.CardBody(html.H5("NBA Rank: 37")),
                                color="warning",
                                style={"text-align": "center"},
                            )
                        ),
                    ]
                ),
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
                        dbc.CardBody(html.H5("NBA Rank : 7")),
                        color="warning",
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Total Wins in season: 54")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Total Losses in season: 20")),
                        color="warning",
                        style={"text-align": "center"},
                    )
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Home games win%: 80%")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Offense Efficiency Ranking: 5")),
                        color="warning",
                        style={"text-align": "center"},
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5("Defense Efficiency Ranking: 11")),
                        color="info",
                        inverse=True,
                        style={"text-align": "center"},
                    )
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Select a Team"),
                        dcc.Dropdown(
                            id="team-widget",
                            style={"width": "340px"},
                            # value='Team 2',  # REQUIRED to show the plot on the first page load
                            options=[
                                {"label": team, "value": team}
                                for team in team_data["Team"].unique()
                            ],
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="bar-chart-2",
                            style={
                                "border-width": "1",
                                "width": "717px",
                                "height": "400px",
                            },
                        )
                    ]
                ),
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
                dbc.Tab(
                    children=[
                        html.Br(),
                        html.H4("Player Statistics"),
                        html.Br(),
                        tab1_content,
                    ],
                    label="Player stats",
                    style={"padding": "10px"},
                ),
                dbc.Tab(
                    children=[
                        html.Br(),
                        html.H4("This is tab for Team statistics"),
                        html.Br(),
                        tab2_content,
                    ],
                    label="Team stats",
                    style={"padding": "10px"},
                ),
                dbc.Tab(
                    children=[
                        html.Br(),
                        html.H4("This is tab for NBA trends"),
                        html.Br(),
                        tab3_content,
                    ],
                    label="NBA trends",
                    style={"padding": "10px"},
                ),
            ]
        ),
    ]
)


app.layout = html.Div(
    [
        dbc.Container([html.Br(), tabs]),
    ]
)

# Set up callbacks/backend
@app.callback(
    Output("bar-chart", "srcDoc"),
    Input("player-widget", "value"),
    Input("year-widget", "value"),
)
def plot_altair(xcol, ycol):
    chart = (
        alt.Chart(
            player_data[(player_data.Player == xcol) & (player_data.Year == int(ycol))]
        )
        .mark_bar()
        .encode(x=alt.X("Points", bin=True), y="count()")
        .properties(title="Histogram of points scored")
    )
    return chart.to_html()


@app.callback(Output("bar-chart-1-1", "srcDoc"), Input("player-widget", "value"))
def plot_altair(selected_player):

    df = nba_FG_data.loc[
        (nba_FG_data["Player"] == selected_player)
        & (nba_FG_data["Stage"] == "Regular_Season")
    ]

    chart = (
        alt.Chart(df, width=220, height=300, title="Rebound per game")
        .mark_bar()
        .encode(
            x=alt.X("Season", axis=alt.Axis(title="Season")),
            y=alt.Y(
                "REB_per_game", axis=alt.Axis(title="Rebounds per game", grid=False)
            ),
        )
        .encode(x=alt.X("Season", axis=alt.Axis(title="Season")))
        .configure_view(stroke="transparent")
        #        .properties(width="container", height="container")
        .configure_axis(labelFontSize=10, titleFontSize=12)
        .configure_title(fontSize=20)
    )
    return chart.to_html()


@app.callback(Output("bar-chart-1-2", "srcDoc"), Input("player-widget", "value"))
def plot_altair(selected_player):

    df = nba_FG_data.loc[
        (nba_FG_data["Player"] == selected_player)
        & (nba_FG_data["Stage"] == "Regular_Season")
    ]

    chart = (
        alt.Chart(df, width=220, height=300, title="Points per game")
        .mark_bar()
        .encode(
            x=alt.X("Season", axis=alt.Axis(title="Season")),
            y=alt.Y("PTS_per_game", axis=alt.Axis(title="Points per game", grid=False)),
        )
        #     .properties(width="container", height="container")
        .configure_view(stroke="transparent")
        .configure_axis(labelFontSize=10, titleFontSize=12)
        .configure_title(fontSize=20)
    )
    return chart.to_html()


@app.callback(Output("bar-chart-1-3", "srcDoc"), Input("player-widget", "value"))
def plot_altair(selected_player):

    df = nba_FG_data.loc[
        (nba_FG_data["Player"] == selected_player)
        & (nba_FG_data["Stage"] == "Regular_Season")
    ]

    chart = (
        alt.Chart(df, width=220, height=300, title="Field goal ratio")
        .mark_bar()
        .encode(
            x=alt.X("Season", axis=alt.Axis(title="Season")),
            y=alt.Y("throws_made", axis=alt.Axis(title="Field Goals made", grid=False)),
            color=alt.Color("FG_type", scale=alt.Scale(scheme="lightmulti")),
        )
        .configure_view(stroke="transparent")
        #      .properties(width="container", height="container")
        .configure_axis(labelFontSize=10, titleFontSize=12)
        .configure_title(fontSize=20)
    )
    return chart.to_html()


@app.callback(Output("bar-chart-1-4", "srcDoc"), Input("player-widget", "value"))
def plot_altair(selected_player):

    df = nba_FG_data.loc[
        (nba_FG_data["Player"] == selected_player)
        & (nba_FG_data["Stage"] == "Regular_Season")
    ]

    chart = (
        alt.layer(
            alt.Chart(df, width=790, height=410, title="Player stats over time")
            .mark_line(color="red", size=1)
            .encode(y=alt.Y("TOV", axis=alt.Axis(title="Count", grid=False))),
            alt.Chart(df).mark_line(color="blue", size=1).encode(y="REB"),
            alt.Chart(df).mark_line(color="green", size=1).encode(y="AST"),
        )
        .encode(x=alt.X("Season", axis=alt.Axis(title="Season")))
        .configure_view(stroke="transparent")
        # .properties(height=160, width=500)
        .configure_axis(labelFontSize=10, titleFontSize=12)
        .configure_title(fontSize=20)
    )
    return chart.to_html()


@app.callback(Output("draft_team_card", "srcDoc"), Input("player-widget", "value"))
def plot_playerName(selected_player):
    draft_team = pd.unique(
        nba_data[nba_data["Player"] == selected_player]["draft_team"]
    )[0]
    return draft_team


@app.callback(Output("bar-chart-2", "srcDoc"), Input("team-widget", "value"))
def plot_altair(selected_team):
    chart = (
        alt.Chart(team_data[team_data.Team == selected_team])
        .mark_bar()
        .encode(y=alt.Y("Year:O"), x=alt.X("Wins"))
        .properties(title="Number of wins by Year")
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)