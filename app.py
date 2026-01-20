import streamlit as st
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType

# --- MAN UTD THEME ---
st.set_page_config(page_title="United AI", page_icon="🔴")
st.markdown("<style>.stApp {background-color: #000000; color: white;} h1 {color: #DA291C !important;}</style>", unsafe_allow_html=True)

st.title("🔴 Manchester United AI Analyst")

# --- CORE LOGIC ---
try:
    # 1. Setup LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

    # 2. Setup Search
    search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"])

    # 3. Setup Agent (The stable 'Legacy' pattern)
    agent = initialize_agent(
        tools=[search],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    query = st.text_input("Ask about United:")
    if query:
        with st.spinner("Searching..."):
            response = agent.run(f"As a Man Utd expert, answer: {query}")
            st.success(response)

except Exception as e:
    st.error(f"Configuration Needed: {e}")
