# -*- coding: utf-8 -*-
import streamlit as st
import pickle
import pandas as pd
import os

# PAGE CONFIG
st.set_page_config(
    page_title="Salary Prediction System",
    page_icon="💼",
    layout="wide"
)

# LOAD MODEL
model_path = os.path.join(os.path.dirname(__file__), "Final_model_SLR.pkl")
model = pickle.load(open(model_path, "rb"))

# ---------------- SESSION INIT ----------------
if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "years_input" not in st.session_state:
    st.session_state.years_input = 0.0

if "expected_input" not in st.session_state:
    st.session_state.expected_input = ""

if "last_years" not in st.session_state:
    st.session_state.last_years = 0.0

if "last_expected" not in st.session_state:
    st.session_state.last_expected = ""

# ---------------- SIDEBAR ----------------
st.sidebar.title("📰 Updated News")
st.sidebar.markdown("""
🔹 **IT Industry Update**  
Average salary hike for 2026 expected around **8–10%**.

🔹 **AI & Data Science**  
AI roles demand increased by **35%** in the last year.

🔹 **Freshers Market**  
Entry-level packages now start from **₹4–6 LPA**.

🔹 **Senior Professionals**  
10+ years experience roles crossing **₹30 LPA** in top firms.

🔹 **Remote Jobs**  
Remote-friendly salaries increased by **12% globally**.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("📌 *News updates are refreshed periodically*")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {background-color: #9ca3af;}

.main-title {
    text-align:center;
    font-size:38px;
    font-weight:800;
    color:#000;
    margin-bottom:5px;
}

.sub-title {
    text-align:center;
    font-size:16px;
    color:#000;
    margin-bottom:20px;
}

.salary-box {
    margin-top:10px;
    padding:18px;
    background-color:#dcfce7;
    border-left:6px solid #16a34a;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
    text-align:center;
}

/* 🔥 Disable manual typing for Years input */
div[data-baseweb="input"] input[type="number"] {
    pointer-events: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">💼 Salary Prediction System 💸</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predict your salary based on years of experience</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
years = st.number_input(
    "📊 Enter Your Years of Experience ★",
    min_value=0.0,
    max_value=50.0,
    step=0.5,
    format="%.1f",
    key="years_input"
)

expected_salary = st.text_input(
    "💰 Enter Your Expected Monthly Salary (₹)(optional)",
    key="expected_input"
)

# -------- AUTO DISAPPEAR --------
if (
    years != st.session_state.last_years or
    expected_salary != st.session_state.last_expected
):
    st.session_state.show_result = False

st.session_state.last_years = years
st.session_state.last_expected = expected_salary

# ---------------- PREDICT BUTTON ----------------
if st.button("Predict Salary"):
    st.session_state.show_result = True

# ---------------- RESULT ----------------
if st.session_state.show_result:

    monthly_salary = model.predict([[years]]).item()
    annual_salary = monthly_salary * 12

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="salary-box">
                💰 Monthly Salary <br><br>
                ₹ {monthly_salary:,.0f}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="salary-box">
                📅 Annual Salary <br><br>
                ₹ {annual_salary:,.0f}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    if annual_salary < 500000:
        st.info("🟢 Entry Level Salary")
    elif annual_salary < 1500000:
        st.success("🔵 Mid Level Salary")
    else:
        st.warning("🟣 Senior Level Salary")

    if expected_salary.strip() != "":
        try:
            expected_value = float(expected_salary)

            lower = monthly_salary * 0.9
            upper = monthly_salary * 1.1

            if expected_value < lower:
                st.warning("⚠️ Your salary expectation is lower than predicted range.")
            elif expected_value > upper:
                st.error("❌ Your expected salary exceeds predicted range.")
            else:
                st.success("✅ Your salary expectation is within acceptable range.")

        except ValueError:
            st.error("🚫 Please enter numbers only (example: 750000)")

    # -------- RESET BUTTON --------
    if st.button("Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
