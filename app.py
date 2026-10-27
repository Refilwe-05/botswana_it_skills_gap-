from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "cleaned data"

# Page settings
st.set_page_config(
    page_title="Botswana IT Skills Gap",
    page_icon="📊",
    layout="wide"
)

# Load datasets
@st.cache_data
def load_data():
    jobs = pd.read_excel(DATA_DIR / "job_postings_clean.xlsx")
    graduates = pd.read_csv(DATA_DIR / "grad_profiles_clean.csv")
    demand = pd.read_csv(DATA_DIR / "demand_skills.csv")
    supply = pd.read_csv(DATA_DIR / "supply_skills.csv")
    gaps = pd.read_csv(DATA_DIR / "skills_gap_by_role.csv")
    return jobs, graduates, demand, supply, gaps

try:
    jobs, graduates, demand, supply, gaps = load_data()
except Exception as e:
    st.error(f"Could not load the project datasets: {e}")
    st.stop()

# Sidebar navigation
st.sidebar.title("Botswana IT Skills Gap")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Skills Demand",
        "Graduate Supply",
        "Gap Analysis",
        "Job Postings"
    ]
)

# Overview
if page == "Overview":
    st.title("Botswana IT Skills Gap")
    st.write(
        "An analysis of IT skills requested by employers "
        "and skills represented in graduate profiles."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Job Postings", len(jobs))
    c2.metric("Graduate Profiles", len(graduates))
    c3.metric("Skill-Gap Records", len(gaps))

    st.subheader("Project Overview")
    st.write(
        "This project compares employer skill demand with graduate "
        "skill supply to identify possible gaps and inform recommendations."
    )

# Skills Demand
elif page == "Skills Demand":
    st.title("IT Skills Demand")
    st.write("Skills identified in the job-posting dataset.")

    demand_chart = demand.sort_values(
        "Demand_Frequency", ascending=True
    )

    fig = px.bar(
        demand_chart,
        x="Demand_Frequency",
        y="Skill",
        orientation="h",
        title="IT Job Demand by Skill",
        labels={
            "Demand_Frequency": "Number of Job Postings",
            "Skill": "IT Skill"
        },
        text="Demand_Frequency"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(demand, use_container_width=True)
# Graduate Supply
elif page == "Graduate Supply":
    st.title("Graduate Skills Supply")
    st.write("Skills represented in the graduate dataset.")
    st.dataframe(supply, use_container_width=True)

    st.info("Review the column names to select the correct chart fields.")

# Gap Analysis
elif page == "Gap Analysis":
    st.title("IT Skills Gap Analysis")
    st.write("Explore the existing skills-gap results.")
    st.dataframe(gaps, use_container_width=True)

# Job Postings
elif page == "Job Postings":
    st.title("IT Job Postings")

    search = st.text_input("Search job titles or companies")

    filtered_jobs = jobs.copy()
    if search:
        mask = filtered_jobs.astype(str).apply(
            lambda col: col.str.contains(search, case=False, na=False)
        ).any(axis=1)
        filtered_jobs = filtered_jobs[mask]

    st.write(f"Showing {len(filtered_jobs)} job postings")
    st.dataframe(filtered_jobs, use_container_width=True)

st.sidebar.caption("Botswana Accountancy College · BIDA Project")
