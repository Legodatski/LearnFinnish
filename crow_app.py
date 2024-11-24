import csv
import random
import os
import customtkinter as ctk
import word as wd
import help as hp

# Initialize the customtkinter theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

class VocabularyQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Finnish Vocabulary Quiz")
        self.geometry("1920x720")
        
        self.path_lessons = "./Lessons/"

        # Lesson Files Setup
        self.lesson_files = [
            name for name in os.listdir(self.path_lessons) 
            if os.path.isfile(os.path.join(self.path_lessons, name)) and name.endswith('.csv')
            ]
        self.words = []
        self.score = 0
        self.current_word = None
        self.current_word_index = None
        self.total_words = 0

        self.cur_slide_num = 0
        self.slide_count = 0
        self.cur_slide_words = []
        self.cur_slide_label = ctk.CTkLabel(self, font=("Arial", 32))

        self.waiting_for_next = False  # Flag to control waiting for Enter after feedback

        # UI Elements
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x")
        self.answers = ctk.CTkLabel(self, font=("Arials", 24))

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

        self.start_button = ctk.CTkButton(
            self, 
            text="Start Quiz", 
            command=self.load_lesson, 
            width=600, 
            height=50, 
            font=("Arials", 64))
        self.start_button.pack(pady=20)

        self.continue_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Continue", 
            command=self.handle_enter_key, 
            width=600, 
            height=50, 
            font=("Arials", 64))

        self.label_question = ctk.CTkLabel(self, text="", font=("Arial", 64), width=600, height=50)
        self.label_question.pack(pady=20)

        self.entry_translation = ctk.CTkEntry(self, placeholder_text="Enter your translation here", width=600, height=50, font=("Arials", 32))
        #self.entry_translation.pack(pady=10)
        self.entry_translation.bind("<Return>", lambda event: self.handle_enter_key())

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 32))
        self.label_feedback.pack(pady=10)

        self.label_score = ctk.CTkLabel(self.bottom_frame, text="Score: 0%", font=("Arial", 64))


        self.label_score.pack(side="left")
        self.continue_button.pack(side="right")

    def load_lesson(self):
        lesson_name = self.lesson_var.get()

        if lesson_name and lesson_name in self.lesson_files:
            self.words.clear()
            self.cur_slide_words.clear()
            self.score = 0
            self.label_score.configure(text=f"Score: 0%")
            self.waiting_for_next = False


            with open(self.path_lessons + lesson_name, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                slide = 0
                for row in csv_reader:
                    if(row[0] == "-"):
                        slide+=1
                    else:
                        finnish = row[0].strip()
                        english = row[1].strip()
                        sentance = "-"

                        if(len(row) > 2):
                            sentance = row[2].strip()

                            if(len(row) > 3):
                                sentance_answer = row[3].strip()
                            else:
                                sentance_answer = row[0].strip()

                        self.words.append(wd.Word(finnish, english, sentance, sentance_answer, slide))

            self.slide_count = slide
            
            self.total_words = len(self.words)
            self.print_slide()
        else:
            self.label_feedback.configure(text="Please select a valid lesson.", text_color="red")

    def next_tranlation(self):    
        #UI
        self.label_question.pack()
        self.entry_translation.pack()
        self.cur_slide_label.pack_forget()

        self.current_word = random.choice(self.cur_slide_words)

        if(self.current_word.english == "-"):
            self.answers.pack(side='bottom')
            self.label_question.configure(text=f"{self.current_word.sentance}")
        else:
            self.answers.pack_forget()
            self.label_question.configure(text=f"Translate: {self.current_word.english}")

        self.entry_translation.delete(0, ctk.END)
        self.label_feedback.configure(text="")
        self.waiting_for_next = False  # Reset flag to allow checking translation

    def handle_enter_key(self):
        if self.waiting_for_next:
            # Move to the next question if waiting for Enter
            if not self.words:
                #to complete quiz
                self.complete_quiz()
            elif not self.cur_slide_words:
                #load new slide
                self.cur_slide_num += 1
                self.print_slide()
            else:
                self.next_tranlation()

        else:
            self.check_quenstion()
            

    def check_quenstion(self):
        self.label_feedback.pack()
        user_input = self.entry_translation.get().strip()

        if user_input.lower() == "stop":
            self.complete_quiz()
            return
        
        correct_answer = ""
        finnish_word = self.current_word.finnish

        if((self.current_word.english == "-" or self.current_word.sentance == "-") and wd.Word.lenght(self.current_word) >= 4):
            correct_answer = self.current_word.answer_sentance
        else:
            correct_answer = finnish_word 

        if user_input.lower() == correct_answer:
            self.label_feedback.configure(text="Correct! Press Enter to continue.", text_color="green")
            self.score += 1
        else:
            self.label_feedback.configure(
                text=f"Wrong! The correct answer is '{correct_answer}'. Press Enter to continue.",
                text_color="red"
            )

        self.current_word_index = self.cur_slide_words.index(self.current_word)

        if(self.current_word.english == "-" or self.current_word.sentance == "-"):
            self.cur_slide_words.remove(self.current_word)
            self.words.remove(self.current_word)
        else:
            self.cur_slide_words[self.current_word_index].english = "-"

        self.label_score.configure(text=f"Score: {round((self.score / (self.total_words * 2)) * 100, 2)}%")
        self.waiting_for_next = True  # Set flag to wait for Enter before next question

    def print_slide(self):
        #UI
        self.label_question.pack_forget()
        self.lesson_menu.pack_forget()
        self.start_button.pack_forget()
        self.entry_translation.pack_forget()
        self.label_feedback.pack_forget()

        text_for_label = ""
        answers = ""

        for word in self.words:

            cmp_sentance = ""
            for c in word.sentance:
                
                if c == "_":
                    cmp_sentance += word.answer_sentance
                else:
                    cmp_sentance += c

            if(word.slide == self.cur_slide_num):
                self.cur_slide_words.append(word)
                text_for_label += f"{word.finnish}  -   {word.english}      {cmp_sentance}\n"
                
                answers += f"{word.answer_sentance} "

        #UI
        self.cur_slide_label.configure(self, text = text_for_label, justify='left', padx = 30)
        self.cur_slide_label.pack()

        self.waiting_for_next = True
        self.answers.configure(text = answers)

    def complete_quiz(self):
        self.label_question.configure(text="Quiz Completed!")
        self.label_feedback.configure(text=f"Final Score: {round((self.score / (self.total_words * 2)) * 100, 2)}%", text_color="green")
        #self.entry_translation.configure(state="disabled")
        self.entry_translation.pack_forget()
        self.lesson_menu.pack(pady = 20)
        self.start_button.pack()

if __name__ == "__main__":
    app = VocabularyQuizApp()
    app.mainloop()
