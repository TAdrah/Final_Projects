from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASS = os.environ.get("MY_PASS")

chrome_driver_path = Service('C:\ChromeDriver\chromedriver.exe')
driver = webdriver.Chrome(service=chrome_driver_path)
driver.get("https://tinder.com/")


def log_me_in():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log in')))
    # main login
    driver.find_element(By.LINK_TEXT, 'Log in').click()
    time.sleep(1)
    # fb login
    driver.find_element(By.XPATH, '//*[@id="c160459658"]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button').click()

    base_window = driver.window_handles[0]
    fb_login_window = driver.window_handles[1]
    driver.switch_to.window(fb_login_window)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginbutton')))
    driver.find_element(By.ID, 'email').send_keys(MY_EMAIL)
    driver.find_element(By.ID, 'pass').send_keys(MY_PASS)
    driver.find_element(By.ID, 'loginbutton').click()

    driver.switch_to.window(base_window)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="c160459658"]/main/div/div/div/div[3]/button[1]')))
    driver.find_element(By.XPATH, '//*[@id="c160459658"]/main/div/div/div/div[3]/button[1]').click()
    time.sleep(.5)
    driver.find_element(By.XPATH, '//*[@id="c160459658"]/main/div/div/div/div[3]/button[2]').click()
    time.sleep(.5)
    driver.find_element(By.XPATH, '//*[@id="c-60880778"]/div/div[2]/div/div/div[1]/div[1]/button').click()




def swipe_left():
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#c-60880778 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div >'
                              ' main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\('
                              'r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml '
                              '> div.recsCardboard__cardsContainer.H\(100\%\).Pos\(r\).Z\(1\) > div'
                              ' > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div'
                              ' > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc'
                              '\(\$c-ds-border-gamepad-nope-default\) > button')))
    decline = driver.find_element(By.CSS_SELECTOR,
                                  '#c-60880778 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div >'
                                  ' main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\('
                                  'r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml '
                                  '> div.recsCardboard__cardsContainer.H\(100\%\).Pos\(r\).Z\(1\) > div'
                                  ' > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div'
                                  ' > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc'
                                  '\(\$c-ds-border-gamepad-nope-default\) > button')
    decline.click()


def swipe_right():
    try:
        accept = driver.find_element(By.XPATH,
                                     '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        accept.click()
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()
        except NoSuchElementException:
            time.sleep(2)


driver.maximize_window()
log_me_in()
for n in range(100):
    time.sleep(1)
    swipe_left()
    # swipe_right()
