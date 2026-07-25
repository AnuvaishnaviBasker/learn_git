import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️")

st.title("⚖️ BMI Calculator")

st.write("Enter your height and weight to calculate your Body Mass Index (BMI).")

height = st.number_input(
    "Height (in centimeters)",
    min_value=50.0,
    max_value=250.0,
    value=170.0,
)

weight = st.number_input(
    "Weight (in kilograms)",
    min_value=10.0,
    max_value=300.0,
    value=70.0,
)

if st.button("Calculate BMI"):
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    st.subheader(f"Your BMI: {bmi:.2f}")

    if bmi < 18.5:
        st.warning("Category: Underweight")
    elif bmi < 25:
        st.success("Category: Normal weight")
    elif bmi < 30:
        st.info("Category: Overweight")
    else:
        st.error("Category: Obesity")

    st.markdown("### BMI Classification")
    st.table({
        "Category": [
            "Underweight",
            "Normal weight",
            "Overweight",
            "Obesity"
        ],
        "BMI Range": [
            "< 18.5",
            "18.5 - 24.9",
            "25.0 - 29.9",
            "30.0 and above"
        ]
    })
