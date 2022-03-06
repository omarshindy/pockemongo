from dash import dcc, Input, Output, Dash, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# Dataset Processing

# importing data
url = "https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/pokemon.csv"

data = pd.read_csv(url,on_bad_lines='skip')


#data cleaning
df = data.copy()
df = df.replace(r'^\s*$', np.nan, regex=True)
df["Ranks"] = round((df["ATK"] - df["DEF"]) * 0.8 + (df["SP_ATK"] - df["SP_DEF"]) * 0.2)
df = df.sort_values(by='Ranks', ascending=False)#sorting the rows in descending order
df = df.drop_duplicates(subset=['NAME'],keep='first') 

# spliting data for generations
df1 = df[df["GENERATION"] > 4]  
df2 = df[df["GENERATION"] <= 4] 

# variables for the analysis
pokemon_skill = ["HP", "ATK", "SP_ATK" ,"DEF", "SP_DEF" ,"SPD"]
pokemon_info = [
    "NAME",
    "GENERATION",
    "TYPE1",
    "ABILITY1",
    "HEIGHT",
    "WEIGHT",
]
labels_table = ["Pokemon", "Generation", "Type", "Ability", "Height (m)", "Weight (kg)"]
skills1 = [
    "ATK",
    "SP_ATK",
    "DEF",
    "SP_DEF",
    "HP",
]
pokemon1 = "Pheromosa"
pokemon2 = "Deoxys"

###################################################   Interactive Components   #########################################
# choice of the pokemons
pokemon_options = []
for i in df1.index:
    pokemon_options.append(
        {"label": df1["NAME"][i], "value": df1["NAME"][i]}
    )

pokemon_options_over_4 = []
for i in df1.index:
    pokemon_options_over_4.append(
        {"label": df1["NAME"][i], "value": df1["NAME"][i]}
    )

pokemon_options_under_4 = []
for i in df2.index:
    pokemon_options_under_4.append(
        {"label": df2["NAME"][i], "value": df2["NAME"][i]}
    )

pokemon_dropdown_over_4 = dcc.Dropdown(
    id="pokemon1",
    options=pokemon_options_over_4,
    value="Pheromosa",
)

pokemon_dropdown_under_4 = dcc.Dropdown(
    id="pokemon2", options=pokemon_options_under_4, value="Deoxys"
)

dashtable_1 = dash_table.DataTable(
    id="table1",
    columns=[
        {"name": col, "id": pokemon_info[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=df[df["NAME"] == pokemon1].to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)


dashtable_2 = dash_table.DataTable(
    id="table2",
    # columns=[{"name": i, "id": i} for i in pokemon_info[::-1]],
    columns=[
        {"name": col, "id": pokemon_info[::-1][idx]}
        for (idx, col) in enumerate(labels_table[::-1])
    ],
    data=df[df["NAME"] == pokemon2].to_dict("records"),
    style_cell={"textAlign": "right", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)



########Dash App Layout##########################

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=app.get_asset_url("logo.png"), height="130px", width="200px"
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("POKEMON GENERATIONS", id="label1"),
                            html.Label(
                                "Explore the differences between old-school and new generations",
                                className="label2",
                            ),
                            html.Br(),
                            html.Label(
                                "Dashboard created by: Omar SHindy",
                                className="label2",
                                style={"margin-bottom": ".34rem"},
                            ),
                        ],
                        width=8,
                    ),
                ],
                align="between",
                # no_gutters=True,
            ),
        ),
    ],
)

controls_player_1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose an new generation Pokemon:"),
                html.Br(),
                pokemon_dropdown_over_4,
            ]
        ),
    ],
    body=True,
    className="pokeomns_control",
)

controls_player_2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose an old school Pokemon:"),
                html.Br(),
                pokemon_dropdown_under_4,
            ]
        ),
    ],
    body=True,
    className="controls_players",
)


cards_1 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Type", className="card-title1"),
                    html.Div(id="P_position1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Ability", className="card-title1"),
                    html.Div(id="P_value1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Attack", className="card-title1"),
                    html.Div(id="P_skill1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Deffence", className="card-title1"),
                    html.Div(id="P_foot1", className="card_info1"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)
