import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib
from database import insert_prediction, fetch_all_predictions

model = joblib.load("news_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

df = pd.read_csv("WELFake_Dataset.csv")

root = tk.Tk()
root.title("Fake News Detection System")
root.geometry("1200x720")
root.configure(bg="#0b0f1a")

# ================= Title =================
tk.Label(
    root,
    text="Fake News Detection System",
    font=("Segoe UI", 26, "bold"),
    bg="#0b0f1a",
    fg="#e5e7eb"
).pack(pady=20)

# ================= Main Layout =================
main_frame = tk.Frame(root, bg="#0b0f1a")
main_frame.pack(fill="both", expand=True, padx=30)

# ================= Left Panel =================
left_frame = tk.Frame(main_frame, bg="#111827", width=350, highlightbackground="#1f2933", highlightthickness=1)
left_frame.pack(side="left", fill="y", padx=12)

tk.Label(
    left_frame,
    text="Dataset Overview",
    font=("Segoe UI", 17, "bold"),
    bg="#111827",
    fg="#38bdf8"
).pack(pady=18)

total = len(df)
fake = len(df[df['label'] == 1])
real = len(df[df['label'] == 0])

def info_box(title, value):
    box = tk.Frame(left_frame, bg="#111827")
    box.pack(pady=14)

    tk.Label(box, text=title, font=("Segoe UI", 13, "bold"), bg="#111827", fg="#9ca3af").pack()
    tk.Label(box, text=value, font=("Segoe UI", 17), bg="#111827", fg="#f9fafb").pack()

info_box("Total News", total)
info_box("Fake News", fake)
info_box("Real News", real)

# ================= Right Panel =================
right_frame = tk.Frame(main_frame, bg="#111827", highlightbackground="#1f2933", highlightthickness=1)
right_frame.pack(side="right", fill="both", expand=True, padx=12)

tk.Label(
    right_frame,
    text="Enter News Text",
    font=("Segoe UI", 20, "bold"),
    bg="#111827",
    fg="#38bdf8"
).pack(pady=14)

news_text = tk.Text(
    right_frame,
    height=8,
    font=("Segoe UI", 13),
    bg="#020617",
    fg="#e5e7eb",
    insertbackground="#e5e7eb",
    wrap="word"
)
news_text.pack(fill="x", padx=25)

word_count_label = tk.Label(
    right_frame,
    text="Words: 0",
    font=("Segoe UI", 14, "bold"),
    bg="#111827",
    fg="#9ca3af"
)
word_count_label.pack(pady=8)

def update_word_count(event=None):
    text = news_text.get("1.0", "end").strip()
    word_count_label.config(text=f"Words: {len(text.split())}")

news_text.bind("<KeyRelease>", update_word_count)

result_label = tk.Label(right_frame, text="Result will appear here", font=("Segoe UI", 20, "bold"), bg="#111827", fg="#e5e7eb")
result_label.pack(pady=14)

message_label = tk.Label(right_frame, text="", font=("Segoe UI", 13), bg="#111827", fg="#9ca3af", wraplength=650, justify="center")
message_label.pack(pady=6)

confidence_label = tk.Label(right_frame, text="", font=("Segoe UI", 13, "bold"), bg="#111827", fg="#38bdf8")
confidence_label.pack(pady=6)

# ================= Prediction =================
def predict_news():
    text = news_text.get("1.0", "end").strip()
    if text == "":
        messagebox.showwarning("Warning", "Please enter news text")
        return

    transformed = vectorizer.transform([text])
    prediction = model.predict(transformed)[0]
    prob = model.predict_proba(transformed)[0]
    confidence = round(max(prob) * 100, 2)

    if prediction == 1:
        result_label.config(text="FAKE NEWS ❌", fg="#ef4444")
        message_label.config(text="This news appears to be misleading or false.", fg="#f87171")
        db_result = "Fake"
    else:
        result_label.config(text="REAL NEWS ✅", fg="#22c55e")
        message_label.config(text="This news looks authentic and reliable.", fg="#4ade80")
        db_result = "Real"

    confidence_label.config(text=f"Confidence: {confidence}%")

    try:
        insert_prediction(text, db_result, confidence)
    except Exception as e:
        print("Database Error:", e)

# ================= History Window =================
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Prediction History")
    history_window.geometry("1100x500")
    history_window.configure(bg="#020617")

    tk.Label(history_window, text="Prediction History", font=("Segoe UI", 18, "bold"), bg="#020617", fg="#38bdf8").pack(pady=10)

    text_box = tk.Text(history_window, wrap="word", bg="#020617", fg="#e5e7eb", font=("Segoe UI", 11))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    records = fetch_all_predictions()
    if not records:
        text_box.insert("end", "No history found.")
    else:
        for row in records:
            text_box.insert("end", f"ID: {row[0]}\nNews: {row[1][:200]}...\nResult: {row[2]} | Confidence: {row[3]}%\nTime: {row[4]}\n{'-'*80}\n")

    text_box.config(state="disabled")

# ================= Buttons =================
btn_frame = tk.Frame(right_frame, bg="#111827")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Predict News", font=("Segoe UI", 14, "bold"), bg="#2563eb", fg="white", width=16, command=predict_news).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="View History", font=("Segoe UI", 13, "bold"), bg="#059669", fg="white", width=14, command=show_history).grid(row=0, column=1, padx=10)

# ================= Footer =================
tk.Label(root, text="Model Loaded Successfully", bg="#020617", fg="#22c55e", anchor="w", font=("Segoe UI", 10)).pack(side="bottom", fill="x")

root.mainloop()