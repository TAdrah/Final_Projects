from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Form_Filler:
    def __init__(self):
        self.chrome_driver_path = Service('C:\ChromeDriver\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.chrome_driver_path)
        self.driver.get("https://forms.gle/kwWzTm4FyLTVpfg7A")

    def answer_questions(self, address:list, price:list, link:list):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')))
        for i in range(len(address)):
            time.sleep(1)
            self.driver.find_element(
                By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > '
                                 'div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')\
                .send_keys(address[i])
            self.driver.find_element(
                By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > '
                                 'div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')\
                .send_keys(price[i])
            self.driver.find_element(
                By.CSS_SELECTOR, '#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > '
                                 'div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')\
                .send_keys(f"https://www.redfin.com{link[i]}")
            self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'body > div.Uc2NEf > div:nth-child(2) > div.RH5hzf.RLS9Fe > div > div.c2gzEf > a'))
            )
            self.driver.find_element(
                By.CSS_SELECTOR,'body > div.Uc2NEf > div:nth-child(2) > div.RH5hzf.RLS9Fe > div > div.c2gzEf > a')\
                .click()
