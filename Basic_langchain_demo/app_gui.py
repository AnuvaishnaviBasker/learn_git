import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# 1. Page Configuration & Styling
st.set_page_config(page_title="AI Master Chef", page_icon="🍳", layout="centered")
st.title("🍳 AI Master Chef")
st.caption("A smart, conversational sous-chef that remembers your ingredients and builds recipes.")

# 2. Initialize Model and Chain (Cached so it doesn't rebuild on every click)
@st.cache_resource
def init_chain():
    model = ChatOllama(model="llama3.2", temperature=0.7)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a master chef. You remember what ingredients the user has already mentioned and help them build a cohesive recipe idea step by step. Keep answers under 3 sentences."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    return prompt_template | model | StrOutputParser()

chef_chain = init_chain()

# 3. Initialize Session State for Chat History if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Display Past Conversation History (Rendered beautifully as chat bubbles)
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🍳"):
            st.write(message.content)

# 5. Handle New User Input
if user_input := st.chat_input("What ingredients are we cooking with today?"):
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("assistant", avatar="🍳"):
        with st.spinner("Chef is brainstorming..."):
            response_text = chef_chain.invoke({
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })
            st.write(response_text)

    st.session_state.chat_history.append(AIMessage(content=response_text))
