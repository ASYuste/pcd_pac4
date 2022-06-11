"""
Exercicis amb resultats de la PAC4 de Programació per a la ciència de dades
Curs 2021/22

Autor: Albert Salvador Yuste
última modificació: 2022/06/11
"""
# !/usr/bin/ python
# -*- coding: utf-8 -*-


import os
import math
from statistics import mean
from pprint import pprint
import itertools
import matplotlib.pyplot as plt
import pandas as pd


def read_add_year_gender(filepath: str, gender: str, year: int) -> pd.DataFrame:
    """
    Dona't un 'filepath' amb la ruta de l'arxiu que es vol llegir, aquest es
    llegeix i s'hi afegeixen dues columnes corresponents al génere 'gender'
    i l'any 'year' corresponents.

    :param filepath: string amb la ruta de l’arxiu que volem llegir
    :param gender: 'M' o 'F' (segons les sigles de “Male” or “Female”)
    :param year: Any al que corresponen les dades en format YYYY
    :return: dataframe resultant
    """
    if not os.path.isfile(filepath):
        raise TypeError("Arxiu no trobat")
    if not isinstance(year, int):
        raise TypeError("Any en valor numèric")
    if not 2016 <= year <= 2022:
        raise TypeError("Anys entre 2016 i 2022")
    if gender not in ['M', 'F']:
        raise TypeError("Gèneres acceptats: 'M'/'F'")

    arxiu: pd.DataFrame = pd.read_csv(filepath, low_memory=False)
    arxiu['gender'] = gender
    arxiu['year'] = year
    return arxiu


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """
    Dona't el path d'una carpeta on tenim les dades d'interès,
    es seleccionen els arxius de l'any 'year' introduït d'ambdós
    géneres acceptats ('Male' i 'Female') i es carreguen en
    un sol dataframe.

    Un cop seleccionats l'any i el gènere es fa una crida a la
    funció read_add_year_gender() per generar el dataframe i,
    posteriorment, unir-los en un de sol.

    :param path: ruta a la carpeta que conté les dades
    :param year: Any al que corresponen les dades en format YYYY
    :return: dataframe resultant
    """
    if not os.path.isdir(path):
        raise TypeError("El nom del directori no existeix")
    if not isinstance(year, int):
        raise TypeError("Any en valor numèric")
    if not 2016 <= year <= 2022:
        raise TypeError("Anys entre 2016 i 2022")

    # Extreiem els dos últims dígits de l'any
    year_last: int = year % 100

    genders: list = ['M', 'F']
    arxiu = []
    for gender in genders:
        ini_file: str = ""
        if gender == "F":
            ini_file: str = "female_"
        file_name: str = "{}players_{}.csv".format(ini_file, year_last)
        file_dir: str = os.path.join(path, file_name)
        arxiu.append(read_add_year_gender(file_dir, gender, year))
    arxiu = pd.concat(arxiu)
    return arxiu


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """
    Dona't el path d'una carpeta on tenim les dades d'interès,
    es seleccionen els arxius de tots els anys 'years' introduïts
    d'ambdós géneres acceptats ('Male' i 'Female') i es carreguen en
    un sol dataframe.

    Un cop seleccionats els anys i el gènere es fa una crida a la
    funció join_male_female() per generar el dataframe i,
    posteriorment, unir-los en un de sol.
    :param path: ruta a la carpeta que conté les dades
    :param years: llista d'anys al que corresponen les dades en format YYYY
    :return: dataframe resultant
    """
    arxiu = []
    if not isinstance(years, list):
        raise TypeError("Introduir una llista d'anys")
    for year in years:
        arxiu.append(join_male_female(path, year))
    arxiu = pd.concat(arxiu)
    return arxiu


