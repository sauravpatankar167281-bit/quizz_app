import streamlit as st
import random
import json
import qrcode
from io import BytesIO

# --- Load questions ---
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# --- Streamlit page setup ---
st.set_page_config(page_title="Python Quiz", page_icon="🎓", layout="centered")
st.title("🎓 Python Quiz App")
st.write("Scan the QR code below to open this quiz on any device!")

# --- QR Code Generation ---
# Replace with your deployed Streamlit URL after first deployment
quiz_url = "https://your-quiz-app.streamlit.app"
qr = qrcode.QRCode(box_size=6, border=2)
qr.add_data(quiz_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
buf = BytesIO()
img.save(buf)
st.image(buf, use_container_width=True)

st.write("---")

# --- Initialize session state ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(questions, 5)

# --- Show question ---
def show_question():
    q = st.session_state.selected_questions[st.session_state.current_question]
    st.subheader(f"Q{st.session_state.current_question + 1}: {q['question']}")
    choice = st.radio("Select your answer:", q["options"], key=st.session_state.current_question)

    if st.button("Submit", key=f"submit_{st.session_state.current_question}"):
        if choice == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")

        st.session_state.current_question += 1
        st.experimental_rerun()

# --- Quiz logic ---
if st.session_state.current_question < len(st.session_state.selected_questions):
    show_question()
    progress = st.session_state.current_question / len(st.session_state.selected_questions)
    st.progress(progress)
else:
    st.subheader(f"🎉 Quiz Finished! Your Score: {st.session_state.score}/{len(st.session_state.selected_questions)}")
    if st.button("🔁 Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.selected_questions = random.sample(questions, 5)
        st.experimental_rerun()
