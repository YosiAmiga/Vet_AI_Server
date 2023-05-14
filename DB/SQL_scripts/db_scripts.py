# from DB.SQL_scripts.queries.select_queries import *
# from DB.SQL_scripts.queries.create_queries import *
# from DB.SQL_scripts.queries.insert_queries import *
# from DB.SQL_scripts.queries.analytics_queries import *
import DB.SQL_scripts.queries.select_queries as select_queries
import DB.SQL_scripts.queries.create_queries as create_queries
import DB.SQL_scripts.queries.insert_queries as insert_queries
import DB.SQL_scripts.queries.analytics_queries as analytics_queries

# list of modules
query_modules = [create_queries, select_queries, insert_queries, analytics_queries]

queries = {}
for module in query_modules:
    queries.update({attr.lower(): getattr(module, attr) for attr in vars(module) if not attr.startswith("__")})

print("queries", queries)
# queries = {
#     'create_users_table': CREATE_USERS_TABLE,
#     'create_pets_table': CREATE_PETS_TABLE,
#     'create_pet_types_table': CREATE_PET_TYPES_TABLE,
#     'create_predictions_types_table': CREATE_PREDICTIONS_TYPES_TABLE,
#     'create_predictions_table': CREATE_PREDICTIONS_TABLE,
#
#     'select_user_by_email_with_type': SELECT_USER_BY_EMAIL_WITH_TYPE,
#     'select_user_by_email': SELECT_USER_BY_EMAIL,
#     'select_pets_by_owner_email': SELECT_PETS_BY_OWNER_EMAIL,
#     'select_pet_by_id_and_owner_email': SELECT_PET_BY_ID_AND_OWNER_EMAIL,
#     'select_all_pet_types': SELECT_ALL_PET_TYPES,
#     'select_pet_predictions_history': SELECT_PET_PREDICTIONS_HISTORY,
#
#     'insert_user_with_type': INSERT_USER_WITH_TYPE,
#     'insert_user_all_data': INSERT_USER_ALL_DATA,
#     'insert_user': INSERT_USER,
#     'insert_pet': INSERT_PET,
#     'insert_cat_type': INSERT_CAT_TYPE,
#     'insert_dog_type': INSERT_DOG_TYPE,
#     'insert_prediction': INSERT_PREDICTION,
#     'insert_vet_prediction': INSERT_VET_PREDICTION,
#
#     'prediction_distribution': PREDICTION_DISTRIBUTION
# }