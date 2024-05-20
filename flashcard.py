import random
import pandas as pd
from tkinter import *
import os

# Building flash card application
#   - creating UI
#   - generate a random question
#   - check user input (right or wrong)
#   - check answer
#   - score mechanism
#   - game over function

BACKGROUND_COLOR = "#B1DDC6"

# Path to the image file
script_dir = os.path.dirname(__file__)
image_folder = os.path.join(script_dir , 'images')
image_path1 = os.path.join(image_folder , 'card_back.png')
image_path2 = os.path.join(image_folder , 'background.png')
image_path3 = os.path.join(image_folder , 'right.png')
image_path4 = os.path.join(image_folder , 'wrong.png')

# Path to the CSV file
csv_path = os.path.join(script_dir , 'data/french_words.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

current_question = None
current_answer = None


# Generate the random question
def cards():
    global current_question , current_answer
    random_row = df.sample(n=1).iloc[0]
    french_word = random_row['French']
    correct_english = random_row['English']
    random_english = df.sample(n=1).iloc[0]['English']

    # 50% chance to show the correct translation or a random wrong translation
    if random.choice([True , False]):
        current_answer = True
        displayed_english = correct_english
    else:
        current_answer = False
        displayed_english = random_english

    current_question = (french_word , correct_english)
    return french_word , displayed_english


# Display question on UI
def display_question():
    french_word , displayed_english = cards()
    canvas.itemconfig(question_text , text=french_word)
    canvas.itemconfig(answer_text , text=displayed_english)


# Check the user's answer
def check_ans( user_ans ):
    global current_answer
    if user_ans == current_answer:
        result_label.config(text="Correct!" , fg="green")
    else:
        result_label.config(text="Incorrect!" , fg="red")
    window.after(1300 , display_question)  # Display next question after 2 seconds


# Handle button press
def user( is_right ):
    check_ans(is_right)


# Creating UI
window = Tk()
window.title("Flash Card App")
window.config(padx=50 , pady=50 , bg=BACKGROUND_COLOR)

title = Label(window , text="Flash Card: Check Your French Knowledge" , font=(18))
title.grid(column=0 , row=0 , columnspan=3 , pady=10)

canvas = Canvas(window , height=400 , width=550 , bg=BACKGROUND_COLOR)
bg_img = PhotoImage(file=image_path2)
canvas.create_image(275 , 225 , image=bg_img)  # Adjust coordinates to center the image
canvas.grid(column=0 , row=1 , columnspan=3 , pady=20)
french = canvas.create_text(275,70, text="French Word ", font=(17))

# Keeping a reference to the image to prevent garbage collection
canvas.bg_img = bg_img
question_text = canvas.create_text(275 , 150 , text="" , font=('Helvetica' , 30 , 'bold'))
english = canvas.create_text(275,250, text="English Word ", font=(17))

answer_text = canvas.create_text(275 , 300 , text="" , font=('Helvetica' , 30))

right_img = PhotoImage(file=image_path3)
right_btn = Button(window , image=right_img , width=50 , height=50 , bg=BACKGROUND_COLOR, command=lambda: user(True))
right_btn.grid(column=0 , row=2 , pady=5 , padx=5)

wrong_img = PhotoImage(file=image_path4)
wrong_btn = Button(window , image=wrong_img , width=50 , height=50 ,bg=BACKGROUND_COLOR, command=lambda: user(False))
wrong_btn.grid(column=2 , row=2 , pady=5 , padx=5)

result_label = Label(window , text="" , font=('Helvetica' , 16))
result_label.grid(column=0 , row=3 , columnspan=3 , pady=10)

display_question()

window.mainloop()
