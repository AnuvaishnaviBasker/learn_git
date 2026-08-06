import streamlit as st

from chatbot import ask_farmassist

st.set_page_config(
    page_title="FarmAssist AI",
    page_icon="🌾"
)


st.title("🌾 FarmAssist AI")


# ==============================
# Sidebar
# ==============================

st.write(
        """
        Knowledge Sources:

        ✅ Farmer Markets

        ✅ Government Schemes

        ✅ Infrastructure Facilities

        ✅ Agriculture Support Programs
        """
    )


if st.button("🗑 Clear Chat"):

        st.rerun()



# ==============================
# Suggested Questions
# ==============================

st.write("Try asking:")


col1, col2, col3 = st.columns(3)


with col1:
    st.button(
        "Where to sell vegetables?"
    )


with col2:
    st.button(
        "Cold storage support?"
    )


with col3:
    st.button(
        "Government schemes?"
    )



# ==============================
# Chat Input
# ==============================

question = st.chat_input(
    "Ask your farming question..."
)



if question:

    st.write("### 👨‍🌾 Farmer")
    st.write(question)


    try:

        with st.spinner(
            "Searching FarmAssist knowledge base..."
        ):

            answer = ask_farmassist(
                question
            )


        st.write("### 🌾 FarmAssist")

        st.write(answer)



    except Exception as e:

        st.error(
            "FarmAssist failed"
        )

        st.exception(e)