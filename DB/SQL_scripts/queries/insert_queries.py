#################################### INSERT queries ####################################

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

INSERT_PERSON_TYPE = '''
INSERT INTO pet_types (id, type_name)
SELECT 3, 'person'
WHERE NOT EXISTS (SELECT id FROM pet_types WHERE id = 3 AND type_name = 'person')
'''

INSERT_PREDICTION = 'INSERT INTO predictions (owner_mail, pet_id, pred_type_id) VALUES (?, ?, ?)'

INSERT_VET_PREDICTION = 'INSERT INTO predictions_vet (owner_mail,pred_type_id) VALUES (?, ?)'

## NEED TO CHANGE THE 2nd value to add it to table
INSERT_PET_PREDICTION_TYPE = '''


'''