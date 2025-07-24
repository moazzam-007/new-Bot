from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import tempfile

async def take_screenshot(url: str) -> str or None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") # Render/Linux environments ke liye zaroori
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720") # Screenshot size

    # Render par Chromium ka path setup karna padega
    # Ye path Render ke build environment par depend karega
    # Usually Render buildpacks khud handle kar lete hain, ya manually specify karna padta hai
    # For Render, you might need to specify the binary path
    # binary_path = os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium-browser") # Example path
    # driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)

    # Simple setup, hoping Render has Chrome/Chromium in PATH
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        # Thodi der wait karein taaki page poora load ho jaaye
        driver.implicitly_wait(5) # Wait for elements to appear

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            screenshot_path = temp_file.name
            driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error taking screenshot of {url}: {e}")
        return None
    finally:
        driver.quit()
