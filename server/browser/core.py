from browser.base import BaseToolkit
from langchain_core.tools import Tool
from settings import PARLOR_TRICK_WEBPAGE
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CoreBrowserToolkit(BaseToolkit):
    """Toolkit for manipulating the core functionality of the browser.

    Includes features such as scrolling, debugging and more.

    Args:
        BaseToolkit (class): the base class for building concrete toolkits.
    """

    def __init__(self):
        super().__init__()

    # *******************************************************
    #                        TOOLS
    # *******************************************************

    def debug_assistant(self):
        """Debug the assistant. Does not take in any arguments."""

        self.logger.info("The assistant shows a parlor trick to impress the user.")

        self.driver.get(PARLOR_TRICK_WEBPAGE)

    def scroll_up(self):
        """Scroll up the webpage. Does not take in any arguments."""

        self.logger.info("The `scroll_up` tool has been invoked.")

        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_UP)

    def scroll_down(self):
        """Scroll down the webpage. Does not take in any arguments."""

        self.logger.info("The `scroll_down` tool has been invoked.")

        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)

    def refresh_page(self):
        """Refresh the webpage. Does not take in any arguments."""

        self.logger.info("The `refresh_page` tool has been invoked.")

        self.driver.refresh()

    def open_new_tab(self):
        """Open a new tab. Does not take in any arguments."""

        self.logger.info("The `open_new_tab` tool has been invoked.")

        self.driver.switch_to.new_window("tab")

    def maximize_browser(self):
        """Maximize the browser. Does not take in any arguments."""

        self.driver.maximize_window()

    def take_screenshot(self):
        """Takes a screenshot. Does not take in any arguments."""

        self.driver.save_screenshot()

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    def get_tools(self) -> list[Tool]:
        """Exposes the the core browser toolkit's tools to the assistant.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        return [
            Tool(
                name="debug_assistant",
                func=lambda _: self.debug_assistant(),
                description=self.get_tool_docstring(self.debug_assistant),
            ),
            Tool(
                name="scroll_up",
                func=lambda _: self.scroll_up(),
                description=self.get_tool_docstring(self.scroll_up),
            ),
            Tool(
                name="scroll_down",
                func=lambda _: self.scroll_down(),
                description=self.get_tool_docstring(self.scroll_down),
            ),
            Tool(
                name="refresh_page",
                func=lambda _: self.refresh_page(),
                description=self.get_tool_docstring(self.refresh_page),
            ),
            Tool(
                name="open_new_tab",
                func=lambda _: self.open_new_tab(),
                description=self.get_tool_docstring(self.open_new_tab),
            ),
            Tool(
                name="maximize_browser",
                func=lambda _: self.maximize_browser(),
                description=self.get_tool_docstring(self.maximize_browser),
            ),
            Tool(
                name="take_screenshot",
                func=lambda _: self.take_screenshot(),
                description=self.get_tool_docstring(self.take_screenshot),
            ),
        ]


if __name__ == "__main__":
    pass
