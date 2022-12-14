import pandas as pd
import pandas_profiling
import streamlit as st

from streamlit_pandas_profiling import st_profile_report

#rodar apenas streamlit run c:\caminho\do\arquivo\no_seu_computador\profile_dropout.py ao invés de executar o arquivo profile_dropout.py 
#se estiver usando o vscode, dá pra: botão direito no arquivo > copy path
def escolaridade_pais(valor): 
        array_fund_inc = [11, 26, 35, 36, 37, 38, 29, 30]
        array_medio_inc = [9, 10, 12, 13, 14, 19, 27, 13, 25]
        medio = 1 
        array_tecnico = [18, 22, 39, 31, 33]
        array_superior = [2, 3, 4, 5, 6, 40, 41, 42, 43, 44]

        if valor in array_fund_inc:
            return 'fundamental incompleto'
        elif valor in array_medio_inc:
            return 'medio imcompleto'
        elif valor == medio:
            return 'medio completo'
        elif valor in array_tecnico:
            return 'tecnico'
        elif valor in array_superior: 
            return 'superior compleco'
        else: return 'sem informacoes'
        

dropout_data = pd.read_csv('data\dropout.csv')


dropout_data["Escolaridade mae"] = dropout_data["Mother's qualification"].apply(lambda valor: escolaridade_pais(valor)) 
dropout_data["Escolaridade pai"] = dropout_data["Father's qualification"].apply(lambda valor: escolaridade_pais(valor))
dropout_data.drop(['Nacionality', 'Previous qualification (grade)', "Mother's qualification", "Father's qualification", "Curricular units 1st sem (credited)", 
"Curricular units 1st sem (evaluations)", "Curricular units 1st sem (without evaluations)", "Curricular units 2nd sem (credited)", "Curricular units 2nd sem (evaluations)",
"Curricular units 2nd sem (without evaluations)"], axis=1, inplace=True)

#dropout_data.loc[dropout_data['Target'] == 'Dropout', "Target"] = 0
#dropout_data.loc[dropout_data['Target'] == 'Enrolled', "Target"] = 1
#dropout_data.loc[dropout_data['Target'] == 'Graduate', "Target"] = 2 

pr = dropout_data.profile_report()
st_profile_report(pr)