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
        """
        loads nlu model
        :param model_path: model directory
        :return:
        """
        self.agent = Agent.load(model_path)
        logging.info("NLU model loaded")

    def __message(self, message: str) -> str:
        """
        :param message: input pattern txt
        :return: result string
        """
        assert self.agent, self.error_message
        message = message.strip()
        result = asyncio.run(self.agent.parse_message_using_nlu_interpreter(message))
        return json_to_string(result)

    def get_predictions(self, sentence_list: list):
        """
        Function to Retrieve the prediction
        :param sentence_list: predicted sentences
        :return: json result
        """
        result = []
        try:
            for sentence in sentence_list:
                result.append(json.loads(self.__message(sentence)))
            return result
        except AssertionError:
            logging.error(traceback.format_exc())
        except Exception as error:
            logging.error(error)
