# app.py
import logging
import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Streamlit App
# ---------------------------------------------------
st.set_page_config(
    page_title="Simple Streamlit App",
    page_icon="🚀",
    layout="centered"
)

logger.info("Streamlit app started")

st.title("🚀 Simple Streamlit App")

st.write("Hello! This is a simple Streamlit application.")

# ---------------------------------------------------
# Name Input
# ---------------------------------------------------
name = st.text_input("What is your name?")

if name:
    logger.info(f"User entered name: {name}")
    st.success(f"Welcome, {name}!")

# ---------------------------------------------------
# Slider
# ---------------------------------------------------
number = st.slider("Pick a number", 0, 100, 25)

logger.info(f"Slider value selected: {number}")

st.write(f"You selected: **{number}**")

# ---------------------------------------------------
# Sample Data
# ---------------------------------------------------
data = pd.DataFrame({
    "x": np.arange(20),
    "y": np.random.randn(20).cumsum()
})

logger.info("Generated sample dataframe")

st.subheader("Sample Chart")
st.line_chart(data.set_index("x"))

# ---------------------------------------------------
# Button Click
# ---------------------------------------------------
if st.button("Click Me"):
    logger.info("Button was clicked")
    st.balloons()
    st.info("Button clicked!")

logger.info("App render completed")
