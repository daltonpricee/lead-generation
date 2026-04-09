import os
import random

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

st.set_page_config(layout="wide")

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding: 2rem;
}
.metric-card {
    background-color: #111;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #222;
}
.small-title {
    font-size: 14px;
    color: #aaa;
}
.big-number {
    font-size: 28px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

LEADS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "leads.xlsx"))


def load_leads(filepath: str) -> pd.DataFrame:
    if os.path.exists(filepath):
        df = pd.read_excel(filepath, engine="openpyxl")
        if not df.empty:
            if "Date Added" not in df.columns:
                df["Date Added"] = pd.Timestamp.now()
            if "Next Follow-Up" not in df.columns:
                df["Next Follow-Up"] = pd.Timestamp.now() + pd.Timedelta(days=3)
            if "Status" not in df.columns:
                df["Status"] = "New"
            if "Source" not in df.columns:
                df["Source"] = "Unknown"
            if "Industry" not in df.columns:
                df["Industry"] = "Construction"
            return df

    return generate_mock_data()


def generate_mock_data(n=30):
    companies = ["Sunset Construction Services", "Pinnacle Builders", "Ridge Line Builders", "Valley Concrete"]
    sources = ["Google Maps", "Thumbtack", "Manual", "Referral"]
    industries = ["Construction", "Concrete", "General Contractor"]
    statuses = ["New", "Contacted", "Meeting", "Proposal", "Closed"]

    data = []
    for i in range(n):
        date_added = datetime.now() - timedelta(days=random.randint(0, 28))
        follow_up = date_added + timedelta(days=random.randint(1, 10))
        data.append({
            "Business Name": f"{random.choice(companies)} {i}",
            "Source": random.choice(sources),
            "Industry": random.choice(industries),
            "Date Added": date_added,
            "Status": random.choice(statuses),
            "Next Follow-Up": follow_up,
        })
    return pd.DataFrame(data)


df = load_leads(LEADS_FILE)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Calendar", "Leads"])

with tab1:
    st.title("Bookkeeping Lead Pipeline")
    st.markdown("Targeting smaller construction companies that are good bookkeeping prospects.")

    this_week = df[df["Date Added"] > datetime.now() - timedelta(days=7)]
    month = df[df["Date Added"] > datetime.now() - timedelta(days=30)]

    new_leads_week = len(this_week)
    total_month = len(month)
    status_series = df["Status"] if "Status" in df.columns else pd.Series([], dtype=str)
    closed = len(df[status_series == "Closed"])
    conversion_rate = (closed / len(df)) * 100 if len(df) else 0

    pipeline_value = total_month * 1800
    cost_per_lead = 22

    cols = st.columns(5)
    metrics = [
        ("New Leads (7d)", new_leads_week),
        ("Total Leads (MTD)", total_month),
        ("Conversion Rate", f"{conversion_rate:.1f}%"),
        ("Pipeline Value", f"${pipeline_value:,}"),
        ("Cost Per Lead", f"${cost_per_lead}"),
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="small-title">{label}</div>
                <div class="big-number">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])
    with left:
        df_time = df.copy()
        df_time["Date"] = pd.to_datetime(df_time["Date Added"]).dt.date
        time_series = df_time.groupby("Date").size().reset_index(name="Leads")

        fig = px.line(time_series, x="Date", y="Leads")
        fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Lead Status")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.pie(status_counts, names="Status", values="Count", hole=0.5)
        fig_status.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_status, use_container_width=True)

with tab2:
    st.title("Follow-Up Calendar")
    events = []

    for _, row in df.iterrows():
        events.append({
            "title": row.get("Business Name", "Untitled"),
            "start": pd.to_datetime(row.get("Next Follow-Up", datetime.now())).strftime("%Y-%m-%d"),
        })

    calendar(events=events, options={
        "initialView": "dayGridMonth",
        "height": 650,
    })

with tab3:
    st.title("Leads")
    search = st.text_input("Search businesses")
    source_filter = st.selectbox("Filter by source", options=["All"] + sorted(df["Source"].dropna().unique().tolist()))
    industry_filter = st.selectbox("Filter by industry", options=["All"] + sorted(df["Industry"].dropna().unique().tolist()))

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df["Business Name"].str.contains(search, case=False, na=False)]
    if source_filter and source_filter != "All":
        filtered_df = filtered_df[filtered_df["Source"] == source_filter]
    if industry_filter and industry_filter != "All":
        filtered_df = filtered_df[filtered_df["Industry"] == industry_filter]

    st.dataframe(filtered_df, use_container_width=True)
