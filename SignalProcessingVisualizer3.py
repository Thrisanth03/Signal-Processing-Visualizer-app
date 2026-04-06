import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

st.set_page_config(page_title="Signal Processing Lab", layout="wide")

st.title("📡 Signal Processing Virtual Lab")

# Sidebar navigation
section = st.sidebar.radio("Navigate", 
                          ["Aim", "Theory", "Experiment", "Quiz", "Feedback"])

# ---------------- AIM ----------------
if section == "Aim":
    st.header("🎯 Aim")
    st.write("""
    To study and analyze the behavior of signals using filtering techniques 
    and understand how noise can be reduced using a low-pass filter.
    """)

# ---------------- THEORY ----------------
elif section == "Theory":
    st.header("📖 Theory")
    st.write("""
    Signal processing is the analysis, interpretation, and manipulation of signals. 
    A low-pass filter allows signals with frequencies lower than a selected cutoff 
    frequency to pass and attenuates frequencies higher than the cutoff frequency.
    
    In digital signal processing, filtering can be implemented using convolution. 
    This experiment demonstrates how noise can be reduced from a signal using a 
    simple moving average filter.
    """)

# ---------------- EXPERIMENT ----------------
elif section == "Experiment":
    st.header("🧪 Experiment: Low Pass Filter")

    st.subheader("Step 1: Generate Signal")

    freq = st.slider("Select Signal Frequency", 1, 50, 5)
    noise_level = st.slider("Noise Level", 0.0, 1.0, 0.5)

    t = np.linspace(0, 1, 500)
    signal = np.sin(2 * np.pi * freq * t)
    noise = noise_level * np.random.randn(len(t))
    noisy_signal = signal + noise

    st.subheader("Step 2: Apply Filter")

    window_size = st.slider("Filter Window Size", 1, 50, 10)
    filtered_signal = np.convolve(noisy_signal, np.ones(window_size)/window_size, mode='same')

    st.subheader("Step 3: Visualization")

    fig, ax = plt.subplots()
    ax.plot(t, noisy_signal, label="Noisy Signal")
    ax.plot(t, filtered_signal, label="Filtered Signal", linewidth=2)
    ax.legend()
    ax.set_title("Signal vs Filtered Output")

    st.pyplot(fig)

    st.success("Observation: Filter reduces noise and smooths the signal.")

# ---------------- QUIZ ----------------
elif section == "Quiz":
    st.header("🧠 Quiz")

    score = 0

    q1 = st.radio("1. What does a low-pass filter do?",
                  ["Blocks low frequency", "Allows low frequency", "Amplifies noise"])

    q2 = st.radio("2. Which method is used in this experiment?",
                  ["Differentiation", "Convolution", "Integration"])

    q3 = st.radio("3. Increasing window size will:",
                  ["Increase noise", "Smooth more", "Remove signal"])

    if st.button("Submit Quiz"):
        if q1 == "Allows low frequency":
            score += 1
        if q2 == "Convolution":
            score += 1
        if q3 == "Smooth more":
            score += 1

        st.write(f"✅ Your Score: {score}/3")

        if score == 3:
            st.success("Excellent!")
        elif score == 2:
            st.info("Good job!")
        else:
            st.warning("Keep practicing!")

# ---------------- FEEDBACK ----------------
elif section == "Feedback":
    st.header("📝 Feedback")

    name = st.text_input("Your Name")
    rating = st.slider("Rate this lab", 1, 5, 3)
    comments = st.text_area("Your Feedback")

    if st.button("Submit Feedback"):
        data = {
            "Name": name,
            "Rating": rating,
            "Comments": comments,
            "Time": datetime.datetime.now()
        }

        df = pd.DataFrame([data])

        try:
            df.to_csv("feedback.csv", mode='a', header=False, index=False)
        except:
            df.to_csv("feedback.csv", index=False)

        st.success("✅ Feedback saved successfully!")

# ---------------- FOOTER ----------------
st.sidebar.info("Developed using Streamlit | Signal Processing Lab")
