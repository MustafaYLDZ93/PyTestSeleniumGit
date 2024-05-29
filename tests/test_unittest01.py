import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.chrome.options import Options


class KayıtOlma(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.url_site = 'https://random-asin-new.vercel.app'
        self.email_testid = '//input[@data-testid="login-email"]'
        self.email = 'mustafa.yldz093@gmail.com'
        self.password_testid = '//input[@data-testid="login-password"]'
        self.password_valid = 'e95f621'
        self.password_invalid = 'e95f622'
        self.email_error_message = '.m_8f816625.mantine-InputWrapper-error.mantine-TextInput-error'
        self.password_error_message = '.m_8f816625.mantine-InputWrapper-error.mantine-TextInput-error'
        self.login_button_testid = '//button[@data-testid="login-submit"]'
        self.close_button = '/html/body/div[5]/div[3]/div[1]/button'

    def tearDown(self):
        self.driver.quit()

    def test_03_login(self):
        self.driver.get(self.url_site)
        wait = WebDriverWait(self.driver, 1)
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Giriş Yap')]").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-container")))
        self.driver.find_element(By.XPATH, self.email_testid).send_keys(self.email)
        self.driver.find_element(By.XPATH, self.password_testid).send_keys(self.password_valid)

        self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[3]/div[3]/div').click()
        sleep(1)
        verify_button = "/html/body/div[5]/div[2]/div[2]/div[3]/div[3]/div"
        verify = self.driver.find_element(By.XPATH, verify_button)
        button_value = verify.get_attribute("data-checked")
        sleep(1)
        assert button_value == 'true'
        sleep(1)
        self.driver.find_element(By.XPATH, "//input[@data-testid='login-remember-me']").click()
        sleep(1)
        forgot_password_button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Şifremi Unuttum')]")
        self.driver.execute_script("arguments[0].click();", forgot_password_button)
        sleep(1)

        verify2 = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[2]/div/label')
        value2 = verify2.get_attribute("innerText")
        sleep(1)
        assert value2 == 'Kullanıcı Adı:'
        sleep(1)

        self.driver.find_element(By.XPATH, self.close_button).click()

        sleep(1)


if __name__ == '__main__':
    unittest.main()
