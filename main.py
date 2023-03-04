import tkinter
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Courier"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    gen_password = "".join(password_list)

    entry3.insert(0, gen_password)
    pyperclip.copy(gen_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    web = entry1.get()
    email = entry2.get()
    password = entry3.get()
    new_data = {web: {
        "email": email,
        "password": password,
        }
    }

    if len(web) == 0 and len(password) == 0:
        messagebox.showinfo(title="Oops", message=f"Please make sure there are no empty fields")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            entry1.delete(0, 'end')
            entry3.delete(0, 'end')


def find_password():
    web = entry1.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File doesn't exist")
    else:
        if web in data:
            email = data[web]["email"]
            password = data[web]["password"]
            messagebox.showinfo(title=web, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Info", message="No details")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tkinter.Canvas(width=200, height=200)
image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

label1 = tkinter.Label(text="Website")
label1.grid(column=0, row=1)

label2 = tkinter.Label(text="Email/Username:")
label2.grid(column=0, row=2)

label3 = tkinter.Label(text="Password")
label3.grid(column=0, row=3)


entry1 = tkinter.Entry(width=34)
entry1.grid(column=1, row=1)
entry1.focus()

entry2 = tkinter.Entry(width=43)
entry2.grid(column=1, row=2, columnspan=2)
entry2.insert(0, "czemrych.patrycja@gmail.com")

entry3 = tkinter.Entry(width=33)
entry3.grid(column=1, row=3)


button1 = tkinter.Button(text="Generate", command=generate_password)
button1.grid(column=2, row=3)

button2 = tkinter.Button(text="Add", width=37, command=save)
button2.grid(column=1, row=4, columnspan=2)

button3 = tkinter.Button(text="Search", width=6, command=find_password)
button3.grid(column=2, row=1)


window.mainloop()