cards_2 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Deffence", className="card-title2"),
                    html.Div(id="P_foot2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Attack", className="card-title2"),
                    html.Div(id="P_skill2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Ability", className="card-title2"),
                    html.Div(id="P_value2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Type", className="card-title2"),
                    html.Div(id="P_position2", className="card_info2"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)
cards_3 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Rank", className="card-title1"),
                    dcc.Graph(id="graph_example_1"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Skills", className="card-title1"),
                    dcc.Graph(id="graph_example_3"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)
cards_4 = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Skills", className="card-title2"),
                    dcc.Graph(id="graph_example_4"),
                ]
            ),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Rank", className="card-title2"),
                    dcc.Graph(id="graph_example_2"),
                ]
            ),
            className="attributes_card",
        ),
    ]
)

tab1_content = (
    html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Pokemon Comparison"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_1),
                                        dbc.Row(
                                            html.Img(
                                                src=app.get_asset_url("pokemon.png"),
                                                className="playerImg",
                                            )
                                        ),
                                    ],
                                    sm=3,
                                ),
                                dbc.Col(
                                    dcc.Graph(id="graph_example"), sm=5, align="center"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_2),
                                        dbc.Row(
                                            html.Img(
                                                src=app.get_asset_url("pokemon.png"),
                                                className="playerImg",
                                            )
                                        ),
                                    ],
                                    sm=3,
                                ),
                            ],
                            justify="between",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dashtable_1,
                                        html.Br(),
                                        cards_1,
                                        html.Br(),
                                        cards_3,
                                    ],
                                    sm=6,
                                ),
                                dbc.Col(
                                    [
                                        dashtable_2,
                                        html.Br(),
                                        cards_2,
                                        html.Br(),
                                        cards_4,
                                    ],
                                    sm=6,
                                ),
                            ]
                        ),
                    ]
                )
            )
        ]
    ),
)



app.layout = dbc.Container(
    [
        navbar,
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Pokemons Comparison"),
            ],
        ),
    ],
    fluid=True,
)


# ----------------Callbacks for pokemons analysis----------------#


@app.callback(
    [
        Output("graph_example", "figure"),
        Output("table1", "data"),
        Output("graph_example_1", "figure"),
        Output("graph_example_3", "figure"),
        Output("table2", "data"),
        Output("graph_example_2", "figure"),
        Output("graph_example_4", "figure"),
        Output("P_position1", "children"),
        Output("P_value1", "children"),
        Output("P_skill1", "children"),
        Output("P_foot1", "children"),
        Output("P_position2", "children"),
        Output("P_value2", "children"),
        Output("P_skill2", "children"),
        Output("P_foot2", "children"),
    ],
    [Input("pokemon1", "value"), Input("pokemon2", "value")],
)

###############################################   radar plot   #####################################################


