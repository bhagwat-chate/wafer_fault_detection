import datetime
import os
import re
import sys
import json
import shutil
import pandas as pd
from os import listdir
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
        logging.info("Start training raw data validation!")
        # self.batch_directory = path
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
            path = os.path.join("wafer/data_ingestion/Training_raw_files_validated/", 'Good_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join("wafer/data_ingestion/Training_raw_files_validated/", 'Bad_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)

            logging.info("Directories created for good and bad raw data")
        except WaferException as e:
            raise WaferException(e, sys)

    def deleteExistingBadDataTrainingFolder(self):
        """
        Method Name: deleteExistingBadDataTrainingFolder
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

    def deleteExistingGoodDataTrainingFolder(self):
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
            if os.path.isdir(path+'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw')
                logging.info("Good Raw directory deleted before starting training data validation")
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
        now = datetime.datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            source = "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw/"

            if os.path.isdir(source):
                # path = "TrainingArchiveBadData"
                #
                # if not os.path.isdir(path):
                #     os.makedirs(path)

                dest = 'wafer/archive/training/Bad_Data_' + str(date) + "_" + str(time)
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

    def validateFileNameRaw(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):

        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()

        # onlyfiles = [f for f in listdir(self.batch_directory)]
        onlyfiles = [f for f in listdir("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/")]
        try:
            for filename in onlyfiles:
                if(re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))

                    if int(splitAtDot[1]) == int(LengthOfDateStampInFile):
                        if len(splitAtDot[2] == LengthOfTimeStampInFile):
                            pass
                        else:
                            shutil.move("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+filename,
                                        "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw/")
                            logging.info("File {} moved from Good to Bad raw".format(filename))
                    else:
                        shutil.move("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/" + filename,
                                    "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw/")
                        logging.info("File {} moved from Good to Bad raw".format(filename))

            logging.info("File name validation complete")
        except WaferException as e:
            raise WaferException(e, sys)

    def validateColumnLength(self, numberOfColumns):
        try:

            for file in listdir("wafer/Training_Batch_Files/"):

                csv = pd.read_csv("wafer/Training_Batch_Files/" + file)

                if csv.shape[1] == numberOfColumns:
                    shutil.copy("wafer/Training_Batch_Files/"+file, "wafer/data_ingestion/Training_raw_files_validated/Good_Raw")
                    logging.info("File {} moved from 'wafer/Training_Batch_Files' to Bad raw".format(file))
                else:
                    shutil.copy("wafer/Training_Batch_Files/"+file, "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw")
                    logging.info("File {} moved from 'wafer/Training_Batch_Files' to Bad raw".format(file))

            logging.info("Column length validation complete")
        except WaferException as e:
            raise WaferException(e, sys)

    def validateMissingValuesInWholeColumn(self):
        try:
            for file in listdir("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"):
                csv = pd.read_csv("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file)
                count = 0

                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file,
                                    "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw")
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file, index=None, header=True)
            logging.info("Missing values in whole column validation complete")
        except WaferException as e:
            raise WaferException(e, sys)