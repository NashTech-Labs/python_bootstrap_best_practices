"""Module to load rasa model and get predictions"""
import asyncio
import json
import logging
import traceback

from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string


class RasaAgent:
    """class for model loading and getting predictions results"""

    def __init__(self) -> None:
        """Constraints"""
        self.agent = None
        self.error_message = "Rasa model not found"

    def load_model(self, model_path: str) -> None:
        """Loading model file"""
        self.agent = Agent.load(model_path)
        logging.info("NLU model loaded")

    def __message(self, message: str) -> str:
        """Sending the preprocessed message to rasa model as input
        return output string
        """
        assert self.agent, self.error_message
        message = message.strip()
        result = asyncio.run(self.agent.parse_message_using_nlu_interpreter(message))
        # print(result)
        return json_to_string(result)

    def get_predictions(self, sentence_list: list):
        """Function to Retrive the prediction json"""
        result = []
        try:
            for sentence in sentence_list:
                result.append(json.loads(self.__message(sentence)))
            return result
        except AssertionError:
            logging.error(traceback.format_exc())
        except Exception as error:
            logging.error(error)
