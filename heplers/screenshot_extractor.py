from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import asyncio # Async operations ke liye

async def take_screenshot(url: str) -> str or None:
    """
    Takes a screenshot of the given URL using a headless Chrome browser.
    Returns the path to the saved screenshot file or None if an error occurs.
    """
    print(f"DEBUG: Attempting to take screenshot for: {url}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Browser window dikhayi nahi degi
    chrome_options.add_argument("--no-sandbox") # Render/Linux environments ke liye zaroori
    chrome_options.add_argument("--disable-dev-shm-usage") # Docker/Container environments ke liye zaroori
    chrome_options.add_argument("--window-size=1280,720") # Screenshot resolution
    chrome_options.add_argument("--disable-gpu") # Cloud environments ke liye

    # Render par Chromium/Chrome executable ka path
    # Render automatic detect kar leta hai agar buildpack sahi ho
    # Ya fir, Render ke environment variables mein path set karna pad sakta hai
    # For example: CHROMIUM_PATH = /usr/bin/google-chrome ya /usr/bin/chromium-browser
    # Agar ye environment variable set ho to use karein, warna default

    # Ye Render ke liye Chrome binary ka expected path hai agar buildpack sahi se set hai
    # Render automatically Chromium install karta hai.
    # Agar phir bhi error aaye, to environment variable CHROMIUM_BIN ko Render settings me set karein
    # For example: CHROMIUM_BIN: /usr/bin/google-chrome-stable

    driver = None
    try:
        # Check for Chrome binary path in environment variables (for Render)
        chrome_binary_path = os.environ.get("CHROMIUM_PATH") or os.environ.get("CHROME_BIN")

        if chrome_binary_path:
            print(f"DEBUG: Using Chrome binary from: {chrome_binary_path}")
            driver = webdriver.Chrome(executable_path=chrome_binary_path, options=chrome_options)
        else:
            # Fallback for local testing or if Render finds it automatically
            print("DEBUG: Using default Chrome/Chromium executable path.")
            driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        # Page load hone ke liye thoda wait karein
        await asyncio.sleep(5) # 5 seconds wait karein for page content to load

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            screenshot_path = temp_file.name
            driver.save_screenshot(screenshot_path)

        print(f"DEBUG: Screenshot saved to: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"ERROR: Failed to take screenshot of {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()
