import streamlit as st

st.title("My first streamlit app")
st.header("This is a header")
st.subheader("This is sub header")
st.markdown("Text with **formatting**")
st.write("Hello World Streamlit!")

name = st.text_input("Enter your name")
st.write(f"Hello {name}")

age = st.number_input("Enter your age:")
st.write(f"You are {age} years old")

if st.button("Click me"):
    st.write("Button clicked!")

number = st.slider("Pick a number", 0, 100)
st.write(f"You picked {number}")

city = st.selectbox("Choose your city", ["Chennai", "Bengaluru", "Mumbai"])
st.write(f"You selected {city}")

agree = st.checkbox("I agree to the terms and conditions")
if agree:
    st.write("Thank you for agreeing")

st.success("This is a success message")
st.warning("This is a warning message")
st.error("This is an error message")
st.info("This is an info message")