def tab_1_function(pokemon1, pokemon2):

    # scatterpolar
    df1_for_plot = pd.DataFrame(df1[df1["NAME"] == pokemon1][pokemon_skill].iloc[0])
    df1_for_plot.columns = ["score"]

    df2_for_plot = pd.DataFrame(df2[df2["NAME"] == pokemon2][pokemon_skill].iloc[0])
    df2_for_plot.columns = ["score"]

    list_scores = [
        df1_for_plot.index[i].capitalize() + " = " + str(df1_for_plot["score"][i])
        for i in range(len(df1_for_plot))
    ]
    text_scores_1 = pokemon1
    for i in list_scores:
        text_scores_1 += "<br>" + i

    list_scores = [
        df2_for_plot.index[i].capitalize() + " = " + str(df2_for_plot["score"][i])
        for i in range(len(df2_for_plot))
    ]
    text_scores_2 = pokemon2
    for i in list_scores:
        text_scores_2 += "<br>" + i

    fig = go.Figure(
        data=go.Scatterpolar(
            r=df1_for_plot["score"],
            theta=df1_for_plot.index,
            fill="toself",
            marker_color="rgb(45,0,198)",
            opacity=1,
            hoverinfo="text",
            name=text_scores_1,
            text=[
                df1_for_plot.index[i] + " = " + str(df1_for_plot["score"][i])
                for i in range(len(df1_for_plot))
            ],
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=df2_for_plot["score"],
            theta=df2_for_plot.index,
            fill="toself",
            marker_color="rgb(255,171,0)",
            hoverinfo="text",
            name=text_scores_2,
            text=[
                df2_for_plot.index[i] + " = " + str(df2_for_plot["score"][i])
                for i in range(len(df2_for_plot))
            ],
        )
    )

    fig.update_layout(
        polar=dict(
            hole=0.1,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type="linear",
                autotypenumbers="strict",
                autorange=False,
                range=[30, 100],
                angle=90,
                showline=False,
                showticklabels=False,
                ticks="",
                gridcolor="black",
            ),
        ),
        width=550,
        height=550,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )

    # table 1
    table_updated1 = df[df["NAME"] == pokemon1].to_dict("records")

    # gauge plot 1
    df1_for_plot = pd.DataFrame(df1[df1["NAME"] == pokemon1]["Ranks"])
    df1_for_plot["name"] = pokemon2
    gauge1 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df1_for_plot.Ranks.iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "#5000bf"}},
        )
    )
    gauge1.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )


    # barplot 1
    df1_for_plot = pd.DataFrame(
        df1[df1["NAME"] == pokemon1][skills1].iloc[0].reset_index()
    )
    df1_for_plot.rename(columns={df1_for_plot.columns[1]: "counts"}, inplace=True)
    df1_for_plot.rename(columns={df1_for_plot.columns[0]: "skills"}, inplace=True)
    barplot1 = px.bar(df1_for_plot, x="skills", y="counts")
    barplot1.update_traces(marker_color="#5000bf")
    barplot1.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=10,
    )
    barplot1.update_yaxes(range=[1, 100])
    
    # table 2
    table_updated2 = df[df["NAME"] == pokemon2].to_dict("records")

    # gauge plot 2
    df2_for_plot = pd.DataFrame(df2[df2["NAME"] == pokemon2]["Ranks"])
    df2_for_plot["name"] = pokemon2
    gauge2 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df2_for_plot.Ranks.iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "rgb(255,171,0)"}},
        )
    )
    gauge2.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )
    
    # # bar plot 2
    df2_for_plot = pd.DataFrame(
        df2[df2["NAME"] == pokemon2][skills1].iloc[0].reset_index()
    )
    df2_for_plot.rename(columns={df2_for_plot.columns[1]: "counts"}, inplace=True)
    df2_for_plot.rename(columns={df2_for_plot.columns[0]: "skills"}, inplace=True)
    barplot2 = px.bar(df2_for_plot, x="skills", y="counts")
    barplot2.update_traces(marker_color="rgb(255,171,0)")
    barplot2.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=10,
    )
    barplot2.update_yaxes(range=[1, 100])
    
    # cards
    p_pos_1 = df1[df1["NAME"] == pokemon1]["TYPE1"]
    p_value_1 = df1[df1["NAME"] == pokemon1]["ABILITY1"]
    p_skill_1 = df1[df1["NAME"] == pokemon1]["ATK"]
    p_foot_1 = df1[df1["NAME"] == pokemon1]["DEF"]

    p_pos_2 = df2[df2["NAME"] == pokemon2]["TYPE1"]
    p_value_2 = df2[df2["NAME"] == pokemon2]["ABILITY1"]
    p_skill_2 = df2[df2["NAME"] == pokemon2]["ATK"]
    p_foot_2 = df2[df2["NAME"] == pokemon2]["DEF"]

    # outputs
    return (
        fig,
        table_updated1,
        gauge1,
        barplot1,
        table_updated2,
        gauge2,
        barplot2,
        p_pos_1,
        p_value_1,
        p_skill_1,
        p_foot_1,
        p_pos_2,
        p_value_2,
        p_skill_2,
        p_foot_2,
    )


if __name__ == "__main__":
    app.run_server(debug=True)