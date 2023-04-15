from bs4 import BeautifulSoup
import requests


class RedFin_Scraper:
    def __init__(self):
        self.list_price = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11"
                          "0.0.0.0 Safari/537.36",
            "Accept-Language": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                               "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;"
                               "q=0.7"
        }
        self.response = requests.get(
            url="https://www.redfin.com/city/13654/CA/Oakland",
            headers=headers
        )
        self.soup = BeautifulSoup(self.response.text, "lxml")
        self.data = self.soup.select('.HomeViews > div > div > div')

    def get_links(self):
        links = []
        for i in self.data:
            try:
                links.append(i.find(name='a').get('href'))
            except AttributeError:
                continue
        return links

    def get_list_price(self):
        prices = []
        for i in self.data:
            try:
                prices.append(i.find(class_='homecardV2Price').text)
            except AttributeError:
                continue
        return prices

    def get_address(self):
        addresses = []
        for i in self.data:
            try:
                addresses.append(i.find(class_='link-and-anchor').text)
            except AttributeError:
                continue
        return addresses
