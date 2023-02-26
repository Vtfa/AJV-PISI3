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

    sidebar_01()

    with st.container():
        st.title(title)

    with st.container():
        st.dataframe(
            filter_dataset(datasets['dropout_data'],
             marital_status='Solteiro',
             course='Tourism',
             gender='Female',
             age_range='',
             escolaridade='medio completo',
            )
        )
        st.header('Dropout Dataset')
        st.dataframe(datasets['dropout_data'])

        st.header('Students')
        demographic_pyramid(datasets['gender_data'])

        gender_tree(datasets['course_data'])

        specific_gender_tree(datasets['course_data'], st.session_state['gender_select'])

        gender_by_course(datasets['course_data'])

        dropout_by_gender(datasets['debt_data'])

        dropout_by_age_debt(datasets['debt_data'])


page_1()
