import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"
API_CHAT = f"{BACKEND_URL.rstrip('/')}/chat"

st.set_page_config(page_title="Farmer Schemes AI", page_icon="🌾")

st.title("Farmer Schemes Chat")
st.write(
    "Ask questions about Indian farmer schemes using the backend API. "
    "Start the backend before sending a request."
)

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_area("Enter your question", height=140)

if st.button("Send"):
    if not question.strip():
        st.warning("Please enter a question before sending.")
    else:
        payload = {
            "question": question.strip(),
            "chat_history": st.session_state.history,
        }

        try:
            response = requests.post(API_CHAT, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()

            answer = result.get("answer", "No answer returned.")
            st.session_state.history.append({"role": "user", "content": question.strip()})
            st.session_state.history.append({"role": "assistant", "content": answer})

            st.success("Response received.")
        except requests.RequestException as error:
            st.error(f"Could not connect to backend at {API_CHAT}: {error}")
        except ValueError:
            st.error("Backend returned invalid JSON.")

if st.session_state.history:
    st.markdown("---")
    st.markdown("### Conversation")
    for message in st.session_state.history:
        role = "You" if message["role"] == "user" else "Assistant"
        st.markdown(f"**{role}:** {message['content']}")

with st.expander("Backend setup instructions"):
    st.write(
        "Run the FastAPI backend before using the frontend app. "
        "The backend should be available at http://localhost:8000."
    )
    st.code(
        "cd Farmassit_ai && /Users/deepakmohanrajamohan/pyautogui/Farmassit_ai/.venv/bin/python -m uvicorn Backend.main:app --reload --port 8000",
        language="bash",
    )
    st.write("Then run this Streamlit app from the `front end` folder:")
    st.code("streamlit run \"front end/app.py\"", language="bash")
