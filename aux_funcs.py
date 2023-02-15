import streamlit as st

def valid_session_data(vars: list[str], msg: str) -> bool:
    for var in vars:
        if var not in st.session_state:
            st.markdown(msg)
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