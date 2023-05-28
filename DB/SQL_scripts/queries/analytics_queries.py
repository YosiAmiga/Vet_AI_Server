#################################### Analitics queries ####################################
PREDICTION_DISTRIBUTION = '''
SELECT predictions_types.pred_type_name,
       timestamp
  FROM predictions,predictions_types
  WHERE pet_id = ? AND predictions_types.pred_type_id = predictions.pred_type_id
'''

PREDICTIONS_BY_USERS = '''
SELECT u.email AS owner_mail, COUNT(p.pred_id) AS prediction_count
FROM users u
LEFT JOIN predictions p ON u.email = p.owner_mail
GROUP BY u.email;
'''

USER_PET_COUNT = '''
SELECT u.email, COUNT(pe.pet_id) AS pet_count
FROM users u
LEFT JOIN pets pe ON u.email = pe.owner_mail
GROUP BY u.email;
'''

PET_TYPES_COUNT = '''
SELECT pet_type, COUNT(*) AS pet_count
FROM pets
GROUP BY pet_type;
'''

COUNT_DAILY_PREDICTIONS = '''
SELECT DATE(timestamp) AS prediction_date, COUNT(*) AS prediction_count
FROM predictions
GROUP BY prediction_date
'''