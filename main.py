from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
done_words = []
rand_dict = {}
to_learn= {}
# ----------------------------------- CREATE FALSH CARDS ---------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original = pandas.read_csv("data/data.csv")
    to_learn = original.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def generate_new_word():
    global rand_dict, flip_timer
    window.after_cancel(flip_timer)
    try:
        rand_dict = random.choice(to_learn)
    except IndexError:
        print("All learned")
    else:
        done_words.append(rand_dict)
        canvas.itemconfig(lang_text, text="French", fill="black")
        canvas.itemconfig(front_text, text=rand_dict["French"], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(3000, flip_card)


# ----------------------------------- SAVE PROGRESS --------------------------- #


def known_cards():
    generate_new_word()
    if rand_dict in to_learn:
        try:
            to_learn.remove(rand_dict)
            to_learn_data = pandas.DataFrame(to_learn)
            to_learn_data.to_csv("data/words_to_learn.csv", index=False)
        except IndexError:
            print("all cards learned")
        print(len(to_learn))


# ----------------------------------- FLIP CARDS ------------------------------ #


def flip_card():
    canvas.itemconfig(lang_text, text="English", fill="white")
    canvas.itemconfig(front_text, text=rand_dict["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# ----------------------------------- UI SETUP -------------------------------- #


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526,
                bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="Images/card_front.png")
card_back_img = PhotoImage(file="Images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
lang_text = canvas.create_text(
    400, 150, text="French", fill="black", font=("Arial", 40, "italic"))

front_text = canvas.create_text(
    400, 263, text="Yo", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="Images/right.png")
right_button = Button(image=right_img, highlightthickness=0,
                      command=known_cards)
right_button.grid(column=1, row=1)

left_img = PhotoImage(file="Images/wrong.png")
left_button = Button(image=left_img, highlightthickness=0,
                     command=generate_new_word)
left_button.grid(column=0, row=1)

generate_new_word()
window.mainloop()
