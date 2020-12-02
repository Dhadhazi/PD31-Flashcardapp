from tkinter import *
import random
import pandas
from os import path

BACKGROUND_COLOR="#B1DDC6"

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

to_learn = {}
current_word = {}
flip_timer = window.after(50000, lambda: print("This will not run, just to have something to cancel at setup"))


def choose_words_file():
    if path.exists("data/words_to_learn.csv"):
        return("data/words_to_learn.csv")
    elif path.exists("data/nlwords.csv"):
        return("data/nlwords.csv")
    else:
        print("WORD FILE NOT EXISTS")


def load_words_file():
    global to_learn;
    data = pandas.read_csv(choose_words_file())
    to_learn = data.to_dict(orient="records")


def save_progress():
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)


def get_new_word():
    return random.choice(to_learn)


def display_front(word):
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text="Dutch", fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")


def display_back(word):
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word, fill="white")


def remove_word_from_to_learn(word):
    to_learn.remove(word)


def right_answer():
    remove_word_from_to_learn(current_word)
    save_progress()
    new_word()


def new_word():
    global flip_timer, current_word
    window.after_cancel(flip_timer)
    current_word = get_new_word()
    display_front(current_word["Dutch"])
    flip_timer = window.after(3000, lambda: display_back(current_word["English"]))


def start():
    load_words_file()
    new_word()


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 260, image=card_front)
title_text = canvas.create_text(400, 150, text="Loading", font=("Ariel", 40))
word_text = canvas.create_text(400,260, text="loading", font=("Ariel", 60))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_answer)
right_button.grid(row=1, column=1)

start()

window.mainloop()