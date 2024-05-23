from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def test_google_search():
    # WebDriver'ı başlat
    driver = webdriver.Chrome()

    # Google ana sayfasını aç
    driver.get("https://www.google.com")

    # Google ana sayfasının yüklendiğini doğrula
    assert "Google" in driver.title

    # Arama kutusunu bul ve bir arama terimi gir
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium WebDriver")

    # Arama butonuna tıkla
    search_box.send_keys(Keys.RETURN)

    # Sonuçların yüklendiğinden emin olmak için kısa bir süre bekle
    time.sleep(3)

    # Sonuçların yüklendiğini doğrula
    assert "Selenium WebDriver" in driver.page_source

    # WebDriver'ı kapat
    driver.quit()


# Testi çalıştır
if __name__ == "__main__":
    test_google_search()
