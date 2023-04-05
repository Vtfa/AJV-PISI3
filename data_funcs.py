import pickle
import streamlit as st
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

from consts import Gender

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, engine='pyarrow')


# função para mapear os valores das profissões dos pais
def escolaridade_pais(data: pd.Series) -> pd.Series:
    fund_inc = np.isin(data, [11, 26, 35, 36, 37, 38, 29, 30])
    medio_inc = np.isin(data, [9, 10, 12, 13, 14, 19, 27, 13, 25])
    medio = data == 1
    tecnico = np.isin(data, [18, 22, 39, 31, 33])
    superior = np.isin(data, [2, 3, 4, 5, 6, 40, 41, 42, 43, 44])

    niveis = [
        'fundamental incompleto',
        'medio incompleto',
        'medio completo',
        'ensino tecnico',
        'ensino superior',
    ]

    return pd.Series(np.select(
        [fund_inc, medio_inc, medio, tecnico, superior],
        niveis,
        'no info'
    ))


def renda_pais(data: pd.Series) -> pd.Series:
    vars = [
        1, 2, 4, 5, 6, 7, 8, 9, 10, 122, 123, 125, 131, 132, 134, 141, 143, 144, 151, 152, 153,
        171, 173, 175, 191, 192, 193, 194, 101, 102, 103, 112, 114, 121, 135, 154, 161, 163,
        172, 174, 181, 182, 183, 195
    ]

    selecao = [data == value for value in vars]

    niveis = [
        3456, 2141, 930, 840, 875, 997, 940, 840, 1749, 2556, 2200, 3452, 1352, 1417, 930, 2248, 930,
        805, 1073, 740, 1042, 827, 915, 873, 799, 824, 710, 1865, 1489, 1124, 3456, 3456, 2141, 3063,
        1609, 840, 875, 875, 1353, 1897, 1061, 889, 884, 794,
    ]

    return pd.Series(np.select(selecao, niveis, 0))

# funcao para substituir o codido pelo nome dos cursos
def rename_courses(df: pd.DataFrame, course_col: str) -> pd.Series:
    courses_map = {
        33: 'Biofuel Production Technologies',
        171: 'Animation and Multimedia Design',
        8014: 'Social Service',
        9003: 'Agronomy',
        9070: 'Communication Design',
        9085: 'Veterinary Nursing',
        9119: 'Informatics Engineering',
        9130: 'Equinculture',
        9147: 'Management',
        9238: 'Social Service',
        9254: 'Tourism',
        9500: 'Nursing',
        9556: 'Oral Hygiene',
        9670: 'Advertising and Marketing Management',
        9773: 'Journalism and Communication',
        9853: 'Basic Education',
        9991: 'Management(Evening)'
    }
    return df[course_col].map(courses_map)


# funcao para calcular as faixas etarias
def age_range_calc(df: pd.DataFrame, age_col: str, interval: int = 5) -> pd.Series:
    age_bins = list(range(17, np.max(df[age_col].values), interval))
    ages_labels = [f'{age_bins[i-1]} - {age_bins[i]-1}' for i in range(1, len(age_bins))]

    return pd.cut(
        df[age_col],
        age_bins,
        labels=ages_labels,
        right=False,
        ordered=False,
    )


def rename_gender(df: pd.DataFrame, gender_col: str) -> pd.Series:
    return np.where(df['Gender'], 'Male', 'Female')


def marital_status_rename(df: pd.DataFrame, marital_status_col: str) -> pd.Series:
    # não solteiros foram agrupados por serem poucos
    return np.where(df[marital_status_col] == 1, 'Solteiro', 'Outros')


def treat_data(df: pd.DataFrame, age_interval: int = 5) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy['Marital status'] = marital_status_rename(df_copy, 'Marital status')
    df_copy["Escolaridade mae"] = escolaridade_pais(df_copy["Mother's qualification"])
    df_copy["Escolaridade pai"] = escolaridade_pais(df_copy["Father's qualification"])
    df_copy["Renda pai"] = renda_pais(df_copy["Father's occupation"])
    df_copy["Renda mae"] = renda_pais(df_copy["Mother's occupation"])
    df_copy["Renda total"] = df_copy["Renda pai"] + df_copy["Renda mae"]
    df_copy['Course'] = rename_courses(df_copy, 'Course')
    df_copy['age_range'] = age_range_calc(df_copy, 'Age at enrollment', age_interval)
    df_copy['Gender'] = rename_gender(df_copy, 'Gender')
    df_copy = get_grade_data(df_copy)
    df_copy = get_social_classes_data(df_copy)
    df_copy = get_schooling_data(df_copy)

    return df_copy


def get_gender_data(df: pd.DataFrame) -> pd.DataFrame:
    gender_data = (
        df[['age_range', 'Gender', 'Course']]
        .groupby(['age_range', 'Gender'])
        .count()
    )
    gender_data = gender_data.unstack('Gender').droplevel(0, 'columns')
    return gender_data

def get_funnel_data(data: pd.DataFrame, course: str, age_range: str, target: str) -> pd.DataFrame:
    cols = ['Course', 'age_range', 'Target', 'Gender']

    dfs = []
    for gender in Gender._member_names_:
        dt = data[cols].query('Gender == @gender').copy()
        course_count = dt.query('Course == @course').count().values[0]
        age_count = dt.query('Course == @course and age_range == @age_range').count().values[0]
        target_count = dt.query('Course == @course and age_range == @age_range and Target == @target').count().values[0]
        df = pd.DataFrame({'count': [course_count, age_count, target_count], 'stages': [course, age_range, target], 'gender': [gender]*3})
        dfs.append(df)


    df = pd.concat(dfs).reset_index().sort_values('count', ascending=False)
    return df


