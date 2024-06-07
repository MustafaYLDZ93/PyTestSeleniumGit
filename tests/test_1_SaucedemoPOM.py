from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


from pages.Saucedemo1_inventory_page import InventoryPage
from pages.Saucedemo1_login_page import LoginPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    base_url = "https://www.saucedemo.com/v1/index.html"
    driver.get(base_url)
    yield driver
    driver.quit()


def test_valid_login(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.enter_username('standard_user')
    login_page.enter_password('secret_sauce')
    login_page.click_login_button()

    # Girişin başarılı olduğunu kontrol et
    WebDriverWait(driver, 10).until(
        EC.url_contains("/v1/inventory.html")
    )
    assert "/v1/inventory.html" in driver.current_url

    inventory_page.wait_for_page_load()
    assert "Products" in inventory_page.get_product_label_text()

    # Logout işlemi
    inventory_page.click_burger_button()
    inventory_page.click_logout_link()
    sleep(1)


def test_invalid_login(driver):
    login_page = LoginPage(driver)

    login_page.enter_username('invaliduser')
    login_page.enter_password('invalidpassword')
    login_page.click_login_button()

    # Hata mesajının göründüğünü kontrol et
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(login_page.error_message)
    )
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
    sleep(1)
