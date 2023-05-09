#################################### CREATE functions ####################################

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
#################################### SELECT functions ####################################

SELECT_USER_BY_EMAIL_WITH_TYPE = 'SELECT email, password, type FROM users WHERE email = ?'

SELECT_USER_BY_EMAIL = 'SELECT * FROM users WHERE email=?'

SELECT_PETS_BY_OWNER_EMAIL = 'SELECT * FROM pets WHERE owner_mail=?'

SELECT_PET_BY_ID_AND_OWNER_EMAIL = 'SELECT * FROM pets WHERE pet_id=? AND owner_mail=?'

SELECT_ALL_PET_TYPES = 'SELECT type_name FROM pet_types'

SELECT_PET_PREDICTIONS_HISTORY = '''
SELECT pred_id,
       owner_mail,
       predictions_types.pred_type_name,
       timestamp
  FROM predictions,predictions_types
  WHERE pet_id = ? AND predictions_types.pred_type_id = predictions.pred_type_id
  '''

#################################### INSERT functions ####################################

INSERT_USER_WITH_TYPE = 'INSERT INTO users (email, password, user_type, first_name, last_name, country, city)) VALUES (?, ?, ?, ?, ?, ?, ?)'

INSERT_USER_ALL_DATA = 'INSERT INTO users (email, password, first_name, last_name, country, city) VALUES (?, ?, ?, ?, ?, ?)'

INSERT_USER = 'INSERT INTO users (email, password) VALUES (?, ?)'

INSERT_PET = 'INSERT INTO pets (owner_mail, pet_type, pet_name, pet_dob) VALUES (?, ?, ?, ?)'

INSERT_CAT_TYPE = '''
INSERT INTO pet_types (id, type_name)
SELECT 1, 'Cat'
WHERE NOT EXISTS (SELECT id FROM pet_types WHERE id = 1 AND type_name = 'Cat')
'''

INSERT_DOG_TYPE = '''
INSERT INTO pet_types (id, type_name)
SELECT 2, 'Dog'
WHERE NOT EXISTS (SELECT id FROM pet_types WHERE id = 2 AND type_name = 'Dog')
'''

INSERT_PREDICTION = 'INSERT INTO predictions (owner_mail, pet_id, pred_type_id) VALUES (?, ?, ?)'

INSERT_VET_PREDICTION = 'INSERT INTO predictions_vet (owner_mail,pred_type_id) VALUES (?, ?)'