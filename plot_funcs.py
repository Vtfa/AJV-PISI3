import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_funcs import *

from plotly.subplots import make_subplots
Dropout = pd.read_csv('data/dropout.csv')
Dropout = treat_data(Dropout)


def gender_tree(data: pd.DataFrame) -> None:
    gender_tree = px.treemap(
        data,
        title="Gender distribution by course",
        path=["Course", "Gender"],
        color_continuous_scale="RdBu",
        color="count",
        values="count",
        height=1000,
    )

    gender_tree.data[0].textinfo = "label+value+percent parent+percent entry+percent root"

    gender_tree.update_layout(
        title_font_size=26,
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
            marker={"color": "rgba(0, 204, 150, 0.5)"},
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
            marker={"color": "rgba(99, 110, 250, 0.5)"},
            hoverinfo="text",
        )
    )

    dem_pyramid.update_layout(
        title="Students' Population Pyramid",
        title_font_size=22,
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
        title=f"Course and age distribution for {gender} students",
        path=["Gender", "Course", "age_range"],
        values="count",
        height=1000,
    )

    specific_gender_tree.data[0].textinfo = "label+value+percent parent+percent entry+percent root"

    specific_gender_tree.update_layout(
        title_font_size=26,
        font_size=16,
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
            marker={"color": "rgba(99, 110, 250, 0.5)"},
        ),
    )

    course_gender_age.add_trace(
        go.Bar(
            name="Male",
            x=course_gender_age_index,
            y=course_gender_data["Male"],
            orientation="v",
            marker={"color": "rgba(0, 204, 150, 0.5)"},
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
        height=900,
        font_size=14,
        title="Gender distribution by course",
        barmode="stack",
        hovermode="x unified",
        margin={"b": 190},
        margin_pad=10,
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
        title_font_size=26,
        font_size=16,
    )

    st.plotly_chart(debt_gender_tree, use_container_width=True)


def dropout_by_age_debt(df: pd.DataFrame) -> None:
    debt_tree = px.treemap(
                df,
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



def dropout_histogram():
    st.subheader("Histograma de evasão por curso")   
    histograma_drop= px.histogram(Dropout, x="Course", color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=["#FF6961", "#98FB98", "#87CEEB"],).update_layout(title={"text": "Percent :Course - Target","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(histograma_drop)


def grade_semesters():
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


def gender_course(gender):
    filtered_df = Dropout[Dropout['Gender'] == gender]
    st.subheader="Estado de estudante por gênero" 
    Gender_PercentBar= px.histogram( filtered_df, x="Course",title=f' {gender} Students' ,color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=["#FF6961", "#98FB98", "#87CEEB"],).update_layout(title={"text": "Percent :Course - Gender","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(Gender_PercentBar)
    Gender_Bar = px.bar(filtered_df, x="Course", color= "Course",barmode= "group" ,text_auto= True, )
    st.subheader="Distribuição de gênero de studantes por curso"    
    Gender_Bar.update_layout(title= "Numéro de estudantes por curso", xaxis_title="Cursos", yaxis_title="Número de estudantes")  
    st.write(Gender_Bar)
        

   
    


def financial_status():
    Financial_Status= px.scatter(Dropout.sort_values(by='Course'), x= "Course", y= "Renda total" )
    st.subheader="Índice de renda por curso"
    Financial_Status.update_layout(xaxis_title="Status do estudante", yaxis_title= "Renda total")
    st.write(Financial_Status)

    st.subheader= "Dropout por idade"
    Dropout= Dropout.sort_values(by= "age_range")
    Age_percent= px.histogram( Dropout.sort_values(by= "age_range"), x="age_range",title=f' Age of Students in course dropout' ,color="Target",barnorm = "percent",text_auto= True, color_discrete_sequence=["#FF6961", "#98FB98", "#87CEEB"],).update_layout(title={"text": "Percent :Course - Gender","x": 0.5},yaxis_title="Percent").update_xaxes(categoryorder='total descending')
    st.write(Age_percent)
