import csv
import random
import os
import customtkinter as ctk
import word as wd

# Initialize the customtkinter theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

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
        self.words = []
        self.score = 0
        self.current_word = None
        self.total_words = 0

        self.cur_slide_num = 0
        self.slide_count = 0
        self.cur_slide_words = []
        self.cur_slide_label = ctk.CTkLabel(self, font=("Arial", 32))

        self.waiting_for_next = False  # Flag to control waiting for Enter after feedback

        # UI Elements
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.label_instruction = ctk.CTkLabel(self, text="Learn suomi :)", font=("Arials", 128))
        self.label_instruction.pack(pady=10)

        self.lesson_var = ctk.StringVar(value="Select a lesson")
        self.lesson_menu = ctk.CTkOptionMenu(
            self, variable=self.lesson_var, 
            values=self.lesson_files, 
            width=600, 
            height=50, 
            font=("Arials", 64))
        self.lesson_menu.pack()

        self.start_button = ctk.CTkButton(self, text="Start Quiz", command=self.load_lesson, width=600, height=50, font=("Arials", 64))
        self.start_button.pack(pady=20)

        self.continue_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Continue", 
            command=self.next_question, 
            width=600, 
            height=50, 
            font=("Arials", 64))

        self.label_question = ctk.CTkLabel(self, text="", font=("Arial", 64), width=600, height=50)
        self.label_question.pack(pady=20)

        self.entry_translation = ctk.CTkEntry(self, placeholder_text="Enter your translation here", width=600, height=50, font=("Arials", 32))
        #self.entry_translation.pack(pady=10)
        self.entry_translation.bind("<Return>", lambda event: self.handle_enter_key())  # Bind Enter key

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 32))
        self.label_feedback.pack(pady=10)

        self.label_score = ctk.CTkLabel(self.bottom_frame, text="Score: 0%", font=("Arial", 64))


        self.label_score.pack(side="left")
        self.continue_button.pack(side="right")

    def load_lesson(self):
        lesson_name = self.lesson_var.get()
        if lesson_name and lesson_name in self.lesson_files:
            self.words.clear()
            self.score = 0
            self.waiting_for_next = False


            with open("Lessons/" + lesson_name, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                slide = 0
                for row in csv_reader:
                    if len(row) >= 2:
                        finnish, english = row[0].strip(), row[1].strip()
                        self.words.append(wd.Word(finnish, english, "to be implemented", slide))
                    
                    if(row[0] == "-"):
                        slide+=1


            self.slide_count = slide
            
            self.total_words = len(self.words)
            self.print_slide()
        else:
            self.label_feedback.configure(text="Please select a valid lesson.", text_color="red")

    def next_question(self):

        if not self.cur_slide_words:
            if(self.cur_slide_num == self.slide_count):
                self.label_question.configure(text="Quiz Completed!")
                self.label_feedback.configure(text=f"Final Score: {round((self.score / self.total_words) * 100, 2)}%", text_color="green")
                #self.entry_translation.configure(state="disabled")
                #to turn on the buttons
            else:
                self.cur_slide_num += 1
                self.load_lesson()
            return

        self.label_question.pack()
        self.entry_translation.pack()
        self.cur_slide_label.pack_forget()

        self.current_word = random.choice(self.cur_slide_words)
        self.label_question.configure(text=f"Translate: {self.current_word.english}")
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

        finnish_word = self.current_word.finnish
        if user_input == finnish_word:
            self.label_feedback.configure(text="Correct! Press Enter to continue.", text_color="green")
            self.score += 1
        else:
            self.label_feedback.configure(
                text=f"Wrong! The correct translation is '{finnish_word}'. Press Enter to continue.",
                text_color="red"
            )
            
        self.cur_slide_words.remove(self.current_word)

        self.label_score.configure(text=f"Score: {round((self.score / self.total_words) * 100, 2)}%")
        self.waiting_for_next = True  # Set flag to wait for Enter before next question

    def print_slide(self):
        self.label_question.pack_forget()
        self.lesson_menu.pack_forget()
        self.start_button.pack_forget()
        self.entry_translation.pack_forget()
        self.label_feedback.pack_forget()
        text_for_label = ""

        for word in self.words:
            if(word.slide == self.cur_slide_num):
                self.cur_slide_words.append(word)
                text_for_label += f"{word.finnish} - {word.english} - {word.sentance}\n"

        self.cur_slide_label.configure(text = text_for_label)
        self.cur_slide_label.pack()


if __name__ == "__main__":
    app = VocabularyQuizApp()
    app.mainloop()
