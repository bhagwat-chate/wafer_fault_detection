# from logger import logging
# from exception import SensorException
import os, sys
from wafer.logger import logging
from wafer.exception import WaferException
class Test:

    def __init__(self):
        pass

    def my_func(self):
        try:
            logging.info("Hello! this is logger")

            x = 1/0

        except Exception as e:
            raise Exception(e, sys)