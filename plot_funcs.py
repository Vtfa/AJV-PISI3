import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from consts import *


TITLE_FONT_SIZE = 26

def gender_tree(data: pd.DataFrame) -> None:
    gender_tree = px.treemap(
        data,
        title="Mapa da distribuição de gêneros por curso",
        path=["Course", "Gender"],
        color_continuous_scale="RdBu",
        color="count",
        values="count",
        height=1000,
    )

    gender_tree.data[0].textinfo = "label+value+percent parent+percent entry+percent root"

    gender_tree.update_traces(
        texttemplate="%{label}<br>" \
            "Total: %{value}<br>" \
            "%{percentParent} de %{parent}<br>" \
            "%{percentRoot} do geral<br>" \
    )

    gender_tree.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    st.plotly_chart(gender_tree, use_container_width=True)


def demographic_pyramid(data: pd.DataFrame):
    dem_pyramid = go.Figure()
    dem_pyramid.add_trace(
        go.Bar(
            x=data["Male"],
            y=data.index,
            orientation="h",
            name="Male",
            marker={"color": MALE_COLOR},
            hoverinfo="x",
        )
    )

    dem_pyramid.add_trace(
        go.Bar(
            x=data["Female"] * -1,
            y=data.index,
            text=data["Female"],
            textfont_color="rgba(0, 0, 0, 0)",
            orientation="h",
            name="Female",
            marker={"color": FEMALE_COLOR},
            hoverinfo="text",
        )
    )

    dem_pyramid.update_layout(
        title="Pirâmide populacional",
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
        barmode="relative",
        bargap=0.15,
        xaxis={
            "tickvals": [-1500, -1000, -500, 0, 500, 1000, 1500],
            "ticktext": ["1.500", "1.000", "500", "0", "500", "1.000", "1.500"],
        },
        xaxis_title="# of students",
        yaxis_title="Age range",
        height=700,
        margin_pad=5,
        margin={"l": 90},
        hovermode="y",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    dem_pyramid.update_yaxes(
        gridcolor="rgba(0, 0, 0, 0.10)",
        title_standoff=20,
    )

    st.plotly_chart(dem_pyramid, use_container_width=True)


def specific_gender_tree(data: pd.DataFrame, gender: str) -> None:
    specific_gender_tree = px.treemap(
        data.query(f'Gender == "{gender}"'),
        title=f"Mapa de distruição de alunos por gênero, curso e faixa etária ({gender})",
        path=["Gender", "Course", "age_range"],
        values="count",
        height=1000,
    )

    specific_gender_tree.data[0].textinfo = "label+value+percent parent+percent entry+percent root"


    specific_gender_tree.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    specific_gender_tree.update_traces(
        texttemplate="Faixa: %{label}<br>" \
            "Total: %{value}<br>" \
            "%{percentParent} de %{parent}<br>" \
            "%{percentRoot} de %{root}<br>" \
            "%{percentEntry} de %{entry}<br>"
    )

    st.plotly_chart(specific_gender_tree, use_container_width=True)


def gender_by_course(data: pd.DataFrame) -> None:
    course_gender_age = go.Figure()
    course_gender_age_index = (
        data["Course"]
        .str.replace("(", " ", regex=False)
        .str.replace(" ", "<br>")
        .str.replace(")", "", regex=False)
        .unique()
    )
    course_gender_age_range = [0, 650]

    course_gender_data = data.groupby(["Course", "Gender"])[["count"]].sum()
    course_gender_data = course_gender_data.unstack().droplevel(0, 1)

    course_gender_age.add_trace(
        go.Bar(
            name="Female",
            x=course_gender_age_index,
            y=course_gender_data["Female"],
            orientation="v",
            marker={"color": FEMALE_COLOR},
        ),
    )

    course_gender_age.add_trace(
        go.Bar(
            name="Male",
            x=course_gender_age_index,
            y=course_gender_data["Male"],
            orientation="v",
            marker={"color": MALE_COLOR},
        ),
    )

    course_gender_age.update_xaxes(
        title_text="Course",
        title_standoff=35,
        tickangle=-90,
    )

    course_gender_age.update_yaxes(
        title_text="Students",
        title_standoff=25,
    )

    course_gender_age.update_layout(
        font_size=14,
        height=900,
        title="Distribuição de gêneros por curso",
        barmode="stack",
        hovermode="x unified",
        margin={"b": 190},
        margin_pad=10,
    )

    course_gender_age.update_layout(
        title_font_size=TITLE_FONT_SIZE,
    )

    st.plotly_chart(course_gender_age, use_container_width=True)


def dropout_by_gender(df: pd.DataFrame) -> None:
    debt_gender_tree = px.treemap(
                df,
                title='Target distribution by gender',
                path=['Gender', 'Target', 'debt'],
                values='count',
                height=1000,
        )

    debt_gender_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    debt_gender_tree.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    st.plotly_chart(debt_gender_tree, use_container_width=True)


def dropout_by_age_debt(df: pd.DataFrame, path) -> None:
    debt_tree = px.treemap(
                df,
                title='Target distribution by age and debt',
                path=path,
                values='count',
                height=1000,
        )

    debt_tree.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    debt_tree.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    st.plotly_chart(debt_tree, use_container_width=True)