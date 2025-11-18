from langchain_core.tools import Tool

from browser.base import BaseToolkit


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

        self.driver.get(
            f"https://www.reuters.com/site-search/?query={query.replace(' ', '+')}&offset=0"
        )

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
        ]


if __name__ == "__main__":
    pass
