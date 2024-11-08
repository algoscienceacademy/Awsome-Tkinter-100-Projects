import tkinter as tk
from tkinter import messagebox

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Simple Quiz App")
        self.geometry("600x400")
        self.configure(bg="#fafafa")  # Lighter background for better readability
        
        # Questions and answers
        self.questions = [
            {
                "question": "What is the capital of France?",
                "choices": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "choices": ["Earth", "Mars", "Jupiter", "Saturn"],
                "answer": "Mars"
            },
            {
                "question": "What is the largest ocean on Earth?",
                "choices": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "answer": "Pacific"
            },
            {
                "question": "Who developed the theory of relativity?",
                "choices": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"],
                "answer": "Albert Einstein"
            }
        ]
        
        self.current_question = 0
        self.score = 0

        # Label for displaying the question
        self.question_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="#fafafa", fg="#333333")
        self.question_label.pack(pady=20)

        # Radio buttons for answer choices
        self.answer_var = tk.StringVar(value="")
        self.answer_buttons = []
        for i in range(4):
            button = tk.Radiobutton(self, text="", variable=self.answer_var, value="", font=("Arial", 12), bg="#ffffff", fg="#333333", selectcolor="#B0E0E6")
            button.pack(anchor="w", padx=20, pady=5)
            self.answer_buttons.append(button)

        # Submit button to check the answer
        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief="flat")
        self.submit_button.pack(pady=20)

        # Label for showing score
        self.score_label = tk.Label(self, text="Score: 0", font=("Arial", 14), bg="#fafafa", fg="#333333")
        self.score_label.pack()

        # Load the first question
        self.load_question()

    def load_question(self):
        """Load the current question and choices into the app."""
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])

        for i, choice in enumerate(question_data["choices"]):
            self.answer_buttons[i].config(text=choice, value=choice)

    def check_answer(self):
        """Check the user's answer and update the score."""
        selected_answer = self.answer_var.get()
        correct_answer = self.questions[self.current_question]["answer"]

        if selected_answer == correct_answer:
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}")

        # Move to the next question
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        """End the quiz and show the result."""
        messagebox.showinfo("Quiz Over", f"Your final score is: {self.score}/{len(self.questions)}")
        self.quit()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()