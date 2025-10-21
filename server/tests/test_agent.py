import json
import pytest
from langchain_core.prompts import ChatPromptTemplate
from assistant.agent import BrowserAssistantBuilder


def test_agent_debug_prompt():
    agent = BrowserAssistantBuilder()
    assert type(agent.get_prompt()) is ChatPromptTemplate
