import streamlit as st
import time

from plot_funcs import *
from data_funcs import *
from aux_funcs import *


title = "Characterization of the dropout data"
config_page(title)
page_style()


def page_1():
    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data']

    if not valid_session_data(dataframes, '## :construction: Please go to Home page before :construction:', 0.15):
        return

    datasets = {data: st.session_state[data] for data in dataframes}

    reset_filters()

    sidebar_01()

    with st.container():
        st.title(title)

    with st.container():
        st.header('Dropout Dataset')
        st.dataframe(
            dataset_filter(datasets['dropout_data'],
             marital_status=st.session_state['marital_status'],
             course=st.session_state['course'],
             gender=st.session_state['gender'],
             age_range=st.session_state['age_range'],
             escolaridade_mae=st.session_state['escolaridade_mae'],
             escolaridade_pai=st.session_state['escolaridade_pai'],
            )
        )

        st.header('Students')
        demographic_pyramid(datasets['gender_data'])

        gender_tree(datasets['course_data'])

        specific_gender_tree(datasets['course_data'], st.session_state['gender_select'])

        gender_by_course(datasets['course_data'])

        dropout_by_gender(datasets['debt_data'])

        dropout_by_age_debt(datasets['debt_data'])


page_1()
