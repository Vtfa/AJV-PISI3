import streamlit as st


def page_style(menu_title: str = '#AJV'):
    st.markdown(
        f'''
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
        [data-baseweb="tab"] {{
            font-size: 1.15rem;
            font-weight: bold;

        }}
        .block-container {{
            padding-top: 2rem;
        }}
        </style>
        ''',
        unsafe_allow_html=True,
    )


def tabs_style():
    st.markdown(
        f'''
        <style>
         [data-testid="stHorizontalBlock"] button[kind="secondary"] {{
            font-size: 1.10rem;
            font-weight: bold;
        }}

         [data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {{
            font-size: 1.10rem;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }}

         [data-testid="stHorizontalBlock"] button[kind="secondary"]:disabled {{
            font-size: 1.10rem;
            font-weight: bold;
            background: indianred;
            color: white;
        }}
        </style>
        ''',
        unsafe_allow_html=True,
    )


def dataframe_style():
    st.markdown(
        f'''
        <style>
         [data-testid="stDataFrameResizable"] {{
            font-size: 1.10rem;
            font-weight: bold;
            height: calc(100vh - 430px)  !important;
        }}
        </style>
        ''',
        unsafe_allow_html=True,
    )


def page1_style():
    st.markdown(
        f'''
        <style>
         .block-container {{
            padding-bottom: 0px;
        }}
        </style>
        ''',
        unsafe_allow_html=True,
    )