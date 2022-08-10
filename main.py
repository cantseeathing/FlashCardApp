from tkinter import *
import pandas as pd
import random

VERSION = 1.0
CANVAS_SIZE = (800, 526)
LANGUAGE = "Russian-English"
BACKGROUND_COLOR = "#B1DDC6"
PADDING = 50
FONT_STYLE_1 = ("Ariel", 40, "italic")
FONT_STYLE_2 = ("Ariel", 60, "bold")
RIGHT_BUTTON = "./images/right.png"
WRONG_BUTTON = "./images/wrong.png"
CARD_BACK = "./images/card_back.png"
CARD_FRONT = "./images/card_front.png"
DATA_FILE = "./russian_3000.csv"
title = f"{LANGUAGE} Flash Card v{VERSION}"
TIMER = 3
current_card = {}
# IMPORTING DATA
DATA_BASE = {}
DATA_BASE_SIZE = len(pd.read_csv(DATA_FILE))
PROGRESS_SIZE = DATA_BASE_SIZE
try:
    DATA_BASE = pd.read_csv("/data/progress.csv")
    # PROGRESS_SIZE = len(DATA_BASE)
except FileNotFoundError:
    DATA_BASE = pd.read_csv(DATA_FILE)
    # PROGRESS_SIZE = DATA_BASE_SIZE
finally:
    words = DATA_BASE.to_dict(orient="records")


# FUNCTIONS
def next_card():
    global current_card, FLIP_TIMER
    current_card = random.choice(words)
    window_object.after_cancel(FLIP_TIMER)
    canvas_object.itemconfig(card_language, text="Russian")
    canvas_object.itemconfig(card_word, text=current_card["Russian"])
    canvas_object.itemconfig(card_bg, image=canvas_front_img)
    canvas_object.itemconfig(card_language, fill="black")
    canvas_object.itemconfig(card_word, fill="black")
    # try:
    #     new_progress = len(pd.read_csv('./data/progress.csv'))
    # except FileNotFoundError:
    #     new_progress = 0
    # progress = DATA_BASE_SIZE-new_progress
    # progress_text_change = f"Progress: {progress}/{DATA_BASE_SIZE}"
    # progress_counter.config(text=progress_text_change)
    FLIP_TIMER = window_object.after(TIMER * 1000, func=flip_card)


def flip_card():
    canvas_object.itemconfig(card_language, text="English")
    canvas_object.itemconfig(card_word, text=current_card["English"])
    canvas_object.itemconfig(card_bg, image=canvas_back_img)
    canvas_object.itemconfig(card_language, fill="white")
    canvas_object.itemconfig(card_word, fill="white")


def remove_word():
    words.remove(current_card)
    data = pd.DataFrame(words)
    data.to_csv("./data/progress.csv", index=False)
    next_card()


# WINDOW OBJECT
window_object = Tk()
window_object.title(title)
window_object.config(background=BACKGROUND_COLOR, pady=PADDING, padx=PADDING)
FLIP_TIMER = window_object.after(TIMER * 1000, func=flip_card)
# FRONT CARD OBJECT
canvas_object = Canvas(width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
canvas_front_img = PhotoImage(file=CARD_FRONT)
canvas_back_img = PhotoImage(file=CARD_BACK)
card_bg = canvas_object.create_image(int(CANVAS_SIZE[0] / 2), int(CANVAS_SIZE[1] / 2), image=canvas_front_img)
canvas_object.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas_object.grid(row=0, column=0, columnspan=2)
# FRONT CARD TEXT
card_language = canvas_object.create_text(400, 150, text="Title", font=FONT_STYLE_1)
card_word = canvas_object.create_text(int(CANVAS_SIZE[0] / 2), int(CANVAS_SIZE[1] / 2), text="word", font=FONT_STYLE_2)
# progress_counter = Label(text=progress_text, font=FONT_STYLE_2, foreground="red", background=BACKGROUND_COLOR)
# progress_counter.config(padx=25, pady=25)
# progress_counter.grid(row=1, column=1)
# BUTTONS
false_icon = PhotoImage(file=WRONG_BUTTON)
false_button = Button(image=false_icon, command=next_card)
false_button.config(highlightthickness=0, background=BACKGROUND_COLOR)
false_button.grid(row=1, column=0)

true_icon = PhotoImage(file=RIGHT_BUTTON)
right_button = Button(image=true_icon, command=remove_word)
right_button.config(highlightthickness=0, background=BACKGROUND_COLOR)
right_button.grid(row=1, column=1)
# RUNTIME COMMANDS
next_card()
window_object.mainloop()
