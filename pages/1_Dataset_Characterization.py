import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from plot_funcs import *
from data_funcs import *
from aux_funcs import *

title = "Dropout dataset characterization"
config_page(title)


def page_1():

    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data']

    if not valid_session_data(dataframes, '## :construction: Please go to Home page before :construction:'):
        return

    datasets = {data: st.session_state[data] for data in dataframes}

    with st.container():
        st.title(title)

    with st.container():

        st.subheader('Students')

        demographic_pyramid(datasets['gender_data'])

        gender_tree(datasets['course_data'])

        specific_gender_tree(datasets['course_data'], 'Female')

        specific_gender_tree(datasets['course_data'], 'Male')

        gender_by_course(datasets['course_data'])

        dropout_by_gender(datasets['debt_data'])

        dropout_by_age_debt(datasets['debt_data'])

page_1()
