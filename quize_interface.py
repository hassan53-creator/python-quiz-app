import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"
QUESTIONS_FILE = "quiz_data.json"
RESULTS_FILE = "results.txt"

# Load or create default password config
def load_password():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("teacher_password", "admin123")
    else:
        # Create default config file
        with open(CONFIG_FILE, "w") as f:
            json.dump({"teacher_password": "admin123"}, f)
        return "admin123"

# Load questions list
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    return []

# Save questions list
def save_questions(questions):
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(questions, f, indent=4)

# Load results string
def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            return f.read()
    return ""

# Save a result line with timestamp
def save_result(name, score, total):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    percent = (score / total) * 100
    line = f"{timestamp} | {name}: Score = {score}/{total}, Percentage = {percent:.2f}%\n"
    with open(RESULTS_FILE, "a") as f:
        f.write(line)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App - Main Menu")
        self.root.geometry("400x300")
        self.show_main_menu()

    def show_main_menu(self):
        # Clear
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Quiz App", font=("Arial", 20)).pack(pady=30)

        tk.Button(self.root, text="Teacher Mode", font=("Arial", 14), command=self.open_teacher).pack(pady=10)
        tk.Button(self.root, text="Student Mode", font=("Arial", 14), command=self.open_student).pack(pady=10)

    def open_teacher(self):
        password = simpledialog.askstring("Password", "Enter Teacher Password:", show="*")
        if password == load_password():
            TeacherPanel(tk.Toplevel(self.root), self)
        else:
            messagebox.showerror("Access Denied", "Incorrect Password!")

    def open_student(self):
        StudentQuiz(tk.Toplevel(self.root), self)

class TeacherPanel:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Teacher Panel - Add Questions")
        self.root.geometry("600x650")

        tk.Label(root, text="Enter Question:", font=("Arial", 14)).pack(pady=5)
        self.question_entry = tk.Text(root, height=3, font=("Arial", 12))
        self.question_entry.pack(pady=5)

        self.options_entries = []
        for opt_label in ['A', 'B', 'C', 'D']:
            tk.Label(root, text=f"Option {opt_label}:", font=("Arial", 12)).pack()
            entry = tk.Entry(root, font=("Arial", 12), width=50)
            entry.pack(pady=3)
            self.options_entries.append(entry)

        tk.Label(root, text="Correct Answer:", font=("Arial", 14)).pack(pady=5)
        self.correct_answer_var = tk.StringVar(value="A")
        correct_menu = tk.OptionMenu(root, self.correct_answer_var, "A", "B", "C", "D")
        correct_menu.pack()

        tk.Button(root, text="Add Question", font=("Arial", 14), command=self.add_question).pack(pady=15)
        tk.Button(root, text="Save All Questions", font=("Arial", 14), command=self.save_questions).pack(pady=10)
        tk.Button(root, text="View Results", font=("Arial", 14), command=self.view_results).pack(pady=10)
        tk.Button(root, text="Clear Results", font=("Arial", 14), command=self.clear_results).pack(pady=10)
        tk.Button(root, text="Back to Main Menu", font=("Arial", 12), command=self.back_to_main).pack(pady=20)

        self.questions_list = load_questions()

    def add_question(self):
        q = self.question_entry.get("1.0", tk.END).strip()
        opts = [opt.get().strip() for opt in self.options_entries]
        ans = self.correct_answer_var.get()

        if not q or any(not o for o in opts):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        self.questions_list.append({
            "question": q,
            "options": [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"],
            "answer": ans
        })

        messagebox.showinfo("Added", "Question added successfully!")
        self.question_entry.delete("1.0", tk.END)
        for opt in self.options_entries:
            opt.delete(0, tk.END)

    def save_questions(self):
        save_questions(self.questions_list)
        messagebox.showinfo("Saved", "Questions saved successfully.")

    def view_results(self):
        data = load_results()
        results_win = tk.Toplevel(self.root)
        results_win.title("Quiz Results")
        results_win.geometry("500x350")

        if data:
            text_widget = tk.Text(results_win, wrap="word", font=("Arial", 12))
            text_widget.pack(expand=True, fill="both")
            text_widget.insert("1.0", data)
            text_widget.config(state="disabled")
        else:
            tk.Label(results_win, text="No results found!", font=("Arial", 14)).pack(pady=50)

    def clear_results(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all results?"):
            if os.path.exists(RESULTS_FILE):
                os.remove(RESULTS_FILE)
            messagebox.showinfo("Cleared", "All results cleared.")

    def back_to_main(self):
        self.root.destroy()
        self.app.show_main_menu()

class StudentQuiz:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Student Quiz")
        self.root.geometry("600x450")

        self.questions = load_questions()
        self.current_q = 0
        self.score = 0

        if not self.questions:
            messagebox.showerror("Error", "No quiz data found! Ask teacher to add questions.")
            self.root.destroy()
            return

        self.name = simpledialog.askstring("Name", "Enter your name:")
        if not self.name:
            messagebox.showinfo("Exit", "Name is required to take the quiz.")
            self.root.destroy()
            return

        self.display_question()

    def display_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        q = self.questions[self.current_q]
        tk.Label(self.root, text=f"Question {self.current_q + 1} of {len(self.questions)}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=q['question'], font=("Arial", 14), wraplength=500).pack(pady=10)

        self.selected_answer = tk.StringVar()
        for opt in q['options']:
            tk.Radiobutton(self.root, text=opt, variable=self.selected_answer, value=opt[0], font=("Arial", 12)).pack(anchor="w", padx=50)

        tk.Button(self.root, text="Next", font=("Arial", 14), command=self.next_question).pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12), command=self.back_to_main).pack(pady=10)

    def next_question(self):
        selected = self.selected_answer.get()
        if selected == self.questions[self.current_q]['answer']:
            self.score += 1

        self.current_q += 1
        if self.current_q < len(self.questions):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        percent = (self.score / len(self.questions)) * 100
        result_msg = f"Thank you, {self.name}!\n\nScore: {self.score} / {len(self.questions)}\nPercentage: {percent:.2f}%"

        if percent >= 80:
            remark = "🏆 Excellent!"
        elif percent >= 50:
            remark = "👍 Good job!"
        else:
            remark = "📖 Needs Improvement."

        tk.Label(self.root, text=result_msg, font=("Arial", 16)).pack(pady=30)
        tk.Label(self.root, text=remark, font=("Arial", 14)).pack()

        save_result(self.name, self.score, len(self.questions))

        tk.Button(self.root, text="Exit to Main Menu", command=self.back_to_main).pack(pady=20)

    def back_to_main(self):
        self.root.destroy()
        self.app.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
