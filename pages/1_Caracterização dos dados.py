from plot_funcs import *
from data_funcs import *
from aux_funcs import *

from streamlit_pandas_profiling import st_profile_report

title = "Caracterização dos dados de evasão acadêmica"
config_page(title)
page_style()


def page_1():
    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data', 'pandas_profile']

    if not valid_session_data(dataframes, '## :construction: Por favor, vá para página _Home_ page antes :construction:', 0.15):
        return

    datasets = {data: st.session_state[data] for data in dataframes}

    with st.container():
        st.title(title)

        tab1, tab2, tab3 = st.tabs(["Dataset", 'Gráficos', "Detalhamento de variáveis"])

        with tab1:
            with st.container():
                st.header('Tabela de dados')
                st.dataframe(
                    dataset_filter(datasets['dropout_data'],
                    marital_status=st.session_state['marital_status'],
                    course=st.session_state['course'],
                    gender=st.session_state['gender'],
                    age_range=st.session_state['age_range'],
                    escolaridade_mae=st.session_state['escolaridade_mae'],
                    escolaridade_pai=st.session_state['escolaridade_pai'],
                    ),
                    use_container_width=True,
                )

        with tab2:
            reset_filters()

            sidebar_01()

            with st.container():
                st.header('População')
                demographic_pyramid(datasets['gender_data'])

                gender_by_course(datasets['course_data'])

                gender_tree(datasets['course_data'])

                specific_gender_tree(datasets['course_data'], st.session_state['gender_select'])

                dropout_by_gender(datasets['debt_data'])

                dropout_by_age_debt(datasets['debt_data'], st.session_state['tree_path'])

        with tab3:
            st_profile_report(
                datasets['pandas_profile'],
                key='pandas_profile_wdgt',
            )


page_1()
