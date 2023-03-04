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

    dropout_data.loc[dropout_data['Admission grade'] <= 133, 'nota_do_vestibular'] = '0 - 132'
    dropout_data.loc[dropout_data['Admission grade'] > 166, 'nota_do_vestibular'] = '167 - 200'
    dropout_data['nota_do_vestibular'].fillna('133 - 166', inplace=True)
    
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
    

    # Início dos gráficos de comparação de nota com classe social
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

    st.write(dropout_data)

    # Definição de Classes Sociais
    dropout_data.loc[dropout_data['Renda total'] <= 1405, 'Classe social'] = 'Classe baixa'
    dropout_data.loc[dropout_data['Renda total'] >= 3000, 'Classe social'] = 'Classe alta'
    dropout_data['Classe social'].fillna('Classe média', inplace=True)


    histograma_teste= px.histogram(
        dropout_data,
        x='nota_do_vestibular',
        title='Contagem das notas de Admissão'
    )
    st.write(histograma_teste)

    histograma_admission1 = px.histogram(
        dropout_data,
        x='Admission grade', color='Classe social',
        title='Comparação da nota do vestibular com a classe social'
    )
    st.write(histograma_admission1)

    # Gráficos de comparação Notas Admission x Classe Social
    chart_type = st.radio('Selecione o tipo de gráfico:', ('Classe Baixa', 'Classe Média', 'Classe Alta'))
    if chart_type == 'Classe Baixa':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe baixa']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'Admission grade',
            title = 'Histograma de notas dos alunos da classe baixa'
        )
        st.write(histograma_admission_csocial)
    elif chart_type == 'Classe Média':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe média']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'Admission grade',
            title = 'Histograma de notas dos alunos da classe média'
        )
        st.write(histograma_admission_csocial)
    elif chart_type == 'Classe Alta':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe alta']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'Admission grade',
            title = 'Histograma de notas dos alunos de classe alta'
        )
        st.write(histograma_admission_csocial)







    histograma_admission2 = px.histogram(
        dropout_data,
        x='Admission grade', color='Classe social', barnorm = "percent",
        title='% Comparação da nota do vestibular com a classe social'
    )
    st.write(histograma_admission2)

    histograma_admission3 = px.histogram(
        dropout_data,
        x='Classe social'
    )

    # Gráficos de comparação Notas 1o sem x Classe Social
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


    # Gráficos de comparação Notas 2o sem x Classe Social
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
        title='Comparação das notas dos 2 semestres com a classe social',
    )
    st.write(scatter_semestres)

