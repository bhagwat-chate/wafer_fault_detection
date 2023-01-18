from wafer.logger import logging
from wafer.exception import WaferException
import json
import sys
import os
import shutil
import re
import pandas as pd
from datetime import datetime
class Prediction_Data_Validation:
    def __init__(self):
        self.schema_path = "wafer/constant/prediction_schema.json"

    def values_from_schema(self):
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

                logging.info("prediction schema details load complete")

            return pattern, LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName

        except WaferException as e:
            raise WaferException(e, sys)

    def manual_regex_creation(self):
        try:
            regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"

            logging.info("manual regular expression load complete")

            return regex
        except WaferException as e:
            raise WaferException(e, sys)

    def validate_file_name(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):

        self.delete_existing_good_bad_data_directories()
        self.create_good_bad_directories()

        for file in os.listdir("wafer/Prediction_Batch_Files/"):
            shutil.copy("wafer/Prediction_Batch_Files/"+file, "wafer/prediction_pipeline/prediction_artifact/Good_data/")

        # onlyfiles = [f for f in listdir(self.batch_directory)]
        onlyfiles = [f for f in os.listdir("wafer/prediction_pipeline/prediction_artifact/Good_data/")]
        try:
            for filename in onlyfiles:
                if re.match(regex, filename):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))

                    if int(splitAtDot[1]) == int(LengthOfDateStampInFile):
                        if len(splitAtDot[2] == LengthOfTimeStampInFile):
                            pass
                        else:
                            shutil.move("wafer/prediction_pipeline/prediction_artifact/Good_data/"+filename, "wafer/prediction_pipeline/prediction_artifact/Bad_data/")
                            logging.info("File {} moved from Good to Bad data".format(filename))
                    else:
                        shutil.move("wafer/prediction_pipeline/prediction_artifact/Good_data/" + filename, "wafer/prediction_pipeline/prediction_artifact/Bad_data/")
                        logging.info("File {} moved from Good to Bad data".format(filename))

            logging.info("File name validation complete")
        except WaferException as e:
            raise WaferException(e, sys)

    def validate_column_length(self, number_of_columns):
        try:
            for file in os.listdir("wafer/prediction_pipeline/prediction_artifact/Good_data/"):
                csv = pd.read_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/" + file)
                if not csv.shape[1] == number_of_columns:
                    shutil.move("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file, "wafer/prediction_pipeline/prediction_artifact/Bad_data")
                    logging.info("File {} moved from 'wafer/prediction_pipeline/prediction_artifact/Good_data' to Bad data".format(file))

            logging.info("Column length validation complete")
        except WaferException as e:
            raise WaferException(e, sys)


    def validate_missing_values_in_whole_column(self):
        try:
            for file in os.listdir("wafer/prediction_pipeline/prediction_artifact/Good_data/"):
                csv = pd.read_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file)

                count = 0

                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file,
                                    "wafer/prediction_pipeline/prediction_artifact/Bad_data")
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file, index=None, header=True)
            logging.info("Missing values in whole column validation complete")
        except WaferException as e:
            raise WaferException(e, sys)

    def move_bad_files_to_archive(self):
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            source = "wafer/prediction_pipeline/prediction_artifact/Bad_data/"

            if os.path.isdir(source):
                dest = 'wafer/archive/prediction/Bad_Data_' + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)

                path = "wafer/prediction_pipeline/prediction_artifact/Bad_data/"
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')

                logging.info("Bad files moved to archive. Bad data directory removed from prediction")

        except WaferException as e:
            raise WaferException(e, sys)



    def delete_existing_good_bad_data_directories(self):
        try:

            path = 'wafer/prediction_pipeline/prediction_artifact/'

            if os.path.isdir(path + 'Bad_data/'):
                shutil.rmtree(path + 'Bad_data')
                logging.info("prediction bad data directory deleted")

            if os.path.isdir(path + 'Good_data/'):
                shutil.rmtree(path + 'Good_data')
                logging.info("prediction good data directory deleted")

        except WaferException as e:
            raise WaferException(e, sys)

    def create_good_bad_directories(self):
        path = 'wafer/prediction_pipeline/prediction_artifact/'

        if not os.path.isdir(path + 'Bad_data/'):
            os.makedirs(path + 'Bad_data')
            logging.info("prediction bad data directory created")

        if not os.path.isdir(path + 'Good_data/'):
            os.makedirs(path + 'Good_data')
            logging.info("prediction good data directory created")