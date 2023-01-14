# from wafer.logger import logging
# from wafer.exception import SensorException
from test_file import Test
import sys

from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline

if __name__ == '__main__':
    obj = TrainingDataPipeline()
    obj.train_data_validation()

