import os
import uvicorn
from fastapi import FastAPI
from payloads import ContentOnlyMessagePayload
from browser.driver import BrowserDriverManager
from fastapi.middleware.cors import CORSMiddleware
from assistant.agent import BrowserAssistantBuilder
from langchain.schema import HumanMessage, AIMessage


# Initialize FastAPI application
app = FastAPI()

# Define allowed origins
origins = [
    "*",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set listener path
LISTENER_PATH = os.path.abspath("../extension/index.html")

# Initialize the assistant and message history
assistant = BrowserAssistantBuilder()
message_history = []


@app.get("/")
def root():
    return "Hello from the server!"


@app.get("/test")
def test_server():
    return "Server is up and running."


@app.get("/debug")
def debug_system():
    return assistant.get_prompt()


@app.post("/chat")
async def chat_endpoint(input: ContentOnlyMessagePayload):
    """
    Receive a JSON body with { "message": "<text>" },
    execute the assistant action, and return the response.
    """

    user_text = input.message
    print(user_text)
    if not user_text:
        return {"error": "No message provided"}

    # Get AI response
    ai_response = assistant.execute_action(user_text, message_history)

    # Add initial user message and received AI response to history
    message_history.append(HumanMessage(content=user_text))
    message_history.append(AIMessage(content=ai_response))

    return {
        "response": ai_response,
    }


def main():
    # Initialize Chromedriver
    driver = BrowserDriverManager.get_driver()

    # Open page for testing
    driver.get(f"file:{LISTENER_PATH}")

    # Open a new tab
    driver.switch_to.new_window("tab")
    driver.get("https://example.com")

    # Start server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