def find_max_col(df_max: pd.DataFrame, filter_col: str,
                 cols_to_return: list) -> pd.DataFrame:
    """
    Dona't un dataframe 'df_max' i una columna numèrica 'filter_col',
    es retorna un dataframe dels registres on el seu valor és màxim,
    només amb les columnes indicades a 'cols_to_return'.

    :param df_max: dataframe que conté les dades
    :param filter_col: nom de la columna de la que volem saber el màxim
    :param cols_to_return: llista de columnes que cal retornar
    :return: dataframe resultant
    """
    # Comprobem que les cols_to_return estan dins del df
    if not all(col in df_max.columns for col in cols_to_return):
        raise TypeError("Les columnes de retorn no són correctes")

    # Volem saber quines columnes són numèriques
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    col_num = df_max.select_dtypes(include=numerics).columns.tolist()

    if filter_col not in col_num:
        raise TypeError("La columna 'filter_col' no és numèrica")
    max_value = df_max[filter_col].max()
    result = df_max[cols_to_return][df_max[filter_col] == max_value]
    return result


def find_rows_query(df_rows: pd.DataFrame, query: tuple,
                    cols_to_return: list) -> pd.DataFrame:
    """
    Dona't un dataframe 'df_rows' i una tupla 'query' es filtren
    els registres que compleixin les condicions de la tupla.

    Un exemple de 'query' és el següent:
    ([“league_name”, “weight_kg”], [“English Premier League”, (60, 70)])

    On en el primer element de la tupla es presenta una llista dels
    atributs a ser filtrats, i el segon valor presenta una llista de valors
    que s'inclouen en el filtre. Si la columna és categòrica, el valor serà
    un string. Si és numèrica, serà una tupla amb el valor mínim i màxim
    (ambdós inclosos). Finalment es tornen les columnes indicades per
    'cols_to_return'.

    :param df_rows: dataframe que conté les dades
    :param query: tupla que conté la query
    :param cols_to_return: llista de columnes que cal retornar
    :return: dataframe resultant
    """
    # Comprobem que les cols_to_return estan dins del df
    if not all(col in df_rows.columns for col in cols_to_return):
        raise TypeError("Les columnes de retorn no són correctes")

    # Volem saber quines columnes són numèriques
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    col_num = df_rows.select_dtypes(include=numerics).columns.tolist()

    # Interessa passar d'una tupla de llistes a una llista de tuples
    # per poder realitzar les comparatives adients
    query = list(zip(query[0], query[1]))
    for cols, vals in query:
        if cols not in df_rows.columns:
            raise TypeError("Columna '{}' no inclosa en df".format(cols))
        if cols in col_num:  # Columna numèrica
            if isinstance(vals, tuple) and len(vals) == 2:
                df_rows = df_rows[df_rows[cols].between(vals[0], vals[1], "both")]
            else:
                raise TypeError("El nombre de valors del rang per la "
                                "columna '{}' no és l'adient".format(cols))
        else:  # Columna categòrica
            df_rows = df_rows[df_rows[cols] == vals]
    return df_rows[cols_to_return]


def calculate_bmi(df_bmi: pd.DataFrame, gender: str, year: int,
                  cols_to_return: list) -> pd.DataFrame:
    """
    Dona't un dataframe 'df_bmi', es seleccionen els registres amb
    gènere 'gender' i any 'year' en les respectives columnes i s'afegeix
    al dataframe original una columna amb el valor calculat d'índex de massa
    corporal (BMI).

    Aquest es calcula amb la següent expressió:

            BMI = pes / alçada²

    on pes en kg i alçada en metres. Finalment el paràmetre 'cols_to_return'
    indica quines columnes presenta el dataframe resultant, a part de la
    nova columna 'BMI'.

    :param df_bmi: dataframe que conté les dades
    :param gender: gènere que volem estudiar
    :param year: Any que volem consultar en format YYYY
    :param cols_to_return: llista de columnes que cal retornar ('BMI' no inclòs)
    :return: dataframe resultant
    """
    gender = gender.upper()
    if gender not in ["M", "F"]:
        raise TypeError("Sexes acceptats: M/F")

    if not isinstance(year, int):
        raise TypeError("Any en valor numèric")
    if not 2016 <= year <= 2022:
        raise TypeError("Anys entre 2016 i 2022")

    # Comprobem que les cols_to_return estan dins del df
    if not all(col in df_bmi.columns for col in cols_to_return):
        raise TypeError("Les columnes de retorn no són correctes")

    df_bmi = df_bmi[(df_bmi['gender'] == gender) & (df_bmi['year'] == year)].copy()
    if len(df_bmi) == 0:
        raise TypeError("No s'han trobat registres amb el gènere i "
                        "any indicats")

    df_bmi['BMI'] = df_bmi['weight_kg'] / ((df_bmi['height_cm'] / 100) *
                                           (df_bmi['height_cm'] / 100))
    cols_to_return.append('BMI')
    return df_bmi[cols_to_return]


