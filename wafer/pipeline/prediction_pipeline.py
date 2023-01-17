from wafer.prediction.prediction_data_DBoperation import Prediction_DB_Operation
from wafer.prediction.prediction_raw_data_validation import Prediction_Raw_Data_Validation
from wafer.prediction.prediction_data_transformation import Prediction_Data_Transform
from wafer.logger import logging
from wafer.exception import WaferException
import sys


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
            self.data_transform.missing_value_imputation()

            # Data load into MongoDB
            self.dbops.loadData()
            self.dbops.readData()

            logging.info("### Prediction data pipeline execution complete ###")
        except WaferException as e:
            raise WaferException(e, sys)