#!/usr/bin/env python3
"""
Supply Chain Crisis Manager - Professional Streamlit Dashboard
Save as dashboard/app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import boto3
import json
import time
from datetime import datetime, timedelta
import requests
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Supply Chain Crisis Manager", 
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .crisis-alert {
        background: #ffebee;
        border: 1px solid #f44336;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-alert {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class SupplyChainAgent:
    """Interface to Bedrock Agent"""
    
    def __init__(self):
        # REPLACE WITH YOUR ACTUAL AGENT ID
        self.agent_id = os.getenv('BEDROCK_AGENT_ID', 'YOUR_AGENT_ID_HERE')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'TSTALIASID')
        
        try:
            self.bedrock_agent_runtime = boto3.client(
                'bedrock-agent-runtime', 
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            self.connected = True
        except Exception as e:
            st.error(f"Failed to connect to Bedrock Agent: {e}")
            self.connected = False
    
    def invoke_agent(self, prompt: str) -> Dict:
        """Invoke the Bedrock Agent with a prompt"""
        
        if not self.connected:
            return {"error": "Agent not connected"}
        
        if self.agent_id == 'YOUR_AGENT_ID_HERE':
            # Fallback to mock data for demo
            return self._mock_agent_response(prompt)
        
        try:
            session_id = f"dashboard-{int(time.time())}"
            
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
            
            return {"response": full_response, "success": True}
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _mock_agent_response(self, prompt: str) -> Dict:
        """Mock response for demo when agent ID not configured"""
        
        mock_responses = {
            "TSMC": {
                "response": "Based on my analysis of TSMC in Taiwan:\n\n**Risk Assessment: HIGH (85/100)**\n\n**Risk Factors:**\n- Geographic concentration in Taiwan (earthquake risk)\n- Single point of failure for global semiconductor supply\n- Geopolitical tensions affecting operations\n\n**Recommendations:**\n1. Immediate alternative sourcing from Samsung (South Korea)\n2. Increase inventory buffer by 40%\n3. Activate emergency procurement protocols\n4. Consider long-term supplier diversification",
                "success": True
            },
            "earthquake": {
                "response": "**CRISIS IMPACT ANALYSIS: Taiwan Earthquake**\n\n**Severity Assessment: CRITICAL**\n\n**Impact Projections:**\n- Production Delay: 22 days\n- Cost Increase: 25%\n- Revenue at Risk: 40%\n- Recovery Time: 5-6 weeks\n\n**Affected Components:**\n- Semiconductors (85% impact)\n- Memory chips (60% impact)\n- Assembly operations (45% impact)\n\n**Immediate Actions Required:**\n1. Switch to Samsung for critical semiconductors\n2. Activate air freight for urgent components\n3. Implement emergency inventory protocols\n4. Notify customers of potential delays",
                "success": True
            }
        }
        
        # Simple keyword matching for demo
        for keyword, response in mock_responses.items():
            if keyword.lower() in prompt.lower():
                return response
        
        return {
            "response": "I'm analyzing the supply chain situation. This is a demo response showing the agent's capabilities for risk assessment and procurement recommendations.",
            "success": True
        }

# Initialize components
@st.cache_resource
def init_agent():
    """Initialize the agent (cached for performance)"""
    return SupplyChainAgent()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_sample_supplier_data():
    """Generate sample supplier data"""
    return pd.DataFrame([
        {"name": "TSMC", "location": "Taiwan", "component": "Semiconductors", "risk_score": 85, "status": "High Risk", "backup_available": False},
        {"name": "Samsung", "location": "South Korea", "component": "Memory Chips", "risk_score": 45, "status": "Medium Risk", "backup_available": True},
        {"name": "Foxconn", "location": "China", "component": "Assembly", "risk_score": 60, "status": "Medium Risk", "backup_available": True},
        {"name": "Intel", "location": "USA", "component": "Processors", "risk_score": 25, "status": "Low Risk", "backup_available": True},
        {"name": "Sony", "location": "Japan", "component": "Camera Sensors", "risk_score": 35, "status": "Low Risk", "backup_available": False},
        {"name": "Micron", "location": "USA", "component": "Storage", "risk_score": 30, "status": "Low Risk", "backup_available": True},
    ])

def display_main_header():
    """Display the main dashboard header"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🚨 Supply Chain Crisis Manager</h1>
        <h3>Autonomous AI Agent for Electronics Supply Chain Risk Management</h3>
        <p>Powered by Amazon Bedrock AgentCore & Nova Model</p>
    </div>
    """, unsafe_allow_html=True)

def display_real_time_monitoring():
    """Display real-time monitoring section"""
    
    st.header("🔍 Real-Time Crisis Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Suppliers", "6", delta="0")
    
    with col2:
        high_risk = len(get_sample_supplier_data()[get_sample_supplier_data()['risk_score'] > 70])
        st.metric("High Risk Suppliers", high_risk, delta="+1", delta_color="inverse")
    
    with col3:
        st.metric("Active Crises", "1", delta="0", delta_color="inverse")
    
    with col4:
        st.metric("Mitigation Actions", "12", delta="+4")

def display_crisis_simulation():
    """Display crisis simulation and agent interaction"""
    
    st.header("🤖 AI Agent Interaction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Crisis Scenarios")
        
        scenario = st.selectbox(
            "Select Crisis Scenario:",
            [
                "Taiwan Earthquake (7.2 magnitude affecting TSMC)",
                "Shanghai Port Congestion (14-day delays)",
                "South Korea Manufacturing Strike",
                "Custom Analysis"
            ]
        )
        
        if scenario == "Custom Analysis":
            custom_prompt = st.text_area(
                "Enter your supply chain question:",
                placeholder="e.g., Analyze risk for Samsung supplier in South Korea"
            )
            analysis_prompt = custom_prompt
        else:
            # Pre-defined prompts for scenarios
            scenario_prompts = {
                "Taiwan Earthquake (7.2 magnitude affecting TSMC)": 
                    "A 7.2 magnitude earthquake has hit Taiwan affecting TSMC semiconductor facilities. Calculate the crisis impact and provide procurement recommendations with critical urgency.",
                "Shanghai Port Congestion (14-day delays)": 
                    "Shanghai port is experiencing 14-day shipping delays affecting Foxconn assembly operations. Analyze the impact and find alternative suppliers for assembly services.",
                "South Korea Manufacturing Strike": 
                    "Manufacturing strikes in South Korea are affecting Samsung memory chip production. Assess the risk and generate procurement recommendations."
            }
            analysis_prompt = scenario_prompts.get(scenario, "Analyze current supply chain risks")
        
        if st.button("🚀 Run AI Analysis", type="primary"):
            if analysis_prompt:
                with st.spinner("🤖 AI Agent is analyzing the situation..."):
                    agent = init_agent()
                    result = agent.invoke_agent(analysis_prompt)
                    
                    if result.get("success", False):
                        st.markdown("""
                        <div class="success-alert">
                            <h4>✅ AI Agent Analysis Complete</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("**Agent Response:**")
                        st.markdown(result["response"])
                        
                        # Store in session state for persistence
                        st.session_state['last_analysis'] = {
                            'prompt': analysis_prompt,
                            'response': result["response"],
                            'timestamp': datetime.now()
                        }
                    else:
                        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
    
    with col2:
        st.subheader("Agent Status")
        agent = init_agent()
        
        if agent.connected:
            if agent.agent_id != 'YOUR_AGENT_ID_HERE':
                st.success("✅ Connected to Bedrock Agent")
                st.info(f"Agent ID: {agent.agent_id[:10]}...")
            else:
                st.warning("⚠️ Demo Mode (Update BEDROCK_AGENT_ID)")
        else:
            st.error("❌ Agent Connection Failed")
        
        # Display recent analysis if available
        if 'last_analysis' in st.session_state:
            st.subheader("Latest Analysis")
            analysis = st.session_state['last_analysis']
            st.caption(f"Analyzed: {analysis['timestamp'].strftime('%H:%M:%S')}")
            
            # Show first 200 characters
            preview = analysis['response'][:200] + "..." if len(analysis['response']) > 200 else analysis['response']
            st.text_area("Response Preview:", preview, height=100, disabled=True)

