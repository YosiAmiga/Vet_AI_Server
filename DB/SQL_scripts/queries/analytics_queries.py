#################################### Analitics queries ####################################
PREDICTION_DISTRIBUTION = '''
SELECT predictions_types.pred_type_name,
       timestamp
  FROM predictions,predictions_types
  WHERE pet_id = ? AND predictions_types.pred_type_id = predictions.pred_type_id
'''