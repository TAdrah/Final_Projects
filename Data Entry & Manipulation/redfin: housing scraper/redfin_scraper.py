from bs4 import BeautifulSoup
import re
import requests


class RedFin_Scraper:
    def __init__(self, url):
        self.list_price = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11"
                          "0.0.0.0 Safari/537.36",
            "Accept-Language": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                               "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;"
                               "q=0.7"
        }
        self.response = requests.get(
            url=url,
            headers=headers
        )
        self.soup = BeautifulSoup(self.response.text, "lxml")
        self.data = self.soup.select('.HomeViews > div > div > div')

    def get_links(self) -> list:
        """
        parses data & returns the url per item
        :return: list
        """
        
        links = []
        for i in self.data:
            try:
                links.append(i.find(name='a').get('href'))
            except AttributeError:
                continue
        return links

    def get_list_price(self) -> list:
        """
        parses data & returns list price per item
        :return: list
        """
        prices = []
        for i in self.data:
            try:
                prices.append(i.find(class_='homecardV2Price').text)
            except AttributeError:
                continue
        return prices

    def get_address(self) -> list:
        """
        parses data & returns address per item
        :return: list
        """
        addresses = []
        for i in self.data:
            try:
                addresses.append(i.find(class_='link-and-anchor').text)
            except AttributeError:
                continue
        return addresses

    def prices(self) -> list:
        """
        parses data & returns prices per item
        :return: list
        """
        prices = []
        for i in self.data:
            try:
                prices.append(i.find(class_='homecardV2Price').text)
            except AttributeError:
                continue
        return prices

   def bed_bath_sqft(self) -> list:
        """
        parses data & returns bed, bath, square foott per item
        :return: list
        """
        bbs = []
        for i in self.data:
            try:
                text = i.find(class_='HomeStatsV2')
                #filters out lots/acres by ensuring first character is a number
                if text.text[0].isdigit():
                    #uses regular expression to find numbers that may or may not have decimal
                    beds = re.findall('\d+\.?\d*',text.findAll('div')[0].text)
                    baths = re.findall('\d+\.?\d*',text.findAll('div')[1].text)
                    sq_ft = re.findall('\d+\.?\d*',text.findAll('div')[2].text)

                    if len(sq_ft)>1:
                        #combines list as str and put it back to list to keep data uniform.
                        sq_ft = list(sq_ft[0] + ',' + sq_ft[1])

                    bbs.append((beds[0], baths[0], sq_ft[0]))

            except AttributeError:
                continue
        print(bbs)
        return bbs
