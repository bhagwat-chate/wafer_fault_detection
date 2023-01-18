from wafer.logger import logging
from wafer.exception import WaferException
import os, sys
import json
import pymongo
import pandas as pd

class Prediction_DB_Operation:

    def __init__(self):
        with open("wafer/constant/prediction_schema_DBoperation.json", "r") as f:
            dic = json.load(f)
            f.close()
        self.dbname = dic["dbname"]
        self.collectionName = dic['collectionName']
        self.mongodb = dic['mongodb']
        client = pymongo.MongoClient(self.mongodb)
        self.DBConnection = client[self.dbname]
        self.collectionConnection = self.DBConnection[self.collectionName]


    def load_data(self):
        try:
            for file in os.listdir("wafer/prediction_pipeline/prediction_artifact/Good_data/"):
                data = pd.read_csv("wafer/prediction_pipeline/prediction_artifact/Good_data/"+file)
                self.collectionConnection.insert_many(data.to_dict(orient='record'))

            logging.info("data load into MongoDB complete")

        except WaferException as e:
            raise WaferException(e, sys)

    def get_data(self):
        try:
            data = pd.DataFrame(list(self.collectionConnection.find()))
            data.drop(['_id', 'Unnamed: 0'], axis=1, inplace=True)
            data.to_csv("wafer/data_ingestion/Data_Export/Training_data.csv", index=False)

            logging.info("prediction data extraction from MongoDB complete!")
            return data
        except WaferException as e:
            raise WaferException(e, sys)