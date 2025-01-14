import sqlite3
from DB.SQL_scripts.db_scripts import *
import DB.SQL_scripts.queries.select_queries as select_queries
import DB.SQL_scripts.queries.create_queries as create_queries
import DB.SQL_scripts.queries.insert_queries as insert_queries
import DB.SQL_scripts.queries.analytics_queries as analytics_queries
DB_NAME = './DB/app_data.db'


def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    connection = get_db()
    # create the database tables if they do not exist
    connection.cursor().execute(create_queries.CREATE_USERS_TABLE)
    connection.cursor().execute(create_queries.CREATE_PETS_TABLE)
    connection.execute(create_queries.CREATE_PET_TYPES_TABLE)
    connection.execute(create_queries.CREATE_PREDICTIONS_TYPES_TABLE)
    connection.execute(create_queries.CREATE_PREDICTIONS_TABLE)

    # Insert the predefined pet types
    connection.execute(insert_queries.INSERT_CAT_TYPE)
    connection.execute(insert_queries.INSERT_DOG_TYPE)

    connection.commit()
    connection.close()


def insert_prediction(owner_mail, pet_id, prediction_id):
    return execute_query('insert_prediction', owner_mail, pet_id, prediction_id)


def get_pet_history_predictions(pet_id):
    predictions_by_pet_id_raw = execute_query('select_pet_predictions_history', pet_id)

    predictions_by_pet_id = []
    if predictions_by_pet_id_raw:
        for prediction in predictions_by_pet_id_raw:
            prediction_obj = {
                "pred_id": prediction[0],
                "owner_mail": prediction[1],
                "pred_type_name": prediction[2],
                "timestamp": prediction[3]
            }
            predictions_by_pet_id.append(prediction_obj)

    return predictions_by_pet_id


def get_pet_types():
    return execute_query('select_all_pet_types')


def get_user_pets(email):
    return execute_query('select_pets_by_owner_email', email)


def insert_pet(owner_email, pet_type, pet_name, pet_dob):
    return execute_query('insert_pet', owner_email, pet_type, pet_name, pet_dob)


def get_login(email):
    return execute_query_single_value('select_user_by_email_with_type', email)


def get_user(email):
    return execute_query_single_value('select_user_by_email', email)


def insert_user(email, password):
    return execute_query_single_value('insert_user', email, password)


def get_prediction_distribution(pet_id):
    return execute_query('prediction_distribution', pet_id)


def get_pet_prediction_types():
    return execute_query('select_pet_prediction_types')


def get_predictions_by_users():
    return execute_query('predictions_by_users')


def get_user_pet_count():
    return execute_query('user_pet_count')


def get_pet_types_count():
    return execute_query('pet_types_count')


def get_count_daily_predictions():
    return execute_query('count_daily_predictions')


def get_all_pets():
    return execute_query('select_all_pets')

def get_all_predictions():
    return execute_query('select_all_predictions')

def execute_query_single_value(query_name, *params):
    connection = get_db()
    cursor = connection.cursor()

    if query_name not in queries:
        raise ValueError(f'Invalid query name: {query_name}')

    query = queries[query_name]
    cursor.execute(query, params)
    result = cursor.fetchone()

    connection.commit()
    connection.close()

    return result


def execute_query(query_name, *params):
    connection = get_db()
    cursor = connection.cursor()

    if query_name not in queries:
        raise ValueError(f'Invalid query name: {query_name}')

    query = queries[query_name]
    cursor.execute(query, params)
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result
init_db()
