from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import BaseMessage

from assistant.prompt import BrowserAssistantPromptTemplate
from browser.core import CoreBrowserToolkit
from browser.news import NewsToolkit
from browser.search import SearchToolkit
from browser.youtube import YoutubeToolkit
from providers.google import GoogleChatModel
from providers.groq import GroqChatModel
from settings import AGENT_VERBOSITY
from utils.logging import ApplicationLogger


class BrowserAssistantBuilder:
    def __init__(self):
        # Initialize logger
        self.logger = ApplicationLogger.get_logger()

        # Initialize model to be used by agent
        self.model = GoogleChatModel()

        # Load tools
        core_tools = CoreBrowserToolkit()
        search_tools = SearchToolkit()
        youtube_tools = YoutubeToolkit()
        news_tools = NewsToolkit()

        # Build agent tool suite from toolkits
        self.tool_suite = (
            core_tools.get_tools()
            + search_tools.get_tools()
            + youtube_tools.get_tools()
            + news_tools.get_tools()
        )

        # Define agent instruction prompt
        self.prompt = BrowserAssistantPromptTemplate()

        # Create agent with tool-calling capabilities
        agent = create_tool_calling_agent(
            self.model,
            self.tool_suite,
            self.prompt,
        )

        # Define agent executor runtime
        self.runnable_agent = AgentExecutor(
            agent=agent,
            tools=self.tool_suite,
            verbose=AGENT_VERBOSITY,
        )

    def get_prompt(self):
        return self.prompt

    def execute_action(self, user_input: str, chat_history: list[BaseMessage]):
        try:
            response = self.runnable_agent.invoke(
                {
                    "input": user_input,
                    "chat_history": chat_history,
                }
            )

            return response["output"]
        except Exception as e:
            self.logger.error("The assistant crashed when executing an action.")
            print(str(e))

            return f"Sorry, the assistant encountered an error: {e}"


# Make module safely exportable
if __name__ == "__main__":
    pass
