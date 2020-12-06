# =============================================================================
# Dashboard file. 
# =============================================================================

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pycountry

#Unclear if this enhances the end result at all:
#init_notebook_mode(connected=True)

app = dash.Dash()


df_country = pd.read_csv('../Datasets/country_est.csv')
df_global = pd.read_csv('../Datasets/reg_glob_est.csv')
df_totalpop = pd.read_excel('../Datasets/totalpopulation.xls')


#to do: combine these 2 statements into 1
df_country = df_country[df_country.Uncertainty != 'Lower']
df_country = df_country[df_country.Uncertainty != 'Upper']
df_country.drop(['Uncertainty'], axis='columns', inplace=True)
df_country = df_country.rename(columns={'ISO.Code': 'ISOCode', 'Country.Name': 'CountryName'})
df_country.drop(df_country.tail(1).index,inplace=True)
                   
df_country = pd.melt(df_country,id_vars=['ISOCode','CountryName'], var_name="Year", value_name="Deaths")

print(df_country)


# =============================================================================
# app.layout = html.Div(children=[
#      html.H1(children='National Child Mortality Data versus World Bank Funding ',
#              style={
#                  'textAlign': 'center',
#                  'color': '#ef3e18'
#              }
#              ),
#      html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),    
#      html.Div([dcc.Graph(figure=fig)
#  ])])
# 
# 
# 
# 
# 
# 
# 
# if __name__ == '__main__':
#      app.run_server()
# 
# =============================================================================
