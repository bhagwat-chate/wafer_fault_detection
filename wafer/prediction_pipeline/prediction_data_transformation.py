from wafer.logger import logging
from wafer.exception import WaferException
import os
import sys
import pandas as pd

class Prediction_Data_Transformation:
    def __init__(self):
        pass

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