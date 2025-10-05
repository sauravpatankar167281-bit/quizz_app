import tkinter as tk
import random
import json

# Load questions from questions.json
with open(r"D:\siddhesh\questio.json", "r", encoding="utf-8") as f:
    questions = json.load(f)


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Python Quiz App")
        self.root.geometry("700x500")
        self.root.config(bg="#f0f0f0")

        self.score = 0
        self.current_question = 0

        # Title
        self.title_label = tk.Label(
            root, text="Python Quiz", font=("Comic Sans MS", 24, "bold"), bg="#4caf50", fg="white", pady=10
        )
        self.title_label.pack(fill="x")

        # Frame for question
        self.q_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        self.q_frame.pack(pady=20, fill="x")

        self.question_label = tk.Label(
            self.q_frame, text="", font=("Arial", 16), wraplength=650, justify="left", bg="#f0f0f0"
        )
        self.question_label.pack()

        # Frame for options
        self.options_frame = tk.Frame(root, bg="#f0f0f0")
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_frame,
                text="",
                width=50,
                font=("Arial", 14),
                bg="white",
                fg="#333",
                relief="raised",
                bd=2,
                activebackground="#4caf50",
                activeforeground="white",
                command=lambda i=i: self.check_answer(i)
            )
            btn.pack(pady=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#d4edda"))  # Hover effect
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="white"))
            self.option_buttons.append(btn)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(
            root, text="🔁 New Quiz", font=("Arial", 14), bg="#2196f3", fg="white", activebackground="#1976d2",
            activeforeground="white", command=self.reset_quiz
        )
        self.reset_button.pack(pady=20)

        # Load first set
        self.load_new_set()

    def load_new_set(self):
        self.score = 0
        self.current_question = 0
        self.result_label.config(text="")
        self.selected_questions = random.sample(questions, 5)
        self.show_question()

    def show_question(self):
        q = self.selected_questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}: {q['question']}")
        for i in range(4):
            self.option_buttons[i].config(text=q["options"][i], state="normal")
        self.result_label.config(text="")

    def check_answer(self, i):
        q = self.selected_questions[self.current_question]
        selected = q["options"][i]
        if selected == q["answer"]:
            self.result_label.config(text="✅ Correct!", fg="green")
            self.score += 1
        else:
            self.result_label.config(text=f"❌ Wrong! Correct: {q['answer']}", fg="red")

        for btn in self.option_buttons:
            btn.config(state="disabled")

        self.root.after(1500, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.selected_questions):
            self.show_question()
        else:
            self.question_label.config(
                text=f"🎉 Quiz Finished! Your Score: {self.score}/{len(self.selected_questions)}"
            )
            for btn in self.option_buttons:
                btn.config(state="disabled")

    def reset_quiz(self):
        self.load_new_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
