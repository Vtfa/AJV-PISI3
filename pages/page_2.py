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
    dropout_data = st.session_state['dropout_data_state']
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
