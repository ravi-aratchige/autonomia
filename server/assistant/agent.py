from settings import AGENT_VERBOSITY
from browser.google import GoogleToolkit
from browser.youtube import YoutubeToolkit
from browser.core import CoreBrowserToolkit
from providers.chat_models import GroqChatModel
from assistant.prompt import BrowserAssistantPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

from utils.logging import ApplicationLogger


class BrowserAssistantBuilder:
    def __init__(self):
        # Initialize logger
        self.logger = ApplicationLogger.get_logger()

        # Initialize model to be used by agent
        self.model = GroqChatModel()

        # Load tools
        core_tools = CoreBrowserToolkit()
        google_tools = GoogleToolkit()
        youtube_tools = YoutubeToolkit()

        # Build agent tool suite from toolkits
        self.tool_suite = (
            core_tools.get_tools()
            + google_tools.get_tools()
            + youtube_tools.get_tools()
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

    def debug_prompt(self):
        return self.prompt

    def execute_action(self, user_input, chat_history):
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

            return f"Sorry, the assistant encountered an error: {e}"


# Make module safely exportable
if __name__ == "__main__":
    pass
