#!/usr/bin/env python3
"""
Supply Chain Crisis Manager - Minimal Chatbot Interface with Theme Support
Save as chatbot/app.py
"""

import streamlit as st
import boto3
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Supply Chain Crisis Manager", 
    page_icon="📦",
    layout="wide"
)

st.markdown("""
<style>
/* --- Theme-Aware Variables --- */
:root {
    --bg-primary: #f0f2f5;
    --bg-secondary: #ffffff;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #ced4da;
    --shadow-light: rgba(0,0,0,0.05);
    --shadow-medium: rgba(0,0,0,0.1);
    --shadow-heavy: rgba(0,0,0,0.15);
}

[data-theme="dark"], [data-baseweb="dark"] {
    --bg-primary: #0e1117;
    --bg-secondary: #262730;
    --text-primary: #fafafa;
    --text-secondary: #a6a6a6;
    --border-color: #4a4a4a;
    --shadow-light: rgba(0,0,0,0.3);
    --shadow-medium: rgba(0,0,0,0.4);
    --shadow-heavy: rgba(0,0,0,0.5);
}

/* --- General Page Styling --- */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* --- Header --- */
.main-header {
    background: linear-gradient(135deg, #4A90E2, #357ABD);
    color: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 6px 20px var(--shadow-medium);
    transition: all 0.3s ease;
}

.main-header:hover {
    box-shadow: 0 8px 25px var(--shadow-heavy);
}

.main-header h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.25rem 0 0;
    font-size: 1rem;
    opacity: 0.9;
}

/* --- Chat container --- */
.chat-container {
    max-height: 550px;
    overflow-y: auto;
    padding: 1rem;
    background-color: var(--bg-secondary);
    border-radius: 16px;
    border: 1px solid var(--border-color);
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px var(--shadow-light);
}

/* --- User messages --- */
.user-message {
    background: linear-gradient(120deg, #4A90E2, #5BA3F5);
    color: white;
    padding: 1rem;
    border-radius: 16px;
    margin: 0.5rem 0;
    margin-left: 22%;
    border-left: 5px solid #2167c9;
    word-wrap: break-word;
    box-shadow: 0 2px 8px var(--shadow-light);
}

.user-message strong {
    color: white;
}

.user-message small {
    color: rgba(255,255,255,0.8);
}

/* --- Agent messages --- */
.agent-message {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    padding: 1rem;
    border-radius: 16px;
    margin: 0.5rem 0;
    margin-right: 22%;
    border-left: 5px solid #6c757d;
    word-wrap: break-word;
    box-shadow: 0 2px 8px var(--shadow-light);
    border: 1px solid var(--border-color);
}

[data-theme="dark"] .agent-message,
[data-baseweb="dark"] .agent-message {
    background-color: #1e1e2e;
    border-color: #3a3a4a;
}

.agent-message strong {
    color: var(--text-primary);
}

.agent-message small {
    color: var(--text-secondary);
}

/* --- System messages --- */
.system-message {
    background: linear-gradient(120deg, #fff3cd, #ffeaa7);
    color: #856404;
    padding: 1rem;
    border-radius: 16px;
    margin: 0.5rem 0;
    border-left: 5px solid #ffc107;
    text-align: center;
    font-style: italic;
    box-shadow: 0 2px 6px var(--shadow-light);
}

[data-theme="dark"] .system-message,
[data-baseweb="dark"] .system-message {
    background: linear-gradient(120deg, #3d3310, #524418);
    color: #ffd97d;
    border-color: #e0a800;
}

/* --- Quick Action Buttons --- */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(120deg, #4A90E2, #357ABD);
    color: white !important;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.2rem;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    box-shadow: 0 3px 8px var(--shadow-medium);
}

.stButton>button:hover {
    background: linear-gradient(120deg, #357ABD, #2464a0);
    transform: translateY(-2px);
    box-shadow: 0 5px 12px var(--shadow-heavy);
}

/* --- Text input --- */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 1px solid var(--border-color);
    padding: 0.6rem;
    font-size: 1rem;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
}

.stTextInput>div>div>input:focus {
    border-color: #4A90E2;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* --- Scrollbar Styling --- */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-thumb {
    background-color: #c1c1c1;
    border-radius: 4px;
}

[data-theme="dark"] .chat-container::-webkit-scrollbar-thumb,
[data-baseweb="dark"] .chat-container::-webkit-scrollbar-thumb {
    background-color: #4a4a4a;
}

.chat-container::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 4px;
}

/* --- Sidebar Styling --- */
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-radius: 12px;
    padding: 1rem !important;
    box-shadow: 0 4px 12px var(--shadow-light);
}

/* --- Sidebar headers --- */
.stSidebar h2, .stSidebar h3 {
    font-weight: 600;
    color: #4A90E2 !important;
}

[data-theme="dark"] .stSidebar h2,
[data-theme="dark"] .stSidebar h3,
[data-baseweb="dark"] .stSidebar h2,
[data-baseweb="dark"] .stSidebar h3 {
    color: #5BA3F5 !important;
}

/* --- Sidebar text --- */
.stSidebar p, .stSidebar li {
    color: var(--text-primary) !important;
}

/* --- Sidebar buttons --- */
.stSidebar button {
    color: var(--text-primary) !important;
}

.stSidebar button:hover {
    background-color: #357ABD !important;
    color: #ffffff !important;
}

/* --- Fix for Streamlit default text colors --- */
[data-theme="dark"] .stMarkdown,
[data-baseweb="dark"] .stMarkdown {
    color: var(--text-primary);
}

/* --- Subheader styling --- */
.stSubheader {
    color: var(--text-primary) !important;
}
</style>
""", unsafe_allow_html=True)


