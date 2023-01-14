import datetime
import os
import sys
import json
import shutil
import pandas as pd
import numpy as np
from wafer.logger import logging
from wafer.exception import WaferException

class Raw_Data_Validation:
    """
    This class shall be used for handling all the validation done on the raw training data!
    Written by: Bhagwat Chate
    Version: 1.0
    Revision: None
    """

    def __init__(self, path):
        logging.info("Start raw data validation!")
        self.batch_directory = path
        self.schema_path = 'wafer/constant/training_schema.json'

    def valuesFromSchema(self):
        """
            Method Name: valuesFromSchema
            Description: This method extracts all the relevant information from the pre-defined "Schema" file.
            Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
            On Failure: Raise ValueError,KeyError,Exception

            Written By: Bhagwat Chate
            Version: 1.0
            Revisions: None
        """
        try:
            logging.info("Load the training schema details")
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()

                pattern = dic['SampleFileName']
                LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
                LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
                NumberofColumns = dic['NumberofColumns']
                ColName = dic['ColName']

                logging.info('**************************************************************************')
                logging.info("pattern: "+str(pattern))
                logging.info("LengthOfDateStampInFile: "+str(LengthOfDateStampInFile))
                logging.info("LengthOfTimeStampInFile: "+str(LengthOfTimeStampInFile))
                logging.info("NumberOfColumns: "+str(NumberofColumns))
                # logging.info("ColName: ", ColName)
                logging.info('**************************************************************************')
                logging.info("Training schema details loaded successfully")

                return pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName

        except WaferException as e:
            raise WaferException(e, sys)

    def manualRegexCreation(self):
        try:
            logging.info("Load the manual regular expression definition")
            regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
            logging.info("Manual regular expression definition loaded")

            return regex
        except WaferException as e:
            raise WaferException(e, sys)

    def createDirectoryForGoodBadRawData(self):
        """
        Method Name: createDirectoryForGoodBadRawData
        Description: This method creates directories to store the Good Data and Bad Data
        after validating the training data.

        Output: None
        On Failure: OSError

        Written By: Bhagwat Chate
        Version: 1.0
        Revisions: None
        """
        try:
            logging.info("Creating directory for good and bad raw data")

            path = os.path.join("wafer/data_ingestion/Training_raw_files_validated/",'Good_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join("wafer/data_ingestion/Training_raw_files_validated/",'Bad_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            logging.info("Directory created for good and bad raw data")
        except WaferException as e:
            raise WaferException(e, sys)

    def deleteExistingBadDataTrainingFolder(self):
        """
        Method Name: deleteExistingGoodDataTrainingFolder
        Description: This method deletes the directory made  to store the Good Data
        after loading the data in the table. Once the good files are
        loaded in the DB,deleting the directory ensures space optimization.
        Output: None
        On Failure: OSError

        Written By: Bhagwat Chate
        Version: 1.0
        Revisions: None
        """

        try:
            path = 'wafer/data_ingestion/Training_raw_files_validated/'
            if os.path.isdir(path+'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw')
                logging.info("Bad Raw directory deleted before starting training data validation")
        except WaferException as e:
            raise WaferException(e, sys)

    def moveBadFilesToArchiveBad(self):
        """
            Method Name: moveBadFilesToArchiveBad
            Description: This method deletes the directory made  to store the Bad Data
            after moving the data in an archive folder. We archive the bad
            files to send them back to the client for invalid data issue.

            Output: None
            On Failure: OSError

            Written By: Bhagwat Chate
            Version: 1.0
            Revisions: None
        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            source = "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw/"

            if os.path.isdir(source):
                path = "TrainingArchiveBadData"

                if not os.path.isdir(path):
                    os.makedirs(path)

                dest = 'TrainingArchiveBadData/Bad_Data_' + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                logging.info("Bad files moved to archive")

                path = "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw/"
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')

        except WaferException as e:
            raise WaferException(e, sys)
