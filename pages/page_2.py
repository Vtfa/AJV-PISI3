import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

header = st.container()
dataset = st.container()

with header:
    st.title('Página 2 teste')

with dataset:
    dropout_data = st.session_state['dropout_data_state']
    st.write(dropout_data)


    bar_age = pd.DataFrame(dropout_data['Age at enrollment'].value_counts())
    st.bar_chart(bar_age)