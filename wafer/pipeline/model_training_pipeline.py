from sklearn.model_selection import train_test_split
from wafer.core_ml.data_preprocessing import Preprocessor
from wafer.logger import logging
from wafer.exception import WaferException
import json
import pandas as pd
import sys
class Model_Training_Pipeline:
    def __init__(self):
        self.col_to_drop = None
        self.data = None
        logging.info("### Model Training Pipeline Initiated ###")
        with open("wafer/constant/model_training_constants.json","r") as f:
            dic = json.load(f)
            f.close()
        self.path = dic["train_data"]
        self.preprocessor = Preprocessor()

    def train_model(self):
        try:
            self.data = self.preprocessor.get_data(self.path)
            self.data = self.preprocessor.remove_column(self.data, 'Wafer')
            flage = self.preprocessor.is_null_present(self.data)
            
            if flage == 1:
                self.data = self.preprocessor.null_value_impute(self.data)
                
            X, Y = self.preprocessor.separate_label_feature(self.data, "Good/Bad")
            self.col_to_drop = self.preprocessor.get_columns_with_zero_std_deviation(self.data)
            self.data = self.preprocessor.remove_column(self.data, self.col_to_drop)

            #####  Applying the Clustering Approach #####
            kmeans =clustering.KMeansClustering(self.file_object, )
        except WaferException as e:
            raise WaferException(e, sys)

        



