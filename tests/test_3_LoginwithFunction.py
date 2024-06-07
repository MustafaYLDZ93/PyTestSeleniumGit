from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options



@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    base_url = "https://www.saucedemo.com/v1/index.html"
    driver.get(base_url)
    yield driver
    driver.quit()


def login_user(driver, username, password):
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()


def test_valid_login(driver):
    login_user(driver, 'standard_user', 'secret_sauce')

    # Girişin başarılı olduğunu kontrol et
    WebDriverWait(driver, 10).until(
        EC.url_contains("/v1/inventory.html")
    )
    assert "/v1/inventory.html" in driver.current_url

    product_label = driver.find_element(By.CLASS_NAME, 'product_label')
    assert "Products" in product_label.text

    # Logout işlemi
    burger_button = driver.find_element(By.CLASS_NAME, 'bm-burger-button')
    burger_button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'logout_sidebar_link'))
    )
    logout_link = driver.find_element(By.ID, 'logout_sidebar_link')
    logout_link.click()
    sleep(1)


def test_invalid_login(driver):
    login_user(driver, 'invaliduser', 'invalidpassword')

    # Hata mesajının göründüğünü kontrol et
    error_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'error-button'))
    )
    assert error_button.is_displayed()

    error_message_data_test = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
    assert "Username and password do not match any user in this service" in error_message_data_test.text

