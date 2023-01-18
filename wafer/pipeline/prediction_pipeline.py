from wafer.prediction_pipeline.predict_from_model import Predict_from_Model
from wafer.prediction_pipeline.prediction_DB_operation import Prediction_DB_Operation
from wafer.prediction_pipeline.prediction_data_validation import Prediction_Data_Validation
from wafer.prediction_pipeline.prediction_data_transformation import Prediction_Data_Transformation
import os
import shutil
from wafer.logger import logging
from wafer.exception import WaferException
import sys

class Prediction_Pipeline:

    def __init__(self):
        self.predict_from_model_obj = Predict_from_Model()
        self.prediction_DB_operation_obj = Prediction_DB_Operation()
        self.prediction_data_validation_obj = Prediction_Data_Validation()
        self.prediction_data_transformation_obj = Prediction_Data_Transformation()

    def prediction_pipeline_execution(self):
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
            data = self.prediction_DB_operation_obj.get_data()
            data.to_csv("wafer/prediction_pipeline/prediction_artifact/data_for_prediction.csv", index=False)

        except WaferException as e:
            raise WaferException(e, sys)


