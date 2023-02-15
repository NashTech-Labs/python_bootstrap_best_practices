"""Module providing functions for deploying a flask app"""
import logging
import os
import time

import werkzeug.exceptions
from flask import Flask, jsonify, request
from waitress import serve
from werkzeug.utils import secure_filename

from lib import error_handlers
from lib.config_validator import ConfigValidator
from lib.logger import Logger
from lib.preprocessor import Preprocessor
from lib.rasa_agent import RasaAgent
from lib.response_creator import ResponseCreator

# Initializing flask application
app = Flask(__name__)


def allowed_file(filename):
    """checks for allowed file"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """stores the response from rasa model"""
    timestamp = time.strftime("[%Y-%b-%d %H:%M]")
    logging.info(
        "%s %s %s %s %s %s",
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status,
    )
    return response


@app.route("/ping", methods=["GET"])
def ping():
    """health check"""
    ping_response = jsonify({"status": "OK"}), 200
    return ping_response


@app.route("/invocations", methods=["POST"])
def transformations():
    """POST request and returns ML model response"""
    # check if the post request has the file part
    if "file" not in request.files:
        raise werkzeug.exceptions.BadRequest()

    # getting the file
    file = request.files["file"]

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        raise werkzeug.exceptions.BadRequest()

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename == "":
            raise werkzeug.exceptions.BadRequest()

        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # if not proc.validate_file(UPLOAD_FOLDER, filename):
        #    raise werkzeug.exceptions.BadRequest()

        # proc.download_all_attachments(EXTRACT_FOLDER)
        proc.pdf_extract(EXTRACT_FOLDER, UPLOAD_FOLDER, filename)
        # data_pattern = proc.extract_patterns()
        data_pattern = proc.extract_pdf_patterns()

        predictions = rasaAgent.get_predictions(data_pattern["pattern"])
        result = responseCreator.get_response(predictions)

        proc.clean()

        return jsonify(result), 201
        # return jsonify({"message": "Hello, all set"}), 201
    else:
        raise werkzeug.exceptions.BadRequest()


if __name__ == "__main__":
    # setting up the logs
    fileLogger = Logger()
    fileLogger.initialize()

    # validating and loading configurations from config.ini
    validator = ConfigValidator()
    config = validator.validate_and_getconfig()

    # setting log level
    fileLogger.set_log_level(config["log_level"])

    # Initializing api variables
    EXTRACT_FOLDER = config["extract_folder"]
    UPLOAD_FOLDER = config["upload_folder"]
    ALLOWED_EXTENSIONS = config["extensions"]

    # Loading Rasa-NLU model
    rasaAgent = RasaAgent()
    rasaAgent.load_model(config["model_path"])

    # Instantiating response_creator object
    responseCreator = ResponseCreator()

    # Instantiating data preprocessor object
    proc = Preprocessor()

    # max size of the file to be uploaded
    app.config["MAX_CONTENT_LENGTH"] = config["max_content_length_mib"]

    # register the error handlers
    app.register_blueprint(error_handlers.blueprint)

    # Starting the server
    serve(app, host=config["host"], port=config["port"])
