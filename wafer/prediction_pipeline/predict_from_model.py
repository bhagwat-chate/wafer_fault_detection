from wafer.logger import logging
from wafer.exception import WaferException
import os, sys

class Predict_from_Model:

    def __init__(self):
        pass

    def delete_prediction_file(self):
        flage = 0
        try:
            if os.path.exists("wafer/prediction_pipeline/prediction_artifact/Training_data.csv"):
                os.remove("wafer/prediction_pipeline/prediction_artifact/Training_data.csv")
                flage = 1

            if flage:
                logging.info("prediction file was exist, deleted")
            else:
                logging.info("prediction file was not exist")

        except WaferException as e:
            raise WaferException(e, sys)