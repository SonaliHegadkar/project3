from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from flask import Flask
from waitress import serve
import threading  # To run the Selenium script in a separate thread

app = Flask(__name__)

@app.route('/')
# def home():
    # return "Hello, world!"

def run_selenium_script():
    # Set up the Chrome WebDriver with options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Opens the browser in full screen
    chrome_options.add_argument('--disable-notifications')  # Disable pop-up notifications

    # Provide the path to your ChromeDriver
    #driver_path = 'C:/project1/chromedriver.exe'  # Update with your driver path
    driver_path = chromedriver_autoinstaller.install()
    service = Service(driver_path)
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

    # Allow time for the home page to load
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
    except:
        print("Unable to locate the '+' button for a new post")

    time.sleep(3)

    # Upload image
    image_path = r'C:\Users\Shreya\PycharmProjects\MLprac1que1\upload1\draw1.jpeg'  # Update with your image path
    upload_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    upload_element.send_keys(image_path)

    # Allow time for the image to be fully uploaded
    time.sleep(5)

    # Clicking the "Next" button after the image is uploaded
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
        )
        next_button.click()
    except Exception as e:
        print(f"Error clicking 'Next' button: {e}")

    # Adding a second click to ensure the second "Next" step (if needed)
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']"))
        )
        next_button.click()
    except Exception as e:
        print(f"Error clicking 'Next' button: {e}")

    # Adding a caption
    try:
        caption = "Demo Project!"

        # Wait for the caption textarea to be present
        caption_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//textarea[@aria-label='Write a caption…'] | //textarea[@placeholder='Write a caption…']"))
        )
        caption_field.send_keys(caption)
    except Exception as e:
        print(f"Error locating caption field: {e}")

    # Clicking the "Share" button to post the image
    try:
        share_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']"))
        )
        share_button.click()
    except Exception as e:
        print(f"Error clicking 'Share' button: {e}")

    # Wait for a few seconds to ensure the post goes live
    time.sleep(5)

    # Check for post shared confirmation message
    try:
        confirmation_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Your post has been shared.')]"))
        )
        print("Post shared successfully:", confirmation_message.text)
    except Exception as e:
        print("Error locating post shared confirmation message:", e)

    driver.quit()


if __name__ == "__main__":
    # Run Flask app in the main thread
    thread = threading.Thread(target=run_selenium_script)
    thread.start()

    # Use Waitress to serve the app
    serve(app, host='0.0.0.0', port=8080)
