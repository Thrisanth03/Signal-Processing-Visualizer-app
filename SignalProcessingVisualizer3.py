import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Signal Lab Pro", layout="wide")

# ---------------- THEME TOGGLE ----------------
theme = st.sidebar.toggle("🌙 Dark Mode")

if theme:
    st.markdown("""
        <style>
        body {background-color: #0e1117; color: white;}
        </style>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>📡 Signal Processing Lab Pro</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Aim", "📖 Theory", "🧪 Experiment", "🧠 Quiz", "📄 Report"])

# ---------------- AIM ----------------
with tab1:
    st.subheader("Aim")
    st.write("""
    To analyze signals and reduce noise using filtering techniques.
    Understand how signal smoothing improves performance.
    """)

# ---------------- THEORY ----------------
with tab2:
    st.subheader("Detailed Theory")

    st.write("""
    Signal Processing is a branch of electrical engineering that focuses on analyzing,
    modifying, and synthesizing signals such as sound, images, and sensor data.

    A **Low-Pass Filter (LPF)** allows low-frequency signals to pass while attenuating 
    high-frequency components. It is widely used in communication systems and noise reduction.

    ### Key Concepts:
    - Sampling
    - Convolution
    - Frequency response
    - Noise reduction

    Mathematical representation:
    y[n] = (1/N) Σ x[n-k]
    """)

# ---------------- EXPERIMENT ----------------
with tab3:
    st.subheader("Interactive Experiment")

    col1, col2 = st.columns(2)

    with col1:
        freq = st.slider("Frequency", 1, 50, 5)
        noise = st.slider("Noise Level", 0.0, 1.0, 0.4)

    with col2:
        window = st.slider("Filter Window", 1, 50, 10)

    t = np.linspace(0, 1, 500)
    signal = np.sin(2 * np.pi * freq * t)
    noisy = signal + noise * np.random.randn(len(t))
    filtered = np.convolve(noisy, np.ones(window)/window, mode='same')

    fig, ax = plt.subplots()
    ax.plot(t, noisy, label="Noisy Signal")
    ax.plot(t, filtered, label="Filtered Signal", linewidth=2)
    ax.legend()

    st.pyplot(fig)

# ---------------- DYNAMIC QUIZ ----------------
with tab4:
    st.subheader("Dynamic Quiz")

    questions = [
        ("What does LPF allow?", ["High freq", "Low freq", "Noise"], "Low freq"),
        ("Filtering method used?", ["Convolution", "Integration", "FFT"], "Convolution"),
        ("Noise effect?", ["Improves signal", "Distorts signal", "No effect"], "Distorts signal"),
        ("Window size increase?", ["More smoothing", "More noise", "No change"], "More smoothing"),
    ]

    selected = random.sample(questions, 3)

    answers = []
    for i, q in enumerate(selected):
        ans = st.radio(q[0], q[1], key=i)
        answers.append((ans, q[2]))

    if st.button("Submit Quiz"):
        score = sum([1 for a, c in answers if a == c])
        st.success(f"Score: {score}/3")

# ---------------- PDF REPORT ----------------
with tab5:
    st.subheader("Download Report")

    if st.button("Generate PDF"):
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph("Signal Processing Lab Report", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph("Aim: Analyze signal filtering.", styles["Normal"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph("Theory: LPF reduces noise.", styles["Normal"]))
        content.append(Spacer(1, 10))

        doc.build(content)

        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="Signal_Report.pdf")
