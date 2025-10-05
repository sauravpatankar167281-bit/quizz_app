import streamlit as st
import json
import random
import qrcode
from io import BytesIO
import os

# --- Load questions ---
file_path = os.path.join(os.path.dirname(__file__), "questio.json")
with open(file_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# --- Streamlit config ---
st.set_page_config(page_title="Python Quiz", page_icon="🎓")
st.title("🎓 Python Quiz App")

# --- QR Code ---
quiz_url = "https://your-deployed-app.streamlit.app"  # replace with your deployed URL
qr_img = qrcode.make(quiz_url)

# Convert PIL image to bytes for Streamlit
buf = BytesIO()
qr_img.save(buf, format="PNG")
buf.seek(0)

st.image(buf, caption="📱 Scan to open this quiz", use_container_width=True)
st.write(f"Or open directly: [Click here]({quiz_url})")

# --- Quiz logic using session_state ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.selected_questions = random.sample(questions, 5)
    st.session_state.show_result = False

if not st.session_state.show_result:
    q = st.session_state.selected_questions[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")
    choice = st.radio("Select your answer:", q['options'], key=st.session_state.current_q)

    if st.button("Submit"):
        if choice == q['answer']:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")

        # Move to next question or show result
        if st.session_state.current_q + 1 < len(st.session_state.selected_questions):
            st.session_state.current_q += 1
        else:
            st.session_state.show_result = True
else:
    st.subheader(f"🎉 Quiz Finished! Your Score: {st.session_state.score}/{len(st.session_state.selected_questions)}")
    if st.button("🔁 Restart Quiz"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.selected_questions = random.sample(questions, 5)
        st.session_state.show_result = False
