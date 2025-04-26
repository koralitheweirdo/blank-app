import streamlit as st
questions=[
    {
        "question": "What is the primary purpose of the Bank of Canada?",
        "options": ["To regulate the stock market", "To manage inflation and monetary policy", "To provide loans to individuals"],
        "answer": "To manage inflation and monetary policy"
    },
    {
        "question": "What is a simple investment strategy mentioned in the Investopedia article?",
        "options": ["Day trading", "Buy and hold", "Options trading"],
        "answer": "Buy and hold"
    },
    {
        "question": "What is the main focus of the article from Bank of Canada?",
        "options": ["Stock market trends", "Inflation in Canada", "Cryptocurrency regulations"],
        "answer": "Inflation in Canada"
    }
]
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


            
            








