import json
import pandas as pd
from flask import current_app

def create_support_files(df_filtered):
    df_filtered = transform_matrix_symmetric_to_asymmetric(df_filtered)
    # obtiene los codigos de la primera columna
    global selected_codes
    selected_codes = df_filtered[df_filtered.columns[0]].apply(lambda row: row[0] if row else None).tolist()
    df_filtered_distances = df_filtered.applymap(get_distance_value_from_row)
    df_filtered_durations = df_filtered.applymap(get_duration_value_from_row)

    print(df_filtered_distances)
    print(df_filtered_durations)


def transform_matrix_symmetric_to_asymmetric(df):  # todo: is this correct?
    print(df.ubigeo.value_counts())
    return df


def get_distance_value_from_row(df):
    return df


def get_duration_value_from_row(df):
    return df


if __name__ == '__main__':

    with open(current_app.config['UPLOAD_FOLDER'] + "data.json", encoding="mbcs") as file:
        data = json.loads(file.read())
        df = pd.DataFrame.from_dict(data)
        print(df.shape)

    # print(df.head())
    print(df.columns)
    print(df.provincia.value_counts())
    # todo: categorias falta en la data aqui

    create_support_files(df[df["provincia"] == 'Santa'])
