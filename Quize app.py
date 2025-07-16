import json

def save_question_to_file(questions, filename='quiz_data.json'):  # Fixed extension here too
    with open(filename, 'w') as f:
        json.dump(questions, f)
        print("\n Questions saved to file \n")

def create_questions():
    questions = []
    num = int(input("How many Questions to add? "))

    for i in range(num):
        print(f"\n Question {i+1}")
        q = input("Enter Question: ")
        a = input('Option A: ')
        b = input("Option B: ")
        c = input("Option C: ")
        d = input("Option D: ")
        ans = input("Correct Answer (A/B/C/D): ").strip().upper()

        questions.append({
            'question': q,
            'options': [f"A. {a}", f"B. {b}", f"C. {c}", f"D. {d}"],
            'answer': ans   # Changed key to 'answer' lowercase
        })

    save_question_to_file(questions)

def load_question_from_file(filename='quiz_data.json'):  # Fixed extension
    with open(filename, 'r') as f:
        return json.load(f)

def take_quiz():   # fixed function name from take_quize to take_quiz
    try:
        questions = load_question_from_file()
    except FileNotFoundError:
        print('No quiz found! Please ask the teacher to add the questions first.')
        return

    print("Welcome Students! Let's begin the quiz")
    student_name = input("Enter your name: ")
    score = 0

    for q in questions:
        print("\n" + q['question'])  # Fixed key 'question'
        for option in q['options']:   # Fixed key 'options'
            print(option)
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == q['answer']:   # Fixed key 'answer'
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! Correct Answer: {q['answer']}")

    percentage = (score / len(questions)) * 100
    print(f"\nQuiz over, {student_name}!")
    print(f"Your score: {score} / {len(questions)}")
    print(f"Percentage: {percentage:.2f}%")

    if percentage >= 80:
        print("Excellent!")
    elif percentage >= 50:
        print("Good job!")
    else:
        print("Needs Improvement")

    save_result(student_name, score, percentage)

def save_result(name, score, percentage, filename="results.txt"):  # fixed filename typo
    with open(filename, 'a') as f:
        f.write(f"{name}: Score = {score}, Percentage = {percentage:.2f}%\n")
    print("📝 Result saved to results.txt")

def main():
    while True:
        print("\n**** Quiz App *****")
        print("1. Add Question (Teacher)")
        print("2. Take Quiz (Student)")
        print("3. Exit")

        choice = input("Choose Option (1/2/3): ").strip()
        if choice == "1":
            create_questions()
        elif choice == "2":
            take_quiz()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

main()
