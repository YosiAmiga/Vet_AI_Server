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

    # Insert the predefined pet types
    connection.execute(INSERT_CAT_TYPE)
    connection.execute(INSERT_DOG_TYPE)

    connection.commit()
    connection.close()

init_db()
