import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

header = st.container()
dataset = st.container()

with header:
    st.title('Página 4 - Notas')

with dataset:
    dropout_data = st.session_state['dropout_data']

    dropout_data.loc[dropout_data['Admission grade'] <= 150, 'nota_do_vestibular'] = 'inferior ou igual a 150'
    dropout_data.loc[dropout_data['Admission grade'] > 150, 'nota_do_vestibular'] = 'superior ou igual a 150'

    df41grad = dropout_data.loc[(dropout_data['Target']=='Graduate')]
    df41drop= dropout_data.loc[(dropout_data['Target']=='Dropout')]


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
        dropout_data,
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

    st.title('Influência da renda dos pais nas notas')


    dropout_data.loc[dropout_data['Renda total'] <= 1405, 'Classe social'] = 'Classe baixa'
    dropout_data.loc[dropout_data['Renda total'] > 1405, 'Classe social'] = 'Classe média'
    dropout_data.loc[dropout_data['Renda total'] >= 3000, 'Classe social'] = 'Classe alta'


    fig6 = px.histogram(
        dropout_data,
        x='Admission grade', color='Classe social',
        title='Comparação da nota do vestibular com a classe social'
    )
    st.write(fig6)

    fig4 = px.histogram(
        dropout_data,
        x='Curricular units 1st sem (grade)', color='Classe social',
        title='Comparação da nota do 1o semestre com a classe social'
    )
    st.write(fig4)

    fig5 = px.histogram(
        dropout_data,
        x='Curricular units 2nd sem (grade)', color='Classe social',
        title='Comparação da nota do 2o semestre com a classe social'
    )
    st.write(fig5)

    fig7 = px.scatter(
        dropout_data,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='Classe social',
        title='Comparação das notas dos 2 semestres com a classe social'
    )
    st.write(fig7)
