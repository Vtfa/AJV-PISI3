from enum import Enum


COR1 = "#FFA07A"
COR2 = "#98FB98"
COR3 = "#FF6961"
COR4 = "#87CEEB"
COR5 = "#DDA0DD"
COR6 = "#EF553B"
COR7 = "#636EFA"
COR8 = "#00CC96"

MALE_COLOR = "rgba(0, 204, 150, 0.5)"
FEMALE_COLOR = "rgba(99, 110, 250, 0.5)"

MODELS_DIR = './models'

# Enums
class Tabs_01(Enum):
    TABLE = 'table',
    PLOTS = 'plots',
    PROFILE = 'profile',

    def __str__(self):
        return f'{self.name}'

class Gender(str, Enum):
    Female = 'Feminino',
    Male = 'Masculino',

    def __str__(self):
        return f'{self.name}'

class Target(str, Enum):
    Graduate = 'Graduado',
    Enrolled = 'Retido',
    Dropout = 'Evadiu',

    def __str__(self):
        return f'{self.name}'