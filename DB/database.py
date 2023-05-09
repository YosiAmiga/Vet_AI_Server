import sqlite3
from DB.SQL_scripts.db_scripts import *

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

    return predictions_by_pet_id



init_db()
