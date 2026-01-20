import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

# --- MAN UTD THEME ---
st.set_page_config(page_title="United AI", page_icon="🔴")
st.markdown("<style>.stApp {background-color: #000000; color: white;} h1 {color: #DA291C !important;}</style>", unsafe_allow_html=True)

# 1. DISPLAY THE CREST
st.image("https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg", width=120)
st.title("🔴 Theatre of Dreams AI")

try:
    # 2. SETUP THE BRAIN (Using the most stable 2026 model)
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", # <--- The new 2026 powerhouse
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)

    # 3. SETUP SEARCH
    search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"])
    agent_executor = create_react_agent(llm, tools=[search])

    query = st.text_input("Ask about United:")
    
    if query:
        with st.spinner("Old Trafford is thinking..."):
            # The rate limit fix: a tiny pause to avoid 429 errors
            time.sleep(1) 
            result = agent_executor.invoke({"messages": [("human", query)]})
            st.info(result["messages"][-1].content)

except Exception as e:
    if "429" in str(e):
        st.warning("⏱️ Rate limit hit! Please wait 30 seconds before your next query.")
    else:
        st.error(f"Configuration Issue: {e}")
