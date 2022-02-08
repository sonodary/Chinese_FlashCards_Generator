import tkinter as tk
from tkinter.simpledialog import askstring
import sys
import os
import pandas as pd
import random
import json

sys.path.append('/')
from Text_process import Text_processor
from Dict import json_to_dict

BACKGROUND_COLOR = "#B1DDC6"
current_directory = os.getcwd()

# The base class that helps the transition
class UI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Chinese study")
        self.config(padx=100, pady=100, bg=BACKGROUND_COLOR)
        self.minsize(width=1000, height=800)
        self._frame = None
        self.switch_frame(TopPage)

    # The function to switch the frame
    def switch_frame(self, frame_class, title=None):
        if title is not None:
            new_frame = frame_class(self, title)
        else:
            new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

# The UI of the top page
class TopPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        canvas = tk.Canvas(self, width=800, height=520, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.top_image = tk.PhotoImage(file=f"{current_directory}/images/panda.png")
        canvas.grid(column=0, row=0, columnspan=2)
        bg_image = canvas.create_image(400, 263, image=self.top_image)
        frequent_button = tk.Button(self, text="Most frequent words", highlightthickness=0, width=30, height=5,
                                    font=("Antique Olive", 20, "normal"), fg="brown", command=lambda: master.switch_frame(
                Everyday_Frequent)).grid(column=0, row=1)
        customized_button = tk.Button(self, text="Customized flash cards", highlightthickness=0, width=30, height=5, font=("Antique Olive", 20, "normal"), fg="green", command=lambda: master.switch_frame(
            Customized)).grid(column=1, row=1)

# The UI of the customized word page
class Customized(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR, padx=200, pady=150)
        top_page_button = tk.Button(self, text="Go back to start page",
                                    command=lambda: master.switch_frame(TopPage)).grid(column=0, row=3)
        create_card_button = tk.Button(self, text="Create new flash cards!", highlightthickness=0, width=30, height=5,
                                       font=("Antique Olive", 20, "normal"), fg="purple", pady=20, command=lambda: master.switch_frame(NewFlashCard)).grid(column=0, row=0)
        use_exist_button = tk.Button(self, text="Use flash cards!", highlightthickness=0, width=30, height=5,
                                     font=("Antique Olive", 20, "normal"), fg="purple", pady=20, command=lambda: master.switch_frame(ExistFlashCard)).grid(column=0, row=1)

# The UI of the existent flash card pages
class ExistFlashCard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR, padx=10)
        buttons = self.buttons()
        for i in range(len(buttons)):
            tk.Button(self, text=buttons[i], highlightthickness=0, width=12, height=2,
                      font=("Antique Olive", 20, "normal"), fg="brown", padx=10, command=lambda: master.switch_frame(
                    FlashCard, buttons[i])).grid(column=i % 5, row=i // 5 + 1)
        previous_page_button = tk.Button(self, text="Go back to previous page", pady=10, bg=BACKGROUND_COLOR,
                                         command=lambda: master.switch_frame(Customized)).grid(column=0, row=0)
        delete_button = tk.Button(self, text="Choose cards to delete", pady=10, bg=BACKGROUND_COLOR,
                                         command=self.delete).grid(column=4, row=0)

    # Create the buttons to use the existent flash cards
    def buttons(self):
        dir = f"{current_directory}/Customized_words"
        files = os.listdir(dir)
        files_file = [file for file in files if os.path.isfile(os.path.join(dir, file))]
        csv_files = [file for file in files_file if 'csv' in file]
        button_name = [name.replace('.csv', '') for name in csv_files]
        return sorted(button_name)

    # Create the button to delete the existent flash cards
    def delete(self):
        cards_to_delete = askstring(title="Delete", prompt="Type the name of the flashcard you want to delete")
        if os.path.exists(f"{current_directory}/Customized_words/{cards_to_delete}.txt"):
            os.remove(f"{current_directory}/Customized_words/{cards_to_delete}.txt")
            os.remove(f"{current_directory}/Customized_words/{cards_to_delete}.csv")
            tk.messagebox.showinfo(title="Result", message="Success")
        elif cards_to_delete is None:
            pass
        else:
            tk.messagebox.showinfo(title="Error", message="The card was not found")

# UI of flash cards
class FlashCard(tk.Frame):
    # Go to the next word
    def next_card(self):
        self.is_front = True
        self.pinyin_displayed = False
        self.current_card = random.choice(self.vocabulary_dic)
        self.canvas.itemconfig(self.bg_image, image=self.card_front_image)
        self.canvas.itemconfig(self.language, text="Chinese", fill="black")
        self.canvas.itemconfig(self.word, text=self.current_card["Vocabulary"], fill="black", font=("Ariel", 40, "bold"))
        self.canvas.itemconfig(self.pinyin, text="")

    # If the card is remembered, they will be deleted from flash cards
    def remembered(self):
        self.vocabulary_dic.remove(self.current_card)
        if self.current_card["Vocabulary"] in self.dict_data.keys():
            self.dict_data.pop(self.current_card["Vocabulary"])
        self.next_card()
        remembered_vocab = pd.DataFrame(self.vocabulary_dic)
        remembered_vocab.to_csv(f"{current_directory}/Customized_words/{self.title}.csv", index=False)

    # Flip the cards to see the translation
    def flip_card(self):
        if self.is_front:
            self.canvas.itemconfig(self.bg_image, image=self.card_back_image)
            self.canvas.itemconfig(self.language, text="English", fill="white")
            if len(self.current_card["Translation"]) > 100:
                font_size = 20
            else:
                font_size = 40
            self.canvas.itemconfig(self.word, text=self.current_card["Translation"], fill="white", font=("Ariel", font_size, "bold"))
            self.canvas.itemconfig(self.pinyin, text="")
            self.is_front = False
        else:
            self.canvas.itemconfig(self.bg_image, image=self.card_front_image)
            self.canvas.itemconfig(self.language, text="Chinese", fill="black")
            self.canvas.itemconfig(self.word, text=self.current_card["Vocabulary"], fill="black", font=("Ariel", 40, "bold"))
            self.is_front = True
            self.pinyin_displayed = False

    # Displays pinyin
    def display_pinyin(self):
        if self.is_front:
            self.canvas.itemconfig(self.pinyin, text=self.current_card["Pinyin"], fill="black")
            if self.pinyin_displayed:
                self.canvas.itemconfig(self.pinyin, text="")
                self.pinyin_displayed = False
            else:
                self.canvas.itemconfig(self.pinyin, text=self.current_card["Pinyin"], fill="black")
                self.pinyin_displayed = True

    # Save changes
    def save(self):
        with open(f"{current_directory}/Dict/Words_to_remember.json", "w") as outfile:
            json.dump(self.dict_data, outfile, ensure_ascii=False)

    # Fix the translation or pinyin if they are wrong
    def fix(self):
        # messagebox.showinfo(title="Alert", message="Pleases do not leave any fields empty")
        fix_pinyin = tk.messagebox.askyesno(title="Fix", message="Do you want to fix pinyin?")
        if fix_pinyin:
            new_pinyin = askstring("New pinyin", "What is the correct pinyin?")
            self.current_card["Pinyin"] = new_pinyin
            tk.messagebox.showinfo(title="Result", message="Success")
        else:
            fix_translation = tk.messagebox.askyesno(title="Fix", message="Do you want to fix translation?")
            if fix_translation:
                new_translation = askstring("New translation", "What is the correct translation?")
                self.current_card["Translation"] = new_translation
                tk.messagebox.showinfo(title="Result", message="Success")

    def __init__(self, master, title):
        self.current_card = None
        self.title = title
        self.is_front = True
        self.pinyin_displayed = False
        try:
            self.data = pd.read_csv(f"{current_directory}/Customized_words/{self.title}.csv")
        except FileNotFoundError:
            tk.messagebox.showinfo(title="Alert", message="File does not exist")
        self.vocabulary_dic = self.data.to_dict(orient="records")

        self.dict_data = {}
        with open(f'{current_directory}/Dict/Words_to_remember.json', "r") as json_data:
            self.dict_data = json.load(json_data)

        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR)

        # Canvas
        self.canvas = tk.Canvas(self, width=800, height=520, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.card_front_image = tk.PhotoImage(file=f"{current_directory}/images/card_front.png")
        self.card_back_image = tk.PhotoImage(file=f"{current_directory}/images/card_back.png")
        self.bg_image = self.canvas.create_image(400, 280, image=self.card_front_image)
        self.canvas.grid(column=0, row=0, columnspan=4)
        self.language = self.canvas.create_text(400, 50, text="Language", font=("Ariel", 20, "italic"))
        self.word = self.canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "bold"))
        self.pinyin = self.canvas.create_text(400, 220, text="", font=("Ariel", 20, "normal"))
        self.next_card()

        # Button
        self.right_image = tk.PhotoImage(file=f"{current_directory}/images/right.png")
        right_button = tk.Button(self, image=self.right_image, highlightthickness=0, command=self.remembered)
        right_button.grid(column=0, row=2)

        self.wrong_image = tk.PhotoImage(file=f"{current_directory}/images/wrong.png")
        wrong_button = tk.Button(self, image=self.wrong_image, highlightthickness=0, command=self.next_card)
        wrong_button.grid(column=3, row=2)

        flip_button = tk.Button(self, text="Flip", highlightthickness=0, width=10, height=3, font=("Ariel", 20, "normal"),
                             fg="blue", command=self.flip_card)
        flip_button.grid(column=1, row=2)

        pinyin_button = tk.Button(self, text="Pinyin", highlightthickness=0, width=9, height=3, font=("Ariel", 20, "normal"),
                               fg="brown", padx=10, command=self.display_pinyin)
        pinyin_button.grid(column=2, row=2)

        previous_page_button = tk.Button(self, text="Go back to the previous page",
                                         command=lambda: master.switch_frame(Customized)).grid(column=0, row=3)
        save_button = tk.Button(self, text="Save", width=20, command=self.save).grid(column=1, row=3)

        fix_button = tk.Button(self, text="fix", highlightthickness=0, font=("Ariel", 15, "normal"), width=20,
                            command=self.fix).grid(column=2, row=3)
        first_page_button = tk.Button(self, text="Go back to the top page",
                                      command=lambda: master.switch_frame(TopPage)).grid(column=3, row=3)


