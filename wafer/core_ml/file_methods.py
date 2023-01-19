import pickle
import os
import sys
import shutil
from wafer.logger import logging
from wafer.exception import WaferException


class File_Operations:

    def __init__(self):
        self.list_of_model_files = None
        self.cluster_number = None
        self.folder_name = None
        self.list_of_files = None
        self.model_name = None
        self.model_directory = "wafer/core_ml/models"

    def save_model(self, model, filename):
        try:
            path = os.path.join(self.model_directory, filename)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + '/' + filename + '.sav', 'wb') as f:
                pickle.dump(model, f)

            logging.info("Model file '{v1}' saved at location '{v2}'".format(v1=filename, v2=path))

        except WaferException as e:
            raise WaferException(e, sys)

    def load_model(self, filename):
        try:
            with open(self.model_directory + filename + '/' + filename + 'sav', 'rb') as f:
                logging.info("Model file '{}' load successful".format(filename))

                return pickle.load(f)
        except WaferException as e:
            raise WaferException(e, sys)

    def load_model_prediction(self, filename):
        try:
            with open(self.model_directory + '/' + filename + '/' + filename + '.sav', 'rb') as f:
                logging.info("Model file '{}' load successful".format(filename))

                return pickle.load(f)
        except WaferException as e:
            raise WaferException(e, sys)

    def find_correct_model_file(self, cluster_number):
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)

            for self.file in self.list_of_files:
                if self.file.index(str(self.cluster_number)) != 1:
                    self.model_name = self.file
                else:
                    continue
            self.model_name = self.model_name.split('.')[0]
            logging.info("Model file find successful")

            return self.model_name
        except WaferException as e:
            raise WaferException(e, sys)