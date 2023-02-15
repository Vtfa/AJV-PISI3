import streamlit as st

def valid_session_data(vars: list[str], msg: str) -> bool:
    for var in vars:
        if var not in st.session_state:
            st.markdown(msg)
            return False

    return True