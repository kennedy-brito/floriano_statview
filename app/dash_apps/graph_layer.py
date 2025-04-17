import pandas as pd
import numpy as np
import plotly.express as px
import data_layer as data

def age_pyramid()->px.Figure:
  graph = px.bar(
    data_frame=data.get_age_group(),
    x='valor',
    y='grupo_idade',
    orientation='h')

  return graph


if __name__ == '__main__':
  print(age_pyramid())