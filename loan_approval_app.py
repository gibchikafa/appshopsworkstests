"""
Loan Approval App — Hopsworks Streamlit application
Submits a loan application to the loanagent deployment and displays
the ML decision together with Claude's plain-language explanation.
"""

import json
import logging

import hopsworks
import hopsworks.client as hc
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Approval",
    page_icon="🏦",
    layout="wide",
)

st.markdown(
    """
    <style>
      .hw-band {background:linear-gradient(90deg,#0E1117,#1A1F2B);
                border-left:6px solid #1EB182; padding:0.75rem 1rem;
                border-radius:6px; margin-bottom:1.5rem;}
      .hw-band h1 {color:#FAFAFA; margin:0; font-size:1.6rem;}
      .approved-box {border:2px solid #1EB182; border-radius:8px;
                     background:#0d2e22; padding:1.2rem; margin-top:1rem;}
      .rejected-box {border:2px solid #e05252; border-radius:8px;
                     background:#2e0d0d; padding:1.2rem; margin-top:1rem;}
      .prob-label   {font-size:0.85rem; color:#aaa; margin-bottom:0.2rem;}
      .stButton>button {background:#1EB182; color:#0E1117;
                        border:none; font-weight:700; font-size:1rem;
                        padding:0.6rem 2rem; border-radius:6px;}
    </style>
    <div class="hw-band"><h1>🏦 Loan Approval Assistant</h1></div>
    """,
    unsafe_allow_html=True,
)

# ── Hopsworks connection (cached) ─────────────────────────────────────────────
@st.cache_resource(show_spinner="Connecting to Hopsworks…")
def _connect():
    project = hopsworks.login()
    token   = hc.get_instance()._auth._token
    ms      = project.get_model_serving()
    agent   = ms.get_deployment("loanagent")
    endpoint = agent.get_endpoint_url().rstrip("/") + "/predict"
    return token, endpoint

try:
    _token, _endpoint = _connect()
except Exception as exc:
    st.error(f"Could not connect to Hopsworks: {exc}")
    st.stop()


def call_agent(application: dict) -> dict:
    resp = requests.post(
        _endpoint,
        headers={"Authorization": f"Bearer {_token}", "Content-Type": "application/json"},
        json={"instances": [application]},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["predictions"][0]


# ── Form ──────────────────────────────────────────────────────────────────────
st.subheader("Applicant Information")

col1, col2, col3 = st.columns(3)

with col1:
    education      = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed  = st.selectbox("Self Employed", ["No", "Yes"])
    no_dependents  = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0, step=1)

with col2:
    income_annum   = st.number_input("Annual Income ($)", min_value=100_000, max_value=100_000_000,
                                     value=5_000_000, step=100_000, format="%d")
    cibil_score    = st.slider("CIBIL Score", min_value=300, max_value=900, value=650, step=1)

with col3:
    loan_amount    = st.number_input("Loan Amount ($)", min_value=100_000, max_value=500_000_000,
                                     value=10_000_000, step=100_000, format="%d")
    loan_term      = st.slider("Loan Term (months)", min_value=2, max_value=20, value=12, step=1)

st.subheader("Asset Details")

acol1, acol2, acol3, acol4 = st.columns(4)
with acol1:
    residential = st.number_input("Residential Assets ($)", min_value=0, max_value=500_000_000,
                                  value=5_000_000, step=100_000, format="%d")
with acol2:
    commercial  = st.number_input("Commercial Assets ($)",  min_value=0, max_value=500_000_000,
                                  value=2_000_000, step=100_000, format="%d")
with acol3:
    luxury      = st.number_input("Luxury Assets ($)",      min_value=0, max_value=500_000_000,
                                  value=3_000_000, step=100_000, format="%d")
with acol4:
    bank_assets = st.number_input("Bank Assets ($)",        min_value=0, max_value=500_000_000,
                                  value=2_000_000, step=100_000, format="%d")

# ── Quick metrics ─────────────────────────────────────────────────────────────
total_assets     = residential + commercial + luxury + bank_assets
loan_to_income   = loan_amount / income_annum if income_annum else 0
asset_to_loan    = total_assets / loan_amount if loan_amount else 0

m1, m2, m3 = st.columns(3)
m1.metric("Total Assets ($)", f"{total_assets:,.0f}")
m2.metric("Loan-to-Income Ratio", f"{loan_to_income:.2f}x")
m3.metric("Asset-to-Loan Ratio", f"{asset_to_loan:.2f}x")

# ── Submit ────────────────────────────────────────────────────────────────────
st.divider()

if st.button("Submit Application"):
    application = {
        "no_of_dependents":        int(no_dependents),
        "education":               education,
        "self_employed":           self_employed,
        "income_annum":            int(income_annum),
        "cibil_score":             int(cibil_score),
        "loan_amount":             int(loan_amount),
        "loan_term":               int(loan_term),
        "residential_assets_value": int(residential),
        "commercial_assets_value":  int(commercial),
        "luxury_assets_value":      int(luxury),
        "bank_asset_value":         int(bank_assets),
    }
    logger.info("Submitting application: %s", application)

    with st.spinner("Evaluating application…"):
        try:
            result = call_agent(application)
        except Exception as exc:
            st.error(f"Agent call failed: {exc}")
            logger.exception("Agent call failed")
            st.stop()

    label       = result["label"]
    probability = result["probability"]
    explanation = result["explanation"]
    approved    = label == "Approved"

    # Decision banner
    if approved:
        st.markdown(
            f"""<div class="approved-box">
            <h2 style="color:#1EB182;margin:0">✅ {label}</h2>
            <p class="prob-label">Model confidence: {probability:.1%}</p>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div class="rejected-box">
            <h2 style="color:#e05252;margin:0">❌ {label}</h2>
            <p class="prob-label">Model confidence: {probability:.1%}</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.subheader("Why was this decision made?")
    st.markdown(explanation)

    logger.info("Result: %s (%.1f%%)", label, probability * 100)
