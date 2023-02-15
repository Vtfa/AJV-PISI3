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

    data_states = ['dropout_data_state', 'gender_data', 'course_data']

    if not valid_session_data(data_states, '## :construction: Please go to Home page before :construction:'):
        return

    gender_data = st.session_state['gender_data']
    course_data = st.session_state['course_data']

    with st.container():
        st.title(title)

    with st.container():

        st.subheader('Students')

        demographic_pyramid(gender_data)

        gender_tree(course_data)

        specific_gender_tree(course_data, 'Female')

        specific_gender_tree(course_data, 'Male')

        gender_by_course(course_data)

page_1()
