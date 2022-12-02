import pandas as pd
import pandas_profiling
import streamlit as st

from streamlit_pandas_profiling import st_profile_report

#rodar apenas streamlit run c:\caminho\do\arquivo\no_seu_computador\profile_dropout.py ao invés de executar o arquivo profile_dropout.py 
#se estiver usando o vscode, dá pra: botão direito no arquivo > copy path

dropout_data = pd.read_csv('data\dropout.csv')
pr = dropout_data.profile_report()
st_profile_report(pr)