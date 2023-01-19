from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline
from wafer.pipeline.prediction_pipeline import Prediction_Pipeline
from wafer.logger import logging
from wafer.exception import WaferException
import sys


if __name__ == '__main__':
    try:
        logging.info("START OF WAFER FAULT DETECTION PROJECT EXECUTION")

        # data_ingestion = TrainingDataPipeline()
        # data_ingestion.train_data_validation()

        # model_training = Model_Training_Pipeline()
        # model_training.train_model()

        prediction_pipeline = Prediction_Pipeline()
        prediction_pipeline.prediction_pipeline_execution()

        logging.info("END OF WAFER FAULT DETECTION PROJECT EXECUTION")

    except WaferException as e:
        raise WaferException(e, sys)
