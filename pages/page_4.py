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

    # Divisão das notas de admissão em 2 tipos
    dropout_data.loc[dropout_data['Admission grade'] <= 145, 'nota_do_vestibular'] = '95 - 145'
    dropout_data.loc[dropout_data['Admission grade'] > 145, 'nota_do_vestibular'] = '146 - 200'
#    dropout_data['nota_do_vestibular'].fillna('67 - 132', inplace=True)
    
    # Divisão das notas dos semestres em 3 tipos
    dropout_data.loc[dropout_data['Curricular units 1st sem (grade)'] < 9.75, 'nota_1o_sem'] = '0 - 1'
    dropout_data.loc[dropout_data['Curricular units 1st sem (grade)'] > 15, 'nota_1o_sem'] = '15 - 20'
    dropout_data['nota_1o_sem'].fillna('10 - 15', inplace=True)

    dropout_data.loc[dropout_data['Curricular units 2nd sem (grade)'] < 9.75, 'nota_2o_sem'] = '0 - 1'
    dropout_data.loc[dropout_data['Curricular units 2nd sem (grade)'] > 15, 'nota_2o_sem'] = '15 - 20'
    dropout_data['nota_2o_sem'].fillna('10 - 15', inplace=True)

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
    

    # definindo cores
    cores_notas_vestibular = ["#FF6961", "#87CEEB"]
    cores_classes = ["#87CEEB", "#FF6961", "#98FB98"]
    cores_notas_semestres = ["#FF6961", "#87CEEB", "#98FB98"]


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
        color_discrete_sequence=cores_notas_vestibular,
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



    # Gráficos de comparação Notas Admission x Classe Social
    '''
    ordem_notas_do_vestibular = ['95 - 145', '146 - 200']
    chart_type = st.radio('Selecione o tipo de gráfico:', ('Classe Baixa', 'Classe Média', 'Classe Alta'))
    if chart_type == 'Classe Baixa':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe baixa']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'nota_do_vestibular',
            category_orders={'nota_do_vestibular': ordem_notas_do_vestibular},
            title = 'Histograma de notas dos alunos da classe baixa'
        )
        st.write(histograma_admission_csocial)
    elif chart_type == 'Classe Média':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe média']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'nota_do_vestibular',
            category_orders={'nota_do_vestibular': ordem_notas_do_vestibular},
            title = 'Histograma de notas dos alunos da classe média'
        )
        st.write(histograma_admission_csocial)
    elif chart_type == 'Classe Alta':
        df_admission_csocial = dropout_data.loc[dropout_data['Classe social'] == 'Classe alta']
        histograma_admission_csocial = px.histogram(
            df_admission_csocial,
            x = 'nota_do_vestibular',
            category_orders={'nota_do_vestibular': ordem_notas_do_vestibular},
            title = 'Histograma de notas dos alunos de classe alta'
        )
        st.write(histograma_admission_csocial)
    '''


    ordem_classes_sociais = ['Classe baixa', 'Classe média', 'Classe alta']
    chart_type_admission = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'))
    
    if chart_type_admission == 'Distribuição':
        histograma_admission1 = px.histogram(
            dropout_data,
            x='Admission grade', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do vestibular com a classe social'
        )
        st.write(histograma_admission1)
    elif chart_type_admission == 'Porcentagem':
        histograma_admission3 = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_do_vestibular',
            color_discrete_sequence=cores_notas_vestibular,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do vestibular por classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_admission3)




    # Gráficos de comparação Notas 1o sem x Classe Social
    chart_type_1o_sem = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'), key='chart_type_1o_sem')
    if chart_type_1o_sem == 'Distribuição':
        histograma_sem1 = px.histogram(
            dropout_data,
            x='Curricular units 1st sem (grade)', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do 1o semestre com a classe social'
        )
        st.write(histograma_sem1)
    elif chart_type_1o_sem == 'Porcentagem':
        histograma_sem1_porcent = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_1o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm = "percent",
            text_auto=True,
            title='Porcentagem de notas do 1o semestre por classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_sem1_porcent)


    # Gráficos de comparação Notas 2o sem x Classe Social
    chart_type_2o_sem = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'), key='chart_type_2o_sem')
    if chart_type_2o_sem == 'Distribuição':
        histograma_sem2 = px.histogram(
            dropout_data,
            x='Curricular units 2nd sem (grade)', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do 2o semestre com a classe social'
        )
        st.write(histograma_sem2)
    elif chart_type_2o_sem == 'Porcentagem':
        histograma_sem2_porcent = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_2o_sem', 
            color_discrete_sequence=cores_notas_semestres,
            barnorm = "percent", 
            text_auto= True,
            title='Comparação da nota do 2o semestre com a classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_sem2_porcent)



    scatter_semestres = px.scatter(
        dropout_data,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='Classe social', color_discrete_sequence=cores_classes,
        title='Comparação das notas dos 2 semestres com a classe social',
    )
    st.write(scatter_semestres)

    # Dataframes de Escolaridade dos Pais
    df_both_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') & (dropout_data['Escolaridade pai'] == 'ensino superior')]

    df_one_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') ^ (dropout_data['Escolaridade pai'] == 'ensino superior')]

    df_both_secondary = dropout_data[(dropout_data['Escolaridade mae'] == 'medio completo') & (dropout_data['Escolaridade pai'] == 'medio completo')]

    df_both_primary = dropout_data[(dropout_data['Escolaridade mae'] == 'fundamental incompleto') & (dropout_data['Escolaridade pai'] == 'fundamental incompleto')]

    # add coluna de escolaridade dos pais no dropout_data
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'ensino superior') & (dropout_data['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'ambos com ensino superior'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'ensino superior') ^ (dropout_data['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'um com ensino superior'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'medio completo') & (dropout_data['Escolaridade pai'] == 'medio completo'), 'Escolaridade_Maes&Pais'] = 'ambos com medio completo'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'fundamental incompleto') & (dropout_data['Escolaridade pai'] == 'fundamental incompleto'), 'Escolaridade_Maes&Pais'] = 'ambos com fundamental incompleto'
    st.write(dropout_data)

    # Plots de Escolaridade dos Pais X Classe Social
    ordem_escolaridade = ['ambos com fundamental incompleto', 'ambos com medio completo', 'um com ensino superior', 'ambos com ensino superior']
    chart_type_escolaridade = st.radio('Selecione o tipo de gráfico:', ('Vestibular', '1o Semestre', '2o Semestre'))
    if chart_type_escolaridade == 'Vestibular':
        histograma_escolaridade_vestibular = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_do_vestibular',
            color_discrete_sequence=cores_notas_vestibular,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do vestibular por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_vestibular)
    elif chart_type_escolaridade == '1o Semestre':
        histograma_escolaridade_1o_sem = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_1o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do 1o semestre por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_1o_sem)
    elif chart_type_escolaridade == '2o Semestre':
        histograma_escolaridade_2o_sem = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_2o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do 2o semestre por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_2o_sem)




