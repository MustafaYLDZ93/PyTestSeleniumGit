import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()  # ChromeDriver path should be set in PATH
    driver.implicitly_wait(10)
    request.cls.driver = driver
    request.cls.base_url = "https://www.saucedemo.com/v1/index.html"
    yield
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestLogin:

    def login_user(self, username, password):
        self.driver.get(self.base_url)

        username_input = self.driver.find_element(By.ID, "user-name")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    def test_valid_login(self):
        self.login_user('standard_user', 'secret_sauce')

        # Girişin başarılı olduğunu kontrol et
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/v1/inventory.html")
        )
        assert "/v1/inventory.html" in self.driver.current_url

        product_label = self.driver.find_element(By.CLASS_NAME, 'product_label')
        assert "Products" in product_label.text

        # Logout işlemi
        burger_button = self.driver.find_element(By.CLASS_NAME, 'bm-burger-button')
        burger_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'logout_sidebar_link'))
        )
        logout_link = self.driver.find_element(By.ID, 'logout_sidebar_link')
        logout_link.click()
        sleep(1)

    def test_invalid_login(self):
        self.login_user('invaliduser', 'invalidpassword')

        # Hata mesajının göründüğünü kontrol et
        error_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'error-button'))
        )
        assert error_button.is_displayed()

        error_message = self.driver.find_element(By.CSS_SELECTOR, 'div#login_button_container h3')
        assert "Username and password do not match any user in this service" in error_message.text

        error_message_data_test = self.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        assert "Username and password do not match any user in this service" in error_message_data_test.text
        sleep(1)
