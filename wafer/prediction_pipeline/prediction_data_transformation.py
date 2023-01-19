from wafer.logger import logging
from wafer.exception import WaferException
import os
import sys
import pandas as pd


class Prediction_Data_Transformation:
    def __init__(self):
        self.col_to_keep = None
        self.col_list = None

    def missing_value_imputation(self):
        try:
            for file in os.listdir("wafer/prediction_pipeline/prediction_artifact/Good_data/"):
                csv = pd.read_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file)
                csv.fillna(0, inplace=True)
                csv.to_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file, index=False)
            logging.info("missing value imputation complete")
            return
        except WaferException as e:
            raise WaferException(e, sys)

    def remove_unwanted_column(self, data):
        try:
            self.col_to_keep = pd.read_csv("wafer/core_ml/data_preprocessing/training_col_list.csv")
            self.col_list = self.col_to_keep['training_col_list'].to_list()
            # self.col_list.remove('Good/Bad')
            self.col_list.remove('Cluster')
            self.col_list.remove('Labels')

            data = data[self.col_list]
            logging.info("prediction removed unwanted columns from the dataset")

            return data
        except WaferException as e:
            raise WaferException(e, sys)