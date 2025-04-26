import streamlit as st  # type: ignore
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader  # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
from langchain.embeddings import HuggingFaceEmbeddings  # type: ignore
from langchain.vectorstores import FAISS  # type: ignore
from langchain.chains import RetrievalQA  # type: ignore
from langchain.chat_models import ChatOpenAI  # type: ignore
from langchain.prompts import ChatPromptTemplate  # type: ignore

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up the LLM
def get_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.5,
        openai_api_key=openai_api_key
    )

# 🌟 Streamlit UI
st.set_page_config(page_title="MarketConfusion - FinanceBot", page_icon="💼")

# 🎀 CSS
st.markdown("""
    <style>
    .stApp { background-color: #e8f5ff; }
    h1, h2, h3, .stTitle, .stSubtitle { color: #00034f !important; font-family: 'Poppins', sans-serif !important; }
    input { background-color: #ffffff !important; color: #4e4b56 !important; border: 2px solid #f48fb1 !important; border-radius: 8px !important; }
    button { background-color: #b0ffbc !important; color: white !important; border-radius: 12px !important; }
    .stTitle { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 🎀 Header
st.title("MarketConfusion")
st.subheader("💼 Your Financial teacher on the go!")
st.write("💬 Meet **FinanceBot** 🤖, your personal financial assistant! Just ask a question and get smart answers!")
st.image("https://chatgpt.com/backend-api/public_content/enc/eyJpZCI6Im1fNjgwYmY5ZWNjZWZjODE5MTk3OTUwYjhlZGU0NDAxZTU6ZmlsZV8wMDAwMDAwMDQ3Njg2MWY2ODk3NTk1OTM3NGFlMDUwMiIsInRzIjoiNDg0ODkzIiwicCI6InB5aSIsInNpZyI6ImZlNmE2MmVhNGU3NTFkZjZjNmQ2ZjE4NzIwM2M2YjAzYWRjZjhmZTNhMzIwMzg5ZDI0NGFmNDU0NjM3ZDM5MWYiLCJ2IjoiMCIsImdpem1vX2lkIjpudWxsfQ==", width=300)
st.write("Hi, what can I do for you today? 😊")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📄 Load documents and create vectorstore
urls = [
    "https://www.bankofcanada.ca/2025/03/price-check-inflation-in-canada/",
    "https://www.investopedia.com/articles/basics/11/3-s-simple-investing.asp",
    # (your other URLs)
]

if st.button("🔍 Load and Index Content"):
    with st.spinner("Loading web pages..."):
        loader = WebBaseLoader(urls)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("finance_vectorstore")

    st.success("✅ Documents Loaded and Indexed!")

# 🧠 Load vectorstore ONCE
if os.path.exists("finance_vectorstore"):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("finance_vectorstore", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
    )
custom_prompt=ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=[
        {
            "role": "user",
            "content": """You are a super friendly and helpful financial assistant named FinanceBot.
Answer the following question based on the provided context.
Be warm, encouraging, and easy to understand.
context={context}
question={question}
Answer:"""
        }
    ],
)
return_messages=True,
# 🧠 Step 2: Ask a Question
st.subheader("Step 2: Ask a Question")

with st.form("chat_form"):
    question = st.text_input("What do you want to know? (e.g. What is a tariff?)")
    submitted = st.form_submit_button("🧠 Get Answer")

if submitted and question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Thinking... 💭"):
        answer = qa.run(question)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# 💬 Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**FinanceBot:** {msg['content']}")
