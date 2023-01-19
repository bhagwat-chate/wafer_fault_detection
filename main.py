from wafer.pipeline.data_ingestion_pipeline import TrainingDataPipeline
from wafer.pipeline.model_training_pipeline import Model_Training_Pipeline
from wafer.pipeline.prediction_pipeline import Prediction_Pipeline
from wafer.logger import logging
from wafer.exception import WaferException
import sys, os

from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
# import flask_monitordashboard as dashboard
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
# dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            prediction_pipeline_obj = Prediction_Pipeline()
            prediction_pipeline_obj.prediction_pipeline_execution(path)

        elif request.form is not None:
            path = request.json['filepath']
            prediction_pipeline_obj = Prediction_Pipeline()
            prediction_pipeline_obj.prediction_pipeline_execution(path)

        else:
            print("Nothing Matched")

    except WaferException as e:
        raise WaferException(e, sys)
    except ValueError:
        return Response("Error occurred: %s"%ValueError)
    except KeyError:
        return Response("Error occurred: %s"%KeyError)
    except Exception as e:
        return Response("Error occurred: %s"%e)


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['FolderPath']
            model_training_pipeline_obj = Model_Training_Pipeline()
            model_training_pipeline_obj.train_model(path)

    except WaferException as e:
        raise WaferException(e, sys)
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

    return Response("Model Training Successfully complete")


if __name__ == '__main__':
    try:
        logging.info("START OF WAFER FAULT DETECTION PROJECT EXECUTION")

        # data_ingestion = TrainingDataPipeline()
        # data_ingestion.train_data_validation()

        # model_training = Model_Training_Pipeline()
        # model_training.train_model()

        # prediction_pipeline = Prediction_Pipeline()
        # prediction_pipeline.prediction_pipeline_execution()

        app.run(debug=True)
        logging.info("END OF WAFER FAULT DETECTION PROJECT EXECUTION")

    except WaferException as e:
        raise WaferException(e, sys)