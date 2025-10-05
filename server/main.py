import uvicorn
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize FastAPI application
app = FastAPI()

# Initialize extension and user profile settings
EXTENSION_PATH = "../extension"


@app.get("/")
def root():
    return "Hello from the server!"


@app.get("/test")
def test_server():
    return "Server is up and running."


def main():
    # Initialize ChromeOptions
    options = Options()

    # Load unpacked extension into browser
    options.add_argument(f"--load-extension={EXTENSION_PATH}")

    # Initialize Chromedriver
    driver = webdriver.Chrome(options=options)

    # Start server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
