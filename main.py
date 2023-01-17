from wafer.logger import logging
from wafer.exception import WaferException
import sys

from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline
from wafer.pipeline.prediction_pipeline import Prediction_Pipeline

if __name__ == '__main__':
    try:
        logging.info("START OF WAFER FAULT DETECTION PROJECT EXECUTION")

        # data_ingestion = TrainingDataPipeline()
        # data_ingestion.train_data_validation()
        #
        # model_training = Model_Training_Pipeline()
        # model_training.train_model()

        prediction = Prediction_Pipeline()
        prediction.prediction_pipeline_execute()

        logging.info("END OF WAFER FAULT DETECTION PROJECT EXECUTION")

    except WaferException as e:
        raise WaferException(e, sys)


