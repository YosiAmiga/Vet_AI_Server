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