import streamlit as st
from langchain.agents import create_react_agent
# In 2026, AgentExecutor is often imported from langchain.agents.agent_executor
from langchain.agents.agent_executor import AgentExecutor 
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI

# --- UI CONFIGURATION ---
st.set_page_config(page_title="United Intelligence", page_icon="🔴")

# --- CUSTOM CSS FOR THE THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1 { color: #FBE122 !important; }
    .stButton>button { background-color: #DA291C; color: white; border: 1px solid #FBE122; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN GATE ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.image("https://images.unsplash.com/photo-1594911772125-07fc7a2d8d9f") # Old Trafford Image
    st.title("🔴 Theatre of Dreams AI")
    password = st.text_input("Enter Access Code", type="password")
    if st.button("Enter"):
        if password == "GGMU2026": # Change this to your preferred password
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Wrong code. Keep the faith.")
    st.stop()

# --- MAIN APP INTERFACE ---
st.title("🔴 Manchester United AI Analyst")
st.write("Real-time web-connected intelligence for the Red Devils.")

# Setup Search and AI (using Streamlit secrets for security)
search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"])
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])

agent = initialize_agent(
    tools=[search],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

query = st.text_input("What would you like to know about United today?")

if query:
    with st.spinner("Searching Old Trafford archives..."):
        response = agent.run(f"As a Manchester United expert, answer this: {query}")
        st.info(response)
