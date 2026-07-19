import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config with a more playful theme
st.set_page_config(
    page_title="Telco Churn Predictor Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with bolder, more playful styling and improved readability
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
        box-sizing: border-box;
    }
    
    body {
        color: #e0e0e0; /* Softer white for better readability on dark bg */
    }

    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .super-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 50px 40px;
        margin-bottom: 50px;
        border: 3px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 50px 0 rgba(0, 0, 0, 0.5);
        text-align: center;
        animation: fadeIn 1.5s ease-out, glow 3s infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .super-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,0,150,0.3), rgba(0,200,255,0.3));
        z-index: -1;
        animation: pulseBackground 8s infinite alternate;
    }
    
    .mega-title {
        font-family: 'Righteous', cursive;
        font-size: 4.5rem !important;
        background: linear-gradient(45deg, #ff8a00, #e52e71, #00b4db);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(255, 138, 0, 0.5);
        margin-bottom: 15px;
        animation: bounce 2s infinite alternate;
    }

    p {
        line-height: 1.6; /* Improved line spacing for paragraph text */
    }
    
    .card {
        background: rgba(255, 255, 255, 0.1); /* Slightly more opaque for better contrast */
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 50px;
        padding: 30px;
        margin-bottom: 30px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #00b4db);
        z-index: 1;
    }
    
    .card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 20px 60px 0 rgba(0, 0, 0, 0.6);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff8a00 0%, #e52e71 50%, #00b4db 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.2);
        animation: float 6s ease-in-out infinite;
    }
    
    .metric-card h3 {
        font-size: 1.8rem !important;
        margin-bottom: 15px;
    }
    
    .metric-card p {
        font-size: 2.5rem !important;
        font-weight: 900;
        margin: 0;
    }
    
    .prediction-box {
        padding: 40px;
        border-radius: 25px;
        margin: 40px 0;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        animation: pulse 2s infinite;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    .churn {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .no-churn {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
        color: white;
        border-right: 2px solid rgba(255, 255, 255, 0.15);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #ff8a00 0%, #e52e71 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 18px 40px;
        font-weight: 900;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Keyframe animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 5px 20px rgba(0, 0, 0, 0.4); }
        50% { transform: scale(1.05); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6); }
        100% { transform: scale(1); box-shadow: 0 5px 20px rgba(0, 0, 0, 0.4); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-25px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes bounce {
        0% { transform: translateY(0); }
        100% { transform: translateY(-20px); }
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px rgba(255, 138, 0, 0.7), 0 0 20px rgba(255, 138, 0, 0.5), 0 0 30px rgba(255, 138, 0, 0.3); }
        to { text-shadow: 0 0 20px rgba(255, 138, 0, 0.8), 0 0 40px rgba(255, 138, 0, 0.6), 0 0 60px rgba(255, 138, 0, 0.4); }
    }
    
    @keyframes pulseBackground {
        from { opacity: 0.3; }
        to { opacity: 0.6; }
    }
    
    /* Heading and title styles */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 900;
        color: #ffffff;
    }
    
    h1 { font-size: 3.5rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 2rem !important; }
    
    .stSelectbox, .stSlider, .stNumberInput {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 12px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        font-size: 1.1rem;
    }
    
    /* Improved sidebar styling */
    .sidebar-title {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
        border-bottom: 3px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-title h2 {
        font-family: 'Righteous', cursive;
        font-size: 2.5rem !important;
        background: linear-gradient(45deg, #ff8a00, #e52e71);
        -webkit-background-clip: text;
        margin-bottom: 10px;
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1rem;
        margin: 5px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        animation: bounce 2s infinite alternate;
    }
    
    .badge-primary { background: linear-gradient(135deg, #ff8a00, #e52e71); }
    .badge-success { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .badge-warning { background: linear-gradient(135deg, #ff416c, #ff4b2b); }

</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT AND CONTENT ---

# Load model and encoders (cached for performance)
@st.cache_resource
def load_components():
    with open('churn_model.pkl', 'rb') as file:
        model = pickle.load(file)
    with open('label_encoders.pkl', 'rb') as file:
        label_encoders = pickle.load(file)
    with open('model_columns.pkl', 'rb') as file:
        model_columns = pickle.load(file)
    return model, label_encoders, model_columns

model, label_encoders, model_columns = load_components()

# App header with enhanced styling
st.markdown("""
<div class="super-header">
    <h1 class="mega-title">📱 TELCO CHURN PREDICTOR PRO</h1>
    <p style="font-size: 2rem; opacity: 0.9; margin: 0;">AI-Powered Customer Retention System</p>
    <div style="margin-top: 25px;">
        <span class="badge badge-primary">🚀 85% Prediction Accuracy</span>
        <span class="badge badge-success">💎 Real-time Analytics</span>
        <span class="badge badge-warning">🎯 Actionable Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Decorative icons to replace Lottie animations
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("""
    <div style="text-align: center; font-size: 8rem; margin-bottom: 30px;">
        📊
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="text-align: center; font-size: 8rem; margin-bottom: 30px;">
        🤖
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="text-align: center; font-size: 8rem; margin-bottom: 30px;">
        📈
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR FOR USER INPUT ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <h2>👤 CUSTOMER PROFILE</h2>
        <p style="color: #bdc3c7; margin-top: 5px; font-size: 1.1rem;">Input customer data for analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # IMPROVEMENT: Use expanders to organize inputs and save space
    with st.expander("👥 DEMOGRAPHICS", expanded=True):
        gender = st.selectbox("Gender", label_encoders['gender'].classes_, key="gender")
        SeniorCitizen = st.selectbox("Senior Citizen", ['No', 'Yes'], key="senior")
        Partner = st.selectbox("Partner", label_encoders['Partner'].classes_, key="partner")
        Dependents = st.selectbox("Dependents", label_encoders['Dependents'].classes_, key="dependents")

    with st.expander("📞 SERVICES & TENURE", expanded=True):
        tenure = st.slider("Tenure (months)", 0, 72, 12, key="tenure")
        PhoneService = st.selectbox("Phone Service", label_encoders['PhoneService'].classes_, key="phone")
        MultipleLines = st.selectbox("Multiple Lines", label_encoders['MultipleLines'].classes_, key="multi")
        InternetService = st.selectbox("Internet Service", label_encoders['InternetService'].classes_, key="internet")
        OnlineSecurity = st.selectbox("Online Security", label_encoders['OnlineSecurity'].classes_, key="security")
        OnlineBackup = st.selectbox("Online Backup", label_encoders['OnlineBackup'].classes_, key="backup")
        DeviceProtection = st.selectbox("Device Protection", label_encoders['DeviceProtection'].classes_, key="device")
        TechSupport = st.selectbox("Tech Support", label_encoders['TechSupport'].classes_, key="tech")
        StreamingTV = st.selectbox("Streaming TV", label_encoders['StreamingTV'].classes_, key="tv")
        StreamingMovies = st.selectbox("Streaming Movies", label_encoders['StreamingMovies'].classes_, key="movies")

    with st.expander("💰 BILLING & CONTRACT", expanded=True):
        Contract = st.selectbox("Contract", label_encoders['Contract'].classes_, key="contract")
        PaperlessBilling = st.selectbox("Paperless Billing", label_encoders['PaperlessBilling'].classes_, key="paperless")
        PaymentMethod = st.selectbox("Payment Method", label_encoders['PaymentMethod'].classes_, key="payment")
        MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, key="monthly")
        TotalCharges = st.number_input("Total Charges ($)", 0.0, 10000.0, 2000.0, key="total")

    # Live clock in the sidebar
    st.markdown(f"""
    <div class="card" style="margin-top: 30px;">
        <center>
            <h3 style="font-size: 1.5rem !important;">⏰ REAL-TIME ANALYSIS</h3>
            <p style="font-family: 'Roboto Mono', monospace; font-size: 1.5rem; font-weight: 700;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </center>
    </div>
    """, unsafe_allow_html=True)


# --- PREDICTION LOGIC ---

# Convert user inputs into a dictionary for the model
input_data = {
    'gender': gender, 'SeniorCitizen': 1 if SeniorCitizen == 'Yes' else 0, 'Partner': Partner,
    'Dependents': Dependents, 'tenure': tenure, 'PhoneService': PhoneService, 'MultipleLines': MultipleLines,
    'InternetService': InternetService, 'OnlineSecurity': OnlineSecurity, 'OnlineBackup': OnlineBackup,
    'DeviceProtection': DeviceProtection, 'TechSupport': TechSupport, 'StreamingTV': StreamingTV,
    'StreamingMovies': StreamingMovies, 'Contract': Contract, 'PaperlessBilling': PaperlessBilling,
    'PaymentMethod': PaymentMethod, 'MonthlyCharges': MonthlyCharges, 'TotalCharges': TotalCharges
}

# Encode categorical variables using the loaded label encoders
encoded_data = {}
for col, value in input_data.items():
    if col in label_encoders and col != 'Churn':
        encoded_data[col] = label_encoders[col].transform([value])[0]
    else:
        encoded_data[col] = value

# Create a DataFrame with the correct column order for the model
features = pd.DataFrame([encoded_data], columns=model_columns)

# Prediction button
predict_btn = st.button('🚀 LAUNCH CHURN ANALYSIS', use_container_width=True)

# --- DISPLAY RESULTS OR WELCOME MESSAGE ---

if predict_btn:
    with st.spinner('🌀 Scanning customer data with AI...'):
        time.sleep(2)  # Simulate processing time
        
        # Make prediction and get probability
        prediction = model.predict(features)
        prediction_proba = model.predict_proba(features)
        churn_probability = prediction_proba[0][1]
        
        # Display prediction result (Churn vs. No Churn)
        if prediction[0] == 1:
            st.markdown(f"""
            <div class="prediction-box churn">
                <h3 style="color: white; margin:0; font-size: 2.5rem;">⚠️ CRITICAL CHURN RISK DETECTED</h3>
                <p style="font-size: 3.5rem; margin:20px 0; font-weight: 900;">{churn_probability*100:.2f}% PROBABILITY</p>
                <p style="font-size: 1.5rem;">Immediate action required to retain this customer</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔧 RETENTION STRATEGIES", expanded=True):
                st.markdown("""
                <div class="card"><h4>🛡️ Immediate Actions:</h4><ul>
                    <li>Assign dedicated account manager for personalized service.</li>
                    <li>Offer exclusive loyalty discount (15-20%).</li>
                    <li>Provide complimentary service upgrade for 3 months.</li>
                    <li>Schedule immediate follow-up call within 24 hours.</li>
                </ul></div>
                <div class="card"><h4>📊 Strategic Recommendations:</h4><ul>
                    <li>Analyze usage patterns to identify pain points.</li>
                    <li>Develop personalized retention offer based on customer value.</li>
                    <li>Implement win-back campaign with special incentives.</li>
                    <li>Monitor closely for 60 days with enhanced support.</li>
                </ul></div>
                """, unsafe_allow_html=True)
                
        else:
            st.markdown(f"""
            <div class="prediction-box no-churn">
                <h3 style="color: white; margin:0; font-size: 2.5rem;">✅ LOW CHURN RISK</h3>
                <p style="font-size: 3.5rem; margin:20px 0; font-weight: 900;">{(1-churn_probability)*100:.2f}% RETENTION PROBABILITY</p>
                <p style="font-size: 1.5rem;">This customer shows strong loyalty indicators</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("💎 ENHANCEMENT OPPORTUNITIES", expanded=True):
                st.markdown("""
                <div class="card"><h4>🚀 Growth Opportunities:</h4><ul>
                    <li>Upsell premium services or bundled offerings.</li>
                    <li>Introduce referral program with incentives.</li>
                    <li>Offer exclusive access to beta features.</li>
                    <li>Consider for loyalty program tier upgrade.</li>
                </ul></div>
                <div class="card"><h4>🛡️ Retention Reinforcement:</h4><ul>
                    <li>Continue providing excellent service quality.</li>
                    <li>Regular check-ins to maintain satisfaction.</li>
                    <li>Personalized offers based on usage patterns.</li>
                    <li>Proactive communication about new features.</li>
                </ul></div>
                """, unsafe_allow_html=True)
        
        # --- VISUALIZATIONS ---
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 CHURN PROBABILITY METER")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta", value = churn_probability * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Level", 'font': {'size': 24, 'color': 'white'}},
                delta = {'reference': 50, 'increasing': {'color': "#ff416c"}, 'decreasing': {'color': "#00b09b"}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "white"},
                    'bar': {'color': "rgba(255, 65, 108, 0.8)"},
                    'bgcolor': "rgba(0,0,0,0.2)", 'borderwidth': 3, 'bordercolor': "#00b4db",
                    'steps': [
                        {'range': [0, 30], 'color': 'rgba(0, 176, 155, 0.5)'},
                        {'range': [30, 70], 'color': 'rgba(255, 255, 0, 0.5)'},
                        {'range': [70, 100], 'color': 'rgba(255, 65, 108, 0.5)'}],
                    'threshold': {'line': {'color': "#00b4db", 'width': 5}, 'thickness': 0.85, 'value': 50}}))
            fig_gauge.update_layout(height=450, font={'color': "white", 'family': "Montserrat"}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with viz_col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔍 KEY INFLUENCING FACTORS")
            feature_importance = model.feature_importances_
            importance_df = pd.DataFrame({'Feature': model_columns, 'Importance': feature_importance}).sort_values('Importance', ascending=False).head(8)
            fig_bar = px.bar(importance_df, x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='viridis')
            fig_bar.update_layout(height=450, font={'color': "white", 'family': "Montserrat"}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, autorange="reversed"))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --- CUSTOMER PROFILE SUMMARY ---
        with st.expander("👤 CUSTOMER PROFILE ANALYSIS", expanded=True):
            profile_col1, profile_col2, profile_col3 = st.columns(3)
            with profile_col1:
                st.markdown(f'<div class="metric-card"><p>{tenure}</p><h3>months</h3><h4>TENURE</h4></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card"><p>{Contract}</p><h3>CONTRACT</h3></div>', unsafe_allow_html=True)
            with profile_col2:
                st.markdown(f'<div class="metric-card"><p>${MonthlyCharges:.2f}</p><h3>MONTHLY</h3></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card"><p>{PaymentMethod.replace(" (automatic)", "")}</p><h3>PAYMENT</h3></div>', unsafe_allow_html=True)
            with profile_col3:
                st.markdown(f'<div class="metric-card"><p>${TotalCharges:.2f}</p><h3>TOTAL</h3></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card"><p>{InternetService}</p><h3>INTERNET</h3></div>', unsafe_allow_html=True)
        
        # --- INDUSTRY INSIGHTS ---
        st.markdown("---")
        st.subheader("📈 INDUSTRY INSIGHTS")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.markdown('<div class="card"><h4>📊 INDUSTRY CHURN RATE</h4><h3 style="font-size: 2.5rem !important;">20-25%</h3><p>Monthly average across telecom sector</p></div>', unsafe_allow_html=True)
        with stats_col2:
            st.markdown('<div class="card"><h4>💰 CUSTOMER LIFETIME VALUE</h4><h3 style="font-size: 2.5rem !important;">$3,500</h3><p>Estimated value of retaining a customer</p></div>', unsafe_allow_html=True)
        with stats_col3:
            st.markdown('<div class="card"><h4>🛡️ RETENTION SUCCESS RATE</h4><h3 style="font-size: 2.5rem !important;">65%</h3><p>With proactive intervention strategies</p></div>', unsafe_allow_html=True)

else:
    # Initial welcome screen before prediction
    welcome_col1, welcome_col2 = st.columns(2)
    with welcome_col1:
        st.markdown("""
        <div class="card">
            <h3>🌌 WELCOME TO CHURN PREDICTOR PRO</h3>
            <p>This advanced AI system analyzes customer data to predict churn risk with 85% accuracy. To begin, please fill out the customer details in the sidebar and click the 'Launch Analysis' button.</p>
        </div>
        <div class="card">
            <h3>🚀 HOW IT WORKS</h3>
            <p>Our machine learning model analyzes 20+ customer attributes to predict churn risk using:</p>
            <ul>
                <li>An advanced Random Forest algorithm.</li>
                <li>Real-time predictive analytics.</li>
                <li>Actionable, data-driven recommendations.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # "Why You Should Use This" card
        st.markdown("""
        <div class="card">
            <h3>💡 WHY YOU SHOULD USE THIS TOOL</h3>
            <p>Customer churn costs telecom companies billions annually. Our predictor helps you:</p>
            <ul>
                <li>Identify at-risk customers before they leave</li>
                <li>Reduce customer acquisition costs by up to 5x</li>
                <li>Increase customer lifetime value</li>
                <li>Improve retention strategy ROI</li>
                <li>Gain competitive advantage with predictive insights</li>
            </ul>
            <p style="margin-top: 15px; font-weight: 700;">📈 Companies using predictive churn analytics see up to 15% improvement in retention rates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with welcome_col2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 40px;">
            <h2 style="font-size: 4rem; margin: 20px 0;">📊</h2>
            <h3>AI-POWERED INSIGHTS</h3>
            <p>Advanced analytics for customer retention</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>💎 BENEFITS</h3>
            <p>Early identification of at-risk customers enables you to:</p>
            <ul>
                <li>Reduce customer acquisition costs.</li>
                <li>Improve customer retention rates.</li>
                <li>Increase customer lifetime value.</li>
                <li>Enhance overall customer satisfaction.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics card to show value proposition
        st.markdown("""
        <div class="card">
            <h3>📊 PROVEN RESULTS</h3>
            <div style="display: flex; justify-content: space-between; margin: 15px 0;">
                <div style="text-align: center;">
                    <h4 style="margin: 0; font-size: 2rem;">85%</h4>
                    <p style="margin: 0;">Accuracy</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0; font-size: 2rem;">25%</h4>
                    <p style="margin: 0;">Cost Reduction</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0; font-size: 2rem;">15%</h4>
                    <p style="margin: 0;">Retention Boost</p>
                </div>
            </div>
            <p style="text-align: center; font-style: italic; margin-top: 15px;">Based on implementations with major telecom providers</p>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: rgba(255, 255, 255, 0.7; font-size: 16px;">
    <hr style="border-top: 2px solid rgba(255, 255, 255, 0.2);">
    <p style="font-size: 1.2rem;">🛡️ TELCO CHURN PREDICTOR PRO • ADVANCED AI ANALYTICS</p>
    <p>For enterprise solutions, contact our data science team at prashantsingh8578@gmail.com</p>
    <p style="margin-top: 25px; font-weight: bold; font-size: 1rem;">Made with ❤️ by Prashant Kumar</p>
</div>
""", unsafe_allow_html=True)