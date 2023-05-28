#################################### CREATE queries ####################################

CREATE_USERS_TABLE = 'CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT,type TEXT first_name TEXT, last_name TEXT, country TEXT, city TEXT)'

CREATE_PETS_TABLE = 'CREATE TABLE IF NOT EXISTS pets (pet_id INTEGER PRIMARY KEY AUTOINCREMENT, owner_mail TEXT, pet_type TEXT, pet_name TEXT, pet_dob TEXT)'

CREATE_PET_TYPES_TABLE = 'CREATE TABLE IF NOT EXISTS pet_types (id INTEGER PRIMARY KEY,type_name TEXT)'

CREATE_PREDICTIONS_TYPES_TABLE = '''
CREATE TABLE IF NOT EXISTS predictions_types (
    pred_type_id SERIAL PRIMARY KEY,
    pred_type_name VARCHAR(255) NOT NULL
);
'''

CREATE_PREDICTIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS predictions (
  pred_id INTEGER PRIMARY KEY,
  owner_mail VARCHAR(255) REFERENCES users (email) ON DELETE CASCADE,
  pet_id INTEGER REFERENCES pets (pet_id) ON DELETE CASCADE,
  pred_type_id INTEGER REFERENCES predictions_types (pred_type_id),
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_PET_PREDICTION_TYPES = '''
CREATE TABLE IF NOT EXISTS pet_prediction_type (
    id INTEGER PRIMARY KEY,
    pet_type_id INTEGER REFERENCES pet_types(id),
    pred_type_id INTEGER REFERENCES predictions_types(pred_type_id),
    UNIQUE (pet_type_id, pred_type_id)
);

'''