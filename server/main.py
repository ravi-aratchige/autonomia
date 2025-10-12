import os
import uvicorn
from fastapi import FastAPI
from selenium import webdriver
from fastapi.middleware.cors import CORSMiddleware
from selenium.webdriver.chrome.options import Options

# Initialize FastAPI application
app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set extension and listener paths
EXTENSION_PATH = "../extension"
LISTENER_PATH = os.path.abspath("../extension/index.html")


@app.get("/")
def root():
    return "Hello from the server!"


@app.get("/test")
def test_server():
    return "Server is up and running."


def main():
    # Initialize ChromeOptions
    options = Options()

    # Set options to allow media device access
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    prefs = {"profile.default_content_setting_values.media_stream_mic": 1}
    options.add_experimental_option("prefs", prefs)

    # Load unpacked extension into browser
    options.add_argument(f"--load-extension={EXTENSION_PATH}")

    # Initialize Chromedriver
    driver = webdriver.Chrome(options=options)

    # Open page for testing
    driver.get(f"file:{LISTENER_PATH}")

    # Open a new tabs
    driver.switch_to.new_window("tab")
    driver.get("https://example.com")

    # Start server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
