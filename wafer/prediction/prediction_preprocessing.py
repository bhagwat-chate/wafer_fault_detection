import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer, SimpleImputer
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import pickle


class Preprocessor:
    def __init__(self):
        self.col_to_drop = None
        self.new_data = None
        self.new_array = None
        self.null_count = None
        self.columns = None
        self.data = None

    def get_data(self, path):
        try:
            pass
        except WaferException as e:
            raise WaferException(e, sys)

    def remove_column(self, data):
        try:

            zero_std_col = pd.read_csv("wafer/core_ml/data_preprocessing/Col_to_drop_with_zero_STD.csv")
            null_value_col = pd.read_csv("wafer/core_ml/data_preprocessing/null_value.csv")
            li1 = zero_std_col['col_to_drop'].to_list()
            li2 = null_value_col['columns'].to_list()
            all_col_for_deletion = li1+li2

            all_col_for_deletion.remove('Good/Bad')
            data.drop(all_col_for_deletion, axis=1, inplace=True)

            logging.info("removed unwanted columns: {}".format(all_col_for_deletion))

            return data
        except WaferException as e:
            raise WaferException(e, sys)

    def null_value_impute(self, data):
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            imputer = imputer.fit(data)
            self.new_array = imputer.fit_transform(data)
            self.new_data = pd.DataFrame(data=self.new_array, columns=data.columns)

            logging.info("missing value imputation complete")
            return self.new_data
        except WaferException as e:
            raise WaferException(e, sys)
