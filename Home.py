import streamlit as st

from plotly.subplots import make_subplots
from data_funcs import *
from plot_funcs import *
from aux_funcs import *


title = "Predição de evasão acadêmica"
config_page(title)
page_style()

if 'dropout_data_raw' not in st.session_state:
    dropout_data_raw = load_data('data/dropout.csv')
    st.session_state['dropout_data_state'] = dropout_data_raw

if 'dropout_data' not in st.session_state:
    dropout_data = treat_data(dropout_data_raw)
    st.session_state['dropout_data'] = dropout_data

if 'gender_data' not in st.session_state:
    st.session_state['gender_data'] = get_gender_data(dropout_data)

if 'course_data' not in st.session_state:
    st.session_state['course_data'] = get_course_data(dropout_data)

if 'debt_data' not in st.session_state:
    st.session_state['debt_data'] = get_debt_data(dropout_data)


def main():
    with st.container():
        st.title(title)

    with st.container():

        st.header('Resumo')

        abstract =('<div class="content-size justified-text indent-text"">' \
            "A evasão do ensino superior ainda é um desafio a ser superado em diversos países, em 2008, a média de evasão de 19 países da OCDE com dados disponível "\
            "era de 31%. Esse trabalho busca analisar dados socioeconômicos de alunos de universidades portuguesas que estão no primeiro ano dos seus estudos, com o"\
            "objetivo de identificar fatores que possam contribuir negativamente ou positivamente para seu desempenho acadêmica e para o abandono escolar, também serão"\
            "analisados fatores econômicos em nível nacional, buscando verificar se também podem  influenciar os resultados dos alunos"\
            '</div><br><br>'
        )
        st.markdown(abstract, unsafe_allow_html=True)

        st.header('Objetivos')

        objectives =('<ul>' \
            '<li class="content-size">Descobrir quais são os principais fatores socioeconômicos que influenciam o desempenho acadêmico dos estudantes no ensino superior e suas chances de  evasão.</li>'\
            '<li class="content-size">Usar métodos de Machine Learning para prever quais estudantes estão em maior risco de evasão</li>'\
            '<li class="content-size">Verificar como fatores macroeconômicos do país interagem com os fatores socioeconômicos dos estudantes </li>'\
            '<li class="content-size">Estudar a literatura e comparar os resultados encontrados para avançar o entendimento sobre o problema</li>'\
            '</ul>'
        )
        st.markdown(objectives, unsafe_allow_html=True)

        st.header('Questionamentos')

        objectives =('<div class="content-size justified-text italic">' \
            '<p>Quais são os principais fatores socioeconômicos que influenciam no desempenho e chances de evasão dos estudantes?<br>' \
            'Como fatores socioeconômicos individuais afetam o desempenho acadêmico dos estudantes e suas chances de desistirem da universidade?<br>' \
            'O nível educacional e ocupação dos pais influencia nisso?<br>' \
            'Como as bolsas de estudo afetam os alunos?' \
            '</p>' \

            '<p>Como os fatores macroeconômicos podem afetar no índice de evasão?<br>' \
            'Levando em conta a situação econômica do país, é possível que fatores macroeconômicos, como inflação, taxa de desemprego e variação do PIB, ' \
            'possam afetar o desempenho dos alunos e causar um aumento na evasão da universidade?' \
            'Como esses fatores afetam alunos de diferentes grupos de alunos?</p>'\

            '<p>Os cursos possuem algum grau de impacto nas taxas de evasão? Se sim, quais cursos?<br>' \
            '</p></div>'
        )

        st.markdown(objectives, unsafe_allow_html=True)


main()
