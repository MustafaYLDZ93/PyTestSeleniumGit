import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.chrome.options import Options


class KayıtOlma(unittest.TestCase):

    def setUp(self):
        #options = Options()
        #options.add_argument("--headless")
        self.driver = webdriver.Chrome()
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
        print("Step 2: Assert - Login Container")
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


class ArraysTest(unittest.TestCase):

    def setUp(self):
        #options = Options()
        #options.add_argument("--headless")
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/v1/index.html")

    def tearDown(self):
        self.driver.quit()

    def test_farklı_kullanıcılar_oturum_acma(self):
        kullanici_bilgileri = [
            {"kullanici_adi": "standard_user", "sifre": "secret_sauce"},
            {"kullanici_adi": "YanlisAd", "sifre": "YanlisSifre"},
        ]

        for kullanici in kullanici_bilgileri:
            kullanici_adi_kutusu = self.driver.find_element(By.ID, "user-name")
            kullanici_adi_kutusu.send_keys(kullanici["kullanici_adi"])

            sifre_kutusu = self.driver.find_element(By.ID, "password")
            sifre_kutusu.send_keys(kullanici["sifre"])

            giris_dugmesi = self.driver.find_element(By.ID, "login-button")
            giris_dugmesi.click()

            if (
                    kullanici["kullanici_adi"] == "standard_user"
                    and kullanici["sifre"] == "secret_sauce"
            ):
                # Oturum açıldığını kontrol et
                WebDriverWait(self.driver, 10).until(EC.url_contains("/inventory.html"))

                # Ürüne tıkla ve sepete ekle
                ilk_urun = self.driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
                urun_adi = ilk_urun.find_element(
                    By.CLASS_NAME, "inventory_item_name"
                ).text
                urun_fiyati_true = ilk_urun.find_element(
                    By.CLASS_NAME, "inventory_item_price"
                ).text
                urun_fiyati = "29.99"
                urun_ekle_dugmesi = ilk_urun.find_element(By.CLASS_NAME, "btn_primary")
                urun_ekle_dugmesi.click()
                sleep(1)

                # Sepete git ve bilgileri doğrula
                sepet_linki = self.driver.find_element(
                    By.CLASS_NAME, "shopping_cart_link"
                )
                sepet_linki.click()
                sleep(1)

                WebDriverWait(self.driver, 10).until(EC.url_contains("/cart.html"))

                sepet_urun_adi = self.driver.find_element(
                    By.CLASS_NAME, "inventory_item_name"
                ).text
                sepet_urun_fiyati = self.driver.find_element(
                    By.CLASS_NAME, "inventory_item_price"
                ).text

                self.assertEqual(urun_adi, sepet_urun_adi)
                self.assertEqual(urun_fiyati, sepet_urun_fiyati)

                # Menüden çıkış yap
                menu_dugmesi = self.driver.find_element(
                    By.CSS_SELECTOR, ".bm-burger-button"
                )
                menu_dugmesi.click()
                sleep(1)

                cikis_dugmesi = self.driver.find_element(By.ID, "logout_sidebar_link")
                cikis_dugmesi.click()

            else:
                # Hata mesajını kontrol et
                hata_mesaji = self.driver.find_element(
                    By.CSS_SELECTOR, "[data-test='error']"
                )
                self.assertTrue(hata_mesaji.is_displayed())
                self.assertEqual(
                    hata_mesaji.text,
                    "Epic sadface: Username and password do not match any user in this service",
                )
                sleep(1)  # pragma: no cover


if __name__ == '__main__':
    unittest.main()
