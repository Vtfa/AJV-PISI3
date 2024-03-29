import streamlit as st
from plot_funcs import *
from data_funcs import *
from aux_funcs import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from ml_funcs import *

title = "Análise dos cursos"



def page_3():
    dropout_data=  dropout_data = st.session_state['dropout_data']

    dataframes = ['dropout_data', 'gender_data', 'course_data', 'debt_data']

    if not valid_session_data(dataframes, '## :construction: Please, go to _Home_ page before :construction:', 0.15):
        return


    reset_filters()


    with st.container():
        st.title(title)

    with st.container():

        st.header('Dados dos cursos')
        plots= ["Histograma de evasão", "Relação das notas com cursos", "Dados socioeconômicos", "Machine Learning"]
        selected_plot= st.selectbox("Selecione para visualizar",plots)
        if selected_plot == "Histograma de evasão":
          dropout_histogram(dropout_data)

        elif selected_plot == "Relação das notas com cursos":
          grade_semesters(dropout_data)

        elif selected_plot=="Dados socioeconômicos":
          st.subheader = "Plots sobre gênero dos estudantes"
          gender = st.radio("Select a gender", [Gender.Male.value, Gender.Female.value])
          gender_course(dropout_data, gender)

          st.subheadder= "Plots sobre renda e finanças"
          fig = px.scatter(dropout_data, x="Age at enrollment", y= "Renda total")
          st.write(fig)

          histograma_age= px.histogram(dropout_data, x="Age at enrollment", y= "Renda total")
          st.write(histograma_age)

        elif selected_plot == "Machine Learning":
          courses = sorted(dropout_data['Course'].unique())


          st.title('Machine Learning')

          selected_course= st.selectbox("Selecione o curso", courses)



          dropout_data= dropout_data[dropout_data['Course']==selected_course]
          dropout_data = dropout_data[dropout_data['Target'] != Target.Enrolled]
         # One-hot encode categorical features
          categorical_features = ['Marital status', 'Course', 'Gender', 'Scholarship holder', 'International',
                                  'Escolaridade mae', 'Escolaridade pai', 'Classe social']
          dropout_data = pd.get_dummies(dropout_data, columns=categorical_features)

          # Split the data into features and target
          X = dropout_data.drop([
                                 'Curricular units 1st sem (approved)', 'Curricular units 2nd sem (approved)', 'Curricular units 1st sem (grade)',
                                 'Curricular units 2nd sem (grade)', 'Curricular units 1st sem (evaluations)', 'Curricular units 2nd sem (evaluations)',
                                 'Curricular units 1st sem (enrolled)', 'Curricular units 2nd sem (enrolled)', 'Curricular units 1st sem (credited)', 'Curricular units 2nd sem (credited)',
                                 'Previous qualification (grade)',
                                 'Target', 'age_range', 'Tuition fees up to date', 'nota_do_vestibular', 'nota_1o_sem',
                                 'nota_2o_sem', 'Escolaridade_Maes&Pais'], axis=1)
          y = dropout_data['Target']

          # Split the dataset into training and testing sets
          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

          # Train and evaluate the models
          models = {
              'Random Forest Classifier': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
              'Gradient Boosting Classifier': GradientBoostingClassifier(n_estimators=100, max_depth=10, random_state=42),
              'Support Vector Machine': SVC(kernel='rbf', C=1, gamma='scale')
          }

          for name, model in models.items():
              model_name = f'{name.replace(" ", "")}_{selected_course.replace(" ", "")}'

              # Fit the model to the training data
              trained_model = train_model(model, X_train, y_train, model_name, MODELS_DIR)

              # Use the model to predict dropout for the testing data
              y_pred = trained_model.predict(X_test)

              # Evaluate the performance of the model
              report = (classification_report(y_test, y_pred))
              st.title(f'Report {name}')
              st.text(report)

              report_dict = classification_report(y_test, y_pred, output_dict=True)
              df = pd.DataFrame(report_dict).transpose()
              df = df.applymap(lambda x: x if isinstance(x, str) else "{:.0%}".format(x))
              st.write(df)

              if name == 'Random Forest Classifier':
                  # Get feature importances
                  importances = trained_model.feature_importances_

                  # Get feature names
                  feature_names = list(X.columns)

                  # Sort feature importances in descending order
                  indices = np.argsort(importances)[::-1]

                  # Get the top n most important features
                  n = 25
                  top_indices = indices[:n]

                  # Sort the features and importances by descending importance
                  sorted_feature_names = [feature_names[i] for i in top_indices][::-1]
                  sorted_importances = importances[top_indices][::-1]

                  # Create horizontal bar chart
                  fig, ax = plt.subplots(figsize=(10, 5))
                  ax.barh(sorted_feature_names, sorted_importances)
                  st.pyplot(fig)




page_3()
