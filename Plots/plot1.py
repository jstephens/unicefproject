# point of this py file is to showcase a map 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


def plot1():

    df1_country = pd.read_csv('../Datasets/country_est.csv')
    df2_global = pd.read_csv('../Datasets/reg_glob_est.csv')
    df_totalpop = pd.read_csv('../Datasets/')

