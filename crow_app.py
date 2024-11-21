import csv
import random
import os
import customtkinter as ctk

# Initialize the customtkinter theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

def split_array(arr):
    num_parts = 0

    for word in arr:
        if(word[0] == "-"):
            num_parts+=1

    parts = [][num_parts]
    current_index = 0
    for word in arr:
        parts[current_index].append(word)        

        if(word.key == "-"):
            current_index+=1
    return parts    

class VocabularyQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Finnish Vocabulary Quiz")
        self.geometry("1280x720")
        
        path_lessons = "./Lessons/"

        # Lesson Files Setup
        self.lesson_files = [
            name for name in os.listdir(path_lessons) 
            if os.path.isfile(os.path.join(path_lessons, name)) and name.endswith('.csv')
            ]
        self.words = {}
        self.units = []
        self.unit_len = 0
        self.score = 0
        self.current_word = None
        self.total_words = 0
        self.waiting_for_next = False  # Flag to control waiting for Enter after feedback

        # UI Elements
        self.label_instruction = ctk.CTkLabel(self, text="Learn suomi :)", font=("Arial", 128))
        self.label_instruction.pack(pady=10)

        self.lesson_var = ctk.StringVar(value="Select a lesson")
        self.lesson_menu = ctk.CTkOptionMenu(
            self, variable=self.lesson_var, 
            values=self.lesson_files, 
            width=600, 
            height=50, 
            font=("Arials", 64))
        self.lesson_menu.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Quiz", command=self.load_lesson, width=600, height=50, font=("Arials", 64))
        self.start_button.pack(pady=10)

        self.label_question = ctk.CTkLabel(self, text="", font=("Arial", 64), width=600, height=50)
        self.label_question.pack(pady=20)

        self.entry_translation = ctk.CTkEntry(self, placeholder_text="Enter your translation here", width=600, height=50, font=("Arials", 32))
        self.entry_translation.pack(pady=10)
        self.entry_translation.bind("<Return>", lambda event: self.handle_enter_key())  # Bind Enter key

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 32))
        self.label_feedback.pack(pady=10)

        self.label_score = ctk.CTkLabel(self, text="Score: 0%", font=("Arial", 64))
        self.label_score.pack(pady=10)

    def load_lesson(self):
        lesson_name = self.lesson_var.get()
        if lesson_name and lesson_name in self.lesson_files:
            self.words.clear()
            self.score = 0
            self.waiting_for_next = False
            # Load words from the selected CSV file
            with open("Lessons/" + lesson_name, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if len(row) >= 2:
                        finnish, english = row[0].strip(), row[1].strip()
                        self.words[finnish] = english

            self.total_words = len(self.words)

            self.units = split_array(self.words)

            self.next_question()
        else:
            self.label_feedback.configure(text="Please select a valid lesson.", text_color="red")

    def next_question(self):
        if not self.words:
            self.label_question.configure(text="Quiz Completed!")
            self.label_feedback.configure(text=f"Final Score: {round((self.score / self.total_words) * 100, 2)}%", text_color="green")
            #self.entry_translation.configure(state="disabled")
            return

        self.current_word = random.choice(list(self.words.items()))
        self.label_question.configure(text=f"Translate: {self.current_word[1]}")
        self.entry_translation.delete(0, ctk.END)
        self.label_feedback.configure(text="")
        self.waiting_for_next = False  # Reset flag to allow checking translation

    def handle_enter_key(self):
        if self.waiting_for_next:
            # Move to the next question if waiting for Enter
            self.next_question()
        else:
            # Otherwise, check the current translation
            self.check_translation()

    def check_translation(self):
        user_input = self.entry_translation.get().strip()
        if user_input.lower() == "stop!":
            self.label_question.configure(text="Quiz Stopped.")
            self.label_feedback.configure(text=f"Final Score: {round((self.score / self.total_words) * 100, 2)}%", text_color="blue")
            #self.entry_translation.configure(state="disabled")
            return

        finnish_word, english_word = self.current_word
        if user_input == finnish_word:
            self.label_feedback.configure(text="Correct! Press Enter to continue.", text_color="green")
            self.score += 1
        else:
            self.label_feedback.configure(
                text=f"Wrong! The correct translation is '{finnish_word}'. Press Enter to continue.",
                text_color="red"
            )

        del self.words[finnish_word]
        self.label_score.configure(text=f"Score: {round((self.score / self.total_words) * 100, 2)}%")
        self.waiting_for_next = True  # Set flag to wait for Enter before next question


if __name__ == "__main__":
    app = VocabularyQuizApp()
    app.mainloop()
