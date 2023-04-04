import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.svm import SVR
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import sklearn.metrics as metrics
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier

header = st.container()
dataset = st.container()

with header:
    st.title('Análise das Notas')

with dataset:
    dropout_data0 = st.session_state['dropout_data']
    dropout_data = dropout_data0.drop(index=dropout_data0[dropout_data0['Target'] == 'Enrolled'].index)

    # Divisão das notas de admissão em 2 tipos
    dropout_data.loc[dropout_data['Admission grade'] <= 145, 'nota_do_vestibular'] = '95 - 145'
    dropout_data.loc[dropout_data['Admission grade'] > 145, 'nota_do_vestibular'] = '146 - 200'
    
    # Divisão das notas dos semestres em 3 tipos
    dropout_data.loc[dropout_data['Curricular units 1st sem (grade)'] < 9.75, 'nota_1o_sem'] = '0 - 1'
    dropout_data.loc[dropout_data['Curricular units 1st sem (grade)'] > 15, 'nota_1o_sem'] = '15 - 20'
    dropout_data['nota_1o_sem'].fillna('10 - 15', inplace=True)

    dropout_data.loc[dropout_data['Curricular units 2nd sem (grade)'] < 9.75, 'nota_2o_sem'] = '0 - 1'
    dropout_data.loc[dropout_data['Curricular units 2nd sem (grade)'] > 15, 'nota_2o_sem'] = '15 - 20'
    dropout_data['nota_2o_sem'].fillna('10 - 15', inplace=True)
    

    # definindo cores
    cores_notas_vestibular = ["#FF6961", "#87CEEB"]
    cores_classes = ["#87CEEB", "#FF6961", "#98FB98"]
    cores_notas_semestres = ["#FF6961", "#87CEEB", "#98FB98"]


    # Início dos gráficos de comparação de nota com classe social
    df41grad = dropout_data.loc[(dropout_data['Target']=='Graduate')]
    df41drop= dropout_data.loc[(dropout_data['Target']=='Dropout')]


    st.title('Relação entre as notas')
    option = st.selectbox(
        'Mudar o grupo visualizado',
        ('Formados', 'Desistentes', 'Todos')
    )

    fig = px.scatter(
        df41grad,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)',
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre'
        },
        title='Notas dos alunos que se formaram',
        width=800, height=400
        )


    fig2 = px.scatter(
        df41drop,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)',
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre'
        },
        title='Notas dos alunos que desistiram',
        width=800, height=400
        )


    fig3 = px.scatter(
        dropout_data,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='nota_do_vestibular',
        color_discrete_sequence=cores_notas_vestibular,
        labels={
            'Curricular units 1st sem (grade)' : 'Notas do 1º Semestre',
            'Curricular units 2nd sem (grade)' : 'Notas do 2º Semestre',
            'nota_do_vestibular' : 'Nota de Admissão'
        },
        title='Notas de todos alunos',
        width=800, height=400
        )
        
    if option == 'Formados':
        st.write(fig)
    elif option == 'Desistentes':
        st.write(fig2)
    else:
        st.write(fig3)

    st.title('Influência da renda dos pais nas notas')

    # Definição de Classes Sociais
    dropout_data.loc[dropout_data['Renda total'] <= 1405, 'Classe social'] = 'Classe baixa'
    dropout_data.loc[dropout_data['Renda total'] >= 3000, 'Classe social'] = 'Classe alta'
    dropout_data['Classe social'].fillna('Classe média', inplace=True)

    # Gráficos de comparação Notas Admission x Classe Social
    st.subheader('Relação entre Notas do Vestibular e Classe Social')

    ordem_classes_sociais = ['Classe baixa', 'Classe média', 'Classe alta']
    chart_type_admission = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'))
    
    if chart_type_admission == 'Distribuição':
        histograma_admission1 = px.histogram(
            dropout_data,
            x='Admission grade', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do vestibular com a classe social'
        )
        st.write(histograma_admission1)
    elif chart_type_admission == 'Porcentagem':
        histograma_admission3 = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_do_vestibular',
            color_discrete_sequence=cores_notas_vestibular,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do vestibular por classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_admission3)


    # Gráficos de comparação Notas 1o sem x Classe Social
    st.subheader('Relação entre Notas do 1o Semestre e Classe Social')
    chart_type_1o_sem = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'), key='chart_type_1o_sem')
    if chart_type_1o_sem == 'Distribuição':
        histograma_sem1 = px.histogram(
            dropout_data,
            x='Curricular units 1st sem (grade)', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do 1o semestre com a classe social'
        )
        st.write(histograma_sem1)
    elif chart_type_1o_sem == 'Porcentagem':
        histograma_sem1_porcent = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_1o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm = "percent",
            text_auto=True,
            title='Porcentagem de notas do 1o semestre por classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_sem1_porcent)


    # Gráficos de comparação Notas 2o sem x Classe Social
    st.subheader('Relação entre Notas do 2o Semestre e Classe Social')
    chart_type_2o_sem = st.radio('Selecione o tipo de gráfico:', ('Distribuição', 'Porcentagem'), key='chart_type_2o_sem')
    if chart_type_2o_sem == 'Distribuição':
        histograma_sem2 = px.histogram(
            dropout_data,
            x='Curricular units 2nd sem (grade)', color='Classe social', color_discrete_sequence=cores_classes,
            title='Comparação da nota do 2o semestre com a classe social'
        )
        st.write(histograma_sem2)
    elif chart_type_2o_sem == 'Porcentagem':
        histograma_sem2_porcent = px.histogram(
            dropout_data,
            x='Classe social',
            color='nota_2o_sem', 
            color_discrete_sequence=cores_notas_semestres,
            barnorm = "percent", 
            text_auto= True,
            title='Comparação da nota do 2o semestre com a classe social',
            category_orders={'Classe social': ordem_classes_sociais}
        )
        st.write(histograma_sem2_porcent)


    st.subheader('Comparação das notas dos 2 semestres com a classe social')
    scatter_semestres = px.scatter(
        dropout_data,
        x='Curricular units 1st sem (grade)', y='Curricular units 2nd sem (grade)', color='Classe social', color_discrete_sequence=cores_classes
    )
    st.write(scatter_semestres)


    # Dataframes de Escolaridade dos Pais
    df_both_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') & (dropout_data['Escolaridade pai'] == 'ensino superior')]

    df_one_higher = dropout_data[(dropout_data['Escolaridade mae'] == 'ensino superior') ^ (dropout_data['Escolaridade pai'] == 'ensino superior')]

    df_both_secondary = dropout_data[(dropout_data['Escolaridade mae'] == 'medio completo') & (dropout_data['Escolaridade pai'] == 'medio completo')]

    df_both_primary = dropout_data[(dropout_data['Escolaridade mae'] == 'fundamental incompleto') & (dropout_data['Escolaridade pai'] == 'fundamental incompleto')]


    # add coluna de escolaridade dos pais no dropout_data
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'ensino superior') & (dropout_data['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'ambos com ensino superior'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'ensino superior') ^ (dropout_data['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'um com ensino superior'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'medio completo') & (dropout_data['Escolaridade pai'] == 'medio completo'), 'Escolaridade_Maes&Pais'] = 'ambos com medio completo'
    dropout_data.loc[(dropout_data['Escolaridade mae'] == 'fundamental incompleto') & (dropout_data['Escolaridade pai'] == 'fundamental incompleto'), 'Escolaridade_Maes&Pais'] = 'ambos com fundamental incompleto'


    # Plots de Escolaridade dos Pais X Classe Social
    st.subheader('Relação entre Escolaridade dos Pais e Notas')
    ordem_escolaridade = ['ambos com fundamental incompleto', 'ambos com medio completo', 'um com ensino superior', 'ambos com ensino superior']
    chart_type_escolaridade = st.radio('Selecione o tipo de gráfico:', ('Vestibular', '1o Semestre', '2o Semestre'))
    if chart_type_escolaridade == 'Vestibular':
        histograma_escolaridade_vestibular = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_do_vestibular',
            color_discrete_sequence=cores_notas_vestibular,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do vestibular por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_vestibular)
    elif chart_type_escolaridade == '1o Semestre':
        histograma_escolaridade_1o_sem = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_1o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do 1o semestre por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_1o_sem)
    elif chart_type_escolaridade == '2o Semestre':
        histograma_escolaridade_2o_sem = px.histogram(
            dropout_data,
            x='Escolaridade_Maes&Pais',
            color='nota_2o_sem',
            color_discrete_sequence=cores_notas_semestres,
            barnorm="percent",
            text_auto=True,
            title='Porcentagem de notas do 2o semestre por escolaridade dos pais',
            category_orders={'Escolaridade_Maes&Pais': ordem_escolaridade}
        )
        st.write(histograma_escolaridade_2o_sem)





    # Definindo X e y para o SVM


    df_notas_svm = dropout_data.copy()
    
    le = LabelEncoder()
    df_notas_svm['Marital status'] = le.fit_transform(df_notas_svm['Marital status'])
    df_notas_svm['Course'] = le.fit_transform(df_notas_svm['Course'])
    df_notas_svm['Gender'] = le.fit_transform(df_notas_svm['Gender'])
    df_notas_svm['Scholarship holder'] = le.fit_transform(df_notas_svm['Scholarship holder'])
    df_notas_svm['International'] = le.fit_transform(df_notas_svm['International'])
    df_notas_svm['Target'] = le.fit_transform(df_notas_svm['Target'])
    df_notas_svm['Escolaridade mae'] = le.fit_transform(df_notas_svm['Escolaridade mae'])
    df_notas_svm['Escolaridade pai'] = le.fit_transform(df_notas_svm['Escolaridade pai'])
    df_notas_svm['Classe social'] = le.fit_transform(df_notas_svm['Classe social'])
    df_notas_svm['Escolaridade_Maes&Pais'] = le.fit_transform(df_notas_svm['Escolaridade_Maes&Pais'])
    df_notas_svm['média_dos_semestres'] = df_notas_svm.apply(lambda row: (row['Curricular units 1st sem (grade)'] + row['Curricular units 2nd sem (grade)']) / 2, axis=1)
    
    st.title('Random Forest Regression')
    chart_type_rf = st.radio('Selecione o tipo de gráfico:', ('1o Semestre', '2o Semestre'))
    if chart_type_rf == '1o Semestre':
        st.subheader('Random Forest Regression para notas do 1o semestre')
        X = df_notas_svm.drop(['Escolaridade_Maes&Pais', 'Target', 'Admission grade', 'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)', 'média_dos_semestres', 'nota_do_vestibular', 'nota_1o_sem', 'nota_2o_sem', 'age_range'], axis=1, inplace=False)
        y = df_notas_svm['Curricular units 1st sem (grade)']


        # Instanciando o modelo de regressão
        rf = RandomForestRegressor()

        # Treinando o modelo
        rf.fit(X, y)

        # Obtendo a importância das colunas
        importances = rf.feature_importances_

        # Criando um DataFrame com as importâncias das colunas
        df_importances = pd.DataFrame({
            "Feature": X.columns,
            "Importance": importances
        })

        # Ordenando o DataFrame pela importância em ordem decrescente
        df_importances = df_importances.sort_values(by="Importance", ascending=True)

        # Criando o gráfico de barras horizontais
        fig, ax = plt.subplots()
        ax.barh(df_importances["Feature"], df_importances["Importance"])
        ax.set_xlabel("Importance")
        ax.set_title("Importance of each feature")

        # Exibindo o gráfico no streamlit
        st.pyplot(fig)
    else:
        # Notas do 2o semestre
        st.subheader('Random Forest Regression para notas do 2o semestre')
        X = df_notas_svm.drop(['Escolaridade_Maes&Pais', 'Target', 'Admission grade', 'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)', 'média_dos_semestres', 'nota_do_vestibular', 'nota_1o_sem', 'nota_2o_sem', 'age_range'], axis=1, inplace=False)
        y = df_notas_svm['Curricular units 2nd sem (grade)']

        # Instanciando o modelo de regressão
        rf = RandomForestRegressor()

        # Treinando o modelo
        rf.fit(X, y)

        # Obtendo a importância das colunas
        importances = rf.feature_importances_

        # Criando um DataFrame com as importâncias das colunas
        df_importances = pd.DataFrame({
            "Feature": X.columns,
            "Importance": importances
        })

        # Ordenando o DataFrame pela importância em ordem decrescente
        df_importances = df_importances.sort_values(by="Importance", ascending=True)

        # Criando o gráfico de barras horizontais
        fig, ax = plt.subplots()
        ax.barh(df_importances["Feature"], df_importances["Importance"])
        ax.set_xlabel("Importance")
        ax.set_title("Importance of each feature")

        # Exibindo o gráfico no streamlit
        st.pyplot(fig)



    dataset_nota_satisfatoria = dropout_data.copy()

    dataset_nota_satisfatoria['nota_satisfatória_dos_semestres'] = dataset_nota_satisfatoria.apply(lambda row: '10 até 20' if row['Curricular units 1st sem (grade)'] + row['Curricular units 2nd sem (grade)'] >= 10 else '0 até 9,9', axis=1)

    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Marital status'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Course'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Gender'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Scholarship holder'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['International'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Escolaridade mae'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Escolaridade pai'])
    dataset_nota_satisfatoria = pd.get_dummies(dataset_nota_satisfatoria, columns=['Classe social'])

    chart_type_previsao = st.radio('Selecione o tipo de gráfico:', ('Random Forest Classifier', 'Report SVM', 'Gradient Boosting'))
    if chart_type_previsao == 'Random Forest Classifier':
        # PREVISAO COM RANDOM FOREST CLASSIFIER
        st.title('Random Forest Classifier')

        X = dataset_nota_satisfatoria.drop(['nota_satisfatória_dos_semestres', 'Escolaridade_Maes&Pais', 'Target', 'Admission grade', 'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)', 'nota_do_vestibular', 'nota_1o_sem', 'nota_2o_sem', 'age_range'], axis=1)
        y = dataset_nota_satisfatoria['nota_satisfatória_dos_semestres']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Instantiate a RandomForestClassifier object
        rfc = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

        # Fit the classifier to the training data
        rfc.fit(X_train, y_train)

        # Use the classifier to predict dropout for the testing data
        y_pred = rfc.predict(X_test)

        # Evaluate the performance of the classifier
        report = (classification_report(y_test, y_pred))

        st.text(report)

        report = metrics.classification_report(y_test, y_pred, output_dict=True)
        df = pd.DataFrame(report).transpose()
        def format_percent(x):
            if isinstance(x, str):
                return x
            else:
                return "{:.2f}".format(x)

        df = df.applymap(format_percent)
        
        st.write(df)

    elif chart_type_previsao == 'Report SVM':

        # REPORT SVM
        X = dataset_nota_satisfatoria.drop(['nota_satisfatória_dos_semestres', 'Escolaridade_Maes&Pais', 'Target', 'Admission grade', 'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)', 'nota_do_vestibular', 'nota_1o_sem', 'nota_2o_sem', 'age_range'], axis=1)
        y = dataset_nota_satisfatoria['nota_satisfatória_dos_semestres']
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Instantiate a Support Vector Machine object
        svm = SVC(kernel='rbf', C=1, gamma='scale')

        # Fit the SVM to the training data
        svm.fit(X_train, y_train)

        # Use the SVM to predict dropout for the testing data
        y_pred = svm.predict(X_test)

        # Evaluate the performance of the SVM
        report = (classification_report(y_test, y_pred))
        st.title('Report SVM')
        st.text(report)

        report_dict = classification_report(y_test, y_pred, output_dict=True)
        df = pd.DataFrame(report_dict).transpose()
        def format_percent(x):
            if isinstance(x, str):
                return x
            else:
                return "{:.2f}".format(x)

        df = df.applymap(format_percent)
        
        st.write(df)
    
    else:
        # GRADIENT BOOSTING
        X = dataset_nota_satisfatoria.drop(['nota_satisfatória_dos_semestres', 'Escolaridade_Maes&Pais', 'Target', 'Admission grade', 'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)', 'Curricular units 1st sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 1st sem (approved)', 'Curricular units 1st sem (without evaluations)', 'nota_do_vestibular', 'nota_1o_sem', 'nota_2o_sem', 'age_range'], axis=1)
        y = dataset_nota_satisfatoria['nota_satisfatória_dos_semestres']
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Instantiate a GradientBoostingClassifier object
        gbc = GradientBoostingClassifier(n_estimators=100, max_depth=10, random_state=42)

        # Fit the classifier to the training data
        gbc.fit(X_train, y_train)

        # Use the classifier to predict dropout for the testing data
        y_pred = gbc.predict(X_test)

        # Evaluate the performance of the classifier
        report = (classification_report(y_test, y_pred))
        st.title('Report Gradient Boosting')


        report_dict = classification_report(y_test, y_pred, output_dict=True)
        df = pd.DataFrame(report_dict).transpose()
        def format_percent(x):
            if isinstance(x, str):
                return x
            else:
                return "{:.2f}".format(x)

        df = df.applymap(format_percent)

        st.text(report)
        st.write(df)