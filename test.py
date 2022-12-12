import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

df = pd.read_csv('data/dropout.csv')
pr= df.profile_report()
st_profile_report(pr)

