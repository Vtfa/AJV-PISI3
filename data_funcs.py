import pandas as pd
import numpy as np


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

#perdão pela monstruosidade. -Vinicius
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