from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.product_label = (By.CLASS_NAME, 'product_label')
        self.burger_button = (By.CLASS_NAME, 'bm-burger-button')
        self.logout_link = (By.ID, 'logout_sidebar_link')

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.product_label)
        )

    def get_product_label_text(self):
        return self.driver.find_element(*self.product_label).text

    def click_burger_button(self):
        self.driver.find_element(*self.burger_button).click()

    def click_logout_link(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.logout_link)
        )
        self.driver.find_element(*self.logout_link).click()
