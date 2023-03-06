import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

header = st.container()
dataset = st.container()

with header:
    st.title('Página 2 teste')

with dataset:
    dropout_data = st.session_state['dropout_data']
    st.write(dropout_data)


    bar_age = pd.DataFrame(dropout_data['Age at enrollment'].value_counts())
    st.bar_chart(bar_age)

    #box graph
    box_sample = dropout_data.sample(n=50, random_state=66)
    box_age = px.box(box_sample, y='Age at enrollment', points='all')
    st.write(box_age)

    #auxiliar df with students and target totals
    status_totals = dropout_data.groupby('Target').size()
    total_students = len(dropout_data)

    female_data = dropout_data[dropout_data['Gender'] == 'Female']
    female_target_totals = female_data.groupby('Target').size()
    female_students_total = len(female_data)

    male_data = dropout_data[dropout_data['Gender'] == 'Male']
    male_target_totals = male_data.groupby('Target').size()
    male_students_total = len(male_data)

    result_df = pd.DataFrame({'total_students': [total_students]})
    result_df = pd.concat([result_df, status_totals.to_frame().T], axis=1)

    st.write(result_df)

    funnel_total = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[total_students, status_totals["Graduate"], status_totals["Dropout"], status_totals["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#98FB98", "#FF6961", "#87CEEB"]}
        #marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_total.update_layout(
        title="Total students",
        title_x = 0.5
    )

    st.write(funnel_total)

    col1, col2 = st.columns(2)


    
    funnel_female = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[female_students_total, female_target_totals["Graduate"], female_target_totals["Dropout"], female_target_totals["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_female.update_layout(
        title="Female students",
        title_x = 0.5
    )
    with col1:
        st.write(funnel_female)

    funnel_male = go.Figure(go.Funnel(
        y=["Total Students", "Dropout", "Graduate", "Enrolled"],
        x=[male_students_total, male_target_totals["Dropout"], male_target_totals["Graduate"], male_target_totals["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_male.update_layout(
        title="Male students",
        title_x = 0.5
    )

    with col2:
        st.write(funnel_male)


    df_marital_status = dropout_data.groupby(['Marital status'])['Marital status'].count().reset_index(name='count')
    st.title('Marital status of students')
    fig = px.pie(df_marital_status, values='count', names='Marital status')
    st.plotly_chart(fig, use_container_width=True)

    box_marital_sample = dropout_data.sample(n=300, random_state=66)
    box_marital_status = px.box(box_marital_sample, x='Marital status', y='Age at enrollment', points="all")
    st.write(box_marital_status)



    st.title('Sudents by marital status')
    col_marital1, col_marital2, col_marital3 = st.columns(3)

    with col_marital1:
        dfaux_target = dropout_data.groupby(['Target'])['Target'].count().reset_index(name='Total students')
        donut_target_total = px.pie(dfaux_target, values='Total students', names='Target', hole=0.5)

        donut_target_total.update_layout(
            title="All students",
            title_x = 0.5
        )

        st.write(donut_target_total)



    with col_marital2: 
        df_single = dropout_data[dropout_data['Marital status'] == 'Solteiro']
        dfaux_single = df_single.groupby(['Target'])['Target'].count().reset_index(name='Total single students')
        donut_target_single = px.pie(dfaux_single, values='Total single students', names='Target', hole=0.5)
        
        donut_target_single.update_layout(
            title="Single students",
            title_x = 0.5
        )

        st.write(donut_target_single)

    with col_marital3:
        colors_marital = ['#ef553b', '#636efa', '#00cc96']

        df_non_single = dropout_data[dropout_data['Marital status'] == 'Outros']
        dfaux_non_single = df_non_single.groupby(['Target'])['Target'].count().reset_index(name='Total non single students')
        donut_target_non_single = px.pie(
        dfaux_non_single, 
        values='Total non single students', 
        names='Target', 
        hole=0.5, 
        color_discrete_sequence=colors_marital, 
        )

        donut_target_non_single.update_layout(
            title="Non single students",
            title_x = 0.5
        )

        st.write(donut_target_non_single)



    box_renda = px.box(dropout_data, y='Renda total', points='all')
    st.write(box_renda)


    df_country = dropout_data.groupby(['Nacionality'])['Nacionality'].count().reset_index(name='count')
    pie_country = px.bar(df_country)
    st.plotly_chart(pie_country, use_container_width=True)


    
    
    st.title('Situação dos estudantes por estado civil')
    option_marital = st.radio(
        'Mudar o grupo visualizado',
        ('Estudantes solteiros', 'Estudantes não solteiros', 'Mostrar todos')
    )
    col_test1, col_test2, col_test3 = st.columns(3)
    with col_test1:
       st.write(donut_target_total)
    with col_test2:
        if option_marital == 'Estudantes solteiros':
            st.write(donut_target_single)
        elif option_marital == 'Estudantes não solteiros':
            st.write(donut_target_non_single)
        else:
            with col_test2:
                st.write(donut_target_single)
            with col_test3:
                st.write(donut_target_non_single)


   
    dropout_data.loc[dropout_data['International'] == 0, "International"] = 'Nativo'
    dropout_data.loc[dropout_data['International'] == 1, "International"] = 'Internacional'

    dropout_data.loc[dropout_data['Scholarship holder'] == 0, "Scholarship holder"] = 'Não bolsista'
    dropout_data.loc[dropout_data['Scholarship holder'] == 1, "Scholarship holder"] = 'Bolsista'
    
    df_native = dropout_data[dropout_data['International'] == 'Nativo']
    dfaux_native = df_native.groupby(['Target'])['Target'].count().reset_index(name='Nacionalidade')
    donut_native = px.pie(dfaux_native, values="Nacionalidade", names='Target', hole=0.5)

    donut_native.update_layout(
        title="Estudantes nativos",
        title_x = 0.5
    )

    df_non_native = dropout_data[dropout_data['International'] == 'Internacional']
    dfaux_non_native = df_non_native.groupby(['Target'])['Target'].count().reset_index(name='Nacionalidade')
    donut_non_native = px.pie(dfaux_non_native, values="Nacionalidade", names='Target', hole=0.5)

    donut_non_native.update_layout(
        title="Estudantes internacionais",
        title_x = 0.5
    )
    

    st.title('Situação dos estudantes nativos e internacionais')
    option_international = st.radio(
        'Mudar o grupo visualizado',
        ('Estudantes nativos', 'Estudantes internacionais', 'Mostrar todos')
    )

    col_international1, col_international2, col_international3 = st.columns(3)

    with col_international1:
       st.write(donut_target_total)
    with col_international2:
        if option_international == 'Estudantes nativos':
            st.write(donut_native)
        elif option_international == 'Estudantes internacionais':
            st.write(donut_non_native)
        else:
            with col_international2:
                st.write(donut_native)
            with col_international3:
                st.write(donut_non_native)

    #df inicial com totais por faixa de inflação
    inflation_totals = dropout_data.groupby(['Inflation rate', 'Target'])['Target'].count().reset_index(name='num_students')

    # inicia df que terá totais e porcentagens de graduate, dropout e enrolled por taxa de inflação
    inflation_totals_pct = inflation_totals.pivot(index='Inflation rate', columns='Target', values='num_students').reset_index()
    inflation_totals_pct.columns = ['Inflation rate', 'dropout', 'enrolled', 'graduate']
  
    inflation_totals_pct['total_students'] = inflation_totals_pct['enrolled'] + inflation_totals_pct['dropout'] + inflation_totals_pct['graduate']

    # 🍝
    inflation_totals_pct['Enrolled percentage'] = inflation_totals_pct['enrolled'] / inflation_totals_pct['total_students'] * 100 
    inflation_totals_pct['Dropout percentage'] = inflation_totals_pct['dropout'] / inflation_totals_pct['total_students'] * 100
    inflation_totals_pct['Graduate percentage'] = inflation_totals_pct['graduate'] / inflation_totals_pct['total_students'] * 100
    inflation_totals_pct['Enrolled percentage'] = inflation_totals_pct['Enrolled percentage'].apply(lambda x: '{:.2f}'.format(x))
    inflation_totals_pct['Dropout percentage'] = inflation_totals_pct['Dropout percentage'].apply(lambda x: '{:.2f}'.format(x))
    inflation_totals_pct['Graduate percentage'] = inflation_totals_pct['Graduate percentage'].apply(lambda x: '{:.2f}'.format(x))


    st.title('Relação da inflação com taxas de graduação')
    option_inflation = st.checkbox('Adicionar linha aos pontos')

    scatter_inflation_graduate = px.scatter(inflation_totals_pct, x='Graduate percentage', y='Inflation rate')
    scatter_inflation_graduate.update_xaxes(categoryorder='category ascending')

    inflation_totals_pct_sort = inflation_totals_pct.sort_values(by='Graduate percentage')
    scatter_inflation_graduate_dots = px.line(inflation_totals_pct_sort, x='Graduate percentage', y='Inflation rate', markers=True)
    scatter_inflation_graduate_dots.update_xaxes(categoryorder='category ascending',)
    
    if option_inflation:
        st.write(scatter_inflation_graduate_dots)
    else:
        st.write(scatter_inflation_graduate)

    st.title('Relação do PIB com taxas de graduação')
    option_gdp = st.checkbox('Adicionar linha aos pontos', key='1')

    gdp_totals = dropout_data.groupby(['GDP', 'Target'])['Target'].count().reset_index(name='num_students')

    gdp_totals_pct = gdp_totals.pivot(index='GDP', columns='Target', values='num_students').reset_index()
    gdp_totals_pct.columns = ['GDP', 'dropout', 'enrolled', 'graduate']
  
    gdp_totals_pct['total_students'] = gdp_totals_pct['enrolled'] + gdp_totals_pct['dropout'] + gdp_totals_pct['graduate']
   
    gdp_totals_pct['Enrolled percentage'] = gdp_totals_pct['enrolled'] / gdp_totals_pct['total_students'] * 100 
    gdp_totals_pct['Dropout percentage'] = gdp_totals_pct['dropout'] / gdp_totals_pct['total_students'] * 100
    gdp_totals_pct['Graduate percentage'] = gdp_totals_pct['graduate'] / gdp_totals_pct['total_students'] * 100
    gdp_totals_pct['Enrolled percentage'] = gdp_totals_pct['Enrolled percentage'].apply(lambda x: '{:.2f}'.format(x))
    gdp_totals_pct['Dropout percentage'] = gdp_totals_pct['Dropout percentage'].apply(lambda x: '{:.2f}'.format(x))
    gdp_totals_pct['Graduate percentage'] = gdp_totals_pct['Graduate percentage'].apply(lambda x: '{:.2f}'.format(x))



    scatter_gdp_graduate = px.scatter(gdp_totals_pct, x='Graduate percentage', y='GDP')
    scatter_gdp_graduate.update_xaxes(categoryorder='category ascending')

    gdp_totals_pct_sort = gdp_totals_pct.sort_values(by='Graduate percentage')
    scatter_gdp_graduate_dots = px.line(gdp_totals_pct_sort, x='Graduate percentage', y='GDP', markers=True)
    scatter_gdp_graduate_dots.update_xaxes(categoryorder='category ascending',)
    
    if option_gdp:
        st.write(scatter_gdp_graduate_dots)
    else:
        st.write(scatter_gdp_graduate)



    st.title('Relação da taxa de desemprego com taxas de graduação')
    option_unemployment = st.checkbox('Adicionar linha aos pontos', key='2')

    unemployment_totals = dropout_data.groupby(['Unemployment rate', 'Target'])['Target'].count().reset_index(name='num_students')

    unemployment_totals_pct = unemployment_totals.pivot(index='Unemployment rate', columns='Target', values='num_students').reset_index()
    unemployment_totals_pct.columns = ['Unemployment rate', 'dropout', 'enrolled', 'graduate']
  
    unemployment_totals_pct['total_students'] = unemployment_totals_pct['enrolled'] + unemployment_totals_pct['dropout'] + gdp_totals_pct['graduate']
   
    unemployment_totals_pct['Enrolled percentage'] = unemployment_totals_pct['enrolled'] / unemployment_totals_pct['total_students'] * 100 
    unemployment_totals_pct['Dropout percentage'] = unemployment_totals_pct['dropout'] / unemployment_totals_pct['total_students'] * 100
    unemployment_totals_pct['Graduate percentage'] = unemployment_totals_pct['graduate'] / unemployment_totals_pct['total_students'] * 100
    unemployment_totals_pct['Enrolled percentage'] = unemployment_totals_pct['Enrolled percentage'].apply(lambda x: '{:.2f}'.format(x))
    unemployment_totals_pct['Dropout percentage'] = unemployment_totals_pct['Dropout percentage'].apply(lambda x: '{:.2f}'.format(x))
    unemployment_totals_pct['Graduate percentage'] = unemployment_totals_pct['Graduate percentage'].apply(lambda x: '{:.2f}'.format(x))

    scatter_unemployment_graduate = px.scatter(unemployment_totals_pct, x='Graduate percentage', y='Unemployment rate')
    scatter_unemployment_graduate.update_xaxes(categoryorder='category ascending')

    unemployment_totals_pct_sort = unemployment_totals_pct.sort_values(by='Graduate percentage')
    scatter_unemployment_graduate_dots = px.line(unemployment_totals_pct_sort, x='Graduate percentage', y='Unemployment rate', markers=True)
    scatter_unemployment_graduate_dots.update_xaxes(categoryorder='category ascending',)
    
    if option_unemployment:
        st.write(scatter_unemployment_graduate_dots)
    else:
        st.write(scatter_unemployment_graduate)

    df_scholarship_grouped = dropout_data.groupby(['Scholarship holder', 'Target'])['Target'].count().reset_index(name='count')
    st.write(df_scholarship_grouped)

    # total de estudantes pra cada grupo
    total_students = df_scholarship_grouped.groupby('Scholarship holder')['count'].transform('sum')

    # calcula a porcentagem de cada groupo
    df_scholarship_grouped['percentage'] = df_scholarship_grouped['count'] / total_students * 100

    bar_scholarship = px.bar(df_scholarship_grouped, x='Scholarship holder', y='percentage', color='Target', barmode='stack')

    bar_scholarship.update_traces(width=0.2)
    bar_scholarship.update_layout(
                    xaxis_title='Scholarship holder',
                    yaxis_title='Percentage'
                    )
    st.title('Status de bolsistas e não bolsistas')
    st.write(bar_scholarship)



    df_classe_baixa= dropout_data[dropout_data['Renda total'] <= 1405]
    classe_baixa_target_total = df_classe_baixa.groupby('Target').size()
    classe_baixa_total = len(df_classe_baixa)

    df_classe_media= dropout_data[(dropout_data['Renda total'] > 1405) & (dropout_data['Renda total'] < 3000)]
    classe_media_target_total = df_classe_media.groupby('Target').size()
    classe_media_total = len(df_classe_media)

    df_classe_alta= dropout_data[dropout_data['Renda total'] >= 3000]
    classe_alta_target_total = df_classe_alta.groupby('Target').size()
    classe_alta_total = len(df_classe_alta)    


    st.title('Situação dos estudantes por classe econômica')

    funnel_classe_baixa = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[classe_baixa_total, classe_baixa_target_total["Graduate"], classe_baixa_target_total["Dropout"], classe_baixa_target_total["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_classe_baixa.update_layout(
        title="Estudantes de classe baixa",
        title_x = 0.5
    )

    funnel_classe_media = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[classe_media_total, classe_media_target_total["Graduate"], classe_media_target_total["Dropout"], classe_media_target_total["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_classe_media.update_layout(
        title="Estudantes de classe média",
        title_x = 0.5
    )

    funnel_classe_alta = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[classe_alta_total, classe_alta_target_total["Graduate"], classe_alta_target_total["Dropout"], classe_alta_target_total["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    funnel_classe_alta.update_layout(
        title="Estudantes de classe alta",
        title_x = 0.5
    )


    # Gambiarra pra diminuir o tamanho do select box. Como existem 4 colunas, o select box vai ocupar 1/4 do espaço que ocuparia sem colunas
    col_funnel_renda_select, col_funnel_renda_select2, col_funnel_renda_select3, col_funnel_renda_select4 = st.columns(4)

    with col_funnel_renda_select:
        select_funnel_renda = st.selectbox('Escola uma classe econômica', ('Classe baixa', 'Classe média', 'Classe alta', 'Mostrar todos'))

    col_funnel_renda1,  col_funnel_renda2 = st.columns(2)

    if select_funnel_renda == 'Classe baixa':
        with col_funnel_renda1:
            st.write(funnel_total)
        with col_funnel_renda2:
            st.write(funnel_classe_baixa)
    elif select_funnel_renda == 'Classe média':
        with col_funnel_renda1:
            st.write(funnel_total)
        with col_funnel_renda2:
            st.write(funnel_classe_media)
    elif select_funnel_renda == 'Classe alta':
        with col_funnel_renda1:
            st.write(funnel_total)
        with col_funnel_renda2:
            st.write(funnel_classe_alta)
    else:
        st.write(funnel_total)
        col_funnel_renda1,  col_funnel_renda2, col_funnel_renda3 = st.columns(3)
        with col_funnel_renda1:
            st.write(funnel_classe_baixa)
        with col_funnel_renda2:
            st.write(funnel_classe_media)
        with col_funnel_renda3:
            st.write(funnel_classe_alta)

    st.title('Situação dos estudantes por educação dos pais')

    df_both_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') & (dropout_data['Escolaridade pai'] == 'ensino superior')]
    dfaux_both_higher = df_both_higher.groupby(['Target'])['Target'].count().reset_index(name='Total students')
    donut_both_higher = px.pie(dfaux_both_higher, values='Total students', names='Target', hole=0.5)

    donut_both_higher.update_layout(
        title="ambos superior",
        title_x = 0.5
    )

    df_one_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') | (dropout_data['Escolaridade pai'] == 'ensino superior')]
    dfaux_one_higher = df_one_higher.groupby(['Target'])['Target'].count().reset_index(name='Total students')
    donut_one_higher = px.pie(dfaux_one_higher, values='Total students', names='Target', hole=0.5)

    donut_one_higher.update_layout(
        title="1 ensino superior",
        title_x = 0.5
    )

    df_both_secondary = dropout_data[(dropout_data['Escolaridade mae'] == 'medio completo') & (dropout_data['Escolaridade pai'] == 'medio completo')]
    dfaux_both_secondary = df_both_secondary.groupby(['Target'])['Target'].count().reset_index(name='Total students')
    donut_both_secondary = px.pie(dfaux_both_secondary, values='Total students', names='Target', hole=0.5)

    donut_both_secondary.update_layout(
        title="Ambos ensino médio",
        title_x = 0.5
    )

    df_both_primary = dropout_data[(dropout_data['Escolaridade mae'] == 'fundamental incompleto') & (dropout_data['Escolaridade pai'] == 'fundamental incompleto')]
    dfaux_both_primary = df_both_primary.groupby(['Target'])['Target'].count().reset_index(name='Total students')
    donut_both_primary = px.pie(dfaux_both_primary, values='Total students', names='Target', hole=0.5)

    donut_both_primary.update_layout(
        title="Ambos ensino fundamental",
        title_x = 0.5
    )
    
    col_parents_education1, col_parents_education2, col_parents_education3, col_parents_education4 = st.columns(4)
    

    with col_parents_education1:
        st.write(donut_both_higher)
    with col_parents_education2:
        st.write(donut_one_higher)
    with col_parents_education3:
        st.write(donut_both_secondary)        
    with col_parents_education4:
        st.write(donut_both_primary)

    df_age_target = dropout_data[['Age at enrollment', 'Target']]
    df_age_target['Age group'] = pd.cut(df_age_target['Age at enrollment'], bins=[16, 29, 150], labels=['Entre 17 e 29 anos', 'Mais de 30 anos'])

    df_age_target_count = df_age_target.groupby(['Age group', 'Target']).size().reset_index(name='Count')

    df_age_target_count['Percentage'] = df_age_target_count.groupby('Age group')['Count'].apply(lambda x: 100 * x / float(x.sum()))
    colors = ['#98FB98', '#87CEEB', '#FF6961']

    bar_age_target = px.bar(df_age_target_count, x='Age group', y='Percentage', color='Target', barmode='stack', color_discrete_sequence=colors,
                category_orders={'Age group': ['17-29', '30+'], 'Target': ['Graduate', 'Enrolled', 'Dropout']}, 
                text=df_age_target_count['Percentage'].round(2)
                )

    st.title('Situação dos estudentes por faixa etária')
    bar_age_target.update_traces(textposition='auto', texttemplate='%{text}%', width=0.2)
    bar_age_target.update_layout(
                    xaxis_title='Faixas etárias no ano de matrícula',
                    yaxis_title='Porcentagem'
                    )
    st.write(bar_age_target)


    st.title('Situação dos estudantes por dívida')

    dfaux_target = dropout_data.groupby(['Target'])['Target'].count().reset_index(name='Total')
    df_sem_divida = dropout_data[dropout_data.Debtor==0]
    dfaux_sem_divida = df_sem_divida.groupby(['Target'])['Target'].count().reset_index(name='Estudantes sem divida')

    df_com_divida = dropout_data[dropout_data.Debtor==1]
    dfaux_com_divida = df_com_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_com_divida')

    
    grafico_target_geral = px.pie(
        dfaux_target, values='Total',
        names='Target',
        color='Target',
        color_discrete_sequence=colors,
        hole=0.5,
        title='Todos estudantes'
    )

    grafico_target_geral.update_layout(
        title_x = 0.48
    )

    grafico_target_endividados = px.pie(
        dfaux_com_divida,
        values='soma_com_divida',
        names='Target',
        color='Target',
        color_discrete_sequence=colors,
        hole=0.5,
        title='Estudantes com dívida'
    )

    grafico_target_endividados.update_layout(
        title_x = 0.48
    )

    grafico_target_estudantes_sem_dividas = px.pie(
        dfaux_sem_divida,
        values='Estudantes sem divida',
        names='Target',
        color='Target',
        color_discrete_sequence=colors,
        hole=0.5,
        title='Estudantes sem dívida'   
    )

    grafico_target_estudantes_sem_dividas.update_layout(
        title_x = 0.48
    )

    option_divida_tuition = st.multiselect(
        'Mudar o grupo visualizado',
        ('Todos estudantes', 'Endividados', 'Sem dívidas'),
        default = ('Todos estudantes')
    )

    column_debt1, column_debt2, column_debt3 = st.columns(3)

    if 'Todos estudantes' in option_divida_tuition:
        with column_debt1:
            st.plotly_chart(grafico_target_geral)
        if ('Sem dívidas' in option_divida_tuition) & ('Endividados' not in option_divida_tuition):
            with column_debt2:
                st.plotly_chart(grafico_target_estudantes_sem_dividas)
        elif ('Endividados' in option_divida_tuition) & ('Sem dívidas' not in option_divida_tuition):
            with column_debt2:
                st.plotly_chart(grafico_target_endividados)
    if len(option_divida_tuition) == 3: 
        with column_debt2:
            st.plotly_chart(grafico_target_endividados)
        with column_debt3:
            st.plotly_chart(grafico_target_estudantes_sem_dividas)   

