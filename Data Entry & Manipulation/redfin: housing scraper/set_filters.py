from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Filters:
    def __init__(self):
        self.chrome_driver_path = Service('C:\ChromeDriver\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.chrome_driver_path)
        self.driver.get("https://www.redfin.com/")

    def get_url(self, inputs: dict):
        """
        given a dictionary, returns a url as string
        :param inputs: dictionary
        :return: string
        """
        city = inputs['city']
        state = inputs['state']
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'search-box-input')))
        self.driver.find_element(By.ID, 'search-box-input').send_keys(f'{city},{state}')
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[2]/div/section/div/div/'
                                           'div/div/div/div/div/div[2]/div/div/form/div[1]/button').click()

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div')))

        self.driver.find_element(By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div').click()

        # sets filters user requested
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filterContent"]/div/div[2]/div[2]/div[3]/span[1]/span/'
                                                  'div/input')))

        # min price
        try:
            min_price = inputs['min-price']
            self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[2]/div[2]/div[3]/span[1]/span/div/'
                                               'input').send_keys(min_price)
        except KeyError:
            pass

        # max price
        try:
            max_price = inputs['max-price']
            self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[2]/div[2]/div[3]/span[3]/span/div/'
                                               'input').send_keys(max_price)
        except KeyError:
            pass

        # bed count
        try:
            bed_count = inputs['min-beds']
        except KeyError:
            bed_count = 1

        if bed_count == 'studio':
            bed_count = 2
        else:
            bed_count = int(bed_count) + 2

        self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[3]/div/div[2]/div/div/div/'
                                           f'div[{bed_count}]').click()

        # bath count
        try:
            bath_count = inputs['min-baths']
            bath_count_mapping = {'any': 1, '1': 2, '1.5': 3, '2': 4, '2.5': 5, '3': 6, '4+': 7}
            bath_count = bath_count_mapping[bath_count]
            self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[4]/div[2]/div/div/'
                                               f'div/div[{bath_count}]').click()
        except KeyError:
            pass

        # home type
        try:
            for i in range(len(inputs['property-type'])):
                home = inputs['property-type']
                home_type_mapping = {'House': 1, 'Townhouse': 2, 'Condo': 3, 'Land': 4, 'Multifamily': 5, 'Mobile': 6,
                                     'Co-op': 7, 'Other': 8
                                     }
                home_type = home_type_mapping[home]
                self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/'
                                                   f'div[{home_type}]/div').click()
        except KeyError:
            pass

        # min square feet
        try:
            min_sqft = inputs['sqftMin']
            min_sqft_list = self.driver.find_element(By.NAME, 'sqftMin').text.split('\n')
            index = min_sqft_list.index(min_sqft) + 1
            self.driver.find_element(By.XPATH,
                                     f'//*[@id="filterContent"]/div/div[7]/div[2]/div[1]/div[1]/div[2]/div/span[1]'
                                     f'/span/span/select/option[{index}]').click()
        except KeyError:
            pass

        # max square feet
        try:
            max_sqft = inputs['sqftMax']
            max_sqft_list = self.driver.find_element(By.NAME, 'sqftMax').text.split('\n')
            index1 = max_sqft_list.index(max_sqft) + 1
            self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[7]/div[2]/div[1]/div[1]/div[2]/div/'
                                               f'span[3]/span/span/select/option[{index1}]').click()
        except KeyError:
            pass

        # garage spots
        try:
            garage_spots = inputs['min-parking']
            if garage_spots == 'any':
                garage_spots = 1
            else:
                garage_spots = int(garage_spots) + 1
            self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[8]/div[2]/div[1]/div[1]/'
                                               f'div[1]/div[2]/div/div/div/div[{garage_spots}]').click()
        except KeyError:
            pass

        # pool type
        try:
            pool_type = inputs['pool-type']
            p_type_temp = self.driver.find_element(By.NAME, 'poolType').text.split('\n')
            p_type = p_type_temp.index(pool_type) + 1
            self.driver.find_element(By.XPATH, f'//*[@id="filterContent"]/div/div[8]/div[2]/div[1]/div[2]/div[2]/'
                                               f'span/span/select/option[{p_type}]')
        except KeyError:
            pass

        # keyword search
        try:
            key_word = inputs['remarks']
            self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[8]/div[2]/div[3]/'
                                               'div/div[2]/span/span/div/input').send_keys(key_word)
        except KeyError:
            pass

        # enter
        self.driver.find_element(By.XPATH, '//*[@id="searchForm"]/form/div[2]/div/div/button').click()

        time.sleep(3)

        return str(self.driver.current_url)
