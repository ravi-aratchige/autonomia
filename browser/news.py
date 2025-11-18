import re

from langchain_core.tools import Tool
from selenium.webdriver.common.by import By

from browser.base import BaseToolkit
from settings import FOREIGN_NEWS_SERVICE


class NewsToolkit(BaseToolkit):
    """Toolkit for working with news websites.

    Args:
        BaseToolkit (class): the base class for building concrete toolkits.
    """

    def __init__(self) -> None:
        super().__init__()

    # *******************************************************
    #                        TOOLS
    # *******************************************************

    def search_news(self, query: str):
        """Search for news. Input should be the search query as a string."""

        self.logger.info(
            f"The `search_news` tool has been invoked with `{query}` as input."
        )

        if FOREIGN_NEWS_SERVICE == "nbcnews":
            self.driver.get(
                f"https://www.nbcnews.com/search/?q={query.replace(' ', '+')}"
            )
        else:
            self.driver.get(
                f"https://www.reuters.com/site-search/?query={query.replace(' ', '+')}&offset=0"
            )

    # *******************************************************

    def open_news_article(self, index: int):
        """Open a specific news article on the news search results page.
        Takes in the index of the article to be opened.
        For example, `index=1` to open the first article.
        `index=10` opens the last article in the page."""

        self.logger.info(
            f"The `open_news_article` tool has been invoked with index {index}."
        )

        if FOREIGN_NEWS_SERVICE == "nbcnews":
            # Select article URLs from the search result page
            articles = self.driver.find_elements(By.CLASS_NAME, "item_text_content")

        # Click the relevant article
        article_to_open = articles[int(re.search(r"\d+", index).group()) - 1]
        article_to_open.click()

        # Switch Selenium context to newly opened tab
        # (Startpage opens results in a new tab)
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])

    # *******************************************************
    #                    TOOL REGISTRY
    # *******************************************************

    def get_tools(self) -> list[Tool]:
        """Exposes the News toolkit's tools to the assistant.

        Returns:
            list[Tool]: list of LangChain-standard tools.
        """

        return [
            Tool(
                name="search_news",
                func=self.search_news,
                description=self.get_tool_docstring(self.search_news),
            ),
            Tool(
                name="open_news_article",
                func=self.open_news_article,
                description=self.get_tool_docstring(self.open_news_article),
            ),
        ]


if __name__ == "__main__":
    pass
