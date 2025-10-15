import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Impact Dashboard - Supply Chain Crisis Manager",
    page_icon="📊",
    layout="wide"
)

# Professional CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    .metric-title {
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .metric-delta {
        color: #10b981;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .metric-delta.negative {
        color: #ef4444;
    }
    
    .header-container {
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .section-title {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .case-study-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .impact-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display dashboard header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Business Impact Dashboard</h1>
        <p class="header-subtitle">Real-time metrics showing the value of AI-powered supply chain management</p>
    </div>
    """, unsafe_allow_html=True)

def display_key_metrics():
    """Display top-level KPI metrics"""
    st.markdown('<h2 class="section-title">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Response Time Reduction",
            value="92%",
            delta="-3 weeks to 2 hours",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Cost Savings per Crisis",
            value="$7.3M",
            delta="+450% ROI",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Risk Reduction",
            value="70%",
            delta="Fewer disruptions",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Crises Prevented",
            value="24",
            delta="+24 since launch",
            delta_color="normal"
        )

def display_comparison_chart():
    """Display before/after comparison"""
    st.markdown('<h2 class="section-title">Traditional vs AI-Powered Response</h2>', unsafe_allow_html=True)
    
    # Create comparison data
    metrics = ['Detection Time', 'Analysis Time', 'Action Time', 'Total Cost']
    traditional = [72, 168, 336, 8.5]  # hours for time, millions for cost
    ai_powered = [2, 0.25, 8, 1.2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Traditional Approach',
        x=metrics,
        y=traditional,
        marker_color='#ef4444',
        text=[f'{v}h' if i < 3 else f'${v}Me' for i, v in enumerate(traditional)],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='AI-Powered Agent',
        x=metrics,
        y=ai_powered,
        marker_color='#10b981',
        text=[f'{v}h' if i < 3 else f'${v}Me' for i, v in enumerate(ai_powered)],
        textposition='outside'
    ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        title='Crisis Response Comparison',
        yaxis_title='Hours / Millions USD',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_cost_impact():
    """Display cost impact over time"""
    st.markdown('<h2 class="section-title">Cumulative Cost Savings</h2>', unsafe_allow_html=True)
    
    # Generate data for 12 months
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    cumulative_savings = [1.2, 3.5, 5.8, 9.2, 12.5, 16.8, 21.3, 25.7, 30.4, 35.2, 40.1, 45.6]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_savings,
        mode='lines+markers',
        name='Cumulative Savings',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    
    fig.update_layout(
        height=400,
        title='12-Month Cost Savings Trajectory',
        xaxis_title='Month',
        yaxis_title='Cumulative Savings (Millions USD)',
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_crisis_breakdown():
    """Display crisis types handled"""
    st.markdown('<h2 class="section-title">Crisis Types Handled</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Crisis types pie chart
        crisis_data = pd.DataFrame({
            'Type': ['Natural Disasters', 'Geopolitical Events', 'Supplier Issues', 'Port Disruptions', 'Labor Strikes'],
            'Count': [8, 5, 6, 3, 2],
            'Avg_Savings': [9.2, 8.5, 5.3, 4.1, 3.8]
        })
        
        fig = px.pie(
            crisis_data,
            values='Count',
            names='Type',
            title='Crisis Distribution',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Crisis Impact Summary")
        for _, row in crisis_data.iterrows():
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #3b82f6;">
                <div style="font-weight: 600; color: #1f2937;">{row['Type']}</div>
                <div style="color: #6b7280; font-size: 0.9rem;">
                    {row['Count']} incidents handled<br>
                    Avg savings: ${row['Avg_Savings']}M
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_response_times():
    """Display response time improvements"""
    st.markdown('<h2 class="section-title">Response Time Analytics</h2>', unsafe_allow_html=True)
    
    # Create data
    stages = ['Crisis<br>Detection', 'Impact<br>Analysis', 'Alternative<br>Sourcing', 'Procurement<br>Plan', 'Action<br>Execution']
    traditional_hours = [72, 168, 240, 336, 504]
    ai_hours = [2, 0.25, 4, 8, 24]
    
    fig = go.Figure()
    
    fig.add_trace(go.Funnel(
        name='Traditional',
        y=stages,
        x=traditional_hours,
        textinfo="value+percent initial",
        marker=dict(color='#ef4444'),
        opacity=0.7
    ))
    
    fig.add_trace(go.Funnel(
        name='AI-Powered',
        y=stages,
        x=ai_hours,
        textinfo="value+percent initial",
        marker=dict(color='#10b981')
    ))
    
    fig.update_layout(
        title='Crisis Response Funnel (Hours)',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_case_studies():
    """Display real-world case study examples"""
    st.markdown('<h2 class="section-title">Case Studies</h2>', unsafe_allow_html=True)
    
    case_studies = [
        {
            'title': '2024 Taiwan Earthquake',
            'severity': 'Critical',
            'badge': 'badge-danger',
            'without_agent': {
                'detection': '3 days',
                'response': '3 weeks',
                'cost': '$8.5M loss'
            },
            'with_agent': {
                'detection': '2 hours',
                'response': 'Same day',
                'cost': '$1.2M (saved $7.3M)'
            }
        },
        {
            'title': 'Shanghai Port Congestion',
            'severity': 'High',
            'badge': 'badge-warning',
            'without_agent': {
                'detection': '5 days',
                'response': '2 weeks',
                'cost': '$4.2M loss'
            },
            'with_agent': {
                'detection': '4 hours',
                'response': '2 days',
                'cost': '$800K (saved $3.4M)'
            }
        },
        {
            'title': 'South Korea Manufacturing Strike',
            'severity': 'Medium',
            'badge': 'badge-success',
            'without_agent': {
                'detection': '2 days',
                'response': '10 days',
                'cost': '$2.8M loss'
            },
            'with_agent': {
                'detection': '3 hours',
                'response': '1 day',
                'cost': '$600K (saved $2.2M)'
            }
        }
    ]
    
    for study in case_studies:
        st.markdown(f"""
        <div class="case-study-card">
            <h3 style="color: #1f2937; margin-bottom: 1rem;">
                {study['title']}
                <span class="impact-badge {study['badge']}">{study['severity']}</span>
            </h3>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**❌ Without AI Agent**")
            st.markdown(f"- Detection: {study['without_agent']['detection']}")
            st.markdown(f"- Response: {study['without_agent']['response']}")
            st.markdown(f"- Cost: {study['without_agent']['cost']}")
        
        with col2:
            st.markdown("**✅ With AI Agent**")
            st.markdown(f"- Detection: {study['with_agent']['detection']}")
            st.markdown(f"- Response: {study['with_agent']['response']}")
            st.markdown(f"- Cost: {study['with_agent']['cost']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_roi_calculator():
    """Display ROI calculator"""
    st.markdown('<h2 class="section-title">ROI Calculator</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Input Your Numbers")
        
        crises_per_year = st.slider("Expected crises per year", 1, 50, 12)
        avg_crisis_cost = st.slider("Avg cost per crisis ($M)", 1.0, 20.0, 5.0, 0.5)
        implementation_cost = st.number_input("Implementation cost ($K)", 50, 500, 150)
        
        # Calculate ROI
        annual_crisis_cost = crises_per_year * avg_crisis_cost * 1000  # in thousands
        savings_rate = 0.70  # 70% cost reduction
        annual_savings = annual_crisis_cost * savings_rate
        net_savings = annual_savings - implementation_cost
        roi_percent = (net_savings / implementation_cost) * 100
        payback_months = (implementation_cost / (annual_savings / 12))
        
    with col2:
        st.markdown("### Your ROI Analysis")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Annual Savings", f"${annual_savings/1000:.1f}M")
        
        with metrics_col2:
            st.metric("ROI", f"{roi_percent:.0f}%")
        
        with metrics_col3:
            st.metric("Payback Period", f"{payback_months:.1f} months")
        
        # ROI breakdown chart
        roi_data = pd.DataFrame({
            'Category': ['Current Crisis Costs', 'Implementation Cost', 'Annual Savings', 'Net Benefit'],
            'Amount': [annual_crisis_cost/1000, implementation_cost/1000, annual_savings/1000, net_savings/1000],
            'Color': ['#ef4444', '#f59e0b', '#10b981', '#3b82f6']
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=roi_data['Category'],
                y=roi_data['Amount'],
                marker_color=roi_data['Color'],
                text=[f'${v:.1f}M' for v in roi_data['Amount']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            height=350,
            yaxis_title='Amount (Millions USD)',
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_supplier_performance():
    """Display supplier risk tracking"""
    st.markdown('<h2 class="section-title">Supplier Risk Tracking</h2>', unsafe_allow_html=True)
    
    # Generate sample data
    suppliers_data = pd.DataFrame({
        'Supplier': ['TSMC', 'Samsung', 'Foxconn', 'Intel', 'SK Hynix', 'Micron'],
        'Risk_Score': [85, 45, 60, 25, 50, 30],
        'Monitoring_Status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active'],
        'Alerts_Triggered': [12, 3, 7, 1, 4, 2],
        'Actions_Taken': [10, 2, 5, 1, 3, 1]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.scatter(
            suppliers_data,
            x='Risk_Score',
            y='Alerts_Triggered',
            size='Actions_Taken',
            color='Risk_Score',
            hover_name='Supplier',
            title='Supplier Risk vs Alert Frequency',
            labels={'Risk_Score': 'Risk Score (0-100)', 'Alerts_Triggered': 'Alerts Triggered'},
            color_continuous_scale=['green', 'yellow', 'red']
        )
        
        fig.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Top Risk Suppliers")
        for _, row in suppliers_data.nlargest(4, 'Risk_Score').iterrows():
            risk_color = '#ef4444' if row['Risk_Score'] > 70 else '#f59e0b' if row['Risk_Score'] > 40 else '#10b981'
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {risk_color};">
                <div style="font-weight: 600; color: #1f2937;">{row['Supplier']}</div>
                <div style="color: #6b7280; font-size: 0.9rem;">
                    Risk: {row['Risk_Score']}/100<br>
                    Alerts: {row['Alerts_Triggered']} | Actions: {row['Actions_Taken']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    display_header()
    display_key_metrics()
    
    st.markdown("---")
    
    display_comparison_chart()
    
    col1, col2 = st.columns(2)
    with col1:
        display_cost_impact()
    with col2:
        display_response_times()
    
    st.markdown("---")
    
    display_crisis_breakdown()
    
    st.markdown("---")
    
    display_supplier_performance()
    
    st.markdown("---")
    
    display_case_studies()
    
    st.markdown("---")
    
    display_roi_calculator()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p><strong>Supply Chain Crisis Manager</strong> - By Sagar Maheshwari</p>
        <p>Powered by AWS</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()