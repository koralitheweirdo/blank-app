import streamlit as st

def quiz():
    score = 0
    for q in questions:
        st.write(q['question'])
        answer = st.radio("Choose an option:", q['options'])
        if answer == q['answer']:
            st.success("Correct!")
            score += 1
        else:
            st.error(f"Wrong! The correct answer is: {q['answer']}")
    st.write(f"Your final score: {score}/{len(questions)}")

if st.button('Start Quiz'):
    quiz()


            
            
            }








</style>
"""








)