import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

chrome_options = Options()
chrome_service = Service('C:/Users/Vlad/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://user.manganelo.com/login")
driver.implicitly_wait(10)

username = driver.find_element(By.NAME, 'username')
password = driver.find_element(By.NAME, 'password')

username.send_keys('SeleniumTest')
password.send_keys('123456789')

captcha_image = driver.find_element(By.XPATH, '//div[@class="captchar"]/img')
captcha_image.screenshot('captcha.png')

captcha_value = input("Captcha: ")

captcha_input = driver.find_element(By.NAME, 'captchar')
captcha_input.send_keys(captcha_value)

login_button = driver.find_element(By.ID, 'submit_login')
login_button.click()

try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.text-nowrap.a-h')))
    print("Login successful")
except TimeoutException:
    print("Login failed")
    driver.quit()
    sys.exit()

time.sleep(5)

def is_logged_in(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'p.text-nowrap.a-h')
        return True
    except NoSuchElementException:
        return False

if not is_logged_in(driver):
    print("Logged out")
    driver.quit()
    sys.exit()

cookies_after_login = driver.get_cookies()

driver.get("https://manganato.com/genre-all?type=newest")
driver.implicitly_wait(10)

genres_elements = driver.find_elements(By.CSS_SELECTOR, ".pn-category-row a.a-h.text-nowrap")
genres = [genre.text for genre in genres_elements]

print("Available genres:")
for genre in genres:
    print(genre)

desired_genres = input("Enter genres (comma separated): ").split(',')
desired_genres = [genre.strip() for genre in desired_genres]

driver.get("https://manganato.com/advanced-search")
driver.implicitly_wait(10)

for genre in desired_genres:
    try:
        genre_checkbox = driver.find_element(By.XPATH, f"//label[text()='{genre}']/preceding-sibling::input")
        if not genre_checkbox.is_selected():
            genre_checkbox.click()
    except NoSuchElementException:
        print(f"Genre {genre} not found on the advanced search page")

apply_button = driver.find_element(By.CSS_SELECTOR, "button.btn-search")
apply_button.click()
driver.implicitly_wait(10)

manga_links = driver.find_elements(By.CSS_SELECTOR, ".panel-content-homepage .content-homepage-item .item-title a")
manga_links = [link.get_attribute('href') for link in manga_links]

min_score = float(input("Enter minimum score: "))
num_to_bookmark = int(input("Enter number of manga to bookmark: "))

def close_banners(driver):
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[text()='AGREE']").click()
    except (NoSuchElementException, TimeoutException):
        pass

    try:
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button.qc-cmp2-summary-buttons").click()
    except (NoSuchElementException, TimeoutException):
        pass

    try:
        overlay_element = driver.find_element(By.CSS_SELECTOR, "div.qc-cmp-cleanslate")
        driver.execute_script("arguments[0].style.visibility='hidden'", overlay_element)
    except NoSuchElementException:
        pass

bookmarked_count = 0

for link in manga_links:
    if bookmarked_count >= num_to_bookmark:
        break

    driver.get(link)
    close_banners(driver)

    genres_elements = driver.find_elements(By.CSS_SELECTOR, ".variations-tableInfo a")
    genres = [genre.text for genre in genres_elements]

    try:
        score_text = driver.find_element(By.CSS_SELECTOR, "em[property='v:average']").text
        score = float(score_text)
    except (NoSuchElementException, ValueError):
        score = 0

    if score >= min_score:
        try:
            bookmark_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".user_btn_follow_i.info-bookmark")))
            bookmark_button.click()
            bookmarked_count += 1
        except ElementClickInterceptedException:
            close_banners(driver)
            try:
                bookmark_button.click()
                bookmarked_count += 1
            except Exception:
                continue
        except (NoSuchElementException, TimeoutException):
            continue

driver.quit()
print(f"Bookmarked {bookmarked_count} manga(s)")
