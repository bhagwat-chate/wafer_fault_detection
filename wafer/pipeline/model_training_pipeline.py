from sklearn.model_selection import train_test_split
from wafer.core_ml.data_preprocessing import Preprocessor
from wafer.core_ml.clustering import KMeansClustering, KMeans
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
            kmeans = KMeansClustering()
            number_of_clusters = kmeans.elbow_plot(X)

            X = kmeans.create_clusters(X, number_of_clusters)
            X['Labels'] = Y

            list_of_clusters = X['Cluster'].unique()

            for i in list_of_clusters:
                cluster_data = X[X['Cluster'] == i]

                cluster_features = cluster_data.drop(['Labels','Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1/3, random_state=355)
                model_finder = tuner.model_finder()
        except WaferException as e:
            raise WaferException(e, sys)

        



