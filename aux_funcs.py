from enum import Enum
import time
import streamlit as st
import pandas as pd


tabs_01 = Enum('tabs_01', ['table', 'plots', 'profile'])

def config_page(title: str) -> None:
    st.set_page_config(
        page_title=title,
        layout='wide',
        page_icon=u"\U0001F393",
        menu_items={
            'About': '''
            #### **Equipe**
            Aldemar S R Filho\n
            Douglas Rafael Miranda de Souza\n
            João Vitor da Silva Pires\n
            Vinicius Thalles Ferreira Araujo''',
        }
    )


def valid_session_data(dataframes: list[str], message: str, sleep_time: float = 0.35) -> bool:
    progress_bar = st.progress(0)
    step = 1 / len(dataframes)

    df_exists = {}
    for i, df in enumerate(dataframes, start=1):
        progress_bar.progress(step * i)
        time.sleep(sleep_time)

        if df not in st.session_state:
            df_exists[df] = False
            continue

        df_exists[df] = True

    time.sleep(sleep_time)
    progress_bar.empty()

    if not all(df_exists.values()):
        st.markdown(message, unsafe_allow_html=True)
        with st.expander('Errors', True):
            for df, exists in df_exists.items():
                if not exists:
                    st.error(f'⚠️ Could not find _**{df}**_ data')

        return False

    return True


def dataset_table_filters(options: dict[str: any]):
    with st.form("dataset_form"):
                marital_status = st.selectbox(
                    'Estado Civil',
                    options['Marital status'],
                    help='Estado civil a ser filtrado na tabela de dados',
                )

                course = st.selectbox(
                    'Curso',
                    options['Course'],
                    help='Curso a ser filtrado na tabela de dados',
                )

                gender = st.multiselect(
                    'Gender',
                    options['Gender'],
                    help='Genero a ser filtrado na tabela de dados',
                )

                age_range = st.multiselect(
                    'Faixa etária',
                    options['age_range'],
                    help='Faixa etária a ser filtrada na tabela de dados',
                )

                escolaridade_mae = st.selectbox(
                    'Escolaridade da mãe',
                    options['Escolaridade mae'],
                    help='Escolaridade da mãe a ser filtrada na tabela de dados',
                )

                escolaridade_pai = st.selectbox(
                    'Escolaridade do pai',
                    options['Escolaridade pai'],
                    help='Escolaridade do pai a ser filtrada na tabela de dados',
                )

                columns = st.multiselect(
                    'Colunas',
                    options['columns'],
                    help='Colunas a serem exibidas na tabela de dados. Vazio representa TODAS',
                )

                submitted = st.form_submit_button('Filtrar')

                if submitted:
                    st.session_state['marital_status'] = marital_status
                    st.session_state['course'] = course
                    st.session_state['gender'] = gender
                    st.session_state['age_range'] = age_range
                    st.session_state['escolaridade_mae'] = escolaridade_mae
                    st.session_state['escolaridade_pai'] = escolaridade_pai
                    st.session_state['dataframe_columns'] = columns


def sidebar_01_table():
    data: pd.DataFrame = st.session_state['dropout_data'][[
        'Marital status',
        'Course',
        'Gender',
        'age_range',
        'Escolaridade mae',
        'Escolaridade pai',
    ]]

    columns = st.session_state['dropout_data'].columns

    options = {column: data[column].dropna().unique().tolist()
            for column in data}

    multiselect_fields = ['Gender', 'age_range']

    for field, option in options.items():
        if field not in multiselect_fields:
            option.append('')
            option.sort()

    options['columns'] = columns

    st.header('Configuração de exibição da tabela')

    dataset_table_filters(options)


def sidebar_01_plots():
    st.header('Mapa de gêneros')
    st.session_state['gender_select'] = st.selectbox(
        'Gender',
        ['Female', 'Male'],
        help='Define the gender to be used at gender related plots',
    )
    st.session_state['age_interval'] = st.number_input(
        'Age range interval',
        step=1,
        help='Define o intervalo (em anos) a ser utilizado nos plts demográficos',
    )

    st.header('Mapa de relações')
    path_options = {
        'Faixa etária': 'age_range',
        'Status': 'Target',
        'Possui débito': 'debt',
        'Gênero': 'Gender',
    }

    path =  st.multiselect(
                'Faixa etária',
                path_options,
                default=['Faixa etária', 'Possui débito'],
                help='Define the variables to be ploted at treemap',
            )

    path = {path_options[var] for var in path}
    st.session_state['tree_path'] = path


def sidebar_01(tab: tabs_01):
    with st.sidebar:
        match tab:
            case tabs_01.table:
                sidebar_01_table()

            case tabs_01.plots:
                sidebar_01_plots()

            case tabs_01.profile:
                pass

            case _:
                pass


def change_tab_state(current_tab: str, tabs: list[str]):
    for tab in tabs:
        st.session_state[tab] = False

    st.session_state[current_tab] = True


def sidebar_page3():
    data: pd.DataFrame = st.session_state['dropout_data'][[
        'Marital status',
        'Course',
        'Gender',
        'age_range',
        'Escolaridade mae',
        'Escolaridade pai',
    ]]

    options = {column: data[column].dropna().unique().tolist()
            for column in data}

    multiselect_fields = ['Gender', 'age_range']

    for field, option in options.items():
        if field not in multiselect_fields:
            option.append('')
            option.sort()

    with st.sidebar:

        st.header('Plots configuration')
        st.session_state['gender_select'] = st.selectbox(
            'Gender',
            ['Female', 'Male'],
            help='Define the gender to be used at gender related plots',
        )
        st.session_state['age_interval'] = st.number_input(
            'Age range interval',
            step=1,
            help='Define the interval (in years) to be used at demographic plots',
        )
