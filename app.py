import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
# from datetime import datetime

title = "Predict Dropout or Academic Success"

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
        João Vitor da SIlva Pires\n
        Vinicius Thalles Ferreira Araujo''',
    }
)

header = st.container()
dataset = st.container()

with header:
    st.title(title)

with dataset:
    dropout_data = pd.read_csv('data/dropout.csv')
    st.session_state['dropout_data_state'] = dropout_data
    # função para mapear os valores das profissões dos pais
    # def escolaridade_pais(valor: str) -> str:
    #     array_fund_inc = [11, 26, 35, 36, 37, 38, 29, 30]
    #     array_medio_inc = [9, 10, 12, 13, 14, 19, 27, 13, 25]
    #     medio = 1
    #     array_tecnico = [18, 22, 39, 31, 33]
    #     array_superior = [2, 3, 4, 5, 6, 40, 41, 42, 43, 44]

    #     if valor in array_fund_inc:
    #         return 'fundamental incompleto'
    #     elif valor in array_medio_inc:
    #         return 'medio incompleto'
    #     elif valor == medio:
    #         return 'medio completo'
    #     elif valor in array_tecnico:
    #         return 'ensino tecnico'
    #     elif valor in array_superior:
    #         return 'ensino superior'
    #     else:
    #         return 'no info'

    # função para mapear os valores das profissões dos pais
    def escolaridade_pais(data: pd.Series) -> pd.Series:
        fund_inc = np.isin(data, [11, 26, 35, 36, 37, 38, 29, 30])
        medio_inc = np.isin(data, [9, 10, 12, 13, 14, 19, 27, 13, 25])
        medio = data == 1
        tecnico = np.isin(data, [18, 22, 39, 31, 33])
        superior = np.isin(data, [2, 3, 4, 5, 6, 40, 41, 42, 43, 44])

        niveis = [
            'fundamental incompleto',
            'medio incompleto',
            'medio completo',
            'ensino tecnico',
            'ensino superior',
        ]

        return pd.Series(np.select(
            [fund_inc, medio_inc, medio, tecnico, superior],
            niveis,
            'no info'
        ))
    #perdão pela monstruosidade. -Vinicius
    def renda_pais(data: pd.Series) -> pd.Series:
        var_1 = data == 1
        var_2 = data == 2
        var_4 = data == 4
        var_5 = data == 5
        var_6 = data == 6
        var_7 = data == 7
        var_8 = data == 8
        var_9 = data == 9
        var_10 = data == 10
        var_122 = data == 122
        var_123 = data == 123
        var_125 = data == 125
        var_131 = data == 131
        var_132 = data == 132
        var_134 = data == 134
        var_141 = data == 141
        var_143 = data == 143
        var_144 = data == 144
        var_151 = data == 151
        var_152 = data == 152
        var_153 = data == 153
        var_171 = data == 171
        var_173 = data == 173
        var_175 = data == 175
        var_191 = data == 191
        var_192 = data == 192
        var_193 = data == 193
        var_194 = data == 194
        var_101 = data == 101
        var_102 = data == 102
        var_103 = data == 103
        var_112 = data == 112
        var_114 = data == 114
        var_121 = data == 121
        var_135 = data == 135
        var_154 = data == 154 
        var_161 = data == 161
        var_163 = data == 163
        var_172 = data == 172
        var_174 = data == 174
        var_181 = data == 181
        var_182 = data == 182
        var_183 = data == 183
        var_195 = data == 195

        niveis = [
            3456, 2141, 930, 840, 875, 997, 940, 840, 1749, 2556, 2200, 3452, 1352, 1417, 930, 2248, 930,
            805, 1073, 740, 1042, 827, 915, 873, 799, 824, 710, 1865, 1489, 1124, 3456, 3456, 2141, 3063, 
            1609, 840, 875, 875, 1353, 1897, 1061, 889, 884, 794, 
        ]

        return pd.Series(np.select(
            [var_1, var_2, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_122, var_123, var_125, var_131, var_132, var_134, var_141, var_143, var_144,
            var_151, var_152, var_153, var_171, var_173, var_175, var_191, var_192, var_193, var_194, var_101, var_102, var_103, var_112, var_114, 
            var_121, var_135, var_154, var_161, var_163, var_172, var_174, var_181, var_182, var_183, var_195,
            ],
            niveis,
            0
        ))


    dropout_data.loc[dropout_data['Marital status'] == 1, "Marital status"] = 'Solteiro'
    dropout_data.loc[dropout_data['Marital status'] == 2, "Marital status"] = 'Casado'
    dropout_data.loc[dropout_data['Marital status'] == 3, "Marital status"] = 'Viúvo'
    dropout_data.loc[dropout_data['Marital status'] == 4, "Marital status"] = 'Divorciado'
    dropout_data.loc[dropout_data['Marital status'] == 5, "Marital status"] = 'União estável'
    dropout_data.loc[dropout_data['Marital status'] == 6, "Marital status"] = 'Separado'


    # utiliza a função para criar uma coluna nova
    # s0 = datetime.now()
    # dropout_data["Escolaridade mae"] = dropout_data["Mother's qualification"].apply(lambda valor: escolaridade_pais(valor))
    # s1 = datetime.now()
    # dropout_data["Escolaridade pai"] = dropout_data["Father's qualification"].apply(lambda valor: escolaridade_pais(valor))
    # s2 = datetime.now()

    # print('mae::', s1 - s0)
    # print('pai::', s2 - s1)

    dropout_data["Escolaridade mae"] = escolaridade_pais(dropout_data["Mother's qualification"])
    dropout_data["Escolaridade pai"] = escolaridade_pais(dropout_data["Father's qualification"])

    dropout_data["Renda pai"] = renda_pais(dropout_data["Father's occupation"])
    dropout_data["Renda mae"] = renda_pais(dropout_data["Mother's occupation"])

    dropout_data["Renda total"] = dropout_data["Renda pai"] + dropout_data["Renda mae"]

    # esse bloco de texto pode ser usado pra printar na tela DFs com a soma de cada nível de escolaridade individual e a soma dos tipos de escolaridade agrupados
    # df_teste_mae = dropout_data.groupby(["Mother's qualification"])["Mother's qualification"].count().reset_index(name='soma_mae')
    # df_teste_mae_novo = dropout_data.groupby(["Escolaridade mae"])["Escolaridade mae"].count().reset_index(name='soma_mae')
    # st.write(df_teste_mae)
    # st.write(df_teste_mae_novo)

    courses_map = {
        33: 'Biofuel Production Technologies',
        171: 'Animation and Multimedia Design',
        8014: 'Social Service',
        9003: 'Agronomy',
        9070: 'Communication Design',
        9085: 'Veterinary Nursing',
        9119: 'Informatics Engineering',
        9130: 'Equinculture',
        9147: 'Management',
        9238: 'Social Service',
        9254: 'Tourism',
        9500: 'Nursing',
        9556: 'Oral Hygiene',
        9670: 'Advertising and Marketing Management',
        9773: 'Journalism and Communication',
        9853: 'Basic Education',
        9991: 'Management(Evening)'
    }
    dropout_data['Course'] = dropout_data['Course'].map(courses_map)

    st.subheader('Data sample')
    #st.write(dropout_data.head(10))
    st.write(dropout_data)

    st.subheader('Age of students')
    age_bins = list(range(17, np.max(dropout_data['Age at enrollment'].values), 5))
    ages_labels = [f'{age_bins[i-1]} - {age_bins[i]-1}' for i in range(1, len(age_bins))]
    dropout_data['age_range'] = pd.cut(
        dropout_data['Age at enrollment'],
        age_bins,
        labels=ages_labels,
        right=False,
        ordered=False,
        )

    dropout_data['Gender'] = np.where(dropout_data['Gender'], 'Male', 'Female')
    gender_data = (
        dropout_data[['age_range', 'Gender', 'Course']]
        .groupby(['age_range', 'Gender'])
        .count()
    )
    gender_data = gender_data.unstack('Gender').droplevel(0, 'columns')

    dem_pyramid = go.Figure()
    dem_pyramid.add_trace(
        go.Bar(
            x=gender_data['Male'],
            y=gender_data.index,
            orientation='h',
            name='Male',
            marker={
                'color': 'rgba(0, 204, 150, 0.5)'
            },
            hoverinfo='x',
        )
    )

    dem_pyramid.add_trace(
        go.Bar(
            x=gender_data['Female'] * -1,
            y=gender_data.index,
            text=gender_data['Female'],
            textfont_color='rgba(0, 0, 0, 0)',
            orientation='h',
            name='Female',
            marker={
                'color': 'rgba(99, 110, 250, 0.5)'
            },
            hoverinfo='text',
        )
    )

    dem_pyramid.update_layout(
        title="Students' Population Pyramid",
        title_font_size=22,
        font_size=16,
        barmode = 'relative',
        bargap=0.15,
        xaxis={
            'tickvals': [-1500, -1000, -500, 0, 500, 1000, 1500],
        'ticktext':
            ['1.500', '1.000', '500', '0', '500', '1.000', '1.500']
        },
        xaxis_title='# of students',
        yaxis_title='Age range',
        height=700,
        margin_pad=5,
        margin={'l': 90},
        hovermode='y',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    dem_pyramid.update_yaxes(
        gridcolor='rgba(0, 0, 0, 0.10)',
        title_standoff=20,
    )

    st.plotly_chart(dem_pyramid, use_container_width=True)

    bar_age = pd.DataFrame(dropout_data['Age at enrollment'].value_counts())
    st.bar_chart(bar_age)


    course_data = (
        dropout_data[['age_range', 'Gender', 'Course', 'Displaced']]
        .groupby(['Course', 'Gender', 'age_range'])
        .count()
        .reset_index()
    )
    course_data.rename(columns={'Displaced': 'count'}, inplace=True)

    gender_tree = px.treemap(
            course_data,
            title='Gender distribution by course',
            path=[ 'Course', 'Gender'],
            color_continuous_scale='RdBu',
            color='count',
            values='count',
            height=1000,
    )

    gender_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    gender_tree.update_layout(
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(gender_tree, use_container_width=True)

    female_tree = px.treemap(
            course_data.query('Gender == "Female"'),
            title='Course and age distribution for female students',
            path=['Gender', 'Course', 'age_range'],
            values='count',
            height=1000,
    )

    female_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    female_tree.update_layout(
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(female_tree, use_container_width=True)

    male_tree = px.treemap(
            course_data.query('Gender == "Male"'),
            title='Course and age distribution for male students',
            path=['Gender', 'Course', 'age_range'],
            values='count',
            height=1000,
    )

    male_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    male_tree.update_layout(
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(male_tree, use_container_width=True)

    course_gender_age = go.Figure()
    course_gender_age_index = (
        course_data['Course'].str.replace('(', ' ', regex=False)
        .str.replace(' ', '<br>')
        .str.replace(')', '', regex=False)
        .unique()
    )
    course_gender_age_range = [0, 650]

    course_gender_data = course_data.groupby(['Course', 'Gender'])[['count']].sum()
    course_gender_data = course_gender_data.unstack().droplevel(0, 1)

    course_gender_age.add_trace(
        go.Bar(
            name="Female",
            x=course_gender_age_index,
            y=course_gender_data["Female"],
            orientation='v',
             marker={
                'color': 'rgba(99, 110, 250, 0.5)'
            },
        ),
    )

    course_gender_age.add_trace(
        go.Bar(
            name="Male",
            x=course_gender_age_index,
            y=course_gender_data["Male"],
            orientation='v',
             marker={
                'color': 'rgba(0, 204, 150, 0.5)'
            },
        ),
    )

    course_gender_age.update_xaxes(
        title_text='Course',
        title_standoff=35,
        tickangle=-90,
    )

    course_gender_age.update_yaxes(
        title_text='Students',
        title_standoff=25,
    )

    course_gender_age.update_layout(
        height=900,
        font_size=14,
        title='Gender distribution by course',
        barmode='stack',
        hovermode='x unified',
        margin={'b': 190},
        margin_pad=10,
    )

    st.plotly_chart(course_gender_age, use_container_width=True)



    #st.title("Testando plotly e manipulação de valores de colunas no pandas!")
    #st.subheader("Aqui trocamos valores '1' e '0' da coluna 'Gender' por valores 'Male' e 'Female' usando o método pandas.DataFrame.loc")

    # dropout_data.loc[dropout_data['Gender'] == 1, "Gender"] = 'Male'
    # dropout_data.loc[dropout_data['Gender'] == 0, "Gender"] = 'Female'
  

    df = dropout_data.groupby(['Gender'])['Gender'].count().reset_index(name='count')
    st.title('Gender of students')
    fig = px.pie(df, values='count', names='Gender')
    st.plotly_chart(fig, use_container_width=True)

    st.title('Dropout rates by gender')

    # novo dataframe apenas com registros em que target = dropout
    df_droupout_gender = dropout_data[(dropout_data['Target'] == 'Dropout')]

    # DF auxiliar com total de male e female para ser usado no gráfico abaixo
    dfaux_dropout_gender = df_droupout_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_dropout_gender')
    pie_dropout_gender = px.pie(
        dfaux_dropout_gender,
        values='soma_dropout_gender',
        names='Gender'
    )

    st.plotly_chart(pie_dropout_gender, use_container_width=True)

    st.title('Graduation rates by gender')

    # novo dataframe apenas com registros em que target = graduate
    df_graduate_gender = dropout_data[(dropout_data['Target'] == 'Graduate')]

    # DF auxiliar com total de male e female para ser usado no gráfico abaixo
    dfaux_graduate_gender = df_graduate_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_graduate_gender')
    pie_graduate_gender = px.pie(
        dfaux_graduate_gender,
        values='soma_graduate_gender',
        names='Gender'
    )

    st.plotly_chart(pie_graduate_gender, use_container_width=True)

    st.title("Histograma de dropout por curso")
    #st.subheader(
       # 'Fica mais fácil visualizar tendências em um Histograma,' +
      #  ' aqui procuro tendências do dropout relacionados aos cursos dos alunos.' +
       # ' Trocamos os valores numéricos dos  cursos por valores correspondentes do dicionário.'
   # )

    # Aqui mapeio os valores numericos dos cursos com seu nome para usar o .replace() do pandas para trocar valores.
    # Dataframe com registros em que target = dropout
    # course_dropout = dropout_data[(dropout_data['Target'] == 'Dropout')].copy()
    # courses_map = {
    #     33: 'Biofuel Production Technologies',
    #     171: 'Animation and Multimedia Design',
    #     8014: 'Social Service',
    #     9003: 'Agronomy',
    #     9070: 'Communication Design',
    #     9085: 'Veterinary Nursing',
    #     9119: 'Informatics Engineering',
    #     9130: 'Equinculture',
    #     9147: 'Management',
    #     9238: 'Social Service',
    #     9254: 'Tourism',
    #     9500: 'Nursing',
    #     9556: 'Oral Hygiene',
    #     9670: 'Advertising and Marketing Management',
    #     9773: 'Journalism and Communication',
    #     9853: 'Basic Education',
    #     9991: 'Management(Evening)'
    # }
    # course_dropout['Course'] = course_dropout['Course'].map(courses_map)
    histograma_drop = px.histogram(
        dropout_data,
        x = "Course",
    )

    st.plotly_chart(histograma_drop, use_container_width=True)


    #
    #
    # Aqui começa o codigo do grafico relacionando a coluna 'Debtor' com a evasao

    dfaux_target = dropout_data.groupby(['Target'])['Target'].count().reset_index(name='soma_target')

    df_sem_divida = dropout_data[dropout_data.Debtor==0]
    dfaux_sem_divida = df_sem_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_sem_divida')

    df_com_divida = dropout_data[dropout_data.Debtor==1]
    dfaux_com_divida = df_com_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_com_divida')

    st.title('Situação dos estudantes por dívida')
    option = st.selectbox(
        'Mudar o grupo visualizado',
        ('Todos estudantes', 'Endividados', 'Sem dívidas')
    )

    grafico_target_geral = px.pie(
        dfaux_target, values='soma_target',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)',
        },
        title='Situação Acadêmica dos Estudantes '
    )

    grafico_target_endividados = px.pie(
        dfaux_com_divida,
        values='soma_com_divida',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)',
        },
        title='Situação Acadêmica dos Estudantes Endividados'
    )

    grafico_target_estudantes_sem_dividas = px.pie(
        dfaux_sem_divida,
        values='soma_sem_divida',
        names='Target',
        color='Target',
        color_discrete_map={
            'Dropout':'rgb(239, 85, 59)',
            'Enrolled':'rgb(99, 110, 250)',
            'Graduate':'rgb(0, 204, 150)',
        },
        title='Situação Acadêmica dos Estudantes Sem dívidas'
    )

    if option == 'Todos estudantes':
        st.plotly_chart(grafico_target_geral, use_container_width=True)
    elif option == 'Endividados':
        st.plotly_chart(grafico_target_endividados, use_container_width=True)
    else:
        st.plotly_chart(grafico_target_estudantes_sem_dividas, use_container_width=True)

st.title('Situação dos estudantes internacionais')
option_internacioal = st.selectbox('Mudar o grupo visualizado', ('Todos estudantes', 'Estudantes Internacionais'))

df_internacional = dropout_data[dropout_data.Nacionality != 1]
dfaux_internacional = df_internacional.groupby(['Target'])['Target'].count().reset_index(name='soma_target_internacional')
pie_target_internacional = px.pie(
    dfaux_internacional,
    values='soma_target_internacional',
    names='Target',
    color='Target',
    color_discrete_map={
        'Dropout':'rgb(239, 85, 59)',
        'Enrolled':'rgb(99, 110, 250)',
        'Graduate':'rgb(0, 204, 150)'
    },
    title='Situação acadêmica dos estudantes'
)

if option_internacioal == 'Todos estudantes':
    st.plotly_chart(grafico_target_geral, use_container_width=True)
else:
    st.plotly_chart(pie_target_internacional, use_container_width=True)

st.title('Situação dos estudantes portadores de bolsas de estudo')
option_scholarship = st.selectbox(
    'Mudar o grupo visualizado',
    ('Estudantes não portadores de bolsas de estudo', 'Estudantes portadores de bolsas de estudo')
)

df_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 1)]
dfaux_scholarship = df_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_scholarship')

df_no_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 0)]
dfaux_no_scholarship = df_no_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_no_scholarship')

pie_scholarship = px.pie(
    dfaux_scholarship,
    values='soma_scholarship',
    names='Target',
    color='Target',
    color_discrete_map={
        'Dropout':'rgb(239, 85, 59)',
        'Enrolled':'rgb(99, 110, 250)',
        'Graduate':'rgb(0, 204, 150)',
    },
    title='Situação acadêmica dos estudantes sem bolsa de estudo',
)

pie_no_scholarship = px.pie(
    dfaux_no_scholarship,
    values='soma_no_scholarship',
    names='Target',
    color='Target',
    color_discrete_map={
        'Dropout':'rgb(239, 85, 59)',
        'Enrolled':'rgb(99, 110, 250)',
        'Graduate':'rgb(0, 204, 150)',
    },
    title='Situação acadêmica dos estudantes sem bolsa de estudos',
)

if option_scholarship == 'Estudantes não portadores de bolsas de estudo':
    st.plotly_chart(pie_no_scholarship, use_container_width=True)
else:
    st.plotly_chart(pie_scholarship, use_container_width=True)


dropout_data['debt'] = np.where(
    (dropout_data['Debtor'] == 1) | (dropout_data['Tuition fees up to date'] == 0), 'has debt', 'up to date'
)

debt_data = (
    dropout_data[['age_range', 'Gender', 'Course', 'debt', 'Displaced', 'Target']]
    .groupby(['Gender', 'Target', 'Course', 'age_range', 'debt'])
    .count()
    .reset_index()
)
# debt_data = debt_data[~debt_data['Target'].isin(['Enrolled'])]
debt_data.rename(columns={'Displaced': 'count'}, inplace=True)

debt_gender_tree = px.treemap(
            debt_data,
            title='Target distribution by gender',
            path=['Gender', 'Target', 'debt'],
            values='count',
            height=1000,
    )

debt_gender_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

debt_gender_tree.update_layout(
    title_font_size=26,
    font_size=16,
)

st.plotly_chart(debt_gender_tree, use_container_width=True)

debt_tree = px.treemap(
            debt_data,
            title='Target distribution by age and debt',
            path=['age_range', 'Target', 'debt'],
            values='count',
            height=1000,
    )

debt_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

debt_tree.update_layout(
    title_font_size=26,
    font_size=16,
)

st.plotly_chart(debt_tree, use_container_width=True)