# The page to create a new flash card
class NewFlashCard(tk.Frame):
    def getTextInput(self):
        result = self.text_text.get("1.0", "end")
        file_name = ""
        while file_name == "":
            file_name = self.getCardName()
        if file_name != None:
            try:
                with open(f'{current_directory}/Customized_words/{file_name}.txt', 'w') as f:
                    f.write(result)
            except:
                tk.messagebox.showinfo(title="Warning", message="Invalid file name. Type another one")
                self.getTextInput()
            else:
                Text_processor.process(file_name, self.dict)

    # Ask for the name of the newly created flash card
    def getCardName(self):
        file_name = askstring("Flash card name", 'Enter the name of flashcards')
        if file_name is not None:
            if file_name == "":
                tk.messagebox.showinfo(title="Warning", message="Invalid file name. Type another one")
            else:
                tk.messagebox.showinfo(title="Success", message="Success! You can see the new flash card!")
            return file_name

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR, padx=80)
        text_label = tk.Label(self, text="Please enter the text to create flash cards", font=('Helvetica', 20, "bold"), bg=BACKGROUND_COLOR)
        text_label.grid(column=0, row=1)
        self.text_text = tk.Text(self, width=50)
        self.text_text.focus()
        self.text_text.grid(column=0, row=2, ipadx=150, ipady=100)
        self.dict = json_to_dict.convert()

        enter_button = tk.Button(self, height=1, width=10, text="Enter",
                            command=self.getTextInput)
        enter_button.grid(column=0, row=3)

        previous_page_button = tk.Button(self, text="Go back to previous page",
                                         command=lambda: master.switch_frame(Customized)).grid(column=0, row=0)

