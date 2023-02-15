import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots


def gender_tree(course_data: pd.DataFrame):
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

    return st.plotly_chart(gender_tree, use_container_width=True)