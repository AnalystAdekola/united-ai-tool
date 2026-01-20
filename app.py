import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Theatre of Dreams AI", page_icon="🔴", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1, h2, h3 { color: #DA291C !important; font-family: 'Arial Black'; }
    .stButton>button { background-color: #DA291C; color: white; border-radius: 5px; width: 100%; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border: 1px solid #DA291C; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (MATCH INFO) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg", width=100)
    st.title("MUFC Dashboard")
    st.write("**Next Match:** Arsenal (A)")
    st.write("**Date:** Jan 25, 2026")
    st.markdown("---")
    st.write("**Top Scorer:** Bryan Mbeumo (8)")
    st.write("**Recent Form:** W-D-D-D-W")

# --- 3. MAIN INTERFACE ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg", width=120)
with col2:
    st.title("Manchester United AI Analyst")
    st.subheader("Tactical Insights & Old Trafford News")

# --- 4. AI AGENT SETUP ---
try:
    # 2026 Stable Model
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", # <--- The new 2026 powerhouse
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)
    
    # Live Search Tool
    search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"], max_results=3)
    
    # Modern Agent Execution
    agent_executor = create_react_agent(llm, tools=[search])

    query = st.text_input("Ask about transfers, tactics, or match results:", placeholder="e.g. How did the derby against City go?")

    if query:
        with st.chat_message("assistant"):
            with st.spinner("Scouting the latest data..."):
                # Safety pause for free tier limits
                time.sleep(1)
                result = agent_executor.invoke({"messages": [("human", query)]})
                st.write(result["messages"][-1].content)

except Exception as e:
    if "429" in str(e):
        st.warning("⏱️ The Analyst is busy. Please wait 60 seconds (API Rate Limit).")
    elif "404" in str(e):
        st.error("🔄 Model version error. Trying to reconnect...")
    else:
        st.error(f"Setup Error: {e}")
