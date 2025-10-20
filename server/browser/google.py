from browser.base import BaseToolkit
from langchain_core.tools import Tool


class GoogleToolkit(BaseToolkit):
    """Toolkit for working with the Google website.

    Args:
        BaseToolkit (class): the base class for building concrete toolkits.
    """

    def __init__(self):
        super().__init__()

    # *******************************************************
    #                        TOOLS
    # *******************************************************

    def open_google(self):
        """Navigate to the Google website. Does not take in any arguments."""

        self.logger.info("The `open_google` tool has been invoked.")

        # Navigate to the Google website
        self.driver.get("https://www.google.com")

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    def get_tools(self) -> list[Tool]:
        """Exposes the Google toolkit's tools to the assistant.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        return [
            Tool(
                name="open_google",
                func=lambda _: self.open_google(),
                description=self.get_tool_docstring(self.open_google),
            ),
        ]


if __name__ == "__main__":
    pass
