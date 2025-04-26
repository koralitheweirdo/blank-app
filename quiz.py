import streamlit as st


# Function to start the quiz
def start_quiz():
    # Initialize session state for storing quiz answers and score
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.answers = {}

    st.title("Finance Quiz")
    st.write("Test your knowledge with this simple finance quiz! 🤓")

    # Question 1
    st.subheader("1. What is the main purpose of a budget?")
    question_1 = st.radio(
        "Choose the correct answer:",
        ["To track your spending", "To avoid paying taxes", "To spend as much as possible", "To invest only in stocks"],
        key="question_1",  # Use a key to ensure state persistence
    )
    st.session_state.answers["question_1"] = question_1

    # Question 2
    st.subheader("2. What is compound interest?")
    question_2 = st.radio(
        "Choose the correct answer:",
        ["Interest on both the initial principal and accumulated interest", 
         "Interest on the initial principal only", 
         "A form of investment", 
         "Interest paid in a fixed amount each year"],
        key="question_2",  # Use a key to ensure state persistence
    )
    st.session_state.answers["question_2"] = question_2

    # Question 3
    st.subheader("3. Which of the following is considered a good practice for financial planning?")
    question_3 = st.radio(
        "Choose the correct answer:",
        ["Living beyond your means", "Having an emergency fund", "Ignoring your credit score", "Avoiding savings"],
        key="question_3",  # Use a key to ensure state persistence
    )
    st.session_state.answers["question_3"] = question_3

    # Button to submit answers
    if st.button("Submit Answers"):
        score = 0
        # Check answers
        if st.session_state.answers["question_1"] == "To track your spending":
            score += 1
        if st.session_state.answers["question_2"] == "Interest on both the initial principal and accumulated interest":
            score += 1
        if st.session_state.answers["question_3"] == "Having an emergency fund":
            score += 1
        
        # Display the score
        st.session_state.score = score  # Save score in session state
        st.write(f"Your score: {score}/3")
        if score == 3:
            st.success("Congratulations! You got all answers correct. 🎉")
        elif score == 2:
            st.warning("Good job! You got 2 out of 3 right. Keep learning! 💪")
        else:
            st.error("Oops! You need to review the material. Better luck next time! 💡")
#     st.session_state.score = score