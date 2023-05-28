#################################### SELECT queries ####################################

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

SELECT_PET_PREDICTIONS_HISTORY = '''
SELECT pred_id,
       owner_mail,
       predictions_types.pred_type_name,
       timestamp
  FROM predictions,predictions_types
  WHERE pet_id = ? AND predictions_types.pred_type_id = predictions.pred_type_id
  '''

SELECT_PET_PREDICTION_TYPES = '''
SELECT pet_types.type_name, predictions_types.pred_type_name
FROM pet_prediction_type
JOIN pet_types ON pet_types.id = pet_prediction_type.pet_type_id
JOIN predictions_types ON predictions_types.pred_type_id = pet_prediction_type.pred_type_id;

'''


SELECT_ALL_PETS = '''
SELECT pet_id,
       owner_mail,
       pet_type,
       pet_name,
       pet_dob
  FROM pets;

'''

SELECT_ALL_PREDICTIONS = '''
SELECT pred_id,
       owner_mail,
       pet_id,
       pred_type_id,
       timestamp
  FROM predictions;
'''