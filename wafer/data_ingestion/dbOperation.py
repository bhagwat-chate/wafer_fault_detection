import pandas as pd
import pymongo
from wafer.logger import logging
from wafer.exception import WaferException
import sys, os
from os import listdir
import json
class DB_Operation:
    def __init__(self):
        self.goodFilePath = "wafer/data_ingestion/Training_raw_files_validated/Good_Raw"
        self.badFilePath = "wafer/data_ingestion/Training_raw_files_validated/Bad_Raw"
        with open("wafer/constant/DBOperation.json","r") as f:
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
            for file in listdir("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"):
                data = pd.read_csv("wafer/data_ingestion/Training_raw_files_validated/Good_Raw/"+file)
                self.collectionConnection.insert_many(data.to_dict(orient='record'))
            logging.info("data load successful!")

        except WaferException as e:
            raise WaferException(e, sys)

    def readData(self):
        try:
            data = pd.DataFrame(list(self.collectionConnection.find()))
            data.drop('_id', axis=1, inplace=True)
            data.to_csv("wafer/data_ingestion/Training_raw_files_validated/Training_data.csv", index=False)

            logging.info("data extraction successful!")
        except WaferException as e:
            raise WaferException(e, sys)