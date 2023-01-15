import pandas as pd
from os import listdir
import sys
from wafer.logger import logging
from wafer.exception import WaferException
class Data_Transform:
    def __init__(self):
        pass
    def missing_value_imputation(self):
        try:
            for file in listdir("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"):
                csv = pd.read_csv("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file)
                csv.fillna('NaN', inplace=True)
                csv.to_csv("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file, index=False)
            logging.info("Missing value imputation complete")
        except WaferException as e:
            raise WaferException(e, sys)