def players_dict(df_dict: pd.DataFrame, ids: list, cols: list) -> dict:
    """
    Dona't un dataframe 'df_dict' i uns identificadors sofifa_id 'ids',
    es genera un diccionari amb clau els identificadors 'ids' i com a
    valors un nou diccionari amb els valors de les columnes 'cols'.
    Aquets valors apareixeran tantes vegades com vegades apareguin a
    'df_dict' corresponent a cada jugador, és a dir, una vegada per any.

    :param df_dict: dataframe que conté les dades
    :param ids: llista d’iidentificador “sofifa_id”
    :param cols: llista de columnes de les que volem informació
    :return: diccionari resultant
    """
    if 'sofifa_id' in cols:
        cols.remove('sofifa_id')
    # Comprobem que les cols estan dins del df
    if not all(col in df_dict.columns for col in cols):
        raise TypeError("Les columnes de retorn no són correctes")

    df_filt: pd.DataFrame = df_dict[df_dict['sofifa_id'].isin(ids)]

    # Inspirat en la següent resposta de stackoverflow:
    # https://stackoverflow.com/a/24370510
    df_dict: dict = {k: g[cols].to_dict('list') for k, g in df_filt.groupby('sofifa_id')}
    return df_dict


def clean_up_players_dict(player_dict: dict, col_query: list) -> dict:
    """
    Dona't un diccionari 'player_dict', es recorren totes les claus i,
    segons el filtre indicat a la tupla 'col_query', es modifica el diccionari
    original.

    Un exemple de 'col_query' és el següent:
    [("player_positions","del_rep"), ("short_name","one")]

    On cada element presenta una llista de dos elements. El primer indica la columna
    a tractar i el segon el tractament que s'hi ha d'aplicar. Aquest segon element
    pot ser 'one', indicant que ens quedem només amb el primer valor, o 'del_rep',
    indicant que ens quedem amb valors únics no repetits després d'una descomposició
    dels valors que s'hi inclouen. Si una columna no apareix no se li aplica
    cap tractament.

    :param player_dict: diccionari amb el format resultant de players_dict()
    :param col_query: llista de tuples amb detalls sobre la informació que cal simplificar
    :return: diccionari resultant del tractament
    """
    for key in player_dict.keys():
        for cols, vals in col_query:
            if vals == 'one':
                player_dict[key][cols] = player_dict[key][cols][0]
            elif vals == 'del_rep':
                li_vals = []
                if all(isinstance(n, str) for n in player_dict[key][cols]):
                    for value in player_dict[key][cols]:
                        li_vals.append(value.split(","))
                    player_dict[key][cols] = list(set([x.strip() for x1 in li_vals for x in x1]))
                else:
                    player_dict[key][cols] = list(set(player_dict[key][cols]))
            else:
                raise TypeError("Filtre no acceptat: 'one'/'del_rep'")
    return player_dict


