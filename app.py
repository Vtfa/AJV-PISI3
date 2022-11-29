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

    st.title('Dropout rates by gender')
    df_droupout_gender = dropout_data[(dropout_data['Target'] == 'Dropout')] #novo dataframe apenas com registros em que target = dropout
    dfaux_dropout_gender = df_droupout_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_dropout_gender') #DF auxiliar com total de male e female para ser usado no gráfico abaixo
    pie_dropout_gender = px.pie(dfaux_dropout_gender, values='soma_dropout_gender', names='Gender')
    st.write(pie_dropout_gender)

    st.title('Graduation rates by gender')
    df_graduate_gender = dropout_data[(dropout_data['Target'] == 'Graduate')] #novo dataframe apenas com registros em que target = graduate
    dfaux_graduate_gender = df_graduate_gender.groupby(['Gender'])['Gender'].count().reset_index(name='soma_graduate_gender') #DF auxiliar com total de male e female para ser usado no gráfico abaixo
    pie_graduate_gender = px.pie(dfaux_graduate_gender, values='soma_graduate_gender', names='Gender')
    st.write(pie_graduate_gender)

    
    # Aqui começa o codigo do grafico relacionando a coluna 'Debtor' com a evasao
    estudantes_sem_divida = dropout_data.loc[dropout_data['Debtor'] == 0]
    estudantes_com_divida = dropout_data.loc[dropout_data['Debtor'] == 1]

    option = st.selectbox(
        'Mudar o grupo visualizado',
        ('Todos estudantes', 'Endividados', 'Sem dívidas'))

    grafico_target_geral = px.pie(dropout_data, names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes ')
    grafico_target_endividados = px.pie(estudantes_com_divida, values='Debtor', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes Endividados')
    grafico_target_estudantes_sem_dividas = px.pie(estudantes_sem_divida, names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes Sem dívidas')
    if option == 'Todos estudantes':
        st.plotly_chart(grafico_target_geral)
    elif option == 'Endividados':
        st.plotly_chart(grafico_target_endividados)
    else:
        st.plotly_chart(grafico_target_estudantes_sem_dividas)

