from browser.base import BaseToolkit
from langchain_core.tools import Tool
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SearchToolkit(BaseToolkit):
    """Toolkit for working with the Google website.

    Args:
        BaseToolkit (class): the base class for building concrete toolkits.
    """

    def __init__(self):
        super().__init__()

    # *******************************************************
    #                        TOOLS
    # *******************************************************

    def go_to_search(self):
        """Navigate to the search website. Does not take in any arguments."""

        self.logger.info("The `go_to_search` tool has been invoked.")

        # Navigate to the search website
        self.driver.get("https://www.startpage.com")

    def perform_search(self, search_str: str):
        """Perform a search. Input should be the search query as a string."""

        self.logger.info(
            f"The `perform_search` tool has been invoked with `{search_str}` as input."
        )

        # Check if already on search website or not
        if "startpage" not in self.driver.current_url.lower():
            self.driver.get("https://www.startpage.com")

        # Select searchbar and enter search query
        searchbar = self.driver.find_element(By.CLASS_NAME, "search-form-input")
        searchbar.click()
        searchbar.clear()
        searchbar.send_keys(search_str)
        searchbar.send_keys(Keys.ENTER)

    def open_search_result(self, index: int):
        """Open an article after the search result. Does not take in any arguments."""

        self.logger.info(
            f"The `open_search_result` tool has been invoked with index {index}."
        )

        # Navigate to the search website
        self.driver.get("https://www.startpage.com")

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    def get_tools(self) -> list[Tool]:
        """Exposes the Search toolkit's tools to the assistant.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        return [
            Tool(
                name="go_to_search",
                func=lambda _: self.go_to_search(),
                description=self.get_tool_docstring(self.go_to_search),
            ),
        ]


if __name__ == "__main__":
    pass
