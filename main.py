# from wafer.logger import logging
# from wafer.exception import SensorException

from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline

if __name__ == '__main__':
    obj = TrainingDataPipeline()
    obj.train_data_validation()

    model_training = Model_Training_Pipeline()
    model_training.train_model()

