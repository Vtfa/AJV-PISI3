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