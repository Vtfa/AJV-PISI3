import streamlit as st
import time

def valid_session_data(dataframes: list[str], msg: str) -> bool:
    progress_text = "Loading data. Please wait..."
    progress_bar = st.progress(0, text=progress_text)
    step = 1 / len(dataframes)

    df_exists = {}
    for i, df in enumerate(dataframes, start=1):
        progress_bar.progress(step * i, text=progress_text)
        time.sleep(0.35)

        if df not in st.session_state:
            df_exists[df] = False
            continue

        df_exists[df] = True

    progress_bar.empty()

    if not all(df_exists.values()):
        st.markdown(msg)
        with st.expander('**Errors**', True):
            for df, exists in df_exists.items():
                if not exists:
                    st.error(f'⚠️ Could not find _**{df}**_ data')

        return False

    return True

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

def sidebar_01():
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