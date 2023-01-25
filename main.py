from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline
from wafer.pipeline.prediction_pipeline import Prediction_Pipeline
from wafer.logger import logging
from wafer.exception import WaferException
import sys, os, json, requests
import flask_monitoringdashboard as dashboard

from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

url = 'http://example.com/api/predict'
data = {'input': 'example input'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['path']

            prediction_pipeline_obj = Prediction_Pipeline()
            path, json_predictions = prediction_pipeline_obj.prediction_pipeline_execution(path)
            return Response("Prediction File created: " +str(path) +' and few of the predictions are '+str(json.loads(json_predictions)))

        if request.form is not None:
            path = request.form['path']

            prediction_pipeline_obj = Prediction_Pipeline()
            path, json_predictions = prediction_pipeline_obj.prediction_pipeline_execution(path)
            return Response("Prediction File created: " +(path) +'and few of the predictions are'+(json.loads(json_predictions)))

            # return render_template('results.html', result=json_predictions)
        else:
            print('Nothing Matched')

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)


if __name__ == '__main__':
    try:
        logging.info("START OF WAFER FAULT DETECTION PROJECT EXECUTION")

        # data_ingestion = TrainingDataPipeline()
        # data_ingestion.train_data_validation()

        # model_training = Model_Training_Pipeline()
        # model_training.train_model()

        prediction_pipeline = Prediction_Pipeline()
        prediction_pipeline.prediction_pipeline_execution('path')

        # app.run(host="0.0.0.0", port=5000)
        # logging.info("END OF WAFER FAULT DETECTION PROJECT EXECUTION")

    except WaferException as e:
        raise WaferException(e, sys)