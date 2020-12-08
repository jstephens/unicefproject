# =============================================================================
# Dashboard file. 
# =============================================================================

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pycountry

#Unclear if this enhances the end result at all:
init_notebook_mode(connected=True)

app = dash.Dash()


df_country = pd.read_csv('../Datasets/country_est.csv')
df_global = pd.read_csv('../Datasets/reg_glob_est.csv')
df_totalpop = pd.read_excel('../Datasets/totalpopulation.xls',sheet_name='ESTIMATES',
                            skiprows=range(0,16))
df_aid = pd.read_csv('../Datasets/netdevelopment.csv')

#======= Altering the df_country dataframe ====================================
df_country = df_country[df_country.Uncertainty != 'Lower']
df_country = df_country[df_country.Uncertainty != 'Upper']
df_country.drop(['Uncertainty'], axis='columns', inplace=True)
#df_country.drop(df_country.iloc[:, 2:35], inplace = True, axis = 1)  #temporary measure to reduce time to load
df_country.dropna
df_country = df_country.rename(columns={'ISO.Code': 'ISOCode', 'Country.Name': 'CountryName'})
df_country.drop(df_country.tail(1).index,inplace=True)
df_country1 = df_country.copy(deep=False)
df_country = pd.melt(df_country,id_vars=['ISOCode','CountryName'], var_name="Year", value_name="Deaths")
#==============================================================================

#======= Altering the df_country dataframe ====================================
df_totalpop.drop(['Index','Variant','Notes','Country code','Parent code','1950','1951','1952','1953','1954','2020'], axis='columns', inplace=True)
df_totalpop = df_totalpop[df_totalpop.Type != 'World']
df_totalpop = df_totalpop[df_totalpop.Type != 'Region']
df_totalpop = df_totalpop[df_totalpop.Type != 'Label/Separator']
df_totalpop = df_totalpop[df_totalpop.Type != 'Subregion']
df_totalpop = df_totalpop[df_totalpop.Type != 'Income Group']
df_totalpop = df_totalpop[df_totalpop.Type != 'Development Group']
df_totalpop = df_totalpop[df_totalpop.Type != 'Special other']
df_totalpop = df_totalpop[df_totalpop.Type != 'SDG region']
df_totalpop.drop(['Type'], axis='columns', inplace=True)
df_totalpop = df_totalpop.rename(columns={'Region, subregion, country or area *': 'CountryName'})
df_totalpop = pd.melt(df_totalpop,id_vars=['CountryName'],var_name="Year",value_name="Population")
#==============================================================================

#======= Merged dataframe; cases per capita ===================================
merged_df = pd.merge(df_country, df_totalpop,  how='left', left_on=['CountryName','Year'], right_on = ['CountryName','Year'])
merged_df['Deaths'] = merged_df['Deaths'].astype(float)
merged_df['Population'] = merged_df['Population'].astype(float)
merged_df['DeathsC'] = merged_df['Deaths']/merged_df['Population']
print(merged_df)
#==============================================================================


#======= Chloropleth map ======================================================
fig = px.choropleth(data_frame = merged_df,
                    locations= "ISOCode",
                    color= "DeathsC",
                    hover_name= "CountryName",
                    color_continuous_scale= 'RdYlGn_r',
                    animation_frame= "Year")
#==============================================================================

#=======Interactive line chart ================================================
df_country1 = df_country1.set_index(['CountryName'])
df_country1.drop(['ISOCode'], axis='columns', inplace=True)
df_country1 = df_country1.T
df_country1.iloc[0] = 0

fig1 = go.Figure()

# set up ONE trace
fig1.add_trace(go.Scatter(x=df_country1.index,
                         y=df_country1[df_country1.columns[0]],
                         visible=True)
             )

updatemenu = []
buttons = []
# button with one option for each dataframe
for col in df_country1.columns:
    buttons.append(dict(method='restyle',
                        label=col,
                        visible=True,
                        args=[{'y':[df_country1[col]],
                               'x':[df_country1.index],
                               'type':'scatter'}, [0]],
                        )
                  )

# some adjustments to the updatemenus
updatemenu = []
your_menu = dict()
updatemenu.append(your_menu)

updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True

# add dropdown menus to the figure
fig1.update_layout(showlegend=False, updatemenus=updatemenu)
fig1.show()
#==============================================================================


#====== Layout for dash =======================================================
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Child Mortality Map', style={'color': '#df1e56'}),
    html.Div('This chloropleth map shows national mortality rates over time.'),

    dcc.Graph(figure=fig),
    html.H3('Line Graph', style={'color': '#df1e56'}),
    html.Div('Same data, with a dropdown.'),
    dcc.Graph(figure=fig1),
    ])
#==============================================================================

if __name__ == '__main__':
      app.run_server()


