import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add the project root to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Load environment variables from .env file
load_dotenv(os.path.join(root_dir, '.env'))

# Support Streamlit Secrets (for Cloud Deployment)
if "GOOGLE_API_KEY" not in os.environ:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("Google API Key not found. Please set it in .env or Streamlit Secrets.")
        st.stop()


from retrieval.retriever import retrieve
from llm.corep_generator import generate_corep
from validation.rules import validate
import pandas as pd

st.title("LLM-Assisted PRA COREP Reporting Assistant")

question = st.text_input("Regulatory Question")
scenario = st.text_area("Reporting Scenario")

if st.button("Generate COREP"):
    regs = retrieve(question + scenario)
    corep = generate_corep(question, scenario, "\n".join(regs))
    warnings = validate(corep)

    st.subheader("COREP C 01.00 Extract")
    df = pd.DataFrame(corep["rows"])
    st.table(df)

    if warnings:
        st.subheader("Validation Warnings")
        for w in warnings:
            st.warning(w)

    st.subheader("Audit Log")
    st.json(corep)
