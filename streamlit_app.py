import streamlit as st  # type: ignore
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader  # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
from langchain.embeddings.openai import OpenAIEmbeddings  # type: ignore
from langchain.vectorstores import FAISS  # type: ignore
from langchain.chains import RetrievalQA  # type: ignore
from langchain.chat_models import ChatOpenAI  # type: ignore

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup LLM
def get_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.5,
        openai_api_key=openai_api_key
    )

# 🎨 Streamlit UI
st.set_page_config(page_title="MarketConfusion", layout="centered")

st.title("MarketConfusion")
st.subheader("💼 Your Financial Teacher On The Go!")
st.subheader("Say Hello to Your Personal Finance Assistant!")
st.write("💬 Meet **FinanceBot** 🤖 — Ready to help you navigate the world of finance. Just ask a question and get smart answers!")

st.image(
    "https://chatgpt.com/backend-api/public_content/enc/eyJpZCI6Im1fNjgwYmY5ZWNjZWZjODE5MTk3OTUwYjhlZGU0NDAxZTU6ZmlsZV8wMDAwMDAwMDQ3Njg2MWY2ODk3NTk1OTM3NGFlMDUwMiIsInRzIjoiNDg0ODkzIiwicCI6InB5aSIsInNpZyI6ImZlNmE2MmVhNGU3NTFkZjZjNmQ2ZjE4NzIwM2M2YjAzYWRjZjhmZTNhMzIwMzg5ZDI0NGFmNDU0NjM3ZDM5MWYiLCJ2IjoiMCIsImdpem1vX2lkIjpudWxsfQ==",
    width=300
)
st.write("Hi, what can I do for you today? 😊")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #e8f5ff;
    }
    h1, h2, h3, .stTitle, .stSubtitle {
        color: #00034f !important;
        font-family: 'Poppins', sans-serif !important;
    }
    input {
        background-color: #ffffff !important;
        color: #4e4b56 !important;
        border: 2px solid #f48fb1 !important;
        border-radius: 8px !important;
    }
    button {
        background-color: #b0ffbc !important;
        color: white !important;
        border-radius: 12px !important;
    }
    .stTitle {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Step 1: Load and index content
st.subheader("Step 1: Load Content")

urls = [
    "https://www.bankofcanada.ca/2025/03/price-check-inflation-in-canada/",
    "https://www.investopedia.com/articles/basics/11/3-s-simple-investing.asp",
    "https://www.investopedia.com/articles/basics/06/invest1000.asp",
    "https://www.investopedia.com/ask/answers/08/trading-frequency-commissions.asp",
    "https://www.investopedia.com/articles/bonds/08/bond-market-basics.asp",
    "https://www.investopedia.com/articles/fundamental/03/022603.asp",
    "https://www.investopedia.com/articles/personal-finance/100516/setting-financial-goals/",
    "https://www.investopedia.com/top-10-personal-finance-podcasts-5088034",
    "https://www.investopedia.com/personal-finance/most-common-financial-mistakes/",
    "https://www.investopedia.com/personal-finance-calendar-5092591",
    "https://www.investopedia.com/articles/pf/09/financial-responsibility.asp",
    "https://www.investopedia.com/terms/t/tariff.asp",
    "https://www.investopedia.com/terms/c/capitalism.asp",
    "https://www.canada.ca/en/department-finance/programs/international-trade-finance-policy/canadas-response-us-tariffs.html",
    "https://www.canada.ca/en/public-health/services/suicide-prevention.html",
    "https://www.canada.ca/en/public-health/services/mental-health-services/mental-health-get-help.html",
    "https://www.canada.ca/en/financial-consumer-agency/services/covid-19-managing-financial-health.html",
    "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/opening-your-fhsas.html",
    "https://www.edc.ca/en/article/how-tariffs-work-for-business.html",
    "https://www.edc.ca/en/campaign/trade-support-canadian-companies.html"
]

if st.button("🔍 Load and Index Content"):
    with st.spinner("Loading and indexing content..."):
        loader = WebBaseLoader(urls)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("finance_vectorstore")

    st.success("✅ Documents successfully indexed!")

# Step 2: Ask a question
st.subheader("Step 2: Ask a Question")

question = st.text_input("Ask me something based on the documents 💬")

if st.button("🧠 Get Answer") and question:
    with st.spinner("Loading knowledge base..."):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.load_local("finance_vectorstore", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

        qa = RetrievalQA.from_chain_type(
            llm=get_llm(),
            retriever=retriever,
        )

    with st.spinner("Thinking... 💭"):
        answer = qa.run(question)
        st.markdown(f"**Answer:** {answer}")

import streamlit as st
import importlib

# Set default state if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'quiz'

# Buttons to navigate between pages
st.subheader("Step 3: Take a Quiz")
st.write("Test your knowledge with a quiz! 📝")


if st.button(Quiz):
    with st.spinner("Loading quiz..."):
    st.session_state.page = 'quiz'
if st.session_state.page == 'quiz':
    # Dynamically import quiz module and run it
    quiz = importlib.import_module('quiz')
    quiz.start_quiz()