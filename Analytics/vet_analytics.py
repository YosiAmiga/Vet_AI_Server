class vet_analytics:
    def __init__(self):
        self.columns = ['pred_id', 'owner_mail', 'pred_type_name', 'timestamp']

    @staticmethod
    def get_data_for_plotting_pie_chart(dataFrame,x:str,y:str):
        return dataFrame[x],dataFrame[y]

    @staticmethod
    def get_predictions_dist(dataFrame=None, owner_email="itaykarat13@gmail.com"):
        """

        :param dataFrame: Input is a dataFrame of the predictions
        :param owner_email: A unique owner email in the system

        :return: Filtered dataFrame of the predictions dist for the specific user
        """
        if dataFrame is None or owner_email is None:
            raise "None dataFrame passed or None owner_email passed"

        else:
            owner_dataFrame = dataFrame[dataFrame['owner_mail'] == owner_email]
            count_distribution = owner_dataFrame['pred_type_name'].value_counts()
            print(count_distribution)
            return count_distribution

    @staticmethod
    def get_animals_dist(dataFrame=None):
        if dataFrame is None:
            raise "None dataFrame passed"