import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from data_funcs import *
from plot_funcs import *
from aux_funcs import *


title = "Predict Dropout or Academic Success"
config_page(title)
page_style()


def main():
    with st.container() as header:
        st.title(title)

    with st.container() as dataset:
        dropout_data = pd.read_csv('data/dropout.csv')
        st.session_state['dropout_data_state'] = dropout_data

        treat_data(dropout_data)

        st.subheader('Resumo')

        abstract =('<div class="content-size justified-text">' \
            "   A evasão do ensino superior ainda é um desafio a ser superado em diversos países, em 2008, a média de evasão de 19 países da OCDE com dados disponível "\
            "era de 31%. Esse trabalho busca analisar dados socioeconômicos de alunos de universidades portuguesas que estão no primeiro ano dos seus estudos, com o"\
            "objetivo de identificar fatores que possam contribuir negativamente ou positivamente para seu desempenho acadêmica e para o abandono escolar, também serão"\
            "analisados fatores econômicos em nível nacional, buscando verificar se também podem  influenciar os resultados dos alunos"\
            '</div><br><br>'
        )
        st.markdown(abstract, unsafe_allow_html=True)

        st.subheader('Objetivos')

        objectives =('<ul>' \
            '<li class="content-size">Descobrir quais são os principais fatores socioeconômicos que influenciam o desempenho acadêmico dos estudantes no ensino superior e suas chances de  evasão.</li>'\
            '<li class="content-size">Usar métodos de Machine Learning para prever quais estudantes estão em maior risco de evasão</li>'\
            '<li class="content-size">Verificar como fatores macroeconômicos do país interagem com os fatores socioeconômicos dos estudantes </li>'\
            '<li class="content-size">Estudar a literatura e comparar os resultados encontrados para avançar o entendimento sobre o problema</li>'\
            '</ul>'
        )
        st.markdown(objectives, unsafe_allow_html=True)

        gender_data = get_gender_data(dropout_data)
        if 'gender_data' not in st.session_state:
            st.session_state['gender_data'] = gender_data

        course_data = get_course_data(dropout_data)
        if 'course_data' not in st.session_state:
            st.session_state['course_data'] = course_data

        df = dropout_data.groupby(['Gender'])['Gender'].count().reset_index(name='count')
        st.title('Gender of students')
        fig = px.pie(df, values='count', names='Gender')
        st.plotly_chart(fig, use_container_width=True)

        st.title('Dropout rates by gender')

        # novo dataframe apenas com registros em que target = dropout
        df_droupout_gender = dropout_data[(dropout_data['Target'] == 'Dropout')]

        # DF auxiliar com total de male e female para ser usado no gráfico abaixo
        dfaux_dropout_gender = df_droupout_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_dropout_gender')
        pie_dropout_gender = px.pie(
            dfaux_dropout_gender,
            values='soma_dropout_gender',
            names='Gender'
        )

        st.plotly_chart(pie_dropout_gender, use_container_width=True)

        st.title('Graduation rates by gender')

        # novo dataframe apenas com registros em que target = graduate
        df_graduate_gender = dropout_data[(dropout_data['Target'] == 'Graduate')]

        # DF auxiliar com total de male e female para ser usado no gráfico abaixo
        dfaux_graduate_gender = df_graduate_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_graduate_gender')
        pie_graduate_gender = px.pie(
            dfaux_graduate_gender,
            values='soma_graduate_gender',
            names='Gender'
        )

        st.plotly_chart(pie_graduate_gender, use_container_width=True)

        st.title("Histograma de dropout por curso")

        histograma_drop = px.histogram(
            dropout_data,
            x = "Course",
        )

        st.plotly_chart(histograma_drop, use_container_width=True)


        #
        #
        # Aqui começa o codigo do grafico relacionando a coluna 'Debtor' com a evasao

        dfaux_target = dropout_data.groupby(['Target'])['Target'].count().reset_index(name='soma_target')

        df_sem_divida = dropout_data[dropout_data.Debtor==0]
        dfaux_sem_divida = df_sem_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_sem_divida')

        df_com_divida = dropout_data[dropout_data.Debtor==1]
        dfaux_com_divida = df_com_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_com_divida')

        st.title('Situação dos estudantes por dívida')
        option = st.selectbox(
            'Mudar o grupo visualizado',
            ('Todos estudantes', 'Endividados', 'Sem dívidas')
        )

        grafico_target_geral = px.pie(
            dfaux_target, values='soma_target',
            names='Target',
            color='Target',
            color_discrete_map={
                'Dropout':'rgb(239, 85, 59)',
                'Enrolled':'rgb(99, 110, 250)',
                'Graduate':'rgb(0, 204, 150)',
            },
            title='Situação Acadêmica dos Estudantes '
        )

        grafico_target_endividados = px.pie(
            dfaux_com_divida,
            values='soma_com_divida',
            names='Target',
            color='Target',
            color_discrete_map={
                'Dropout':'rgb(239, 85, 59)',
                'Enrolled':'rgb(99, 110, 250)',
                'Graduate':'rgb(0, 204, 150)',
            },
            title='Situação Acadêmica dos Estudantes Endividados'
        )

        grafico_target_estudantes_sem_dividas = px.pie(
            dfaux_sem_divida,
            values='soma_sem_divida',
            names='Target',
            color='Target',
            color_discrete_map={
                'Dropout':'rgb(239, 85, 59)',
                'Enrolled':'rgb(99, 110, 250)',
                'Graduate':'rgb(0, 204, 150)',
            },
            title='Situação Acadêmica dos Estudantes Sem dívidas'
        )

        if option == 'Todos estudantes':
            st.plotly_chart(grafico_target_geral, use_container_width=True)
        elif option == 'Endividados':
            st.plotly_chart(grafico_target_endividados, use_container_width=True)
        else:
            st.plotly_chart(grafico_target_estudantes_sem_dividas, use_container_width=True)

    st.title('Situação dos estudantes internacionais')
    option_internacioal = st.selectbox('Mudar o grupo visualizado', ('Todos estudantes', 'Estudantes Internacionais'))

    df_internacional = dropout_data[dropout_data.Nacionality != 1]
    dfaux_internacional = df_internacional.groupby(['Target'])['Target'].count().reset_index(name='soma_target_internacional')
    pie_target_internacional = px.pie(
        dfaux_internacional,
        values='soma_target_internacional',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)'
        },
        title='Situação acadêmica dos estudantes'
    )

    if option_internacioal == 'Todos estudantes':
        st.plotly_chart(grafico_target_geral, use_container_width=True)
    else:
        st.plotly_chart(pie_target_internacional, use_container_width=True)

    st.title('Situação dos estudantes portadores de bolsas de estudo')
    option_scholarship = st.selectbox(
        'Mudar o grupo visualizado',
        ('Estudantes não portadores de bolsas de estudo', 'Estudantes portadores de bolsas de estudo')
    )

    df_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 1)]
    dfaux_scholarship = df_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_scholarship')

    df_no_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 0)]
    dfaux_no_scholarship = df_no_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_no_scholarship')

    pie_scholarship = px.pie(
        dfaux_scholarship,
        values='soma_scholarship',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)',
        },
        title='Situação acadêmica dos estudantes sem bolsa de estudo',
    )

    pie_no_scholarship = px.pie(
        dfaux_no_scholarship,
        values='soma_no_scholarship',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)',
        },
        title='Situação acadêmica dos estudantes sem bolsa de estudos',
    )

    if option_scholarship == 'Estudantes não portadores de bolsas de estudo':
        st.plotly_chart(pie_no_scholarship, use_container_width=True)
    else:
        st.plotly_chart(pie_scholarship, use_container_width=True)


    dropout_data['debt'] = np.where(
        (dropout_data['Debtor'] == 1) | (dropout_data['Tuition fees up to date'] == 0), 'has debt', 'up to date'
    )

    debt_data = (
        dropout_data[['age_range', 'Gender', 'Course', 'debt', 'Displaced', 'Target']]
        .groupby(['Gender', 'Target', 'Course', 'age_range', 'debt'])
        .count()
        .reset_index()
    )
    # debt_data = debt_data[~debt_data['Target'].isin(['Enrolled'])]
    debt_data.rename(columns={'Displaced': 'count'}, inplace=True)

    debt_gender_tree = px.treemap(
                debt_data,
                title='Target distribution by gender',
                path=['Gender', 'Target', 'debt'],
                values='count',
                height=1000,
        )

    debt_gender_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    debt_gender_tree.update_layout(
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(debt_gender_tree, use_container_width=True)

    debt_tree = px.treemap(
                debt_data,
                title='Target distribution by age and debt',
                path=['age_range', 'Target', 'debt'],
                values='count',
                height=1000,
        )

    debt_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    debt_tree.update_layout(
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(debt_tree, use_container_width=True)

main()