def display_supplier_dashboard():
    """Display supplier risk dashboard"""
    
    st.header("📊 Supplier Risk Dashboard")
    
    suppliers = get_sample_supplier_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Risk score visualization
        fig = px.bar(
            suppliers,
            x='name',
            y='risk_score',
            color='risk_score',
            color_continuous_scale=['green', 'yellow', 'red'],
            title="Supplier Risk Scores",
            labels={'risk_score': 'Risk Score (0-100)', 'name': 'Supplier'},
            text='risk_score'
        )
        fig.update_layout(height=400, showlegend=False)
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Geographic distribution
        location_counts = suppliers['location'].value_counts()
        fig_pie = px.pie(
            values=location_counts.values,
            names=location_counts.index,
            title="Geographic Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed supplier table
    st.subheader("Detailed Supplier Information")
    
    # Add filtering
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location_filter = st.multiselect(
            "Filter by Location:",
            suppliers['location'].unique(),
            default=suppliers['location'].unique()
        )
    
    with col2:
        risk_filter = st.selectbox(
            "Risk Level:",
            ["All", "High Risk (>70)", "Medium Risk (40-70)", "Low Risk (<40)"]
        )
    
    with col3:
        backup_filter = st.selectbox(
            "Backup Available:",
            ["All", "Yes", "No"]
        )
    
    # Apply filters
    filtered_suppliers = suppliers[suppliers['location'].isin(location_filter)]
    
    if risk_filter != "All":
        if risk_filter == "High Risk (>70)":
            filtered_suppliers = filtered_suppliers[filtered_suppliers['risk_score'] > 70]
        elif risk_filter == "Medium Risk (40-70)":
            filtered_suppliers = filtered_suppliers[(filtered_suppliers['risk_score'] >= 40) & (filtered_suppliers['risk_score'] <= 70)]
        else:  # Low Risk
            filtered_suppliers = filtered_suppliers[filtered_suppliers['risk_score'] < 40]
    
    if backup_filter != "All":
        backup_bool = backup_filter == "Yes"
        filtered_suppliers = filtered_suppliers[filtered_suppliers['backup_available'] == backup_bool]
    
    # Style the dataframe
    def color_risk_score(val):
        if val > 70:
            return 'background-color: #ffcdd2'
        elif val > 40:
            return 'background-color: #fff3e0'
        else:
            return 'background-color: #e8f5e8'
    
    styled_df = filtered_suppliers.style.applymap(color_risk_score, subset=['risk_score'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

def display_sidebar():
    """Display sidebar with controls and settings"""
    
    st.sidebar.header("⚙️ Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)")
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Agent configuration
    st.sidebar.header("🤖 Agent Configuration")
    
    # Show current agent status
    agent = init_agent()
    
    if agent.agent_id == 'YOUR_AGENT_ID_HERE':
        st.sidebar.warning("⚠️ Demo Mode")
        st.sidebar.info("Set BEDROCK_AGENT_ID environment variable to use your real agent")
    else:
        st.sidebar.success("✅ Agent Connected")
    
    # Quick actions
    st.sidebar.header("⚡ Quick Actions")
    
    if st.sidebar.button("📊 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    if st.sidebar.button("🧪 Test Agent"):
        with st.spinner("Testing agent connection..."):
            result = agent.invoke_agent("Test connection - analyze TSMC risk level")
            if result.get("success", False):
                st.sidebar.success("✅ Agent responding")
            else:
                st.sidebar.error("❌ Agent test failed")

def main():
    """Main dashboard application"""
    
    # Display components
    display_main_header()
    display_real_time_monitoring()
    
    # Two-column layout for main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        display_crisis_simulation()
    
    with col2:
        display_supplier_dashboard()
    
    # Sidebar
    display_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🏆 Supply Chain Crisis Manager - Built for AWS AI Agent Global Hackathon 2025</p>
        <p>Powered by Amazon Bedrock AgentCore • Amazon Nova • AWS Lambda</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()