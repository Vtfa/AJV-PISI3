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

    result_df = pd.DataFrame({'total_students': [total_students]})
    result_df = pd.concat([result_df, status_totals.to_frame().T], axis=1)

    st.write(result_df)

    # Creates Funnel Graph
    funnel_total = go.Figure(go.Funnel(
        y=["Total Students", "Graduate", "Dropout", "Enrolled"],
        x=[total_students, status_totals["Graduate"], status_totals["Dropout"], status_totals["Enrolled"]],
        textinfo="value+percent initial",
        marker={"color": ["#FFA07A", "#87CEEB", "#98FB98", "#DDA0DD"]}
    ))

    # Funnel's title and labels
    funnel_total.update_layout(
        title="Student Status Funnel Graph",
        yaxis_title="Student Status"
    )

    st.write(funnel_total)