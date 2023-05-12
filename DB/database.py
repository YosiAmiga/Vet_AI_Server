import sqlite3

# from Analytics.pet_analytics import analysis_pandas
from DB.SQL_scripts.db_scripts import *
import pandas as pd

DB_NAME = './DB/app_data.db'
def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    connection = get_db()
    # create the database tables if they do not exist
    connection.cursor().execute(CREATE_USERS_TABLE)
    connection.cursor().execute(CREATE_PETS_TABLE)
    connection.execute(CREATE_PET_TYPES_TABLE)
    connection.execute(CREATE_PREDICTIONS_TYPES_TABLE)
    connection.execute(CREATE_PREDICTIONS_TABLE)

    # Insert the predefined pet types
    connection.execute(INSERT_CAT_TYPE)
    connection.execute(INSERT_DOG_TYPE)

    connection.commit()
    connection.close()

def insert_prediction(owner_mail, pet_id, prediction_id):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(INSERT_PREDICTION, (owner_mail, pet_id, prediction_id))
    connection.commit()
    connection.close()

def get_pet_history_predictions(pet_id):
    df = pd.DataFrame(columns=['pred_id', 'owner_mail', 'pred_type_name','timestamp'])
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(SELECT_PET_PREDICTIONS_HISTORY, (pet_id,))
    connection.commit()
    predictions_by_pet_id_raw = cursor.fetchall()
    connection.close()
    predictions_by_pet_id = []
    for prediction in predictions_by_pet_id_raw:
        prediction_obj = {
            "pred_id": prediction[0],
            "owner_mail": prediction[1],
            "pred_type_name": prediction[2],
            "timestamp": prediction[3]
        }
        predictions_by_pet_id.append(prediction_obj)
        df = df.append(prediction_obj, ignore_index=True)
    # print(f"This is the prediction data: \n {predictions_by_pet_id}")

    return predictions_by_pet_id,df

def get_pets_data():
    df = pd.DataFrame(columns=['pet_id', 'owner_mail', 'pet_type','pet_name','pet_dob'])
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(SELECT_ALL_PET_TABLE)
    connection.commit()
    table = cursor.fetchall()
    connection.close()
    table_lines_as_dicts = []
    for sample in table:
        sample_as_dict = {
            "pet_id": sample[0],
            "owner_mail": sample[1],
            "pet_type": sample[2],
            "pet_name": sample[3],
            "pet_dob": sample[4]
        }
        table_lines_as_dicts.append(sample_as_dict)
        df = df.append(sample_as_dict, ignore_index=True)
    # print(f"This is the prediction data: \n {predictions_by_pet_id}")

    return table_lines_as_dicts,df

def get_users_data():
    user_table_columns = ['email', 'password', 'type','first_name','last_name','country','city']
    df = pd.DataFrame(columns=['email', 'password', 'type','first_name','last_name','country','city'])
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(SELECT_ALL_USERS_TABLE)
    connection.commit()
    table = cursor.fetchall()
    connection.close()
    table_lines_as_dicts = []
    for sample in table:
        sample_as_dict = {
            f"{user_table_columns[0]}": sample[0],
            f"{user_table_columns[1]}": sample[1],
            f"{user_table_columns[2]}": sample[2],
            f"{user_table_columns[3]}": sample[3],
            f"{user_table_columns[4]}": sample[4]
        }
        table_lines_as_dicts.append(sample_as_dict)
        df = df.append(sample_as_dict, ignore_index=True)
    # print(f"This is the prediction data: \n {predictions_by_pet_id}")

    return df










init_db()
