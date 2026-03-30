import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import signal
from fpdf import FPDF
import io
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SignalPro | Virtual Lab", layout="wide", initial_sidebar_state="collapsed")

# --- APPLE-INSPIRED CSS INJECTION ---
st.markdown("""
    <style>
    /* Global Styles */
    .main { background-color: #000000; color: #f5f5f7; font-family: 'SF Pro Display', -apple-system, sans-serif; }
    
    /* Glassmorphism Header */
    .stHeader {
        background: rgba(22, 22, 23, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        position: fixed; top: 0; width: 100%; z-index: 99;
    }

    /* Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 18px;
        transition: 0.3s;
    }
    
    /* Sleek Buttons */
    .stButton>button {
        border-radius: 30px;
        background: #0071e3;
        color: white;
        border: none;
        padding: 10px 25px;
        font-weight: 500;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #0077ed; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def generate_pdf(freq, amp, phase):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Signal Processing Virtual Lab Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Frequency: {freq} Hz", ln=True)
    pdf.cell(200, 10, txt=f"Amplitude: {amp} V", ln=True)
    pdf.cell(200, 10, txt=f"Phase: {phase} rad", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# --- APP LAYOUT ---
st.title("SignalPro")
st.markdown("### The Future of Digital Signal Analysis.")
st.write("---")

# Layout: Sidebar for Controls (Apple Style Minimalist)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", width=50) # Just for aesthetic
    st.header("Parameters")
    sig_type = st.selectbox("Signal Waveform", ["Sine", "Square", "Sawtooth"])
    freq = st.slider("Frequency (Hz)", 1, 100, 10)
    amp = st.slider("Amplitude (V)", 0.1, 5.0, 1.0)
    noise = st.slider("Signal Noise Level", 0.0, 1.0, 0.1)

# Main Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Time Domain Visualization")
    t = np.linspace(0, 1, 1000)
    
    # Generate Signal
    if sig_type == "Sine":
        y = amp * np.sin(2 * np.pi * freq * t)
    elif sig_type == "Square":
        y = amp * signal.square(2 * np.pi * freq * t)
    else:
        y = amp * signal.sawtooth(2 * np.pi * freq * t)
    
    y += np.random.normal(0, noise, t.shape)

    # Plotly Real-time Interactive Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, line=dict(color='#0071e3', width=2), name="Live Signal"))
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Spectral Analysis")
    fft_vals = np.abs(np.fft.fft(y))[:500]
    fft_freq = np.fft.fftfreq(len(t), t[1]-t[0])[:500]
    
    fig_fft = go.Figure()
    fig_fft.add_trace(go.Bar(x=fft_freq, y=fft_vals, marker_color='#34c759'))
    fig_fft.update_layout(
        template="plotly_dark",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_fft, use_container_width=True)

# --- ANIMATION & EXPORT SECTION ---
st.write("---")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("▶ Run Live Animation"):
        placeholder = st.empty()
        for i in range(20):
            new_t = np.linspace(i/10, (i+1)/10, 100)
            new_y = amp * np.sin(2 * np.pi * freq * new_t)
            placeholder.line_chart(new_y)
            time.sleep(0.05)

with c2:
    pdf_bytes = generate_pdf(freq, amp, 0)
    st.download_button(
        label="📄 Download Lab Report (PDF)",
        data=pdf_bytes,
        file_name="signal_report.pdf",
        mime="application/pdf",
    )

with c3:
    st.metric(label="Sampling Rate", value="44.1 kHz", delta="Optimal")

