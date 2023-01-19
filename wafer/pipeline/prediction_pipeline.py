from wafer.prediction_pipeline.predict_from_model import Predict_from_Model
from wafer.prediction_pipeline.prediction_DB_operation import Prediction_DB_Operation
from wafer.prediction_pipeline.prediction_data_validation import Prediction_Data_Validation
from wafer.prediction_pipeline.prediction_data_transformation import Prediction_Data_Transformation
from wafer.core_ml.file_methods import File_Operations
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import pandas as pd


class Prediction_Pipeline:

    def __init__(self):
        self.predict_from_model_obj = Predict_from_Model()
        self.prediction_DB_operation_obj = Prediction_DB_Operation()
        self.prediction_data_validation_obj = Prediction_Data_Validation()
        self.prediction_data_transformation_obj = Prediction_Data_Transformation()
        self.file_operations_obj = File_Operations()

        self.col_to_del = None

    def prediction_pipeline_execution(self, path):
        try:
            self.predict_from_model_obj.delete_prediction_file()

            # Data validation
            pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName = self.prediction_data_validation_obj.values_from_schema()
            regex = self.prediction_data_validation_obj.manual_regex_creation()
            self.prediction_data_validation_obj.validate_file_name(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            self.prediction_data_validation_obj.validate_column_length(NumberofColumns)
            # self.prediction_data_validation_obj.validate_missing_values_in_whole_column()
            self.prediction_data_validation_obj.move_bad_files_to_archive()

            # Data Transformation
            self.prediction_data_transformation_obj.missing_value_imputation()

            # Data DB operations
            self.prediction_DB_operation_obj.load_data()
            data_with_wafer = self.prediction_DB_operation_obj.get_data()
            data = data_with_wafer.drop('wafer', axis=1)

            data = self.prediction_data_transformation_obj.remove_unwanted_column(data)

            kmeans = self.file_operations_obj.load_model_prediction('KMeans')
            clusters = kmeans.predict(data)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()

            data['wafer'] = data_with_wafer['wafer']
            for i in clusters:
                cluster_data = data[data['clusters'] == i]
                wafer_name = list(cluster_data['wafer'])
                cluster_data.drop(['wafer', 'clusters'], axis=1, inplace=True)

                model_name = self.file_operations_obj.find_correct_model_file(i)
                model = self.file_operations_obj.load_model_prediction(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_name, result)), columns=['wafer', 'prediction'])

                # result.to_csv("wafer/prediction_pipeline/prediction_artifact/PREDICTION_RESULT.csv", index=False, mode='a+')
                result.to_json("wafer/prediction_pipeline/prediction_artifact/PREDICTION_RESULT.json")

                logging.info("predictions with model '{}' complete".format(model_name))
            logging.info("### Prediction Pipeline Execution Complete ###")
        except WaferException as e:
            raise WaferException(e, sys)