def top_average_column(data: dict, identifier: str, col: str, threshold: int) -> list:
    """
    Dona't un diccionari 'data' ja tractat per la funció clean_up_players_dict(), es
    calcula el valor mitjà de la característica 'col' si es disponen de 'treshold' o més
    vegades valors a calcular. 'identifier' indica la columna que s'utilitzarà com a
    identificador.

    Es retornarà una llista amb el 'identifier', el valor mitjà calculat, i un
    diccionari amb els valors de la columna 'col' i a quins anys pertanyen. Com exemple,
    si 'identifier'='short_name' i 'col'='shooting', un possible element de la llista
    podria ser:
        ('L. Schelin', 85.0, {'value': [87.0, 84.0, 84.0], 'year': [2016, 2017, 2018]})

    Els elements de la llista s'ordenaran pel valor mitjà calculat.

    :param data: diccionari “net” que conté la informació de diversos sofifa_id
    :param identifier: columna/clau que es farà servir com identificador
    :param col: nom d’una columna/clau numérica
    :param threshold: mínim número de dades necessàries
    :return: llista resultant
    """
    if not isinstance(data, dict):
        raise TypeError("'data' no és un diccionari")
    if not isinstance(col, str):
        raise TypeError("'col' no és un string")
    if not isinstance(threshold, int):
        raise TypeError("'threshold' no és un enter")

    list_result = []
    for key in data.keys():
        if not all(isinstance(n, (int, float)) for n in data[key][col]):
            raise TypeError("{} no és una columna numèrica".format(col))
        if ((len(data[key][col]) < threshold) |
                (any([math.isnan(n) for n in data[key][col]]))):
            continue
        val_mitja = mean(data[key][col])
        tuple_result = (data[key][identifier], val_mitja,
                        {'value': data[key][col],
                         'year': data[key]['year']})
        list_result.append(tuple_result)

    list_result.sort(key=lambda x: x[1], reverse=True)
    return list_result


# Dues funcions creades per a l'exercici 6:
# Retornar dataframes amb més columnes
pd.set_option('display.expand_frame_repr', False)


def calculate_characteristics(df_players: pd.DataFrame) -> list:
    """
    Dona't un dataframe 'df' de jugadors/es segons la seva posició en calcula les
    característiques mitjanes més altes per caracteritzar les possibles
    característiques pròpies d'una posició concreta.

    Un cop definides les característiques, en sumem les respectives valoracions
    amb una 'puntuacio' global del/de la jugador/a. Després s'ordenen tots per
    ordre descendent d'aquesta 'puntuacio'.

    Finalment, es creen tres dataframes més en què filtrem els jugadors veterans,
    els masculins i els femenins. S'ha decidit que un/a jugador/a no pot estar
    en més d'un equip. Per exemple: Un jugador masculí de 32 estarà a l'equip
    de veterans, però no al masculí.

    La funció retorna una llista amb els següents dataframes:
    · dataframe original amb una columna de 'puntuacio' i ordenada per aquesta última
    · dataframe de jugadors i jugadores veterans/es
    · dataframe de jugadors masculins
    · dataframe de jugadores femenines

    :param df_players:
        df (pd.DataFrame): df de jugadors d'una posició
    :return:
        (list): llista de dataframes
    """
    # Càlcul mitjanes
    df_median: object = df_players.median(numeric_only=True).sort_values(ascending=False).head(5)
    # Característiques criteri
    df_crit: list = list(df_median.index)
    # Dataframe puntuacio, els sumem i ordenem
    df_punt: pd.DataFrame = df_players.copy()
    df_punt['puntuacio'] = df_players[df_crit].sum(axis=1)
    df_punt = df_punt.sort_values(by='puntuacio', ascending=False)
    # Dataframe veterans
    df_vet = df_punt[df_punt['age'] >= 30]
    # Dataframe masculí
    df_punt_m = df_punt[(df_punt['gender'] == 'M') & (df_punt['age'] < 30)]
    # Dataframe femení
    df_punt_f = df_punt[(df_punt['gender'] == 'F') & (df_punt['age'] < 30)]
    return [df_punt, df_vet.head(50), df_punt_m.head(50), df_punt_f.head(50), df_crit]


