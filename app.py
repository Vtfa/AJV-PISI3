import streamlit as st
import pandas as pd
import plotly.express as px


header = st.container()
dataset = st.container()


with header:
    st.title("Predict Dropout or Academic Success")


with dataset:
    dropout_data = pd.read_csv('data/dropout.csv')
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

    st.title("Histograma de dropout por curso")
    st.subheader('Fica mais fácil visualizar tendências em um Histograma, aqui procuro tendências do dropout relacionados aos cursos dos alunos. Trocamos os valores numéricos dos  cursos por valores correspondentes do dicionário.')
    #Aqui mapeio os valores numericos dos cursos com seu nome para usar o .replace() do pandas para trocar valores.
    course_dropout= dropout_data[(dropout_data['Target']== 'Dropout')]#Dataframe com registros em que target = dropout
    mapping= {33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design', 8014: 'Social Service', 9003:'Agronomy', 9070:'Communication Design', 9085:'Veterinary Nursing', 9119:'Informatics Engineering',9130: 'Equinculture', 9147: 'Management', 9238: 'Social Service', 9254:'Tourism', 9500:'Nursing', 9556:'Oral Hygiene', 9670:'Advertising and Marketing Management', 9773: 'Journalism and Communication', 9853: 'Basic Education', 9991: 'Management(Evening)'}    
    course_dropout['Course'] = course_dropout['Course'].map(mapping)
    histograma_drop= px.histogram(course_dropout, x= "Course")
    st.write(histograma_drop)




    
    # Aqui começa o codigo do grafico relacionando a coluna 'Debtor' com a evasao

    dfaux_target = dropout_data.groupby(['Target'])['Target'].count().reset_index(name='soma_target')

    df_sem_divida = dropout_data[dropout_data.Debtor==0]
    dfaux_sem_divida = df_sem_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_sem_divida')

    df_com_divida = dropout_data[dropout_data.Debtor==1]
    dfaux_com_divida = df_com_divida.groupby(['Target'])['Target'].count().reset_index(name='soma_com_divida')
    
    st.title('Situação dos estudantes por dívida')
    option = st.selectbox(
        'Mudar o grupo visualizado',
        ('Todos estudantes', 'Endividados', 'Sem dívidas'))

    grafico_target_geral = px.pie(dfaux_target, values='soma_target', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes ')
    grafico_target_endividados = px.pie(dfaux_com_divida, values='soma_com_divida', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes Endividados')
    grafico_target_estudantes_sem_dividas = px.pie(dfaux_sem_divida, values='soma_sem_divida', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação Acadêmica dos Estudantes Sem dívidas')
    
    if option == 'Todos estudantes':
        st.plotly_chart(grafico_target_geral)
    elif option == 'Endividados':
        st.plotly_chart(grafico_target_endividados)
    else:
        st.plotly_chart(grafico_target_estudantes_sem_dividas)

   
st.title('Situação dos estudantes internacionais')
option_internacioal = st.selectbox('Mudar o grupo visualizado', ('Todos estudantes', 'Estudantes Internacionais'))

df_internacional = dropout_data[dropout_data.Nacionality != 1]
dfaux_internacional = df_internacional.groupby(['Target'])['Target'].count().reset_index(name='soma_target_internacional')
pie_target_internacional = px.pie(dfaux_internacional, values='soma_target_internacional', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação acadêmica dos estudantes')

if option_internacioal == 'Todos estudantes':
    st.write(grafico_target_geral)
else:
    st.write(pie_target_internacional)


st.title('Situação dos estudantes portadores de bolsas de estudo')
option_scholarship = st.selectbox('Mudar o grupo visualizado', ('Estudantes não portadores de bolsas de estudo', 'Estudantes portadores de bolsas de estudo'))

df_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 1)]
dfaux_scholarship = df_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_scholarship')
df_no_scholarship = dropout_data[(dropout_data['Scholarship holder'] == 0)]
dfaux_no_scholarship = df_no_scholarship.groupby(['Target'])['Target'].count().reset_index(name='soma_no_scholarship')

pie_scholarship = px.pie(dfaux_scholarship, values='soma_scholarship', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação acadêmica dos estudantes sem bolsa de estudo')
pie_no_scholarship = px.pie(dfaux_no_scholarship, values='soma_no_scholarship', names='Target', color='Target', color_discrete_map={'Dropout':'rgb(239, 85, 59)', 'Enrolled':'rgb(99, 110, 250)', 'Graduate':'rgb(0, 204, 150)'}, title='Situação acadêmica dos estudantes sem bolsa de estudos')

if option_scholarship =='Estudantes não portadores de bolsas de estudo':
    st.write(pie_no_scholarship)
else:

    st.write(pie_scholarship)


    st.write(pie_scholarship)
