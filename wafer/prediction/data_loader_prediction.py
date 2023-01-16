from wafer.logger import logging
from wafer.exception import WaferException
import os, sys
import pandas as pd
class Data_load_for_Prediction:
    def __init__(self):
        self.data = None
        self.prediction_data = "wafer/prediction/prediction_artifact/prediction_data.csv"

    def get_data(self):
        try:
            self.data = pd.read_csv(self.prediction_data)
            logging.info("Prediction data load complete")
            return self.data
        except WaferException as e:
            raise WaferException(e, sys)