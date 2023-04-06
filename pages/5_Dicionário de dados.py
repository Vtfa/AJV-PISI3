import base64
import streamlit as st

from style_funcs import *

page_style()
pdf_style()

glossary_file = './docs/glossary_00.pdf'


def page_5():
    with open(glossary_file,"rb") as pdf:
        base64_pdf = base64.b64encode(pdf.read()).decode('utf-8') + '#toolbar=1&navpanes=0&scrollbar=1&view=FitH'

    with st.container():
        st.title('Dicionário de dados')
        warning = '<p style="color: indianred; font-style: italic; font-weight: bold; font-size: 1.25rem;">' + \
        'Dicionário contendo as variáveis do dataset antes do tratamento.<br><br>'

        st.markdown(warning, unsafe_allow_html=True)

        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' + \
         'width="100%" height="100%" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

page_5()