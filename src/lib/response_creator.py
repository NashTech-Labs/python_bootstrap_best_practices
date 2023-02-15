"""Module to create a json response """
import copy
from datetime import datetime


class ResponseCreator:
    """Response creation"""

    def __init__(self):
        """JSON variable constraints"""
        self.action = ""
        self.serial = ""
        self.asset = ""
        self.destination = ""
        self.address = ""
        self.email = ""
        self.data_to_update = ""
        self.io_dict = {
            "input": None,
            "output": {
                "intentIdentified": None,
                "entitiesIdentified": {
                    "action": None,
                    "serialNo": None,
                    "asset": None,
                    "destination": None,
                    "address": None,
                    "email": None,
                    "data_to_update": None,
                },
            },
        }
        self.resp_dict = {"applicationName": "HAPAG_FIS", "dateTime": "", "data": []}

    def get_response(self, predictions: list):
        """Fetching response from model and updating JSON
        returns json
        """
        response = copy.deepcopy(self.resp_dict)
        response["dateTime"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        action = self.action
        serial = self.serial
        asset = self.asset
        destination = self.destination
        address = self.address
        email = self.email
        data_to_update = self.data_to_update

        for i, prediction in enumerate(predictions):
            intent = prediction["intent"]["name"]
            for entity in prediction["entities"]:
                if entity["entity"] == "action":
                    action = entity["value"]
                elif entity["entity"] == "serial_no":
                    serial = entity["value"]
                elif entity["entity"] == "asset":
                    asset = entity["value"]
                elif entity["entity"] == "destination":
                    serial = entity["value"]
                elif entity["entity"] == "address":
                    serial = entity["value"]
                elif entity["entity"] == "email":
                    serial = entity["value"]
                elif entity["entity"] == "data_to_update":
                    serial = entity["value"]

            response["data"].append(copy.deepcopy(self.io_dict))
            response["data"][i]["input"] = prediction["text"]
            response["data"][i]["output"]["intentIdentified"] = intent
            response["data"][i]["output"]["entitiesIdentified"]["action"] = action
            response["data"][i]["output"]["entitiesIdentified"]["serialNo"] = serial
            response["data"][i]["output"]["entitiesIdentified"]["asset"] = asset
            response["data"][i]["output"]["entitiesIdentified"]["destination"] = destination
            response["data"][i]["output"]["entitiesIdentified"]["address"] = address
            response["data"][i]["output"]["entitiesIdentified"]["email"] = email
            response["data"][i]["output"]["entitiesIdentified"]["data_to_update"] = data_to_update

        return response