def create_teams(cm_df: pd.DataFrame, rb_df: pd.DataFrame,
                 lb_df: pd.DataFrame) -> pd.DataFrame:
    """
    Dona't tres dataframes (cm, rb i lb), corresponents a jugadors diferents posicions,
    es creen totes les possibles combinacions de línies de defensa sense repeticions.

    Els equips es valoraran segons la suma de la variable 'puntuacio' dels 4 jugadors
    de la línia defensiva proposta. Després es presentaran valors d'atac, defensa i
    possessió (els dos primers diferenciats en dreta, esquerra i centre).

    ·Atac: es valoraran les característiques 'pace' i 'shooting'
    ·Defensa: es valoraran les característiques 'defending' i 'physic'
    ·Possessió: es valoraran les característiques 'passing' i 'dribbling'

    Finalment es retorna un dataframe amb les diferents combinacions d'equips, juntament
    amb les puntuacions i valoracions dels diferents valors esmentats.

    :param cm_df: dataframe de jugadors de posició 'CM'
    :param rb_df: dataframe de jugadors de posició 'RB'
    :param lb_df: dataframe de jugadors de posició 'LB'
    :return: dataframe amb les combinacions d'equips i puntuacions
    """
    # Obtenim els noms de tots els jugadors
    names = list(cm_df['short_name']) + list(rb_df['short_name']) + list(lb_df['short_name'])
    # Creem totes les combinacions d'equips amb els noms i el convertim a dataframe
    equips = list(itertools.combinations(names, 4))
    equips = pd.DataFrame(equips, columns=['cm_1', 'cm_2', 'rb', 'lb'])
    # Filtrem les files en què un nom no pertany a la posició que li correspon
    equips = equips[(equips['cm_1'].isin(CM_ALL['short_name'])) &
                    (equips['cm_2'].isin(CM_ALL['short_name'])) &
                    (equips['rb'].isin(RB_ALL['short_name'])) &
                    (equips['lb'].isin(LB_ALL['short_name']))]
    # Degut a que un jugador pot estar en més d'un grup, és possible que hi hagi
    # combinacions repetides. Ens quedem només amb una d'elles:
    equips = equips.drop_duplicates(keep='first')
    # Les columnes amb puntuacions que volem observar
    puntuacions = ['puntuacio', 'atac_dreta', 'atac_centre', 'atac_esquerra',
                   'possessio', 'defensa_dreta', 'defensa_centre', 'defensa_esquerra']

    for col in puntuacions:
        # Atac (valorem 'pace' i 'shooting')
        if col == 'atac_dreta':
            equips[col] = 0
            for caract in ['pace', 'shooting']:
                dict_rb = pd.Series(RB_ALL[caract].values, index=RB_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['rb'].map(dict_rb)
        if col == 'atac_centre':
            equips[col] = 0
            for caract in ['pace', 'shooting']:
                dict_cm = pd.Series(CM_ALL[caract].values, index=CM_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['cm_1'].map(dict_cm) + \
                    equips['cm_2'].map(dict_cm)
        if col == 'atac_esquerra':
            equips[col] = 0
            for caract in ['pace', 'shooting']:
                dict_lb = pd.Series(LB_ALL[caract].values, index=LB_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['lb'].map(dict_lb)
        # Defensa (valorem 'defending' i 'physic')
        if col == 'defensa_dreta':
            equips[col] = 0
            for caract in ['defending', 'physic']:
                dict_rb = pd.Series(RB_ALL[caract].values, index=RB_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['rb'].map(dict_rb)
        if col == 'defensa_centre':
            equips[col] = 0
            for caract in ['defending', 'physic']:
                dict_cm = pd.Series(CM_ALL[caract].values, index=CM_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['cm_1'].map(dict_cm) +\
                    equips['cm_2'].map(dict_cm)
        if col == 'defensa_esquerra':
            equips[col] = 0
            for caract in ['defending', 'physic']:
                dict_lb = pd.Series(LB_ALL[caract].values, index=LB_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['lb'].map(dict_lb)

        # Possessió (valorem 'passing' i 'dribbling')
        if col == 'possessio':
            equips[col] = 0
            for caract in ['passing', 'dribbling']:
                dict_cm = pd.Series(CM_ALL[caract].values, index=CM_ALL.short_name).to_dict()
                dict_rb = pd.Series(RB_ALL[caract].values, index=RB_ALL.short_name).to_dict()
                dict_lb = pd.Series(LB_ALL[caract].values, index=LB_ALL.short_name).to_dict()
                equips[col] = equips[col] + equips['cm_1'].map(dict_cm) +\
                    equips['cm_2'].map(dict_cm) + equips['rb'].map(dict_rb) +\
                    equips['lb'].map(dict_lb)
        # Puntuació
        if col == 'puntuacio':
            # Creem diccionaris per cada jugador amb la valoració de la categoria 'col'
            dict_cm = pd.Series(CM_ALL[col].values, index=CM_ALL.short_name).to_dict()
            dict_rb = pd.Series(RB_ALL[col].values, index=RB_ALL.short_name).to_dict()
            dict_lb = pd.Series(LB_ALL[col].values, index=LB_ALL.short_name).to_dict()
            equips[col] = equips['cm_1'].map(dict_cm) + equips['cm_2'].map(dict_cm) + \
                equips['rb'].map(dict_rb) + equips['lb'].map(dict_lb)

    equips = equips.sort_values(by='puntuacio', ascending=False)
    return equips


if __name__ == "__main__":
    print('')
    print('Exercici 2.c:')
    print('')

    DF = join_datasets_year("data", list(range(2016, 2023)))
    COLS_TO_RETURN = ["short_name", "year", "age", "overall", "potential"]

    print('Els jugadors de nacionalitat belga menors de 25 anys '
          'màxim "potential" al futbol masculí:')
    QUERY = (['nationality_name', 'age'], ['Belgium', (0, 24)])
    print('')
    print(find_max_col(
        find_rows_query(DF, QUERY, COLS_TO_RETURN),
        "potential", COLS_TO_RETURN))
    print('')

    print('Les porteres majors de 28 anys amb "overall" superior '
          'a 85 al futbol femení:')
    QUERY = (["player_positions", "age", "overall", "gender"],
             ["GK", (28, 100), (85, 100), "F"])
    print('')
    print(find_rows_query(DF, QUERY, COLS_TO_RETURN))
    print('')
    print('#######################################################')

    print('')
    print('Exercici 3.b:')
    print('')

    # Obtenim un dataframe general, tant d'homes com dones, per l'any 2022
    DF = join_datasets_year("data", [2022])

    # Utilitzant la funció calculate_bmi() obtenim el BMI per a cada jugador
    BMI = calculate_bmi(DF, "M", 2022, ['club_flag_url'])

    # Identifiquem el país de cada jugador a partir de la següent expressió
    BMI['country'] = BMI['club_flag_url'].str.split("/").str[-1].str[:2]

    # Obtenim el valor màxim de BMI per país
    BMI_MAX = BMI.groupby('country')['BMI'].max().reset_index()

    # Grafiquem els resultats
    plt.rcParams["figure.figsize"] = (20, 10)
    plt.bar(BMI_MAX['country'], BMI_MAX['BMI'])
    plt.xticks(rotation=90)
    plt.ylabel("BMI")
    for i in [18.5, 25, 30]:
        plt.axhline(y=i, color='r', linestyle='--')
    plt.text(1, 15, "Underweight", fontsize=15, color='white',
             bbox=dict(facecolor='r', alpha=0.7))
    plt.text(1, 22, "Normal weight", fontsize=15, color='white',
             bbox=dict(facecolor='r', alpha=0.7))
    plt.text(1, 27.5, "Overweight", fontsize=15, color='white',
             bbox=dict(facecolor='r', alpha=0.7))
    plt.text(1, 32, "Obese", fontsize=15, color='white',
             bbox=dict(facecolor='r', alpha=0.7))
    PATH_IMG = os.path.join("result", "pac4_ex3b.png")
    plt.savefig(PATH_IMG)
    plt.show()
    print("La figura també es pot observar a {}".format(PATH_IMG))

    # Tal i com s'observa a la figura pac4_ex3b.png, els valors màxims de BMI per país es troben
    # majoritàriament en el rang de "Overweight". Els únic casos diferents són Xipre
    # ("Normal Weight") i Gran Bretanya i Estats Units ("Obese").

    # Tot i que es podria esperar que la majoria de jugadors es trobessin en el rang
    # "Normal Weight", hem de tenir present dos aspectes: com que estem considerant el cas
    # màxim per país, amb què tan sols un jugador es trobi amb una situació de sobrepès ja
    # "contamina" els valors màxims de BMI, per lo que poden tractar-se de valors esperats.
    # El segon punt és que es tracta d'esportistes d'elit, per lo que la seva massa muscular
    # general pot ser superior a les persones 'normals', augmentant-ne l'index BMI.

    print('')
    print('#######################################################')

    print('')
    print('Exercici 3.c:')
    print('')

    # Players
    DF = join_datasets_year("data", [2022])
    DF['country'] = DF['club_flag_url'].str.split("/").str[-1].str[:2]

    # Observem alguns estadístics de l'edat dels jugadors masculins
    # print(df['age'][(df['gender'] == 'M') & (df['country'] == 'es')].describe())

    # Se n'extreu que el rang interquartil està entre 22 i 29 anys,
    # per lo que s'intentarà abordar aquestes edats en la comparativa

    # Utilitzant la funció calculate_bmi() obtenim el BMI per a cada jugador
    BMI = calculate_bmi(DF, "M", 2022, ['club_flag_url'])

    # Identifiquem el país de cada jugador a partir de la següent expressió
    BMI['country'] = BMI['club_flag_url'].str.split("/").str[-1].str[:2]

    # Seleccionem els jugadors que juguen a Espanya ('es'):
    BMI = BMI[BMI['country'] == 'es'].copy()

    BMI['group'] = pd.cut(BMI['BMI'], bins=[0, 18.5, 20, 25, 30], include_lowest=True,
                          labels=['Underweight', 'Normal weight', 'Overweight', 'Obesity'])

    BMI_GROUP = BMI.groupby('group')['BMI'].count().reset_index()
    BMI_GROUP['% players'] = 100 * BMI_GROUP['BMI'] / BMI_GROUP['BMI'].sum()

    # INE
    # Un cop realitzada la consulta, n'extreiem els valors d'interès:

    INE = pd.read_csv(os.path.join("data","01001bsc.csv"), sep=";", thousands=",")

    INE_GROUP = INE.groupby('Adult body mass index')['Total'].sum().reset_index()
    INE_GROUP['group'] = INE_GROUP['Adult body mass index'].str.split("(").str[0].str[:-1]

    FINAL_COLS = ['group', '% people']

    INE_GROUP['% people'] = 100 * INE_GROUP['Total'] / INE_GROUP['Total'].sum()

    # INE vs Players
    BMI_FULL = pd.merge(INE_GROUP, BMI_GROUP, how='inner', on='group')

    plt.rcParams["figure.figsize"] = (20, 10)
    plt.bar(BMI_FULL['group'], BMI_FULL['% people'], alpha=0.7,
            label="Men from 18 to 34 years old")
    plt.bar(BMI_FULL['group'], BMI_FULL['% players'], alpha=0.7,
            label="Men Players")
    plt.xticks(rotation=90)
    plt.ylabel("%")
    plt.legend()
    PATH_IMG = os.path.join("result", "pac4_ex3c.png")
    plt.savefig(PATH_IMG)
    plt.show()
    print("La figura també es pot observar a {}".format(PATH_IMG))

    # S'observa com, a diferència de les persones normals, la gran
    # majoria de jugadors es troben al grup de sobrepès 'Overweight'.
    # Això possiblement és degut a la seva diferent tonificació
    # muscular, molt més enfortida que la població general. Aquest
    # fet provoca que l'índex BMI es vegi augmentat.

    print('')
    print('#######################################################')

    print('')
    print('Exercici 4.c:')
    print('')

    DF = join_datasets_year("data", [2016, 2017, 2018])

    COLS = ['short_name', 'overall', 'potential', 'player_positions', 'year']
    IDS = [226328, 192476, 230566]

    PLAYER_DICT = players_dict(DF, IDS, COLS)

    print("Diccionari apartat 4a:")
    print('')
    pprint(PLAYER_DICT)
    print('')

    COL_QUERY = [("player_positions", "del_rep"), ("short_name", "one")]

    print("Query:")
    print('')
    print(COL_QUERY)
    print('')

    CLEAN_DICT = clean_up_players_dict(PLAYER_DICT, COL_QUERY)

    print("Diccionari net:")
    print('')
    pprint(CLEAN_DICT)
    print('')
    print('#######################################################')

    print('')
    print('Exercici 5.b:')
    print('')

    # data #
    # Obtenim totes les dades necessàries fins ara
    DF = join_datasets_year("data", list(range(2016, 2023)))
    # Utilitzarem TOTS els ids que tenim
    IDS = list(set(DF['sofifa_id']))
    print("S'estan analitzant {} jugadors/es, pot demorar-se una mica...".format(len(IDS)))
    print("")
    COLS = ['short_name', 'year', 'movement_sprint_speed']
    PLAYER_DICT = players_dict(DF, IDS, COLS)
    COL_QUERY = [("short_name", "one")]
    DATA = clean_up_players_dict(PLAYER_DICT, COL_QUERY)
    # Indiquem threshold = 7 per tenir en compte tots els
    # anys (2016 - 2022)
    THRESHOLD = 7
    COL = 'movement_sprint_speed'
    IDENTIFIER = 'short_name'

    # function
    RESULT = top_average_column(DATA, IDENTIFIER, COL, THRESHOLD)
    print("TOP 4 millors futbolistes segons {}:".format(COL))
    print("")
    pprint(RESULT[:4])
    print("")

    # plot
    TOP_4 = RESULT[:4]

    plt.rcParams["figure.figsize"] = (15, 10)
    for i, top_value in enumerate(TOP_4):
        plt.plot(
            TOP_4[i][2]['year'],
            TOP_4[i][2]['value'],
            label=TOP_4[i][0]
        )
    plt.ylabel("Movement Sprint Speed")
    plt.xlabel("Any")
    plt.legend()
    PATH_IMG = os.path.join("result", "pac4_ex5b.png")
    plt.savefig(PATH_IMG)
    plt.show()
    print("La figura també es pot observar a {}".format(PATH_IMG))
    print('')
    print('#######################################################')

    print('')
    print('Exercici 6:')
    print('')

    # Any d'estudi
    ANY_ESTUDI = 2022

    # Obtenció registres per pantalla
    NUM_REGISTRES = 10

    # Obtenim les dades de jugadors
    print('Carregant dades...')
    DF = join_male_female("data", ANY_ESTUDI)
    print('Dades carregades')
    print('')

    # Seleccionem quines columnes volem analitzar i en filtrem el dataframe
    NUMBER_COLUMNS = [2, 4, 9, 28, 29, *range(37, 78)]
    DF_COLUMNS = list(DF.columns[i] for i in NUMBER_COLUMNS)
    DF_COLUMNS.append('gender')
    DF_FILT = DF[DF_COLUMNS]

    # Agrupem els jugadors segons la seva posició. Poden estar en més d'un grup
    CM_PLAYERS = DF_FILT[DF_FILT['player_positions'].str.contains("CM")]
    RB_PLAYERS = DF_FILT[DF_FILT['player_positions'].str.contains("RB")]
    LB_PLAYERS = DF_FILT[DF_FILT['player_positions'].str.contains("LB")]

    print("Classificant jugadors per posicions i categoria...")
    CM_ALL, CM_VET, CM_M, CM_F, CM_CRIT = calculate_characteristics(CM_PLAYERS)
    RB_ALL, RB_VET, RB_M, RB_F, RB_CRIT = calculate_characteristics(RB_PLAYERS)
    LB_ALL, LB_VET, LB_M, LB_F, LB_CRIT = calculate_characteristics(LB_PLAYERS)
    print('Posició "CM" caracteritzada per:')
    print(CM_CRIT)
    print('Posició "RB" caracteritzada per:')
    print(RB_CRIT)
    print('Posició "LB" caracteritzada per:')
    print(LB_CRIT)
    print("Jugadors classificats")
    print('')

    print("Creant combinacions d'equips...")
    EQUIP_M = create_teams(CM_M, RB_M, LB_M)
    print('Equips masculins creats')
    EQUIP_F = create_teams(CM_F, RB_F, LB_F)
    print('Equips femenins creats')
    EQUIP_VET = create_teams(CM_VET, RB_VET, LB_VET)
    print('Equips de veterans creats')
    print('Tots els equips creats')

    print('')
    print('TOP{} equips masculins:'.format(NUM_REGISTRES))
    print(EQUIP_M.head(NUM_REGISTRES))
    print('')
    print('TOP{} equips femenins:'.format(NUM_REGISTRES))
    print(EQUIP_F.head(NUM_REGISTRES))
    print('')
    print('TOP{} equips veterans:'.format(NUM_REGISTRES))
    print(EQUIP_VET.head(NUM_REGISTRES))

    print('')
    print('#######################################################')
