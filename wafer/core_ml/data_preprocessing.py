import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from wafer.logger import logging
from wafer.exception import WaferException
import sys
import pickle


class Preprocessor:

    def __init__(self):
        self.col_to_drop = None
        self.new_data = None
        self.y = None
        self.columns = None
        self.X = None
        self.new_array = None
        self.null_count = None
        self.data = None

    def get_data(self, path):
        try:
            self.data = pd.read_csv(path)

            self.data = self.data[self.data['Good/Bad'] == -1].replace(-1, 0)
            logging.info("Data loaded for model training")
            return self.data
        except WaferException as e:
            raise WaferException(e, sys)

    def remove_column(self, data, columns):
        try:
            self.columns = columns
            data.drop(columns, axis=1, inplace=True)
            
            logging.info("removed unwanted columns: {}".format(columns))

            return data
        except WaferException as e:
            raise WaferException(e, sys)

    def separate_label_feature(self, data, label_column_name):
        try:
            self.X = data.drop(label_column_name, axis=1)
            self.y = data[label_column_name]

            logging.info("Label & features separated")
            return self.X, self.y
        except WaferException as e:
            raise WaferException(e, sys)

    def is_null_present(self, data):
        try:
            flage = 0
            self.null_count = self.data.isna().sum()

            for i in self.null_count:
                if i > 0:
                    flage = 1

            if flage == 1:
                df_with_null = pd.DataFrame()
                df_with_null['columns'] = self.data.columns
                df_with_null['missing_value_count'] = np.asarray(self.data.isna().sum())
                df_with_null = df_with_null[df_with_null.missing_value_count > 0]
                df_with_null.to_csv("wafer/core_ml/data_preprocessing/null_value.csv", index=False)
                logging.info("Null value present")

            if flage == 0:
                logging.info("Null value absent")

            return flage
        except WaferException as e:
            raise WaferException(e, sys)

    def null_value_impute(self, data):
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)

            self.new_array = imputer.fit_transform(self.data)
            self.new_data = pd.DataFrame(data=self.new_array, columns=self.data.columns)

            imputer = imputer.fit(self.data)
            with open("wafer/core_ml/data_preprocessing/imputer_object.sav", 'wb') as f:
                pickle.dump(imputer, f)

            logging.info("missing value imputation complete")
            return self.new_data
        except WaferException as e:
            raise WaferException(e, sys)

    def get_columns_with_zero_std_deviation(self, data):
        data = self.remove_column(data, 'Wafer')
        columns = data.columns
        data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in columns:
                if data_n[x]['std'] == 0:  # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            df = pd.DataFrame(self.col_to_drop)
            df.columns = ['col_to_drop']
            df.to_csv('wafer/core_ml/data_preprocessing/Col_to_drop_with_zero_STD.csv', index=False, header=True)
            logging.info("0 STD columns list prepared")
            return self.col_to_drop
        except WaferException as e:
            raise WaferException(e, sys)

