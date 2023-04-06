import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_funcs import *

from consts import *


TITLE_FONT_SIZE = 26


def demographic_pyramid(data: pd.DataFrame):
    dem_pyramid = go.Figure()
    dem_pyramid.add_trace(
        go.Bar(
            x=data[Gender.Male],
            y=data.index,
            orientation="h",
            name=Gender.Male,
            marker={"color": MALE_COLOR},
            hoverinfo="x",
        )
    )

    dem_pyramid.add_trace(
        go.Bar(
            x=data[Gender.Female] * -1,
            y=data.index,
            text=data[Gender.Female],
            textfont_color="rgba(0, 0, 0, 0)",
            orientation="h",
            name=Gender.Female,
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
        xaxis_title="# de estudantes",
        yaxis_title="Faixa etária",
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


def population_tree(data: pd.DataFrame) -> None:
    gender_tree = px.treemap(
        data,
        title="Mapa da distribuição de gêneros por curso (escala contínua)",
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


def gender_by_course(data: pd.DataFrame) -> None:
    courses = (
        data["Course"]
        .str.replace("(", " ", regex=False)
        .str.replace(")", "", regex=False)
        .unique()
    )
    MAX = 23
    courses_map = {course: course[:MAX-3] + '...' if len(course) > MAX else course for course in courses}
    courses_labels = sorted(courses_map.values())

    course_gender_age = go.Figure()

    course_gender_data = data.groupby(["Course", "Gender"])[["count"]].sum()
    course_gender_data = course_gender_data.unstack().droplevel(0, 1)

    course_gender_age.add_trace(
        go.Bar(
            name=Gender.Female,
            x=course_gender_data[Gender.Female],
            y=courses_labels,
            orientation='h',
            marker={"color": FEMALE_COLOR},
        ),
    )

    course_gender_age.add_trace(
        go.Bar(
            name=Gender.Male,
            x=course_gender_data[Gender.Male],
            y=courses_labels,
            orientation='h',
            marker={"color": MALE_COLOR},
        ),
    )

    course_gender_age.update_layout(
        font_size=14,
        height=900,
        title="Distribuição de gêneros por curso",
        barmode="stack",
        hovermode="y unified",
        margin={"b": 190},
        margin_pad=5,
        showlegend=True,
    )

    course_gender_age.update_xaxes(
        title_text="# de estudantes",
        title_standoff=35,
    )

    course_gender_age.update_yaxes(
        title_text="Curso",
        title_standoff=5,
    )

    course_gender_age.update_layout(
        title_font_size=TITLE_FONT_SIZE,
    )

    st.plotly_chart(course_gender_age, use_container_width=True)


def generic_treemap(df: pd.DataFrame, path: list[str], gender: Gender = '') -> None:
    data = df

    if gender != '':
        data = data.query(f'Gender == "{gender}"')

    tree_map = px.treemap(
                data,
                path=path,
                values='count',
                height=1000,
        )

    tree_map.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    tree_map.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    tree_map.update_traces(
        texttemplate="Faixa: %{label}<br>" \
            "Total: %{value}<br>" \
            "%{percentParent} de %{parent}<br>" \
            # "%{percentRoot} de %{root}<br>" \
            "%{percentEntry} de %{entry}<br>"
    )

    st.plotly_chart(tree_map, use_container_width=True)


def generic_sunburst(df: pd.DataFrame, path: list[str], gender: Gender = '') -> None:
    data = df

    if gender != '':
        data = data.query(f'Gender == "{gender}"')

    sunburst = px.sunburst(
                data,
                path=path,
                values='count',
                height=1000,
        )

    sunburst.data[0].textinfo = 'label+value+percent parent+percent entry+percent root'

    sunburst.update_layout(
        title_font_size=TITLE_FONT_SIZE,
        font_size=16,
    )

    sunburst.update_traces(
        texttemplate="%{label}<br>" \
            "%{value}<br>" \
            "%{percentParent} de %{parent}<br>" \
            # "%{percentRoot} de %{root}<br>" \
            "%{percentEntry} de %{entry}<br>"
    )

    st.plotly_chart(sunburst, use_container_width=True)


def funnel_pop(df, **kwargs):
    color_map = {Gender.Male: MALE_COLOR, Gender.Female: FEMALE_COLOR}
    funnel_pop = px.funnel(df, color_discrete_map=color_map, **kwargs)

    funnel_pop.update_traces(textinfo='value+percent initial')
    funnel_pop.update_layout(
        margin_pad=5,
        showlegend=True,
        height=600,
    )

    st.plotly_chart(funnel_pop, use_container_width=True)


def dropout_histogram(Dropout):
    st.subheader("Histograma de evasão por curso")
    histograma_drop= px.histogram(Dropout, x="Course", color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=[COR3, COR2, COR4],).update_layout(title={"text": "Percent :Course - Target","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(histograma_drop)


def grade_semesters(Dropout):
    st.subheader("Distribuição de notas por curso ")
    box_1stSemester= px.box (Dropout.sort_values(by='Course'),  x="Course" , y="Curricular units 1st sem (grade)", color= "Course")
    box_2ndSemester= px.box (Dropout.sort_values(by='Course'),  x="Course" , y="Curricular units 2nd sem (grade)", color= "Course")
    st.subheader("Primeiro semestre")
    st.write(box_1stSemester)
    st.subheader("Segundo semestre")
    st.write(box_2ndSemester)

    st.subheader("Primeiro Semestre")
    bar_1stSemester= px.bar(Dropout.sort_values(by='Course'), x="Course", y="Curricular units 1st sem (grade)")
    st.write(bar_1stSemester)
    st.subheader("Segundo Semestre")
    bar_2ndSemester= px.bar(Dropout.sort_values(by='Course'), x="Course", y="Curricular units 2nd sem (grade)")
    st.write(bar_2ndSemester)

    scatter= px.scatter(Dropout, x= "Course", y="Curricular units 1st sem (grade)" , color= "Target" )
    st.write(scatter)
    scatter= px.scatter(Dropout, x= "Course", y="Curricular units 2nd sem (grade)" , color= "Target" )
    st.write(scatter)


def gender_course(Dropout, gender):
    filtered_df = Dropout[Dropout['Gender'] == gender]
    st.subheader="Estado de estudante por gênero"
    Gender_PercentBar= px.histogram( filtered_df, x="Course",title=f' {gender} Students' ,color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=[COR3, COR2, COR4],).update_layout(title={"text": "Percent :Course - Gender","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(Gender_PercentBar)
    Gender_Bar = px.bar(filtered_df, x="Course", color= "Course",barmode= "group" ,text_auto= True, )
    st.subheader="Distribuição de gênero de studantes por curso"
    Gender_Bar.update_layout(title= "Numéro de estudantes por curso", xaxis_title="Cursos", yaxis_title="Número de estudantes")
    st.write(Gender_Bar)






def financial_status(Dropout):
    Financial_Status= px.scatter(Dropout.sort_values(by='Course'), x= "Course", y= "Renda total" )
    st.subheader="Índice de renda por curso"
    Financial_Status.update_layout(xaxis_title="Status do estudante", yaxis_title= "Renda total")
    st.write(Financial_Status)

    st.subheader= "Evasão por idade"
    Dropout= Dropout.sort_values(by= "age_range")
    Age_percent= px.histogram( Dropout.sort_values(by= "age_range"), x="age_range",title=f' Age of Students in course dropout' ,color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=[COR3, COR2, COR4],).update_layout(title={"text": "Percent :Course - Gender","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(Age_percent)
