import pandas as pd
import pymongo
from wafer.logger import logging
from wafer.exception import WaferException
import sys
from os import listdir
import json
import warnings
warnings.filterwarnings('ignore')


class Prediction_DB_Operation:
    def __init__(self):
        self.goodFilePath = "wafer/prediction/prediction_artifact/Good_Data"
        self.badFilePath = "wafer/prediction/prediction_artifact/Bad_Data"
        with open("wafer/constant/prediction_schema_DBoperation.json", "r") as f:
            dic = json.load(f)
            f.close()
        self.dbname = dic["dbname"]
        self.collectionName = dic['collectionName']
        self.mongodb = dic['mongodb']
        client = pymongo.MongoClient(self.mongodb)
        self.DBConnection = client[self.dbname]
        self.collectionConnection = self.DBConnection[self.collectionName]

    def loadData(self):
        try:
            for file in listdir("wafer/prediction/prediction_artifact/Good_Raw"):
                data = pd.read_csv("wafer/prediction/prediction_artifact/Good_Raw/"+file)
                self.collectionConnection.insert_many(data.to_dict(orient='record'))

            logging.info("prediction data load to database complete")
        except WaferException as e:
            raise WaferException(e, sys)

    def readData(self):
        try:
            data = pd.DataFrame(list(self.collectionConnection.find()))
            data.drop('_id', axis=1, inplace=True)
            data.to_csv("wafer/prediction/prediction_artifact/Prediction_data.csv", index=False)

            logging.info("prediction data extraction complete")
        except WaferException as e:
            raise WaferException(e, sys)
