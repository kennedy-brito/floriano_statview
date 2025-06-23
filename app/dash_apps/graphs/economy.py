import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
from app.dash_apps.data import education as educ, population as pop, economy as econ
import plotly.graph_objects as go
from app.dash_apps.graphs.utils import format_pib_value
from app.dash_apps.graphs.constants import *
