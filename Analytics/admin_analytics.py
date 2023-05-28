from DB import database
import csv
import os

class admin_analytics:
    def __init__(self, To_Csv_File=False):
        if To_Csv_File:
            self.get_predictions_by_users(To_Csv_File)
            self.get_pet_prediction_types(To_Csv_File)
            self.get_user_pet_count(To_Csv_File)
            self.get_pet_types_count(To_Csv_File)
            self.get_count_daily_predictions(To_Csv_File)
        else:
            self.get_predictions_by_users()
            self.get_pet_prediction_types()
            self.get_user_pet_count()
            self.get_pet_types_count()
            self.get_count_daily_predictions()

    def save_data_as_csv(self, data, filename):
        # Create the 'query_csv_files' folder if it doesn't exist
        folder_name = './Analytics/query_csv_files'

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the data as a CSV file in the 'query_csv_files' folder
        csv_file = os.path.join(folder_name, filename)
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return csv_file

    def get_predictions_by_users(self, To_Csv_File=False):
        predictions_by_users = database.get_predictions_by_users()
        if To_Csv_File:
            csv_file = self.save_data_as_csv(predictions_by_users, "predictions_by_users.csv")
            return csv_file
        else:
            return predictions_by_users

    def get_pet_prediction_types(self, To_Csv_File=False):
        pet_prediction_types = database.get_pet_prediction_types()
        if To_Csv_File:
            csv_file = self.save_data_as_csv(pet_prediction_types, "pet_prediction_types.csv")
            return csv_file
        else:
            return pet_prediction_types

    def get_user_pet_count(self, To_Csv_File=False):
        user_pet_count = database.get_user_pet_count()
        if To_Csv_File:
            csv_file = self.save_data_as_csv(user_pet_count, "user_pet_count.csv")
            return csv_file
        else:
            return user_pet_count

    def get_pet_types_count(self, To_Csv_File=False):
        pet_types_count = database.get_pet_types_count()
        if To_Csv_File:
            csv_file = self.save_data_as_csv(pet_types_count, "pet_types_count.csv")
            return csv_file
        else:
            return pet_types_count

    def get_count_daily_predictions(self, To_Csv_File=False):
        count_daily_predictions = database.get_count_daily_predictions()
        if To_Csv_File:
            csv_file = self.save_data_as_csv(count_daily_predictions, "count_daily_predictions.csv")
            return csv_file
        else:
            return count_daily_predictions


if __name__ == "__main__":
    analytics = admin_analytics(To_Csv_File=False)
