import tkinter as tk
import json
import keyboard
from tkinter import messagebox


def load_data() -> dict:
    """
    If data.txt exists, load info. Otherwise, create empty dictionary
    """
    try:
        with open('data.txt', 'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}
    return data


def update_data(data):
    """
    Create data.txt if it doesn't exist, update file with data
    """
    with open('data.txt', 'w') as file:
        json.dump(data, file)


def add_update_snippet():
    """
    Adds or updates a snippet to gui, and data file,
    """
    abbreviation = abv_entry.get()
    expansion = text_entry.get('1.0', 'end')

    # ensure both fields are filled out and update data
    if abbreviation and expansion != '\n':
        data[abbreviation] = expansion
        keyboard.add_abbreviation(abbreviation, expansion)
        update_data(data)
        create_label()
    else:
        messagebox.showinfo("Error", "Both abbreviation & expansion are required to create a snippet")


def delete_snippet():
    """
    Deletes the snippet from existing labels & data.txt
    """

    abbreviation = abv_entry.get()

    # deletes the abbreviation in data & recreates labels
    if abbreviation in data:
        del data[abbreviation]
        keyboard.remove_abbreviation(abbreviation)
        update_data(data)
        create_label()
    else:
        messagebox.showinfo("Error", "Abbreviation is not saved")



def create_label():
    """
    Create & display abbreviations to the gui
    """
    # delete all labels
    for widget in new_labels.winfo_children():
        widget.destroy()

    # create new labels
    for key, value in data.items():
        label = tk.Label(new_labels, text=f'{key} | {value}')
        label.pack(pady=5)


# ----- set up UI ----- #

root = tk.Tk()
root.title("Text Expander")
root.geometry("800x600")
root.configure(padx=20, pady=20)

add_button = tk.Button(root, text='Add snippet', command=add_update_snippet)
add_button.pack(side="left")

del_button = tk.Button(root, text='Delete snippet', command=delete_snippet)
del_button.pack(side="left")

abv_label = tk.Label(root, text="Abbreviation")
abv_label.pack()

abv_entry = tk.Entry(root)
abv_entry.pack()

text_label = tk.Label(root, text="Text")
text_label.pack()

text_entry = tk.Text(root, width=50, height=15)
text_entry.pack()

existing_abv_label = tk.Label(root, text='Existing abbreviations:')
existing_abv_label.pack(side='left')

new_labels = tk.Label(root)
new_labels.pack(pady=5)


data = load_data()
create_label()
for key, value in data.items():
    keyboard.add_abbreviation(key, value)

root.mainloop()
