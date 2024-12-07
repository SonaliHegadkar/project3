import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from flask import Flask
from waitress import serve
import logging
import chromedriver_autoinstaller

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Selenium function to run the script
def run_selenium_script():
    try:
        # Install chromedriver automatically
        chromedriver_autoinstaller.install()

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Path to ChromeDriver (chromedriver will be installed by chromedriver_autoinstaller)
        service = Service(chromedriver_autoinstaller.install())

        # Start Chrome WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open Instagram
        driver.get("https://www.instagram.com/")
        time.sleep(3)

        # Logging into Instagram
        username = '56project__'
        password = 'project123@'

        # Locate and interact with the login fields
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)

        # Click on login button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # Skip saving login info (if prompted)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            ).click()
        except:
            pass

        # Skip turning on notifications (if prompted)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            ).click()
        except:
            pass

        # Wait for the + button to appear and click it
        try:
            plus_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='New post']"))
            )
            plus_button.click()
        except Exception as e:
            logging.error(f"Error locating '+' button: {e}")

        time.sleep(3)

        # Upload image
        image_path = r'C:\path_to_your_image\draw1.jpeg'
        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_element.send_keys(image_path)

        time.sleep(5)

        # Click the "Next" button after image is uploaded
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
            )
            next_button.click()
        except Exception as e:
            logging.error(f"Error clicking 'Next' button: {e}")

        # Add a caption
        try:
            caption_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//textarea[@aria-label='Write a caption…'] | //textarea[@placeholder='Write a caption…']"))
            )
            caption_field.send_keys("Demo Project!")
        except Exception as e:
            logging.error(f"Error locating caption field: {e}")

        # Click "Share" to post the image
        try:
            share_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']"))
            )
            share_button.click()
        except Exception as e:
            logging.error(f"Error clicking 'Share' button: {e}")

        # Wait for confirmation
        time.sleep(5)
        driver.quit()

    except Exception as e:
        logging.error(f"Selenium script error: {e}")

# Flask route for testing
@app.route('/')
def home():
    return "Hello, world!"

# Run Flask app in a separate thread for production
if __name__ == "__main__":
    # Running the Selenium script in a separate thread
    threading.Thread(target=run_selenium_script).start()

    # Use Waitress to serve the app
    serve(app, host='0.0.0.0', port=8080)
