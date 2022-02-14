import pandas as pd
import os
import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output


url = "https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/bd584ee6c307cc9fab5ba38916e98a85de9c2ba7/pokemon.csv"

df = pd.read_csv(url,error_bad_lines= False)
df.drop_duplicates(subset=['TYPE1'],keep='first') 

# print(df[df["TYPE1"] == "Grass"])

test = [] 

for type in df["TYPE1"].unique():
    test.append({'label': type, 'value': type})

df["Ranks"] = (df["ATK"] - df["DEF"]) * 0.8 + (df["SP_ATK"] - df["SP_DEF"]) * 0.2 

df = df.sort_values(by='Ranks', ascending=False)#sorting the rows in descending order

# print(df.head())
# print(df.tail())
# # strong.drop_duplicates(subset=['TYPE2'],keep='first')

# # print(strong.head())


app = dash.Dash(__name__)
server = app.server
# df = px.data.stocks()


app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = test,
        value = 'Grass'),
        dcc.Graph(id = 'bar-chart'),
        dash.dash_table.DataTable(
            df.head().to_dict('records')
        ),
        dash.dash_table.DataTable(
            df.tail().to_dict('records')
        )

    ])
    
    
@app.callback(Output(component_id='bar-chart', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)
    fig = px.bar(df,x = df["NAME"][df["TYPE1"] == '{}'.format(dropdown_value)],\
                    y = df["TOTAL"][df["TYPE1"] == '{}'.format(dropdown_value)])
    
    fig.update_layout(title = 'Pockemons by Type',
                      xaxis_title = 'Name',
                      yaxis_title = 'Total'
                      )
    return fig  



if __name__ == '__main__': 
    app.run_server(debug = True)