# UI for the most frequent cards
class Everyday_Frequent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR, pady=50)
        top_page_button = tk.Button(self, text="Go back to the start page",
                                    command=lambda: master.switch_frame(TopPage)).grid(column=0, row=0)
        tk.Label(self, text="To master language, it is very important to learn the words most frequently used!\nIn this mode, you can study the words most frequent used Chinese words!", font=('Helvetica', 20, "bold"),
                 bg=BACKGROUND_COLOR, pady=30).grid(column=0, row=1, rowspan=2)
        with open(f'{current_directory}/Frequent_words/number_of_memorized_words.txt') as f:
            line = f.readline()
        num_words = int(line)
        tk.Label(self, text=f"You have studied {num_words} words in total!",  font=('Helvetica', 50, "bold"),
                 bg=BACKGROUND_COLOR, pady=50).grid(column=0, row=3)
        start_button = tk.Button(self, text="Start", highlightthickness=0, width=20, height=3,
                                 font=("Antique Olive", 30, "normal"), fg="purple", pady=10, command=lambda: master.switch_frame(FrequentFlashCard, num_words)).grid(column=0, row=4)

# UI for the flash cards
class FrequentFlashCard(tk.Frame):

    def next_card(self):
        self.is_front = True
        self.pinyin_displayed = False
        self.current_card = random.choice(self.vocabulary_dic)
        self.canvas.itemconfig(self.bg_image, image=self.card_front_image)
        self.canvas.itemconfig(self.language, text="Chinese", fill="black")
        self.canvas.itemconfig(self.word, text=self.current_card["Vocabulary"], fill="black", font=("Ariel", 40, "bold"))
        self.canvas.itemconfig(self.pinyin, text="")

    def remembered(self):
        self.vocabulary_dic.remove(self.current_card)
        self.num_words += 1
        self.next_card()
        remembered_vocab = pd.DataFrame(self.vocabulary_dic)
        remembered_vocab.to_csv(f"{current_directory}/Frequent_words/Words_to_remember.csv", index=False)
        with open(f"{current_directory}/Frequent_words/number_of_memorized_words.txt", "w") as file:
            file.write(str(self.num_words))


    def flip_card(self):
        if self.is_front:
            self.canvas.itemconfig(self.bg_image, image=self.card_back_image)
            self.canvas.itemconfig(self.language, text="English", fill="white")
            if len(self.current_card["Translation"]) > 100:
                font_size = 20
            else:
                font_size = 40
            self.canvas.itemconfig(self.word, text=self.current_card["Translation"], fill="white", font=("Ariel", font_size, "bold"))
            self.canvas.itemconfig(self.pinyin, text="")
            self.is_front = False
        else:
            self.canvas.itemconfig(self.bg_image, image=self.card_front_image)
            self.canvas.itemconfig(self.language, text="Chinese", fill="black")
            self.canvas.itemconfig(self.word, text=self.current_card["Vocabulary"], fill="black", font=("Ariel", 40, "bold"))
            self.is_front = True
            self.pinyin_displayed = False

    def display_pinyin(self):
        if self.is_front:
            self.canvas.itemconfig(self.pinyin, text=self.current_card["Pinyin"], fill="black")
            if self.pinyin_displayed:
                self.canvas.itemconfig(self.pinyin, text="")
                self.pinyin_displayed = False
            else:
                self.canvas.itemconfig(self.pinyin, text=self.current_card["Pinyin"], fill="black")
                self.pinyin_displayed = True

    def fix(self):
        # messagebox.showinfo(title="Alert", message="Pleases do not leave any fields empty")
        fix_pinyin = tk.messagebox.askyesno(title="Fix", message="Do you want to fix pinyin?")
        if fix_pinyin:
            new_pinyin = askstring("New pinyin", "What is the correct pinyin?")
            self.current_card["Pinyin"] = new_pinyin
            tk.messagebox.showinfo(title="Result", message="Success")
        else:
            fix_translation = tk.messagebox.askyesno(title="Fix", message="Do you want to fix translation?")
            if fix_translation:
                new_translation = askstring("New translation", "What is the correct translation?")
                self.current_card["Translation"] = new_translation
                tk.messagebox.showinfo(title="Result", message="Success")

    def __init__(self, master, num):
        self.current_card = None
        self.num_words = num
        self.is_front = True
        self.pinyin_displayed = False
        try:
            self.data = pd.read_csv(f"{current_directory}/Frequent_words/Words_to_remember.csv").loc[0:29]
        except FileNotFoundError:
            tk.messagebox.showinfo(title="Alert", message="File does not exist")
        self.vocabulary_dic = self.data.to_dict(orient="records")

        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BACKGROUND_COLOR)

        # Canvas
        self.canvas = tk.Canvas(self, width=800, height=520, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.card_front_image = tk.PhotoImage(file=f"{current_directory}/images/card_front.png")
        self.card_back_image = tk.PhotoImage(file=f"{current_directory}/images/card_back.png")
        self.bg_image = self.canvas.create_image(400, 280, image=self.card_front_image)
        self.canvas.grid(column=0, row=0, columnspan=4)
        self.language = self.canvas.create_text(400, 50, text="Language", font=("Ariel", 20, "italic"))
        self.word = self.canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "bold"))
        self.pinyin = self.canvas.create_text(400, 220, text="", font=("Ariel", 20, "normal"))
        self.next_card()

        # Button
        self.right_image = tk.PhotoImage(file=f"{current_directory}/images/right.png")
        right_button = tk.Button(self, image=self.right_image, highlightthickness=0, command=self.remembered)
        right_button.grid(column=0, row=2)

        self.wrong_image = tk.PhotoImage(file=f"{current_directory}/images/wrong.png")
        wrong_button = tk.Button(self, image=self.wrong_image, highlightthickness=0, command=self.next_card)
        wrong_button.grid(column=3, row=2)

        flip_button = tk.Button(self, text="Flip", highlightthickness=0, width=10, height=3, font=("Ariel", 20, "normal"),
                             fg="blue", command=self.flip_card)
        flip_button.grid(column=1, row=2)

        pinyin_button = tk.Button(self, text="Pinyin", highlightthickness=0, width=9, height=3, font=("Ariel", 20, "normal"),
                               fg="brown", padx=10, command=self.display_pinyin)
        pinyin_button.grid(column=2, row=2)

        previous_page_button = tk.Button(self, text="Go back to the previous page",
                                         command=lambda: master.switch_frame(Everyday_Frequent)).grid(column=0, row=3)
        save_button = tk.Button(self, text="Save", width=20).grid(column=1, row=3)

        fix_button = tk.Button(self, text="fix", highlightthickness=0, font=("Ariel", 15, "normal"), width=20,
                            command=self.fix).grid(column=2, row=3)
        first_page_button = tk.Button(self, text="Go back to the top page",
                                      command=lambda: master.switch_frame(TopPage)).grid(column=3, row=3)


if __name__ == "__main__":
    app = UI()
    app.mainloop()




