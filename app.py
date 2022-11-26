import streamlit as st
import pandas as pd
import plotly.express as px

header = st.container()
dataset = st.container()


with header:
    st.title("Predict Dropout or Academic Success")


with dataset:
    dropout_data = pd.read_csv('data\dropout.csv')
    st.write(dropout_data.head())

    st.subheader('Enrollment age of students')
    age = pd.DataFrame(dropout_data['Age at enrollment'].value_counts())
    st.bar_chart(age)

    st.subheader('Gender of students 1 for male and 2 for female')
    gender = pd.DataFrame(dropout_data['Gender'].value_counts())
    st.bar_chart(gender)
    # O gráfico desse bloquinho acima de 3 linhas ficou estranho com o gráfico do streamlit. Ver como fazer no ploty
    
    st.title("Testando plotly e manipulação de valores de colunas no pandas!")
    st.subheader("Aqui trocamos valores '1' e '0' da coluna 'Gender' por valores 'Male' e 'Female' usando o método pandas.DataFrame.loc")

    dropout_data.loc[dropout_data['Gender'] == 1, "Gender"] = 'Male'
    dropout_data.loc[dropout_data['Gender'] == 0, "Gender"] = 'Female'

    st.write(dropout_data.head())
    
    df = dropout_data.groupby(['Gender'])['Gender'].count().reset_index(name='count')
    st.title('Gender of students')
    st.subheader('Gráfico feito com plotly')
    fig = px.pie(df, values='count', names='Gender')

    st.write(fig)
