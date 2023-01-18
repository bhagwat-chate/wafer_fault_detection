import pandas as pd
from os import listdir
import sys
from wafer.logger import logging
from wafer.exception import WaferException
import pickle

class Prediction_Data_Transform:
    def __init__(self):
        self.new_data = None
        self.new_array = None

    def load_imputer(self):
        try:
            with open("wafer/core_ml/data_preprocessing/imputer_object.sav", 'rb') as f:
                imputer = pickle.load(f)
                f.close()
            logging.info("Impute object load successful")
            return imputer
        except WaferException as e:
            raise WaferException(e, sys)

    def missing_value_imputation(self, data):
        try:
            # for file in listdir("wafer/prediction/prediction_artifact/Good_Raw"):
            #     csv = pd.read_csv("wafer/prediction/prediction_artifact/Good_Raw/"+file)
            #     csv.fillna('NaN', inplace=True)
            #     csv.to_csv("wafer/prediction/prediction_artifact/Good_Raw/"+file, index=False)

            imputer = self.load_imputer()
            self.new_array = imputer.transform(data)
            self.new_data = pd.DataFrame(data=self.new_array, columns=data.columns)
            self.new_data.to_csv("wafer/prediction/prediction_artifact/Prediction_data.csv", index=False)

            logging.info("prediction data missing value imputation complete")

            return self.new_data
        except WaferException as e:
            raise WaferException(e, sys)