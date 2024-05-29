import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Değişkenleri tanımlama
    driver.url_site1 = 'https://random-asin-new.vercel.app'
    driver.email_testid = '//input[@data-testid="login-email"]'
    driver.email = 'mustafa.yldz093@gmail.com'
    driver.password_testid = '//input[@data-testid="login-password"]'
    driver.password_valid = 'e95f621'
    driver.login_button_testid = '//button[@data-testid="login-submit"]'
    driver.close_button = '/html/body/div[5]/div[3]/div[1]/button'

    yield driver
    driver.quit()


def test_login(driver):
    driver.get(driver.url_site1)
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, "//*[contains(text(), 'Giriş Yap')]").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-container")))
    driver.find_element(By.XPATH, driver.email_testid).send_keys(driver.email)
    driver.find_element(By.XPATH, driver.password_testid).send_keys(driver.password_valid)

    driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[3]/div[3]/div').click()
    sleep(1)
    verify_button = "/html/body/div[5]/div[2]/div[2]/div[3]/div[3]/div"
    verify = driver.find_element(By.XPATH, verify_button)
    button_value = verify.get_attribute("data-checked")
    sleep(1)
    assert button_value == 'true'
    sleep(1)
    driver.find_element(By.XPATH, "//input[@data-testid='login-remember-me']").click()
    sleep(1)
    forgot_password_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Şifremi Unuttum')]")
    driver.execute_script("arguments[0].click();", forgot_password_button)
    sleep(1)

    verify2 = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div[2]/div/label')
    value2 = verify2.get_attribute("innerText")
    sleep(1)
    assert value2 == 'Kullanıcı Adı:'
    sleep(1)

    driver.find_element(By.XPATH, driver.close_button).click()
    sleep(1)


def test_combined_login_cases(driver):
    # Test 1: Standard Kullanıcı Bilgileri ile Oturum Açma
    driver.get("https://www.saucedemo.com/v1/index.html")
    WebDriverWait(driver, 10)

    kullanici_adi_kutusu = driver.find_element(By.ID, "user-name")
    sifre_kutusu = driver.find_element(By.ID, "password")
    giris_dugmesi = driver.find_element(By.ID, "login-button")

    kullanici_adi_kutusu.send_keys("standard_user")
    sifre_kutusu.send_keys("secret_sauce")
    giris_dugmesi.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

    # Ürüne tıkla ve sepete ekle
    ilk_urun = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
    urun_adi = ilk_urun.find_element(By.CLASS_NAME, "inventory_item_name").text
    urun_fiyati_true = ilk_urun.find_element(By.CLASS_NAME, "inventory_item_price").text
    urun_fiyati = "29.99"
    urun_ekle_dugmesi = ilk_urun.find_element(By.CLASS_NAME, "btn_primary")
    urun_ekle_dugmesi.click()
    sleep(1)

    # Sepete git ve bilgileri doğrula
    sepet_linki = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    sepet_linki.click()
    sleep(1)

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

    # Test 2: Yanlış Kullanıcı Bilgileri ile Oturum Açma
    for kullanici in [
        {"kullanici_adi": "YanlisAd", "sifre": "YanlisSifre"}
    ]:
        kullanici_adi_kutusu = driver.find_element(By.ID, "user-name")
        sifre_kutusu = driver.find_element(By.ID, "password")
        giris_dugmesi = driver.find_element(By.ID, "login-button")

        kullanici_adi_kutusu.send_keys(kullanici["kullanici_adi"])
        sifre_kutusu.send_keys(kullanici["sifre"])
        giris_dugmesi.click()

        # Hata mesajını kontrol et
        hata_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert hata_message.is_displayed()
        assert hata_message.text == "Epic sadface: Username and password do not match any user in this service"
        sleep(1)
