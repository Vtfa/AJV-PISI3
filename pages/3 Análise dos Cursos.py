import streamlit as st
from plot_funcs import *
from data_funcs import *
from aux_funcs import *


title = "Análise dos cursos"
config_page(title)
page_style()


def page_3():
    

    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data']

    if not valid_session_data(dataframes, '## :construction: Please, go to _Home_ page before :construction:', 0.15):
        return

    datasets = {data: st.session_state[data] for data in dataframes}

    reset_filters()


    with st.container():
        st.title(title)

    with st.container():
        st.header('Dados dos cursos')
        plots= ["Histograma de evasão", "Relação das notas com cursos", "Dados socioeconômicos"]
        selected_plot= st.selectbox("Selecione para visualizar",plots)
        if selected_plot == "Histograma de evasão":
          dropout_histogram()

        elif selected_plot == "Relação das notas com cursos":
          grade_semesters()

        elif selected_plot=="Dados socioeconômicos":
          st.subheader = "Plots sobre gênero dos estudantes"
          gender = st.radio("Select a gender", ["Male", "Female"])
          gender_course(gender)

          st.subheadder= "Plots genéricos"
          financial_status()

       
        


page_3()

