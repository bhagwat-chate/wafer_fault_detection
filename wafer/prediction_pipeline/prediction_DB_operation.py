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

        with open("wafer/constant/secrets/credentials.json", "r") as f1:
            credential = json.load(f1)
            f1.close()

        self.dbname = dic["dbname"]
        self.collectionName = dic['collectionName']
        self.mongodb = dic['mongodb']

        self.username = credential['username']
        self.password = credential["password"]

        self.mongodb = self.mongodb.replace("username", self.username)
        self.mongodb = self.mongodb.replace("password", self.password)

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
            data.drop(['_id'], axis=1, inplace=True)
            data.rename(columns={'Unnamed: 0': 'wafer'}, inplace=True)
            # data.to_csv("wafer/prediction_pipeline/prediction_artifact/data_for_prediction.csv", index=False)
            data.to_json("wafer/prediction_pipeline/prediction_artifact/data_for_prediction.json")

            logging.info("prediction data extraction from MongoDB complete!")
            return data
        except WaferException as e:
            raise WaferException(e, sys)