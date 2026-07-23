import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Grade Calculator", page_icon="🎓")

st.title("🎓 Student Grade Calculator")
st.write("Enter the student's details and marks to calculate the result.")

# Student Name
name = st.text_input("Student Name")

# Subject Marks
maths = st.number_input("Mathematics", min_value=0, max_value=100, value=0)
science = st.number_input("Science", min_value=0, max_value=100, value=0)
english = st.number_input("English", min_value=0, max_value=100, value=0)
computer = st.number_input("Computer Science", min_value=0, max_value=100, value=0)
social = st.number_input("Social Science", min_value=0, max_value=100, value=0)

# Calculate Button
if st.button("Calculate Result"):

    # Total and Average
    total = maths + science + english + computer + social
    average = total / 5

    # Grade Calculation
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "E"

    # Pass or Fail
    if (
        maths >= 35
        and science >= 35
        and english >= 35
        and computer >= 35
        and social >= 35
    ):
        result = "PASS ✅"
        st.success(result)
    else:
        result = "FAIL ❌"
        st.error(result)

    # Display Results
    st.subheader("📋 Student Report Card")

    st.write(f"**Student Name:** {name}")
    st.write(f"**Total Marks:** {total} / 500")
    st.write(f"**Average:** {average:.2f}%")
    st.write(f"**Grade:** {grade}")

    # Marks Table
    st.table(
        {
            "Subject": [
                "Mathematics",
                "Science",
                "English",
                "Computer Science",
                "Social Science",
            ],
            "Marks": [
                maths,
                science,
                english,
                computer,
                social,
            ],
        }
    )

    # Progress Bar
    st.subheader("Percentage")
    st.progress(int(average))

    # Balloon Animation for High Score
    if average >= 90:
        st.balloons()
        st.success("🎉 Outstanding Performance!")
    elif average >= 80:
        st.info("👏 Great Job!")
    elif average >= 70:
        st.info("👍 Good Work!")
    elif average >= 60:
        st.warning("🙂 Keep Improving!")
    else:
        st.error("📚 Work Hard and Try Again!")
