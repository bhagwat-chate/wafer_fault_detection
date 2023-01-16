import pandas as pd
from wafer.core_ml.file_methods import File_Operations
from wafer.data_ingestion.dataTransformation import Data_Transform
from wafer.prediction.data_loader_prediction import Data_load_for_Prediction
from wafer.prediction.prediction_data_validation import Predict_Raw_Data_Validation
from wafer.core_ml.data_preprocessing import Preprocessor
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import datetime
class Prediction:
    def __init__(self, path):
        if path is not None:
            self.pred_data_val = Predict_Raw_Data_Validation(path)

    def prediction_from_model(self):
        try:
            data_getter = Data_load_for_Prediction()
            data = data_getter.get_data()

            preprocessor = Preprocessor()

            is_null_present = preprocessor.is_null_present(data)

            if is_null_present:
                data = preprocessor.null_value_impute(data)

            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(data)
            data = preprocessor.remove_column(data, cols_to_drop)

            file_loader = File_Operations()
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(data.drop(['Wafer']), axis=1)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()

            now = datetime.datetime.now()
            date = now.date()
            time = now.strftime("%H%M%S")

            for i in clusters:
                logging.info("Predictions for cluster: {}".format(i))
                cluster_data = data[data['clusters'] == i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(labels=['Wafer', 'clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_names, result)), columns=['Wafer', 'Prediction'])
                path = "wafer/prediction/prediction_artifact/Prediction_"+str(date)+"_"+str(time)
                result.to_csv(path+'/'+"Predictions.csv", header=True, mode='a+')
            logging.info("prediction from model complete")

        except WaferException as e:
            raise WaferException(e, sys)