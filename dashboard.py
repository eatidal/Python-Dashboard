# import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import seaborn as sns
from dash.dependencies import Input, Output, State

# choose a Stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read dataset
df = pd.read_csv('https://raw.githubusercontent.com/jtrob704/BaseballData-Tableau/master/baseball_data.csv')
# create bar to display handedness and avg
fig1 = px.bar(df, x='handedness', y ='avg', title = 'Average for Each Type of Handedness',
               labels=dict(handedness="Handedness", avg="Average"))
fig1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', 
                   marker_line_width=1.5, opacity=0.6)
# create scatter to display HR and avg
fig2 = px.scatter(df, x='avg', y='HR', color="handedness",
                  labels=dict(avg="Average", HR= "Home Run"),
                 title = 'Relation Between Average and HR(Players Home Run) Depending on Handedness')

# set App Layout
app.layout = html.Div(children=[
    html.H5(children='Players Names'),
  
  # create Dropdwon menu
    dcc.Dropdown(id='name', options=[
        {'label': i, 'value': i} for i in df.name.unique()], 
                 multi=True,
                  value = 'Denny Lemaster',
                 placeholder='Filter by name...'),
    html.Div(id='table-container'),
    dcc.Graph(id='indicator-graphic'),
  
    # create graph 1 object
    dcc.Graph(
        id='handedeness_avg',
        figure=fig1
    ),
  # create graph 2 object
     dcc.Graph(
        id='hr_avg',
        figure=fig2
    )
])
# callback to recongnize the inputs
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('name', 'value'))

# function update graph based on name
def update_graph(i):
    if i == None:
        filtered_df = df
    elif type(i) == str:
        filtered_df = df[df.name == i]
    else:
        filtered_df = df[df.name.isin(i)] 
        
    print(filtered_df.head())
    print(i)
    
    # create scatter for selected names in filtered_df
    fig = px.scatter(filtered_df, x='avg', y='HR' , size ='avg', 
                     color='name',title='Players’ name according each HR',
                       labels=dict(avg="Average", HR= "Home Run"),
                    )
    # update layout
    fig.update_layout(transition_duration=500)
    return fig
  
# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