def get_course_data(df: pd.DataFrame) -> pd.DataFrame:
    course_data = (
        df[['age_range', 'Gender', 'Course', 'Displaced']]
        .groupby(['Course', 'Gender', 'age_range'])
        .count()
        .reset_index()
    )

    course_data.rename(columns={'Displaced': 'count'}, inplace=True)

    return course_data


def get_debt_data(df: pd.DataFrame) -> pd.DataFrame:
    debt_data = df.copy()
    debt_data['debt'] = np.where(
        (debt_data['Debtor'] == 1) | (debt_data['Tuition fees up to date'] == 0), 'has debt', 'up to date'
    )

    debt_data = (
        debt_data[['age_range', 'Gender', 'Course', 'debt', 'Displaced', 'Target']]
        .groupby(['Gender', 'Target', 'Course', 'age_range', 'debt'])
        .count()
        .reset_index()
    )
    # debt_data = debt_data[~debt_data['Target'].isin(['Enrolled'])]
    debt_data.rename(columns={'Displaced': 'count'}, inplace=True)
    return debt_data


def get_grade_data(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    # Divisão das notas de admissão em 2 tipos
    df_copy.loc[df_copy['Admission grade'] <= 145, 'nota_do_vestibular'] = '95 - 145'
    df_copy.loc[df_copy['Admission grade'] > 145, 'nota_do_vestibular'] = '146 - 200'

    # Divisão das notas dos semestres em 3 tipos
    df_copy.loc[df_copy['Curricular units 1st sem (grade)'] < 9.75, 'nota_1o_sem'] = '0 - 1'
    df_copy.loc[df_copy['Curricular units 1st sem (grade)'] > 15, 'nota_1o_sem'] = '15 - 20'
    df_copy['nota_1o_sem'].fillna('10 - 15', inplace=True)

    df_copy.loc[df_copy['Curricular units 2nd sem (grade)'] < 9.75, 'nota_2o_sem'] = '0 - 1'
    df_copy.loc[df_copy['Curricular units 2nd sem (grade)'] > 15, 'nota_2o_sem'] = '15 - 20'
    df_copy['nota_2o_sem'].fillna('10 - 15', inplace=True)

    return df_copy


def get_social_classes_data(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    # Definição de Classes Sociais
    df_copy.loc[df_copy['Renda total'] <= 1405, 'Classe social'] = 'Classe baixa'
    df_copy.loc[df_copy['Renda total'] >= 3000, 'Classe social'] = 'Classe alta'
    df_copy['Classe social'].fillna('Classe média', inplace=True)

    return df_copy


def get_schooling_data(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    # add coluna de escolaridade dos pais no dropout_data
    df_copy.loc[(df_copy['Escolaridade mae'] == 'ensino superior') & (df_copy['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'ambos com ensino superior'
    df_copy.loc[(df_copy['Escolaridade mae'] == 'ensino superior') ^ (df_copy['Escolaridade pai'] == 'ensino superior'), 'Escolaridade_Maes&Pais'] = 'um com ensino superior'
    df_copy.loc[(df_copy['Escolaridade mae'] == 'medio completo') & (df_copy['Escolaridade pai'] == 'medio completo'), 'Escolaridade_Maes&Pais'] = 'ambos com medio completo'
    df_copy.loc[(df_copy['Escolaridade mae'] == 'fundamental incompleto') & (df_copy['Escolaridade pai'] == 'fundamental incompleto'), 'Escolaridade_Maes&Pais'] = 'ambos com fundamental incompleto'

    return df_copy


def dataset_filter(df: pd.DataFrame, **filters) -> pd.DataFrame:
    df_copy = df.copy()
    columns = []

    if 'colunas' in filters.keys() and isinstance(filters['colunas'], list):
        if len(filters['colunas']) > 0:
            columns = filters['colunas']
            df_copy = df_copy[columns]


    select_fields = {
        'marital_status': 'Marital status',
        'course': 'Course',
        'escolaridade_mae': 'Escolaridade mae',
        'escolaridade_pai': 'Escolaridade pai',
    }

    multiselect_fields = {
        'gender': 'Gender',
        'age_range': 'age_range',
    }

    query = ''
    for key in filters.keys():
        if key in select_fields and filters[key] != '':
            if len(columns) > 0 and select_fields[key] not in columns:
                continue

            if len(query) > 0:
                query += ' and '

            query += f'`{select_fields[key]}` == "{filters[key]}"'
            continue

        if key in multiselect_fields and filters[key] != []:
            if len(columns) > 0 and multiselect_fields[key] not in columns:
                continue
            if len(query) > 0:
                query += ' and '

            query += f'`{multiselect_fields[key]}` in {filters[key]}'

    if query != '':
        df_copy = df_copy.query(query)

    return df_copy


def format_percent(item):
    if not isinstance(item, str):
        return f'{item:.0%}'

    return item

def pandas_profile(df: pd.DataFrame) -> ProfileReport:
    report = ProfileReport(
        df,
        title="Perfil do dataset de evasão acadêmica",
        minimal=True,
        lazy=False,
    )

    return report