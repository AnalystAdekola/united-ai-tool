import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent # The new 2026 standard

# --- MAN UTD THEME ---
st.set_page_config(page_title="United AI", page_icon="🔴")
st.markdown("<style>.stApp {background-color: #000000; color: white;} h1 {color: #DA291C !important;}</style>", unsafe_allow_html=True)

st.title("🔴 Manchester United AI Analyst")

try:
    # 1. Setup the "Brain"
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", # <--- The new 2026 powerhouse
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)

    # 2. Setup the "Eyes"
    search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"])

    # 3. Create the Agent (New 2026 Pattern)
    # This replaces 'initialize_agent' and 'AgentType'
    agent_executor = create_react_agent(llm, tools=[search])

    query = st.text_input("What's the latest at Old Trafford?")
    if query:
        with st.spinner("Analyzing..."):
            # New 2026 response pattern
            result = agent_executor.invoke({"messages": [("human", query)]})
            st.info(result["messages"][-1].content)

except Exception as e:
    st.error(f"Waiting for Configuration: {e}")
