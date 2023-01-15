from wafer.data_ingestion.rawValidation import Raw_Data_Validation
from wafer.data_ingestion.dataTransformation import Data_Transform
from wafer.data_ingestion.dbOperation import DB_Operation
from wafer.logger import logging
from wafer.exception import WaferException
import sys

class TrainingDataPipeline:

    def __init__(self):
        self.raw_data_validation = Raw_Data_Validation("wafer/Training_Batch_Files")
        self.data_transform = Data_Transform()
        self.dbops = DB_Operation()

    def train_data_validation(self):

        """
        Method Name: manualRegexCreation
        Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
        This Regex is used to validate the filename of the training data.
        Output: Regex pattern
        On Failure: None

        Written By: Bhagwat Chate
        Version: 1.0
        Revisions: None
        """
        try:
            logging.info("Start training raw data validation!")

            # Data Validation
            pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName = self.raw_data_validation.valuesFromSchema()
            regex = self.raw_data_validation.manualRegexCreation()
            self.raw_data_validation.validateFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            self.raw_data_validation.validateColumnLength(NumberofColumns)
            self.raw_data_validation.validateMissingValuesInWholeColumn()
            self.raw_data_validation.moveBadFilesToArchiveBad()

            # Data Transformation
            self.data_transform.missing_value_imputation()

            # Data load into MongoDB
            self.dbops.loadData()
            self.dbops.readData()

            logging.info("Training raw data validation complete")

        except WaferException as e:
            raise WaferException(e, sys)

