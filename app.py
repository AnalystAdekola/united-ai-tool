import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearchResults
from langgraph.prebuilt import create_react_agent

# --- UI & THEME ---
st.set_page_config(page_title="United AI", page_icon="🔴")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1 { color: #FBE122 !important; }
    .stButton>button { background-color: #DA291C; color: white; border: 1px solid #FBE122; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 Manchester United AI Analyst")

# --- SECRETS & AI SETUP ---
try:
    # 2026 standard for high-speed agents
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )
    
    # Dedicated Tavily tool for 2026
    search_tool = TavilySearchResults(
        api_key=st.secrets["TAVILY_API_KEY"],
        max_results=3
    )

    # In 2026, LangGraph is the "Standard" for all agents
    agent_executor = create_react_agent(llm, tools=[search_tool])

    # --- CHAT INTERFACE ---
    query = st.text_input("Ask about United (Transfers, Scores, News):")

    if query:
        with st.spinner("Searching Old Trafford records..."):
            # New 2026 'invoke' pattern
            result = agent_executor.invoke({"messages": [("human", query)]})
            # The answer is in the last message of the result
            st.info(result["messages"][-1].content)

except Exception as e:
    st.error(f"Waiting for Configuration: {e}")
    st.info("Check your 'Advanced Settings > Secrets' in Streamlit.")