class SupplyChainAgent:
    """Supply Chain Crisis Manager AI Agent"""
    
    def __init__(self):
        self.agent_id = os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        print(self.agent_id)
        
        self.bedrock_agent_runtime = boto3.client(
            'bedrock-agent-runtime', 
            region_name=self.region
        )
    
    def invoke_agent(self, prompt: str, session_id: str):
        """Send message to the Bedrock Agent"""
        
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId=session_id,
                inputText=prompt
            )
            
            # Process streaming response
            full_response = ""
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        chunk_text = chunk['bytes'].decode('utf-8')
                        full_response += chunk_text
            
            return {
                "response": full_response,
                "success": True,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "success": False,
                "timestamp": datetime.now()
            }

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session-{int(time.time())}"

if 'agent' not in st.session_state:
    st.session_state.agent = SupplyChainAgent()

def display_header():
    """Display the main header"""
    
    st.markdown("""
    <div class="main-header">
        <h1>Supply Chain Crisis Manager</h1>
        <p>AI Agent for Electronics Supply Chain Risk Management</p>
        <small>ⓘ AI can make mistakes. Please double check info.</small>
    </div>
    """, unsafe_allow_html=True)

def display_quick_actions():
    """Display quick action buttons"""
    
    st.subheader("Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Analyze TSMC Risk"):
            handle_quick_action("Analyze the risk level for TSMC supplier in Taiwan")
    
    with col2:
        if st.button("Taiwan Earthquake Impact"):
            handle_quick_action("A 7.2 earthquake hit Taiwan affecting TSMC. Analyze impact and provide recommendations.")
    
    with col3:
        if st.button("Find Alternatives"):
            handle_quick_action("Find alternative suppliers for semiconductors if TSMC is affected")
    
    with col4:
        if st.button("Procurement Plan"):
            handle_quick_action("Generate procurement recommendations for a crisis affecting TSMC with critical urgency")

def handle_quick_action(prompt):
    """Handle quick action button clicks"""
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    # Get agent response
    with st.spinner("Agent is analyzing..."):
        response = st.session_state.agent.invoke_agent(prompt, st.session_state.session_id)
    
    # Add agent response
    st.session_state.messages.append({
        "role": "agent",
        "content": response["response"],
        "success": response["success"],
        "timestamp": response["timestamp"]
    })
    
    st.rerun()

def display_chat_interface():
    """Display the main chat interface"""
    
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown('''
            <div class="system-message">
                Welcome! I'm your Supply Chain Crisis Manager AI Agent.<br>
                I can help you analyze risks, assess crisis impacts, and provide procurement recommendations.<br>
                Ask me anything about supply chain management.
            </div>
            ''', unsafe_allow_html=True)
        
        # Display messages
        for message in st.session_state.messages:
            timestamp = message["timestamp"].strftime("%H:%M:%S")
            
            if message["role"] == "user":
                st.markdown(f'''
                <div class="user-message">
                    <strong>You</strong> <small>({timestamp})</small><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            
            elif message["role"] == "agent":
                st.markdown(f'''
                <div class="agent-message">
                    <strong>Agent</strong> <small>({timestamp})</small><br>
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_chat_input():
    """Display chat input interface"""
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask about supply chain risks, crisis analysis, or procurement recommendations:",
            placeholder="e.g., What's the risk level for Samsung in South Korea?",
            key="chat_input"
        )
    
    with col2:
        send_button = st.button("Send", type="primary")
    
    # Handle input
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get agent response
        with st.spinner("Agent is processing..."):
            response = st.session_state.agent.invoke_agent(user_input, st.session_state.session_id)
        
        # Add agent response
        st.session_state.messages.append({
            "role": "agent",
            "content": response["response"],
            "success": response["success"],
            "timestamp": response["timestamp"]
        })
        
        st.rerun()

def display_sidebar():
    """Display sidebar with controls"""
    
    st.sidebar.header("Agent Controls")
    
    st.sidebar.text(f"Session: {st.session_state.session_id[:8]}...")
    st.sidebar.text(f"Messages: {len(st.session_state.messages)}")
    
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.sidebar.button("New Session"):
        st.session_state.session_id = f"session-{int(time.time())}"
        st.session_state.messages = []
        st.rerun()
    
    st.sidebar.header("Capabilities")
    st.sidebar.markdown("""
    **I can help with:**
    - Supplier risk analysis
    - Crisis impact assessment
    - Alternative supplier recommendations
    - Procurement planning
    - Emergency response actions
    
    **Example questions:**
    - "Analyze supplier risk for NVIDIA in Taiwan"
    - "Find alternative semiconductor suppliers for TSMC"
    - "Generate procurement recommendations if Foxconn is affected by a strike."
    """)
    
    st.sidebar.header("Tech Stack")
    st.sidebar.markdown("""
    - Amazon Bedrock
    - Amazon Nova Model
    - AWS Lambda Functions
    - AWS S3 
    - Streamlit Interface
    """)

    st.sidebar.markdown("---")
    # Developer Info
    st.sidebar.info(
        """
        **👨‍💻 Developed by: Sagar Maheshwari**  
        🔗 [LinkedIn](https://www.linkedin.com/in/sagar--maheshwari)  
        💻 [GitHub](https://github.com/maheshwari2000)
        """
    )

def main():
    """Main application"""
    
    display_header()
    display_quick_actions()
    display_chat_interface()
    display_chat_input()
    display_sidebar()

if __name__ == "__main__":
    main()