import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")

# -----------------------------
# MOCK DATA (for demo)
# -----------------------------
def generate_mock_data(n: int = 50) -> pd.DataFrame:
    """
    Generates mock lead data for dashboard demo.

    Args:
        n (int): Number of leads.

    Returns:
        pd.DataFrame: Lead dataset.
    """
    companies = ["Plumbing Co", "HVAC Pros", "Roofing Experts", "Desert Electric"]
    sources = ["Google Maps", "Yelp", "Manual", "API"]
    industries = ["Plumbing", "HVAC", "Roofing", "Electrical"]
    statuses = ["New", "Contacted", "Meeting", "Closed", "Lost"]

    data = []

    for i in range(n):
        date_added = datetime.now() - timedelta(days=random.randint(0, 30))
        follow_up = date_added + timedelta(days=random.randint(1, 7))

        data.append({
            "Business Name": f"{random.choice(companies)} {i}",
            "Contact Name": f"Owner {i}",
            "Email": f"owner{i}@example.com",
            "Phone": "602-555-1234",
            "Industry": random.choice(industries),
            "Source": random.choice(sources),
            "Date Added": date_added,
            "Status": random.choice(statuses),
            "Next Follow-Up": follow_up
        })

    return pd.DataFrame(data)


df = generate_mock_data()

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
this_week = df[df["Date Added"] > datetime.now() - timedelta(days=7)]
month = df[df["Date Added"] > datetime.now() - timedelta(days=30)]

new_leads_week = len(this_week)
total_month = len(month)
closed = len(df[df["Status"] == "Closed"])
conversion_rate = (closed / len(df)) * 100 if len(df) else 0

avg_value = 1500  # pretend client monthly value
pipeline_value = total_month * avg_value
cost_per_lead = 25  # fake number for demo

# -----------------------------
# TOP KPI ROW
# -----------------------------
st.title("📊 Lead Generation Dashboard")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("New Leads (7d)", new_leads_week)
col2.metric("Total Leads (MTD)", total_month)
col3.metric("Conversion Rate", f"{conversion_rate:.1f}%")
col4.metric("Pipeline Value", f"${pipeline_value:,}")
col5.metric("Cost Per Lead", f"${cost_per_lead}")

# -----------------------------
# MIDDLE SECTION
# -----------------------------
left, right = st.columns([2, 1])

# LEFT: GRAPHS
with left:
    st.subheader("Leads Over Time")
    df_time = df.copy()
    df_time["Date"] = df_time["Date Added"].dt.date
    time_series = df_time.groupby("Date").size().reset_index(name="Leads")

    fig = px.line(time_series, x="Date", y="Leads")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Leads by Source")
    source_counts = df["Source"].value_counts().reset_index()
    source_counts.columns = ["Source", "Count"]

    fig2 = px.pie(source_counts, names="Source", values="Count")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Lead Status Breakdown")
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig3 = px.bar(status_counts, x="Status", y="Count")
    st.plotly_chart(fig3, use_container_width=True)

# RIGHT: FOLLOW-UP CALENDAR (simplified)
with right:
    st.subheader("📅 Follow-Ups")

    today = datetime.now().date()

    for _, row in df.sort_values("Next Follow-Up").head(10).iterrows():
        follow_date = row["Next Follow-Up"].date()

        if follow_date < today:
            color = "🔴"
        elif follow_date == today:
            color = "🟡"
        else:
            color = "🟢"

        st.write(f"{color} {row['Business Name']} — {follow_date}")

# -----------------------------
# BOTTOM TABLE
# -----------------------------
st.subheader("📋 Lead Table")

search = st.text_input("Search business...")

filtered_df = df.copy()
if search:
    filtered_df = filtered_df[
        filtered_df["Business Name"].str.contains(search, case=False)
    ]

st.dataframe(filtered_df, use_container_width=True)