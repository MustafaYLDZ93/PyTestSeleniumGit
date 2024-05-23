import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class OturumAcmaTestleri(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.saucedemo.com/v1/index.html')

    def tearDown(self):
        self.driver.quit()

    def test_farkli_kullanici_bilgileriyle_oturum_acma(self):
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

            if kullanici["kullanici_adi"] == "standard_user" and kullanici["sifre"] == "secret_sauce":
                # Oturum açıldığını kontrol et
                WebDriverWait(self.driver, 10).until(
                    EC.url_contains("/inventory.html")
                )

                # Ürüne tıkla ve sepete ekle
                ilk_urun = self.driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
                urun_adi = ilk_urun.find_element(By.CLASS_NAME, "inventory_item_name").text
                urun_fiyati_true = ilk_urun.find_element(By.CLASS_NAME, "inventory_item_price").text
                urun_fiyati = '29.99'
                urun_ekle_dugmesi = ilk_urun.find_element(By.CLASS_NAME, "btn_primary")
                urun_ekle_dugmesi.click()
                sleep(1)

                # Sepete git ve bilgileri doğrula
                sepet_linki = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
                sepet_linki.click()
                sleep(1)

                WebDriverWait(self.driver, 10).until(
                    EC.url_contains("/cart.html")
                )

                sepet_urun_adi = self.driver.find_element(By.CLASS_NAME, "inventory_item_name").text
                sepet_urun_fiyati = self.driver.find_element(By.CLASS_NAME, "inventory_item_price").text

                self.assertEqual(urun_adi, sepet_urun_adi)
                self.assertEqual(urun_fiyati, sepet_urun_fiyati)

                # Menüden çıkış yap
                menu_dugmesi = self.driver.find_element(By.CSS_SELECTOR, ".bm-burger-button")
                menu_dugmesi.click()
                sleep(1)

                cikis_dugmesi = self.driver.find_element(By.ID, "logout_sidebar_link")
                cikis_dugmesi.click()

            else:
                # Hata mesajını kontrol et
                hata_mesaji = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
                self.assertTrue(hata_mesaji.is_displayed())
                self.assertEqual(hata_mesaji.text, "Epic sadface: Username and password do not match any user in this service")
                sleep(1)

if __name__ == "__main__":
    unittest.main()
