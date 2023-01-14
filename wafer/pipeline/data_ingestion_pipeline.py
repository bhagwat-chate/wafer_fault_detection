from wafer.data_ingestion.rawValidation import Raw_Data_Validation
from wafer.logger import logging
from wafer.exception import WaferException
import sys
from datetime import datetime

class TrainingDataPipeline:

    def __init__(self):
        self.raw_data_validation = Raw_Data_Validation("wafer\Training_Batch_Files")


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

            pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName = self.raw_data_validation.valuesFromSchema()
            manualexp = self.raw_data_validation.manualRegexCreation()
            self.raw_data_validation.createDirectoryForGoodBadRawData()
            self.raw_data_validation.deleteExistingBadDataTrainingFolder()
            self.raw_data_validation.moveBadFilesToArchiveBad()

            logging.info("Training raw data validation completed")

        except WaferException as e:
            raise WaferException(e, sys)

