import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

header = st.container()
dataset = st.container()

with header:
    st.title('Unidades Curriculares e Notas')

with dataset:
    dropout_data = st.session_state['dropout_data_state']

    st.subheader('Unidades Curriculares')

    st.text("Em relação as Unidades curricular a Europa possui um sistema bem diferente ao brasileiro, em temporada de aplicação cerca de 40 disciplinas")
    st.text(" podem ser aplicadas para avaliação, abaixo segue a relação da quantidade de diciplinas escolhidas e aprovadas pelos alunos.")
    dfpagina42 = dropout_data[['Curricular units 1st sem (approved)','Curricular units 2nd sem (approved)',
                               'Curricular units 1st sem (enrolled)','Curricular units 2nd sem (enrolled)',
                               'Curricular units 1st sem (evaluations)','Curricular units 2nd sem (evaluations)','Target']]

    conta_1sem_apv = pd.DataFrame(dfpagina42['Curricular units 1st sem (approved)'].value_counts())
    conta_2sem_apv = pd.DataFrame(dfpagina42['Curricular units 2nd sem (approved)'].value_counts())
    option2 = st.selectbox(
        'Mudar o grupo visualizado',
        ('1º Semestre', '2º Semestre',)
    )

    if option2 == '1º Semestre':
        st.bar_chart(conta_1sem_apv)
    elif option2 == '2º Semestre':
        st.bar_chart(conta_2sem_apv)
        
    conta_1sem_cur = pd.DataFrame(dfpagina42['Curricular units 1st sem (enrolled)'].value_counts())
    conta_2sem_cur = pd.DataFrame(dfpagina42['Curricular units 2nd sem (enrolled)'].value_counts())
    option3 = st.selectbox(
        'Mudar o grupo visualizado',
        ('1º Semestre', '2º Semestre',),
        key = 'option3'
    )

    if option3 == '1º Semestre':
        st.bar_chart(conta_1sem_cur)
    elif option3 == '2º Semestre':
        st.bar_chart(conta_2sem_cur)

    conta_1sem_ava = pd.DataFrame(dfpagina42['Curricular units 1st sem (enrolled)'].value_counts())
    conta_2sem_ava = pd.DataFrame(dfpagina42['Curricular units 2nd sem (enrolled)'].value_counts())
    option4 = st.selectbox(
        'Mudar o grupo visualizado',
        ('1º Semestre', '2º Semestre',),
        key = 'option4'
    )

    if option4 == '1º Semestre':
        st.bar_chart(conta_1sem_ava)
    elif option4 == '2º Semestre':
        st.bar_chart(conta_2sem_ava)
    

    dfpagina41 = dropout_data[['Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)', 'Target', 'Admission grade', 'Debtor']]
    dfpagina41.loc[dfpagina41['Admission grade'] <= 140, 'nota_do_vestibular'] = 'inferior ou igual a 140'
    dfpagina41.nota_do_vestibular = dfpagina41.nota_do_vestibular.fillna('superior a 140', inplace=False)

    df41grad = dfpagina41.loc[(dfpagina41['Target']=='Graduate')]
    df41drop= dfpagina41.loc[(dfpagina41['Target']=='Dropout')]


    st.title('Relação entre as notas')
    option = st.selectbox(
        'Mudar o grupo visualizado',
        ('Formados', 'Desistentes', 'Todos')
    )

    fig = px.scatter(
        df41grad,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)',
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre'
        },
        title='Notas dos alunos que se formaram',
        width=800, height=400
        )


    fig2 = px.scatter(
        df41drop,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)',
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre'
        },
        title='Notas dos alunos que desistiram',
        width=800, height=400
        )


    fig3 = px.scatter(
        dfpagina41,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='nota_do_vestibular',
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre',
            'nota_do_vestibular' : 'Nota de Admissão'
        },
        title='Notas de todos alunos',
        width=800, height=400
        )

        
    if option == 'Formados':
        st.write(fig)
    elif option == 'Desistentes':
        st.write(fig2)
    else:
        st.write(fig3) 