from plot_funcs import *
from data_funcs import *
from aux_funcs import *
from style_funcs import *

from streamlit_pandas_profiling import st_profile_report

title = "Caracterização dos dados de evasão acadêmica"
config_page(title)
page_style()
tabs_style()
dataframe_style()
page1_style()

dataset_tab = 'dataset_tab_active'
plots_tab = 'plots_tab_active'
profile_tab = 'profile_tab_active'

tabs = ['dataset_tab_active', 'plots_tab_active', 'profile_tab_active']

for tab in tabs:
    if 'dataset_tab_active' not in st.session_state:
        st.session_state['dataset_tab_active'] = True

    if tab not in st.session_state:
        st.session_state[tab] = False


def page_1():
    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data', 'pandas_profile']

    if not valid_session_data(dataframes, '## :construction: Por favor, vá para página _Home_ page antes :construction:', 0.05):
        return

    datasets = {data: st.session_state[data] for data in dataframes}

    with st.container():
        st.title(title)

        col1, col2, col3, _ = st.columns([1, 1, 4, 4])
        col1.button("Dataset", on_click=change_tab_state, args=(dataset_tab, tabs), disabled=st.session_state[dataset_tab])
        col2.button("Gráficos", on_click=change_tab_state, args=(plots_tab, tabs), disabled=st.session_state[plots_tab])
        col3.button("Detalhamento de variáveis", on_click=change_tab_state, args=(profile_tab, tabs), disabled=st.session_state[profile_tab])

        if st.session_state[dataset_tab]:
            reset_filters()
            sidebar_01(tabs_01.table)
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
                    colunas=st.session_state['dataframe_columns'],
                    ),
                    use_container_width=True,
                )

        if st.session_state[plots_tab]:
            sidebar_01(tabs_01.plots)
            with st.container():
                st.header('População')
                demographic_pyramid(datasets['gender_data'])

                gender_by_course(datasets['course_data'])

                gender_tree(datasets['course_data'])

                specific_gender_tree(datasets['course_data'], st.session_state['gender_select'])

                dropout_by_gender(datasets['debt_data'])

                dropout_by_age_debt(datasets['debt_data'], st.session_state['tree_path'])

        if st.session_state[profile_tab]:
            sidebar_01(tabs_01.profile)
            st_profile_report(
                datasets['pandas_profile'],
                key='pandas_profile_wdgt',
            )


page_1()
