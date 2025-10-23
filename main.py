from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import time
import os

load_dotenv()
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")

# Open the browser
driver = webdriver.Chrome(service=service, options=options)

# Open link: megaphone/onefootballclub
driver.get("https://app.megaphone.xyz/pages/onefootballclub")

wait = WebDriverWait(driver, 10)

try:
    login_button_xpath = "//button[text()='Login']"
    print("Button 'Login' has been found!")

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))

    print("Click on Login")

    login_button.click()

    email_field_id = "email-input"

    print("Search for email field")
    email_field = wait.until(EC.visibility_of_element_located((By.ID, email_field_id)))

    print("Input email...")
    my_email = os.getenv("USER_EMAIL")
    email_field.send_keys(my_email)

    # Freeze
    loader_xpath = "//span[contains(@class, 'StyledButtonLoader')]"
    wait.until(EC.invisibility_of_element_located((By.XPATH, loader_xpath)))

    # Enter Submit
    submit_button_xpath = "//span[text()='Submit']/.."
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    submit_button.click()
    time.sleep(20)

except Exception as e:
    print(f"Something went wrong: {e}")

finally:
    # Exit
    driver.quit()
    print("Browser closed")
