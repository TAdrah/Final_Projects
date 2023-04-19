from redfin_scraper import RedFin_Scraper
from form_filler import Form_Filler
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pprint
from set_filters import Filters

url = ''

def start(url):
    """
    Given a url, this function will go there & scrape the date, cost & link then post to google sheets
    :param: url as string
    :return:
    """
    scraper = RedFin_Scraper(url)

    prices = scraper.get_list_price()
    links = scraper.get_links()
    addresses = scraper.get_address()

    #fill google form
    filler = Form_Filler()
    filler.answer_questions(addresses, prices, links)


def start():
    """
    - Gets values from inputs
    - get correct redfin url
    - add values to the url & go there
    - scrape address, cost, link
    - post to google sheets
    """
    inputs = {}

    if list_of_entries[0].get() == '' or list_of_entries[1].get() == '':
        if list_of_entries[0].get() == '':
            list_of_entries[0].focus_set()
        else:
            list_of_entries[1].focus_set()
        messagebox.showinfo("Error", "City & State are required!")
        return ''

    for i in range(len(list_of_entries)):
        inputs[labels[i]] = list_of_entries[i].get()
    for i in range(len(list_of_combos)):
        inputs[drop_down_menus[i][0]] = list_of_combos[i].get()

    selected_text_list = [property_type_listbox.get(i) for i in property_type_listbox.curselection()]
    print(selected_text_list)
    # starts on 2nd value in list to avoid adding a + in an empty var

    try:
        prop_text = selected_text_list[0]
        for i in selected_text_list[1:]:
            prop_text = prop_text + "+" + i
        inputs["property_type"] = prop_text
    except IndexError:
        inputs["property_type"] = 'House'

    new_inputs = {key: value for (key, value) in inputs.items() if value != '' and value != 'any'}

    filters = Filters()
    global url
    url = filters.get_url(new_inputs)


root = tk.Tk()
root.title("Real Estate Filter")

# Create labels and entry fields
labels = ["city", "state", "min-price", "max-price", "sqftMin", "sqftMax", "min-parking", "max_parking", "remarks", ]

list_of_entries = []
for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    list_of_entries.append(entry)

# Create drop-down menus
drop_down_menus = [
    ("min-beds", ["any", "studio", "1", "2", "3", "4", "5+"]),
    ("max-beds", ["any", "studio", "1", "2", "3", "4", "5+"]),
    ("min-baths", ["any", "1", "1.5+", "2+", "2.5+", "3+", "4+"]),
    ("max-baths", ["any", "1", "1.5+", "2+", "2.5+", "3+", "4+"]),
    ("pool-type", ["any", "Private pool", "Community pool", "Private or Community pool", "No Private pool"]),
    ("property-type", ["House", "Townhouse", "Condo", "Land", "Multifamily", "Mobile", "Co-op", "Other"]),
]

list_of_combos = []
for i, (label, options) in enumerate(drop_down_menus):
    if label == 'property_type':
        continue
    else:
        tk.Label(root, text=label).grid(row=i, column=2, pady=5)
        combo = ttk.Combobox(root, values=options)
        combo.grid(row=i, column=3)
        combo.set(options[0])
        list_of_combos.append(combo)

property_label = tk.Label(root, text="property_type: ")
property_label.grid(row=7, column=2)

# Select multiple property types
property_type_var = tk.StringVar(value=drop_down_menus[5][1])
property_type_listbox = tk.Listbox(root, listvariable=property_type_var, selectmode=tk.MULTIPLE)
property_type_listbox.grid(row=7, column=3)

search_box = tk.Button(root, text="Search", command=start)
search_box.grid(row=10, pady=10)

start(url)
root.mainloop()
