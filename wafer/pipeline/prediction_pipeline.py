from wafer.prediction.prediction_data_DBoperation import Prediction_DB_Operation
from wafer.prediction.prediction_raw_data_validation import Prediction_Raw_Data_Validation
from wafer.prediction.prediction_data_transformation import Prediction_Data_Transform
from wafer.prediction.prediction_preprocessing import Preprocessor
from wafer.core_ml.file_methods import File_Operations
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import pandas as pd

class Prediction_Pipeline:

    def __init__(self):
        self.raw_data_validation = Prediction_Raw_Data_Validation("wafer/Prediction_Batch_Files")
        self.data_transform = Prediction_Data_Transform()
        self.dbops = Prediction_DB_Operation()

    def prediction_pipeline_execute(self):
        try:
            logging.info("### Prediction Data Pipeline Initiated ###")

            # Prediction Data Validation
            pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName = self.raw_data_validation.valuesFromSchema()
            regex = self.raw_data_validation.manualRegexCreation()
            self.raw_data_validation.validateFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            self.raw_data_validation.validateColumnLength(NumberofColumns)
            # self.raw_data_validation.validateMissingValuesInWholeColumn() # ----> pending for debug
            self.raw_data_validation.moveBadFilesToArchiveBad()

            # Data Transformation


            # Data load into MongoDB
            self.dbops.loadData()
            data = self.dbops.readData()

            preprocessor = Preprocessor()

            data = preprocessor.remove_column(data)  # DONE

            data = self.data_transform.missing_value_imputation(data)

            file_loader = File_Operations()
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(data.drop("Wafer", axis=1))
            data['clusters'] = clusters
            clusters = data['clusters'].unique()

            for i in clusters:
                cluster_data = data[data['clusters'] == i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(labels=['Wafer'], axis=1)
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_names, result)), columns=['Wafer', 'Prediction'])
                path = "Prediction_Output_File/Predictions.csv"
                result.to_csv("wafer/prediction/prediction_artifact/output/Predictions.csv", header=True)

            logging.info("### Prediction data pipeline execution complete ###")
        except WaferException as e:
            raise WaferException(e, sys)