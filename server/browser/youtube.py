from browser.base import BaseToolkit
from langchain_core.tools import Tool
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class YoutubeToolkit(BaseToolkit):
    """Toolkit for working with the YouTube website.

    Args:
        BaseToolkit (class): the base class for building concrete toolkits.
    """

    def __init__(self):
        super().__init__()

    # *******************************************************
    #                        TOOLS
    # *******************************************************

    def open_youtube(self):
        """Open the YouTube website. Does not take in any arguments."""

        self.logger.info("The `open_youtube` tool has been invoked.")

        # Navigate to YouTube
        self.driver.get("https://www.youtube.com")

    def search_on_youtube(self, search_str: str):
        """Search for a video on YouTube. Input should be the search query as a string."""

        self.logger.info("The `search_on_youtube` tool has been invoked.")

        # Check if already on YouTube or not
        if "youtube" not in self.driver.current_url.lower():
            self.driver.get("https://www.youtube.com")

        # Select searchbar
        searchbar = self.driver.find_element(By.NAME, "search_query")
        searchbar.click()
        searchbar.clear()
        searchbar.send_keys(search_str)
        searchbar.send_keys(Keys.ENTER)

    def select_search_result_by_video_title(self, input_video_title: str):
        """Click on a search result in YouTube. Input must be the video title or part of it as a string."""

        self.logger.info(
            "The `select_search_result_by_video_title` tool has been invoked."
        )

        # Check whether in search results page or not
        if "youtube.com/results" not in self.driver.current_url.lower():
            self.logger.warning(
                "The browser is not in the YouTube search results page."
            )

            return """The browser is not in the search results page.
            Check the conversation history and perform the search first."""

        # Get list of video titles from the search results
        video_titles = self.driver.find_elements(By.ID, "video-title")

        for title in video_titles:
            # Check whether each video title contains the provided information
            if input_video_title.lower() in title.get_attribute("title").lower():
                self.logger.info("Found the YouTube search result the user requested.")

                # Click the correct video and exit the loop
                title.click()
                break

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    def get_tools(self) -> list[Tool]:
        """Exposes the YouTube toolkit's tools to the assistant.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        return [
            Tool(
                name="open_youtube",
                func=lambda _: self.open_youtube(),
                description=self.get_tool_docstring(self.open_youtube),
            ),
            Tool(
                name="search_on_youtube",
                func=self.search_on_youtube,
                description=self.get_tool_docstring(self.search_on_youtube),
            ),
            Tool(
                name="select_search_result_by_video_title",
                func=self.select_search_result_by_video_title,
                description=self.get_tool_docstring(
                    self.select_search_result_by_video_title
                ),
            ),
        ]


if __name__ == "__main__":
    pass
