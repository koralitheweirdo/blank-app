import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Load vectorstore
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings()
    return FAISS.load_local("finance_vectorstore", embeddings, allow_dangerous_deserialization=True).as_retriever()

retriever = load_vectorstore()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
)
template="""You are a super friendly and helpful financial assistant named FinanceBot. 
Answer the following question based on the provided context.
Be warm, encouraging, and easy to understand.

Context:
{context}

Question:
{question}

Answer:"""


# App title and intro
st.title("MarketConfusion")
st.subheader("💼 Your Financial teacher on the go!")
st.write("Say hello to **FinanceBot**! Ask me anything about finance and I’ll do my best to explain it.")

# Style
st.markdown("""
    <style>
    .stApp { background-color: #e8f5ff; }
    h1, h2, h3 { color: #00034f; font-family: 'Poppins', sans-serif; }
    input, textarea { border: 2px solid #f48fb1 !important; border-radius: 8px !important; }
    button { background-color: #b0ffbc !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat UI
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask something:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("FinanceBot is thinking..."):
        response = qa.run(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**FinanceBot:** {msg['content']}")
