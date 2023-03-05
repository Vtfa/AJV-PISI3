import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

plots= ["Histograma de evasão", "Relação das notas com cursos", "Dados socioeconômicos"]
selected_plot= st.selectbox("Selecione para visualizar",plots)

header = st.container()
dataset = st.container()
Dropout_data = pd.read_csv('data/dropout.csv')
mapping= {33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design', 8014: 'Social Service', 9003:'Agronomy', 9070:'Communication Design', 9085:'Veterinary Nursing', 9119:'Informatics Engineering',9130: 'Equinculture', 9147: 'Management', 9238: 'Social Service', 9254:'Tourism', 9500:'Nursing', 9556:'Oral Hygiene', 9670:'Advertising and Marketing Management', 9773: 'Journalism and Communication', 9853: 'Basic Education', 9991: 'Management(Evening)'}
Dropout_data['Course'] = Dropout_data['Course'].map(mapping)


with header:
    st.title('Análise dos cursos')
    if selected_plot == "Histograma de evasão":
      st.subheader("Histograma de evasão por curso")   
      histograma_drop= px.histogram( Dropout_data.sort_values(by='Course'), x="Course", color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=["mediumvioletred", "lightblue", "pink"],).update_layout(title={"text": "Percent :Course - Target","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
      st.write(histograma_drop)

    elif selected_plot == "Relação das notas com cursos":
      st.subheader("Distribuição de notas por curso (Double-click para isolar") 
      box_1stSemester= px.box (Dropout_data.sort_values(by='Course'),  x="Course" , y="Curricular units 1st sem (grade)", color= "Course")
      box_2ndSemester= px.box (Dropout_data.sort_values(by='Course'),  x="Course" , y="Curricular units 2nd sem (grade)", color= "Course")
      st.subheader("Primeiro semestre")
      st.write(box_1stSemester)
      st.subheader("Segundo semestre")
      st.write(box_2ndSemester)

      st.subheader("Primeiro Semestre")
      bar_1stSemester= px.bar(Dropout_data.sort_values(by='Course'), x="Course", y="Curricular units 1st sem (grade)")
      st.write(bar_1stSemester)
      st.subheader("Segundo Semestre")
      bar_2ndSemester= px.bar(Dropout_data.sort_values(by='Course'), x="Course", y="Curricular units 2nd sem (grade)")
      st.write(bar_2ndSemester)
          

      scatter= px.scatter(Dropout_data, x= "Course", y="Curricular units 1st sem (grade)" , color= "Target" )
      st.write(scatter)

  

    elif selected_plot == "Dados socioeconômicos":
        Gender_Map= {0:'Female', 1: 'Male'}
        Dropout_data['Gender'] = Dropout_data['Gender'].map(Gender_Map)
        st.subheader("Porcentagem de estado de estudante por gênero")   
        Gender_PercentBar= px.histogram( Dropout_data.sort_values(by='Gender'), x="Gender", color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=["mediumvioletred", "lightblue", "pink"],).update_layout(title={"text": "Percent :Course - Gender","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
        st.write(Gender_PercentBar)

        Gender_Bar = px.bar(Dropout_data.sort_values(by='Gender'), x="Course", color= "Gender",barmode= "group" ,text_auto= True, color_discrete_sequence=["pink", "lightblue"],)
        st.subheader("Distribuição de gênero de studantes por curso")     
        Gender_Bar.update_layout(title= "Numéro de estudantes por curso", xaxis_title="Cursos", yaxis_title="Número de estudantes")  
        st.write(Gender_Bar)
        

        Financial_Status= px.histogram(Dropout_data.sort_values(by='Course'), x= "Course", y= "Renda total", color="Course", barnorm= "percent")
        st.subheader("Índice de formação por renda total")
        Financial_Status.update_layout(xaxis_title="Cursos", yaxis_title= "Renda total")
        st.write(Financial_Status)
