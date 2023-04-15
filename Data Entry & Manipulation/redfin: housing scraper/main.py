from redfin_scraper import RedFin_Scraper
from form_filler import Form_Filler

#Get prices, links, addresses
scraper = RedFin_Scraper()
prices = scraper.get_list_price()
links = scraper.get_links()
addresses = scraper.get_address()

#fill google form
filler = Form_Filler()
