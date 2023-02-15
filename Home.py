import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from data_funcs import *
from plot_funcs import *


title = "Predict Dropout or Academic Success"

st.set_page_config(
    page_title=title,
    layout='wide',
    page_icon=u"\U0001F393",
    menu_items={
        'About': '''
        #### **Equipe**
        Aldemar S R Filho\n
        Arthur de Barros Botelho dos Santos\n
        Douglas Rafael Miranda de Souza\n
        João Vitor da Silva Pires\n
        Vinicius Thalles Ferreira Araujo''',
    }
)


def main():
    with st.container() as header:
        st.title(title)

    with st.container() as dataset:
        dropout_data = pd.read_csv('data/dropout.csv')

        st.session_state['dropout_data_state'] = dropout_data

        treat_data(dropout_data)

        st.subheader('Age of students')

        gender_data = (
            dropout_data[['age_range', 'Gender', 'Course']]
            .groupby(['age_range', 'Gender'])
            .count()
        )
        gender_data = gender_data.unstack('Gender').droplevel(0, 'columns')

        if 'gender_data' not in st.session_state:
            st.session_state['gender_data'] = gender_data

        demographic_pyramid(gender_data)

        bar_age = pd.DataFrame(dropout_data['Age at enrollment'].value_counts())
        st.bar_chart(bar_age)


        course_data = (
            dropout_data[['age_range', 'Gender', 'Course', 'Displaced']]
            .groupby(['Course', 'Gender', 'age_range'])
            .count()
            .reset_index()
        )
        course_data.rename(columns={'Displaced': 'count'}, inplace=True)

        gender_tree = px.treemap(
                course_data,
                title='Gender distribution by course',
                path=[ 'Course', 'Gender'],
                color_continuous_scale='RdBu',
                color='count',
                values='count',
                height=1000,
        )

        gender_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

        gender_tree.update_layout(
            title_font_size=26,
            font_size=16,
        )

        st.plotly_chart(gender_tree, use_container_width=True)

        female_tree = px.treemap(
                course_data.query('Gender == "Female"'),
                title='Course and age distribution for female students',
                path=['Gender', 'Course', 'age_range'],
                values='count',
                height=1000,
        )

        female_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

        female_tree.update_layout(
            title_font_size=26,
            font_size=16,
        )

        st.plotly_chart(female_tree, use_container_width=True)

        male_tree = px.treemap(
                course_data.query('Gender == "Male"'),
                title='Course and age distribution for male students',
                path=['Gender', 'Course', 'age_range'],
                values='count',
                height=1000,
        )

        male_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

        male_tree.update_layout(
            title_font_size=26,
            font_size=16,
        )

        st.plotly_chart(male_tree, use_container_width=True)

        course_gender_age = go.Figure()
        course_gender_age_index = (
            course_data['Course'].str.replace('(', ' ', regex=False)
            .str.replace(' ', '<br>')
            .str.replace(')', '', regex=False)
            .unique()
        )
        course_gender_age_range = [0, 650]

        course_gender_data = course_data.groupby(['Course', 'Gender'])[['count']].sum()
        course_gender_data = course_gender_data.unstack().droplevel(0, 1)

        course_gender_age.add_trace(
            go.Bar(
                name="Female",
                x=course_gender_age_index,
                y=course_gender_data["Female"],
                orientation='v',
                marker={
                    'color': 'rgba(99, 110, 250, 0.5)'
                },
            ),
        )

        course_gender_age.add_trace(
            go.Bar(
                name="Male",
                x=course_gender_age_index,
                y=course_gender_data["Male"],
                orientation='v',
                marker={
                    'color': 'rgba(0, 204, 150, 0.5)'
                },
            ),
        )

        course_gender_age.update_xaxes(
            title_text='Course',
            title_standoff=35,
            tickangle=-90,
        )

        course_gender_age.update_yaxes(
            title_text='Students',
            title_standoff=25,
        )

        course_gender_age.update_layout(
            height=900,
            font_size=14,
            title='Gender distribution by course',
            barmode='stack',
            hovermode='x unified',
            margin={'b': 190},
            margin_pad=10,
        )

        st.plotly_chart(course_gender_age, use_container_width=True)


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
