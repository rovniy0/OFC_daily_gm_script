from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

from gmail_helper import get_login_code

load_dotenv()

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")

driver = None

try:
    print("Открываю браузер...")
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    print("Перехожу на OFC...")
    driver.get("https://app.megaphone.xyz/pages/onefootballclub")

    login_button_xpath = "//button[text()='Login']"
    print("Ищу кнопку 'Login'...")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    print("Нажимаю 'Login'...")
    login_button.click()

    email_field_id = "email-input"
    print("Ищу поле 'Email'...")
    email_field = wait.until(EC.visibility_of_element_located((By.ID, email_field_id)))

    my_email = os.getenv("USER_EMAIL")
    print(f"Ввожу email: {my_email}")
    email_field.send_keys(my_email)

    submit_button_xpath = "//span[text()='Submit']/.."
    print("Ищу кнопку 'Submit'...")
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    print("Нажимаю 'Submit'...")
    submit_button.click()

    print("[Selenium] Жду код подтверждения с почты...")
    login_code = get_login_code()

    if login_code:
        print(f"[Selenium] Получил код: {login_code}")

        code_inputs_xpath = "//div[contains(@class, 'CodeInput')]//input"
        print("[Selenium] Ищу 6 полей для ввода кода...")

        code_inputs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, code_inputs_xpath)))

        if len(code_inputs) == 6 and len(login_code) == 6:
            print("[Selenium] Ввожу код по одной цифре...")

            for box, digit in zip(code_inputs, login_code):
                box.send_keys(digit)
                time.sleep(0.1)

            print("[Selenium] Код введен! Жду загрузки главной страницы (10 сек)...")
            time.sleep(10)

            claim_button_xpath = "//h2[contains(text(), 'Community portal')]/following-sibling::span//button"
            print("[Selenium] Ищу финальную кнопку 'Claim'...")

            claim_button = wait.until(EC.visibility_of_element_located((By.XPATH, claim_button_xpath)))

            print("[Selenium] Кнопка найдена! Проверяю, активна ли она...")

            if claim_button.is_enabled():
                print("[Selenium] Кнопка АКТИВНА! Нажимаю...")
                claim_button.click()
                print("[Selenium] УСПЕХ! Награда получена. Скрипт завершен.")
                time.sleep(5)
            else:
                print("[Selenium] Кнопка НЕ АКТИВНА (disabled).")
                print("[Selenium] Похоже, награда на сегодня уже была получена.")
                time.sleep(3)

        else:
            print(
                f"[Selenium] Ошибка: Нашел {len(code_inputs)} полей, но код {login_code} имеет {len(login_code)} цифр.")

    else:
        print("[Selenium] Не смог получить код с почты. Остановка.")

except Exception as e:
    print(f"Что-то пошло не так (глобальная ошибка): {e}")

finally:
    if driver:
        driver.quit()
        print("Закрыл браузер")