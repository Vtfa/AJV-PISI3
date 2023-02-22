import streamlit as st

def valid_session_data(dataframes: list[str], msg: str) -> bool:
    df_exists = {}
    for df in dataframes:
        if df not in st.session_state:
            df_exists[df] = False
            continue

        df_exists[df] = True

    if not all(df_exists.values()):
        st.markdown(msg)
        with st.expander('Errors'):
            for df, exists in df_exists.items():
                if not exists:
                    st.error(f'⚠️ Could not find {df} data ⚠️')
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


def page_style():
    st.markdown("""
        <style>
        .justified-text {
            text-align: justify;
        }
        .content-size {
            font-size:1.05em !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )