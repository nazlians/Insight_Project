#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:40:17 2019

@author: nazli
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

query = 'SELECT COUNT(Label) FROM attack WHERE id BETWEEN %s and %s AND Label!=1 GROUP BY Label'

query2='SELECT COUNT(Label),IP_Addr FROM attack WHERE id BETWEEN %s and %s AND Label!=1 GROUP BY IP_Addr'

query3='SELECT COUNT(Label),IP_Addr FROM attack WHERE id BETWEEN %s and %s GROUP BY IP_Addr'


B_size=1000
i=0
j=0

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  database="python_DB", 
  user="nazli",
  passwd="Nm*171993",
)

mycursor = mydb.cursor()
mycursor.execute("USE python_DB")
curA =  mydb.cursor(buffered=True)
curB =  mydb.cursor(buffered=True)
curA.execute("USE python_DB")
curB.execute("USE python_DB")



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Attack Proof'),

    html.Div(children='''
        Analyze Network Flow to detect real time attacks
    '''),

    dcc.Graph(id='a_graph'),

    dcc.Graph(id='a2_graph'),

    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])
@app.callback(Output('a2_graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_traffic_live(n):
    
    global j
    mycursor.execute(query2,(1, 1+j))
    records = mycursor.fetchall()
    j+=1
    
    tracey1=[]
    tracex1=[]
    for row in records:
        tracey1.append(row[0])
        tracex1.append(row[1])
    
    
    mycursor.execute(query3,(1, 1+j))
    record2 = mycursor.fetchall()
    
    tracey2=[]
    tracex2=[]
    for row in record2:
        tracey2.append(row[0])
        tracex2.append(row[1])
        
        
    Normal_Data = go.Bar(
    x=tracex1,
    y=tracey1,
    opacity=0.75,
    name='Normal',
)   
    Attack_Data = go.Bar(
    x=tracex2,
    y=tracey2,
    opacity=0.75,
    name='Attack'
)     
    
    '''
    data = [trace1, trace2]
    layout = go.Layout(barmode='overlay')
    fig = go.Figure(data=data, layout=layout)
    return fig
    '''
    
    fig = {
    'data':[Normal_Data, Attack_Data],
    'layout': {
        'height': 400,
        'title': 'Predicted attacks by server',
        'xaxis': {
            'title': 'IP Servers'
        },
        'yaxis': {
            'title': '# of Packets',
            'automargin': True
        }
    }
    }

    return fig
    
    '''
    fig = {
    'data': [
                {
                    'x': tracex1,
                    'y': tracey1,
                    'text': ['a', 'b', 'c', 'd'],
                    'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
                    'name': 'NORMAL DATA',
                    'mode': 'Bar',
                    'marker': {'size': 12}
                },
                {
                    'x': tracex2,
                    'y': tracey2,
                    
                    'name': 'ATTACK DATA',
                    'mode': 'Bar',
                    'marker': {'size': 12}
                }
            ],
    'layout': {
        'height': 400,
        'title': 'Predicted attacks by number',
        'xaxis': {
            'title': '# of predicted attacks per second'
        },
        'yaxis': {
            'title': 'Server IPs',
            'automargin': True
        }
    }
    }

    return fig
    '''
    
    

@app.callback(Output('a_graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_attack_live(n):
    """
    This function will update the bar graph
    showing predicted attacks per second per
    server ip address. It pulls data from
    cassandra table and only retrieves first
    row since the data are presorted by time
   
    data = {
        'servers': server_list,
        'attacks': []
    }
    """
    global i
    mycursor.execute(query,(1, i+1))
    records = mycursor.fetchall()
    i+=1
    
    a=[]
    for row in records:
        a.append(row[0])
    # Create the graph with subplots
    
    
    
    clrred = 'rgb(222,0,0)'
    clrblue = 'rgb(31,119,180)'
    clrs  = [clrred if x >15 else clrblue for x in a]
    
    fig = {
    'data': [go.Bar(x=a,
                    y=[1,2,3,4,5,6],
                    orientation='h', marker=dict(color=clrs))],
    'layout': {
        'height': 400,
        'title': 'Predicted attacks by Number',
        
        'xaxis': {
            'title': '# of predicted attacks',
            'range':[0,50],
        },
                
        'yaxis': {
                
             'ticktext':['Brute Force', 'DDoS', 'Botnet','Infilteration','Port Scan','Web'],
             'tickvals':['1','2','3','4','5','6'],
             'categoryorder': 'array',
             'categoryarray': [1,2,3,4,5,6]   
            
        },
                
    }
    }

    return fig



if __name__ == '__main__':
    app.run_server()