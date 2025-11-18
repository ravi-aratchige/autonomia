"""Contains chat models and chat model connection managers to use in workflows."""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from settings import GOOGLE_CHAT_MODEL_NAME


class GoogleChatModel:
    """Generate a single instance of a Google chat model."""

    def __new__(cls, temperature=0.7, model=GOOGLE_CHAT_MODEL_NAME):
        """Create and return a single instance of Groq's chat model.

        Args:
            temperature (float, optional): The temperature (creativity) of the model. Defaults to 0.5.
            model (str, optional): The foundational model to be selected.

        Returns:
            ChatGroq: instance of Groq's chat model
        """

        # Load model API key
        load_dotenv()
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        # Instantiate and return model from `langchain_google_genai.ChatGoogleGenerativeAI`
        model_instance = ChatGoogleGenerativeAI(
            temperature=temperature,
            model=model,
        )

        return model_instance


class GoogleChatModelConnection:
    """Generate a connection to access Google's chat models."""

    def __init__(self, temperature=0.5, model=GOOGLE_CHAT_MODEL_NAME):
        """Constructor to initialize connection to Google's chat model.

        Args:
            temperature (float, optional): The temperature (creativity) of the model. Defaults to 0.5.
            model (str, optional): The foundational model to be selected.
        """

        # Load model API key
        load_dotenv()
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        # Initialize model configurations from input parameters
        self.temperature = temperature
        self.model: str = model

        # Instantiate model from `langchain_google_genai.ChatGoogleGenerativeAI`
        self._model = ChatGoogleGenerativeAI(
            temperature=self.temperature,
            model=self.model,
        )

    @property
    def model(self):
        """Return an instance of the model.

        Returns:
            ChatGroq: instance of Groq's chat model
        """

        return self._model


# Make module exportable
if __name__ == "__main__":
    pass
