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
    dropout_data = st.session_state['dropout_data']

    dropout_data.loc[dropout_data['Admission grade'] <= 150, 'nota_do_vestibular'] = 'inferior ou igual a 150'
    dropout_data.loc[dropout_data['Admission grade'] > 150, 'nota_do_vestibular'] = 'superior ou igual a 150'
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
    
    #??
    dfpagina41 = dropout_data[['Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)', 'Target', 'Admission grade', 'Debtor']]
    dfpagina41.loc[dfpagina41['Admission grade'] <= 140, 'nota_do_vestibular'] = 'inferior ou igual a 140'
    dfpagina41.nota_do_vestibular = dfpagina41.nota_do_vestibular.fillna('superior a 140', inplace=False)
    #??

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


    histograma_admission1 = px.histogram(
        dropout_data,
        x='Admission grade', color='Classe social',
        title='Comparação da nota do vestibular com a classe social'
    )
    st.write(histograma_admission1)

    histograma_admission2 = px.histogram(
        dropout_data,
        x='Admission grade', color='Classe social', barnorm = "percent",
        title='% Comparação da nota do vestibular com a classe social'
    )
    st.write(histograma_admission2)

    histograma_sem1 = px.histogram(
        dropout_data,
        x='Curricular units 1st sem (grade)', color='Classe social',
        title='Comparação da nota do 1o semestre com a classe social'
    )
    st.write(histograma_sem1)

    histograma_sem1_porcent = px.histogram(
        dropout_data,
        x='Classe social', color='Curricular units 1st sem (grade)', barnorm = "percent",
        title='Comparação da nota do 1o semestre com a classe social'
    )
    st.write(histograma_sem1_porcent)



    histograma_sem2 = px.histogram(
        dropout_data,
        x='Curricular units 2nd sem (grade)', color='Classe social',
        title='Comparação da nota do 2o semestre com a classe social'
    )
    st.write(histograma_sem2)

    histograma_sem2_porcent = px.histogram(
        dropout_data,
        x='Curricular units 2nd sem (grade)', color='Classe social', barnorm = "percent", text_auto= True,
        title='Comparação da nota do 2o semestre com a classe social'
    )
    st.write(histograma_sem2_porcent)

    scatter_semestres = px.scatter(
        dropout_data,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='Classe social',
        title='Comparação das notas dos 2 semestres com a classe social'
    )
    st.write(scatter_semestres)
