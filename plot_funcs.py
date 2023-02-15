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


def demographic_pyramid(data: pd.DataFrame):
    dem_pyramid = go.Figure()
    dem_pyramid.add_trace(
        go.Bar(
            x=data['Male'],
            y=data.index,
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
            x=data['Female'] * -1,
            y=data.index,
            text=data['Female'],
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