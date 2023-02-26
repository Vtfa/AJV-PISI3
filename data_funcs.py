import streamlit as st
import pandas as pd
import numpy as np


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
    var_1 = data == 1
    var_2 = data == 2
    var_4 = data == 4
    var_5 = data == 5
    var_6 = data == 6
    var_7 = data == 7
    var_8 = data == 8
    var_9 = data == 9
    var_10 = data == 10
    var_122 = data == 122
    var_123 = data == 123
    var_125 = data == 125
    var_131 = data == 131
    var_132 = data == 132
    var_134 = data == 134
    var_141 = data == 141
    var_143 = data == 143
    var_144 = data == 144
    var_151 = data == 151
    var_152 = data == 152
    var_153 = data == 153
    var_171 = data == 171
    var_173 = data == 173
    var_175 = data == 175
    var_191 = data == 191
    var_192 = data == 192
    var_193 = data == 193
    var_194 = data == 194
    var_101 = data == 101
    var_102 = data == 102
    var_103 = data == 103
    var_112 = data == 112
    var_114 = data == 114
    var_121 = data == 121
    var_135 = data == 135
    var_154 = data == 154
    var_161 = data == 161
    var_163 = data == 163
    var_172 = data == 172
    var_174 = data == 174
    var_181 = data == 181
    var_182 = data == 182
    var_183 = data == 183
    var_195 = data == 195

    niveis = [
        3456, 2141, 930, 840, 875, 997, 940, 840, 1749, 2556, 2200, 3452, 1352, 1417, 930, 2248, 930,
        805, 1073, 740, 1042, 827, 915, 873, 799, 824, 710, 1865, 1489, 1124, 3456, 3456, 2141, 3063,
        1609, 840, 875, 875, 1353, 1897, 1061, 889, 884, 794,
    ]

    return pd.Series(np.select(
        [var_1, var_2, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_122, var_123, var_125, var_131, var_132, var_134, var_141, var_143, var_144,
        var_151, var_152, var_153, var_171, var_173, var_175, var_191, var_192, var_193, var_194, var_101, var_102, var_103, var_112, var_114,
        var_121, var_135, var_154, var_161, var_163, var_172, var_174, var_181, var_182, var_183, var_195,
        ],
        niveis,
        0
    ))


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

    return df_copy


def get_gender_data(df: pd.DataFrame) -> pd.DataFrame:
    gender_data = (
        df[['age_range', 'Gender', 'Course']]
        .groupby(['age_range', 'Gender'])
        .count()
    )
    gender_data = gender_data.unstack('Gender').droplevel(0, 'columns')
    return gender_data


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


def filter_dataset(df: pd.DataFrame, **filters) -> pd.DataFrame:
    df_copy = df.copy()
    fields_map = {
        'marital_status': 'Marital status',
        'course': 'Course',
        'gender': 'Gender',
        'age_range': 'age_range',
        'escolaridade': 'Escolaridade mae',
        'escolaridade': 'Escolaridade pai',
    }

    st.write(filters)

    query = ''
    for key in filters.keys():
        if key in fields_map and filters[key] != '':
            if len(query) > 0:
                query += ' and '

            query += f'`{fields_map[key]}` == "{filters[key]}"'
    st.write(query)
    return df_copy.query(query)
