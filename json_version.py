from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

email = "szabo.gergo.bme@gmail.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    # password = ""
    # for char in password_list:
    #     password += char

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------ #
def find_password():
    website_to_find = website_entry.get()
    if len(website_to_find) == 0:
        messagebox.showinfo(title="Ooops", message="Please don't leave website field empty!")
    else:
        try:
            with open("geheimnis.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No data file found!")
        else:
            try:
                messagebox.showinfo(title=f"{website_to_find}",
                                    message=f"Email: {data[website_to_find]['email']}\nPassword: {data[website_to_find]['password']}")
            except KeyError:
                messagebox.showinfo(title="Error", message="No such website found!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_to_save = website_entry.get()
    email_to_save = email_entry.get()
    password_to_save = password_entry.get()
    new_data = {website_to_save: {
        "email": email_to_save,
        "password": password_to_save,
    }
    }

    if len(website_to_save) == 0 or len(password_to_save) == 0:
        messagebox.showinfo(title="Ooops", message="Please don't leave any field empty!")
    else:
        # write to json:
        # with open("geheimnis.json", "w") as file:
        #     json.dump(new_data, file, indent=4)

        # read from json:
        # with open("geheimnis.json", "r") as file:
        #     data = json.load(file)
        #     print(data)

        # update json (append):
        try:
            with open("geheimnis.json", "r") as file:
                # Reading existing data
                data = json.load(file)
        except FileNotFoundError:
            with open("geheimnis.json", "w") as file:
                # Saving data into json
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data in dictionary
            data.update(new_data)
            with open("geheimnis.json", "w") as file:
                # Saving updated data into json
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=30)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1)

email_entry = Entry(width=40)
email_entry.insert(0, email)
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate", command=generate_password, width=7)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", command=save, width=34)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=find_password, width=7)
search_button.grid(column=2, row=1)

window.mainloop()
