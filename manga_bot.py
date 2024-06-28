from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_service = Service('C:/Users/Vlad/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    driver.get("https://user.manganelo.com/login?l=manganato&re_l=login")

    driver.implicitly_wait(10)

    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')

    username.send_keys('SeleniumTest')
    password.send_keys('123456789')

    captcha_image = driver.find_element(By.XPATH, '//div[@class="captchar"]/img')
    captcha_image.screenshot('captcha.png')

    print("Captcha-ul va trebui introdus manual.")
    captcha_value = input("Captcha: ")

    captcha_input = driver.find_element(By.NAME, 'captchar')
    captcha_input.send_keys(captcha_value)

    login_button = driver.find_element(By.ID, 'submit_login')
    login_button.click()

    print("Cel mai recent updatate manga/manhua/manhwa-uri sunt:")

    time.sleep(5)

    driver.get("https://manganato.com/")

    driver.implicitly_wait(10)

    manga_titles = driver.find_elements(By.CSS_SELECTOR, ".panel-content-homepage .content-homepage-item .item-title a")

    for title in manga_titles:
        print(title.text)

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()