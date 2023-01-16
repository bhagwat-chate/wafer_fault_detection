from wafer.prediction.predict_from_model import Prediction
from wafer.logger import logging
from wafer.exception import WaferException
import sys

class Model_Prediction_Pipeline:
    def __init__(self):
        self.prediction = Prediction()

    def predict_with_model(self):
        try:
            logging.info("Prediction pipeline execution start")
            self.prediction.prediction_from_model()
            logging.info("Prediction pipeline execution complete")
        except WaferException as e:
            raise WaferException(e, sys)