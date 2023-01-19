from sklearn.model_selection import train_test_split
from wafer.core_ml.data_preprocessing import Preprocessor
from wafer.core_ml.clustering import KMeansClustering
from wafer.core_ml.model_tuner import Model_Finder
from wafer.core_ml.file_methods import File_Operations
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import pandas as pd


class Model_Training_Pipeline:
    def __init__(self):
        self.col_to_drop = None
        self.data = None
        logging.info("### Model Training Pipeline Initiated ###")
        self.path = "wafer/data_ingestion/Data_Export/Training_data.csv"
        self.preprocessor = Preprocessor()

    def train_model(self):
        try:
            self.data = self.preprocessor.get_data(self.path)
            self.col_to_drop = self.preprocessor.get_columns_with_zero_std_deviation(self.data.drop('Good/Bad', axis=1))
            self.data = self.preprocessor.remove_column(self.data, self.col_to_drop)
            self.data = self.preprocessor.remove_column(self.data, 'Wafer')

            flage = self.preprocessor.is_null_present(self.data)
            if flage == 1:
                self.data = self.preprocessor.null_value_impute(self.data)

            self.data.to_csv("wafer/core_ml/data_preprocessing/Data_after_imputation.csv", index=False)
            X, Y = self.preprocessor.separate_label_feature(self.data, "Good/Bad")
            Y = self.data['Good/Bad']
            Y.to_csv("wafer/core_ml/data_preprocessing/Y.csv", index=False)

            self.data.to_csv("wafer/core_ml/data_preprocessing/data_after_remove_unwanted_col.csv", index=False)

            #####  Applying the Clustering Approach #####

            kmeans = KMeansClustering()
            number_of_clusters = kmeans.elbow_plot(self.data.drop('Good/Bad', axis=1))

            self.data.drop('Good/Bad', axis=1).to_csv("wafer/core_ml/data_preprocessing/data_for_clustering.csv", index=False)
            X = kmeans.create_clusters(self.data.drop('Good/Bad', axis=1), number_of_clusters)
            X['Labels'] = Y
            pd.DataFrame(data=X.columns, columns=['training_col_list']).to_csv("wafer/core_ml/data_preprocessing/training_col_list.csv", index=False)

            list_of_clusters = X['Cluster'].unique()

            for i in list_of_clusters:

                logging.info("start model training for cluster {}".format(i))
                cluster_data = X[X['Cluster'] == i]

                cluster_features = cluster_data.drop(['Labels','Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1/3, random_state=355)
                model_finder = Model_Finder()
                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

                file_op = File_Operations()
                file_op.save_model(best_model, best_model_name+str(i))
            logging.info("model training pipeline execution complete")

        except WaferException as e:
            raise WaferException(e, sys)