from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def login(driver, username, password, captcha):
    driver.get("https://www.google.com")  
    time.sleep(2)
    driver.get("https://user.manganelo.com/login?l=manganato&re_l=login")
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "captchar").send_keys(captcha)
        driver.find_element(By.ID, "submit_login").click()
        time.sleep(5)
    except Exception as e:
        print("Error during login:", e)
        driver.quit()

def navigate_to_newest_manga(driver):
    driver.get("https://manganato.com/genre-all?type=newest")
    time.sleep(2)

def get_available_genres(driver):
    navigate_to_newest_manga(driver)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='container container-main']")))
    genres = driver.find_elements(By.XPATH, "//div[@class='container container-main']//a[@class='a-h text-nowrap']")
    genre_list = [genre.text for genre in genres]
    return genre_list

def apply_filters(driver, genres):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'FILTER (ADVANCED SEARCH)')]"))).click()
    time.sleep(2)
    for genre in genres:
        genre_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//label[contains(text(),'{genre}')]/preceding-sibling::input")))
        genre_checkbox.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))).click()

def get_manga_list(driver):
    time.sleep(5)
    mangas = driver.find_elements(By.XPATH, "//div[@class='panel-content-genres']//h3/a")
    manga_links = [manga.get_attribute('href') for manga in mangas]
    return manga_links

def add_to_bookmarks(driver, manga_links, min_score, max_bookmarks):
    bookmarks_added = 0
    for link in manga_links:
        if bookmarks_added >= max_bookmarks:
            break
        driver.get(link)
        time.sleep(2)
        try:
            accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(),'AGREE')]")
            accept_cookies_button.click()
            time.sleep(1)
        except:
            pass  
        try:
            score_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//em[@property='v:average']")))
            score = float(score_element.text)
            if score >= min_score:
                try:
                    bookmark_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='user_btn_follow_i info-bookmark']")))
                    bookmark_button.click()
                    time.sleep(1)
                    bookmarks_added += 1
                except Exception as e:
                    print(f"Failed to add bookmark for {link}: {e}")
        except Exception as e:
            print(f"Failed to get score for {link}: {e}")

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    captcha = input("Enter the captcha value: ")

    login(driver, username, password, captcha)
    genres = get_available_genres(driver)
    print("Available genres:")
    for genre in genres:
        print(genre)
    
    selected_genres = input("Enter the genres you want to include, separated by commas: ").split(',')
    apply_filters(driver, selected_genres)
    
    manga_links = get_manga_list(driver)
    min_score = float(input("Enter the minimum score: "))
    max_bookmarks = int(input("Enter the number of bookmarks to add: "))
    
    add_to_bookmarks(driver, manga_links, min_score, max_bookmarks)
    
    driver.quit()
