import time
import streamlit as st
import pandas as pd


def config_page(title: str) -> None:
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


def page_style(menu_title: str = '#AJV'):
    st.markdown(f"""
        <style>
        .justified-text {{
            text-align: justify;
        }}
        .content-size {{
            font-size:1.05em !important;
        }}
        .indent-text {{
            text-indent: 40px;
        }}
        .italic {{
            font-style: italic;
        }}
        .streamlit-expanderHeader {{
            font-size: 1.05em;
            font-weight: bold;
            color: IndianRed;
        }}
        [data-testid="stSidebarNav"]::before {{
            content: "{menu_title}";
            color: indianred;
            font-weight: bold;
            margin-left: 20px;
            font-size: 30px;
            position: relative;
            top: 100px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
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


def sidebar_01():
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
        st.header('Dataset table configuration')

        with st.expander('Filtros', True):
            with st.form("dataset_form"):
                marital_status =  st.selectbox(
                    'Estado Civil',
                    options['Marital status'],
                    help='Define the gender to be filtered at dataset',
                )

                course =  st.selectbox(
                    'Curso',
                    options['Course'],
                    help='Define the course to be filtered at dataset',
                )

                gender =  st.multiselect(
                    'Gender',
                    options['Gender'],
                    help='Define the gender to be filtered at dataset',
                )

                age_range =  st.multiselect(
                    'Faixa etária',
                    options['age_range'],
                    help='Define the age range to be filtered at dataset',
                )

                escolaridade_mae =  st.selectbox(
                    'Escolaridade da mãe',
                    options['Escolaridade mae'],
                    help='Define the mothers schooling to be filtered at dataset',
                )

                escolaridade_pai =  st.selectbox(
                    'Escolaridade do pai',
                    options['Escolaridade pai'],
                    help='Define the fathers schooling to be filtered at dataset',
                )

                submitted = st.form_submit_button('Filtrar')

                if submitted:
                    st.session_state['marital_status'] = marital_status
                    st.session_state['course'] = course
                    st.session_state['gender'] = gender
                    st.session_state['age_range'] = age_range
                    st.session_state['escolaridade_mae'] = escolaridade_mae
                    st.session_state['escolaridade_pai'] = escolaridade_pai

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
