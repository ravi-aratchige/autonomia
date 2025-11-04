from abc import ABC, abstractmethod
from langchain_core.tools import Tool
from utils.logging import ApplicationLogger
from browser.driver import BrowserDriverManager


class BaseToolkit(ABC):
    """Abstract toolkit for developing custom toolkits for the assistant.

    CAUTION: please ensure all tools have descriptive docstrings.

    Args:
        ABC (class): "Abstract Base Class"
    """

    def __init__(self):
        self.driver = BrowserDriverManager.get_driver()
        self.logger = ApplicationLogger.get_logger()

    # *******************************************************
    #                    CLASS METHODS
    # *******************************************************

    def get_tool_docstring(self, fn) -> str:
        """Retrieve the docstring for a tool from a toolkit.

        All tools are required to have a docstring for the agent to operate them.

        Args:
            fn (function): tool function.

        Raises:
            ValueError: error if tool is missing its docstring.

        Returns:
            str: the tool's docstring.
        """

        # Check if it's a class or static method
        if isinstance(fn, (classmethod, staticmethod)):
            fn = fn.__func__

        doc = fn.__doc__

        if not doc:
            err = f"The `{getattr(fn, '__name__', str(fn))}` tool is missing its docstring."
            self.logger.error(err)
            raise ValueError(err)

        return doc.strip()

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    @abstractmethod
    def get_tools(self) -> list[Tool]:
        """Exposes the toolkit's tools to the assistant. Implement in concrete subclasses.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        err = f"{self.__class__.__name__} has not implemented the tool registry!"
        self.logger.error(err)
        raise NotImplementedError(err)
