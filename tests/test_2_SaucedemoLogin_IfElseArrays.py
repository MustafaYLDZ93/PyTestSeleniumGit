import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/v1/index.html")

    yield driver
    driver.quit()


def test_farkli_kullanici_bilgileriyle_oturum_acma(driver):
    kullanici_bilgileri = [
        {"kullanici_adi": "standard_user", "sifre": "secret_sauce"},
        {"kullanici_adi": "YanlisAd", "sifre": "YanlisSifre"},
    ]

    for kullanici in kullanici_bilgileri:
        kullanici_adi_kutusu = driver.find_element(By.ID, "user-name")
        kullanici_adi_kutusu.send_keys(kullanici["kullanici_adi"])

        sifre_kutusu = driver.find_element(By.ID, "password")
        sifre_kutusu.send_keys(kullanici["sifre"])

        giris_dugmesi = driver.find_element(By.ID, "login-button")
        giris_dugmesi.click()

        if (
                kullanici["kullanici_adi"] == "standard_user"
                and kullanici["sifre"] == "secret_sauce"
        ):
            # Oturum açıldığını kontrol et
            WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

            # Ürüne tıkla ve sepete ekle
            ilk_urun = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
            urun_adi = ilk_urun.find_element(By.CLASS_NAME, "inventory_item_name").text
            urun_fiyati = "29.99"
            urun_ekle_dugmesi = ilk_urun.find_element(By.CLASS_NAME, "btn_primary")
            urun_ekle_dugmesi.click()
            sleep(1)

            # Sepete git ve bilgileri doğrula
            sepet_linki = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
            sepet_linki.click()

            WebDriverWait(driver, 10).until(EC.url_contains("/cart.html"))

            sepet_urun_adi = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
            sepet_urun_fiyati = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

            assert urun_adi == sepet_urun_adi
            assert urun_fiyati == sepet_urun_fiyati

            # Menüden çıkış yap
            menu_dugmesi = driver.find_element(By.CSS_SELECTOR, ".bm-burger-button")
            menu_dugmesi.click()
            sleep(1)

            cikis_dugmesi = driver.find_element(By.ID, "logout_sidebar_link")
            cikis_dugmesi.click()

        else:
            # Hata mesajını kontrol et
            hata_mesaji = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
            assert hata_mesaji.is_displayed()
            assert hata_mesaji.text == "Epic sadface: Username and password do not match any user in this service"


