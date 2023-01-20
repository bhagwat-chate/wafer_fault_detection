from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline
from wafer.pipeline.prediction_pipeline import Prediction_Pipeline
from wafer.logger import logging
from wafer.exception import WaferException
import sys, os, json

from flask import Flask, request, render_template
from flask import Response
import os, json
from flask_cors import CORS, cross_origin

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['path']

            prediction_pipeline_obj = Prediction_Pipeline()
            path, json_predictions = prediction_pipeline_obj.prediction_pipeline_execution(path)
            return Response("Prediction File created: " +str(path) +' and few of the predictions are '+str(json.loads(json_predictions)))

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

        # prediction_pipeline = Prediction_Pipeline()
        # prediction_pipeline.prediction_pipeline_execution('path')

        app.run(debug=True)
        logging.info("END OF WAFER FAULT DETECTION PROJECT EXECUTION")

    except WaferException as e:
        raise WaferException(e, sys)