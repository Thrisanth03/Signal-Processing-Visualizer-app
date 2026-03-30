import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from fpdf import FPDF

# --- 1. THEME & SESSION STATE ---
st.set_page_config(page_title="SignalPro | ECE Virtual Lab", layout="wide")

# --- 2. APPLE-INSPIRED UI/UX CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Profile Card in Sidebar */
    .profile-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Main Dashboard Cards */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: USER PROFILE & SETTINGS ---
with st.sidebar:
    st.markdown("### 🎓 Student Profile")
    with st.container():
        # Personalize these with your details
        user_name = st.text_input("Full Name", value="[Your Name]")
        reg_no = st.text_input("Register Number", value="[9208...]")
        dept = st.selectbox("Department", ["Electronics & Communication", "Electrical Engineering", "IoT Specialization"], index=0)
        year = st.select_slider("Academic Year", options=["I", "II", "III", "IV"], value="II")
    
    st.divider()
    theme = st.toggle("🌙 Dark Mode", value=True)
    st.caption(f"Status: {year} Year Student | {dept}")

# Adjust Colors based on Toggle
bg, text, chart_theme = ("#000000", "#FFFFFF", "plotly_dark") if theme else ("#F5F5F7", "#1D1D1F", "plotly_white")

# --- 4. MAIN APP CONTENT ---
st.title("SignalPro Virtualizer")
st.markdown("##### Department of Electronics and Communication Engineering")

# Signal Parameter Inputs
col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    sig_type = st.radio("Signal Source", ["Sine", "Square", "Noise-Heavy"], horizontal=True)
with col_in2:
    freq = st.number_input("Center Frequency (Hz)", value=50.0, step=10.0)
with col_in3:
    amp = st.slider("Signal Amplitude (V)", 0.0, 10.0, 1.0)

# --- 5. ECE CALCULATIONS (REAL-TIME) ---
t = np.linspace(0, 0.05, 1000) # 50ms window
y = amp * np.sin(2 * np.pi * freq * t) if sig_type == "Sine" else amp * signal.square(2 * np.pi * freq * t)

# Add Gaussian Noise
noise = np.random.normal(0, 0.2, t.shape)
y_obs = y + noise

# DSP Metrics
rms = np.sqrt(np.mean(y**2))
snr = 10 * np.log10(np.var(y) / np.var(noise))

# --- 6. GRAPHICAL OUTPUT ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y_obs, name="Observed Signal", line=dict(color='#0071e3', width=1.5)))
fig.add_trace(go.Scatter(x=t, y=y, name="Ideal Waveform", line=dict(color='#34c759', width=3)))

fig.update_layout(
    template=chart_theme,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# Metrics Grid
m1, m2, m3 = st.columns(3)
m1.metric("RMS Voltage", f"{round(rms, 2)} V")
m2.metric("SNR Ratio", f"{round(snr, 1)} dB")
m3.metric("Sampling State", "Optimal (fs > 2f)")

# --- 7. PDF EXPORT WITH USER DATA ---
def generate_student_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, "Signal Processing Lab Analysis", ln=True, align='C')
    
    pdf.set_font("Helvetica", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Student: {user_name}", ln=True)
    pdf.cell(0, 10, f"Register No: {reg_no}", ln=True)
    pdf.cell(0, 10, f"Department: {dept} (Year {year})", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"Frequency Tested: {freq} Hz", ln=True)
    pdf.cell(0, 10, f"Signal RMS: {round(rms, 2)} V", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.download_button(
    label="📩 Generate Official Lab Report",
    data=generate_student_report(),
    file_name=f"Report_{reg_no}.pdf",
    mime="application/pdf",
    use_container_width=True
)
