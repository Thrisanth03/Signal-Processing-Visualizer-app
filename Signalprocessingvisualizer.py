import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
from fpdf import FPDF
import io

# --- 1. SET PAGE THEME ---
st.set_page_config(page_title="SignalPro | ECE Virtual Lab", layout="wide")

# --- 2. APPLE-STYLE CSS CUSTOMIZATION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #000000; }
    
    .stApp { background: linear-gradient(180deg, #050505 0%, #111111 100%); }
    
    /* Glassmorphic Cards */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }
    
    /* Custom Headers */
    .main-header {
        font-size: 50px; font-weight: 600;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { color: #0071e3 !important; font-size: 32px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT CONTROL CENTER ---
st.markdown('<p class="main-header">SignalPro Lab</p>', unsafe_allow_html=True)
st.markdown("##### Precision Signal Visualization & Filtering")

# Top Control Bar
with st.container():
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        sig_type = st.selectbox("Waveform", ["Sine Wave", "Square Wave", "Sawtooth"])
    with col_b:
        freq = st.number_input("Frequency (Hz)", min_value=1.0, max_value=1000.0, value=10.0)
    with col_c:
        amp = st.number_input("Amplitude (V)", min_value=0.1, max_value=10.0, value=1.0)
    with col_d:
        noise_lvl = st.slider("Ambient Noise", 0.0, 2.0, 0.2)

# --- 4. SIGNAL PROCESSING ENGINE ---
fs = 1000  # Sampling frequency
t = np.linspace(0, 1, fs)

# Generate Base Signal
if sig_type == "Sine Wave":
    clean_y = amp * np.sin(2 * np.pi * freq * t)
elif sig_type == "Square Wave":
    clean_y = amp * signal.square(2 * np.pi * freq * t)
else:
    clean_y = amp * signal.sawtooth(2 * np.pi * freq * t)

# Add Noise
noisy_y = clean_y + np.random.normal(0, noise_lvl, t.shape)

# Filter Processing (Butterworth Low-Pass)
cutoff = freq * 1.5 if freq < 450 else 499
b, a = signal.butter(4, cutoff, fs=fs, btype='low')
filtered_y = signal.filtfilt(b, a, noisy_y)

# --- 5. VISUALIZATION LAYOUT ---
tab1, tab2 = st.tabs(["📊 Time & Frequency Analysis", "🧪 Filter Lab"])

with tab1:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("#### Oscilloscope View")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t[:200], y=noisy_y[:200], name="Noisy Input", line=dict(color='rgba(255,255,255,0.3)')))
        fig.add_trace(go.Scatter(x=t[:200], y=clean_y[:200], name="Clean Signal", line=dict(color='#0071e3', width=3)))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Signal Info")
        st.metric("Peak-to-Peak", f"{2*amp} V")
        st.metric("RMS Value", f"{round(amp/np.sqrt(2), 3)} V")
        st.metric("SNR Estimate", f"{round(20*np.log10(amp/max(noise_lvl, 0.01)), 1)} dB")

with tab2:
    st.markdown("#### Real-time Digital Filtering (Butterworth LPF)")
    fig_filt = go.Figure()
    fig_filt.add_trace(go.Scatter(x=t[:300], y=noisy_y[:300], name="Raw", line=dict(color='rgba(255,0,0,0.2)')))
    fig_filt.add_trace(go.Scatter(x=t[:300], y=filtered_y[:300], name="Filtered", line=dict(color='#34c759', width=3)))
    fig_filt.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_filt, use_container_width=True)

# --- 6. EXPORT & REPORTING ---
st.divider()
ec1, ec2 = st.columns([3, 1])

with ec2:
    # PDF Generation Logic
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "ECE Virtual Lab Report", ln=True, align='C')
        pdf.set_font("Helvetica", size=12)
        pdf.ln(10)
        pdf.cell(0, 10, f"Signal Type: {sig_type}", ln=True)
        pdf.cell(0, 10, f"Frequency: {freq} Hz", ln=True)
        pdf.cell(0, 10, f"Noise Level: {noise_lvl}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    st.download_button(
        label="Download Analysis Report (PDF)",
        data=create_pdf(),
        file_name="ECE_Lab_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


