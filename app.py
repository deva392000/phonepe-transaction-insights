import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
# Page configuration
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    layout="wide"
)

# Database connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-55JNORK\\SQLEXPRESS;"
    "DATABASE=phonepe;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

# =========================
# Sidebar
# =========================

st.sidebar.title("📱 PhonePe Analytics")

st.sidebar.write("Navigate through the analysis")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Home",
        "Case 1 - Transaction Dynamics",
        "Case 2 - User Engagement",
        "Case 3 - Insurance Analysis",
        "Case 4 - Market Expansion",
        "Case 5 - User Growth"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "📊 PhonePe Transaction Insights\n\n"
    "Built using Python, SQL Server & Streamlit"
)
# =========================
# HOME
# =========================

if page == "Home":

    st.title("📱 PhonePe Transaction Insights")

    st.subheader("Digital Payment Analytics Dashboard")

    st.write(
        "This project analyzes PhonePe transaction, "
        "user, insurance, and market data."
    )

    st.success("SQL Connected Successfully! ✅")

    st.markdown("---")

    # =========================
    # Project Overview
    # =========================

    st.subheader("📊 Project Overview")

    st.write(
        "This dashboard analyzes PhonePe data using "
        "Python, SQL Server, Pandas, Matplotlib, "
        "Seaborn and Streamlit."
    )

    # =========================
    # KPI Cards
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Transactions", "941B+")
    col2.metric("💵 Transaction Value", "₹1,382T+")
    col3.metric("📈 Analysis Cases", "5")
    col4.metric("🗄️ Data Source", "SQL Server")

    st.markdown("---")

    # =========================
    # Analysis Areas
    # =========================

    st.subheader("🔍 Analysis Areas")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        ### 💰 Case 1 - Transaction Dynamics

        - Transaction dynamics
        - Transaction types
        - Top states
        """)

        st.markdown("""
        ### 👥 Case 2 - User Engagement

        - Device brands
        - Registered users
        - State-wise users
        """)

        st.markdown("""
        ### 🛡️ Case 3 - Insurance Analysis

        - Insurance amount
        - Insurance types
        - State-wise insurance
        """)

    with col2:

        st.markdown("""
        ### 📈 Case 4 - Market Expansion

        - Market expansion
        - State analysis
        - District analysis
        """)

        st.markdown("""
        ### 🚀 Case 5 - User Growth

        - User growth
        - User trends
        - Growth analysis
        """)

    st.markdown("---")

    st.info(
        "👈 Select a case from the sidebar to explore the analysis."
    )


# =========================
# CASE 1
# =========================

elif page == "Case 1 - Transaction Dynamics":

    st.title("💰 Case 1 - Transaction Dynamics")

    # =========================
    # Get Data
    # =========================
    query = """
    SELECT *
    FROM aggregated_transaction
    """

    df = pd.read_sql(query, conn)

    # =========================
    # Filters
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(df["Years"].unique())
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(df["Quarter"].unique())
        )

    df = df[
        (df["Years"] == selected_year) &
        (df["Quarter"] == selected_quarter)
    ]

    # =========================
    # KPI Cards
    # =========================

    total_amount = df["Transaction_amount"].sum()
    total_transactions = df["Transaction_count"].sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "💰 Total Transaction Amount",
        f"₹{total_amount:,.0f}"
    )

    col2.metric(
        "🔢 Total Transactions",
        f"{total_transactions:,.0f}"
    )

    # =========================
    # Top 10 States
    # =========================

    st.subheader("🗺️ Top 10 States by Transaction Amount")

    transaction_states = (
        df.groupby("States")["Transaction_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_amount": "Total_Amount"
        })
        .sort_values(
            "Total_Amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=transaction_states,
        x="Total_Amount",
        y="States",
        ax=ax1
    )

    ax1.set_title("Top 10 States by Transaction Amount")
    ax1.set_xlabel("Transaction Amount")
    ax1.set_ylabel("State")

    st.pyplot(fig1)

    # =========================
    # Transaction Type
    # =========================

    st.subheader("🥧 Transaction Amount Distribution by Type")

    transaction_type = (
        df.groupby("Transaction_type")["Transaction_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_amount": "Total_Amount"
        })
    )

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    ax2.pie(
        transaction_type["Total_Amount"],
        labels=transaction_type["Transaction_type"],
        autopct="%1.1f%%"
    )

    ax2.set_title("Transaction Amount Distribution by Type")

    st.pyplot(fig2)
        # =========================
    # Business Insights
    # =========================

    st.markdown("---")

    st.subheader("💡 Business Insights")

    top_state = transaction_states.iloc[0]["States"]
    top_state_amount = transaction_states.iloc[0]["Total_Amount"]

    top_transaction_type = (
        transaction_type
        .sort_values("Total_Amount", ascending=False)
        .iloc[0]["Transaction_type"]
    )

    st.info(
        f"""
        • **Top Performing State:** {top_state} recorded the highest
        transaction amount of ₹{top_state_amount:,.0f}.

        • **Leading Transaction Type:** {top_transaction_type}
        contributed the highest transaction amount among the
        transaction categories.

        • **Business Value:** These insights help identify
        high-performing markets and understand customer
        transaction preferences.
        """
    )

# Case 2
elif page == "Case 2 - User Engagement":

    st.title("👥 Case 2 - User Engagement")

    # =========================
    # Get Data
    # =========================

    query = """
    SELECT *
    FROM aggregated_user
    """

    df = pd.read_sql(query, conn)

    # =========================
    # Filters
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(df["Years"].unique()),
            key="case2_year"
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(df["Quarter"].unique()),
            key="case2_quarter"
        )

    df = df[
        (df["Years"] == selected_year) &
        (df["Quarter"] == selected_quarter)
    ]
    # =========================
    # User Distribution by Brand
    # =========================

    st.subheader("📱 User Distribution by Device Brand")

    brand_users = (
        df.groupby("Brands")["Transaction_count"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_count": "Total_Users"
        })
        .sort_values(
            "Total_Users",
            ascending=False
        )
    )

    fig1, ax1 = plt.subplots(figsize=(7, 7))

    ax1.pie(
        brand_users["Total_Users"],
        labels=brand_users["Brands"],
        autopct="%1.1f%%"
    )

    ax1.set_title("User Distribution by Device Brand")

    st.pyplot(fig1)

    # =========================
    # Top 10 States
    # =========================

    st.subheader("🗺️ Top 10 States by Registered Users")

    user_states = (
        df.groupby("States")["Transaction_count"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_count": "Total_Users"
        })
        .sort_values(
            "Total_Users",
            ascending=False
        )
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=user_states,
        x="Total_Users",
        y="States",
        ax=ax2
    )

    ax2.set_title("Top 10 States by Registered Users")
    ax2.set_xlabel("Registered Users")
    ax2.set_ylabel("State")

    st.pyplot(fig2)
        # =========================
    # Business Insights
    # =========================

    st.markdown("---")

    st.subheader("💡 Business Insights")

    top_brand = brand_users.iloc[0]["Brands"]
    top_brand_users = brand_users.iloc[0]["Total_Users"]

    top_user_state = user_states.iloc[0]["States"]
    top_user_state_count = user_states.iloc[0]["Total_Users"]

    st.info(
        f"""
        • **Top Device Brand:** {top_brand} has the highest
        user activity with {top_brand_users:,.0f} users.

        • **Top Performing State:** {top_user_state} has the
        highest user activity with {top_user_state_count:,.0f} users.

        • **Business Value:** Device and state-wise analysis
        helps understand user preferences and identify regions
        with stronger PhonePe adoption.
        """
    )

# Case 3
elif page == "Case 3 - Insurance Analysis":

    st.title("🛡️ Case 3 - Insurance Analysis")

    # =========================
    # Get Data
    # =========================

    query = """
    SELECT *
    FROM aggregated_insurance
    """

    df = pd.read_sql(query, conn)

    # =========================
    # Filters
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(df["Years"].unique()),
            key="case3_year"
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(df["Quarter"].unique()),
            key="case3_quarter"
        )

    df = df[
        (df["Years"] == selected_year) &
        (df["Quarter"] == selected_quarter)
    ]

    # =========================
    # Top 10 States
    # =========================

    st.subheader("🗺️ Top 10 States by Insurance Amount")

    insurance_states = (
        df.groupby("States")["Insurance_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Insurance_amount": "Total_Amount"
        })
        .sort_values(
            "Total_Amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=insurance_states,
        x="Total_Amount",
        y="States",
        ax=ax1
    )

    ax1.set_title("Top 10 States by Insurance Amount")
    ax1.set_xlabel("Insurance Amount")
    ax1.set_ylabel("State")

    st.pyplot(fig1)

    # =========================
    # Insurance Type Distribution
    # =========================

    st.subheader("🥧 Insurance Amount Distribution by Type")

    insurance_type = (
        df.groupby("Insurance_type")["Insurance_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Insurance_amount": "Total_Amount"
        })
    )

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    if insurance_type["Total_Amount"].sum() > 0:

        ax2.pie(
            insurance_type["Total_Amount"],
            labels=insurance_type["Insurance_type"],
            autopct="%1.1f%%"
        )

    else:

        ax2.text(
            0.5,
            0.5,
            "No insurance data available\nfor selected Year & Quarter",
            ha="center",
            va="center",
            fontsize=12
        )

        ax2.axis("off")

    ax2.set_title("Insurance Amount Distribution by Type")

    st.pyplot(fig2)
        # =========================
    # Business Insights
    # =========================

    st.markdown("---")

    st.subheader("💡 Business Insights")

    if not insurance_states.empty and insurance_states["Total_Amount"].sum() > 0:

        top_insurance_state = insurance_states.iloc[0]["States"]
        top_insurance_amount = insurance_states.iloc[0]["Total_Amount"]

        top_insurance_type = (
            insurance_type
            .sort_values("Total_Amount", ascending=False)
            .iloc[0]["Insurance_type"]
        )

        st.info(
            f"""
            • **Top Insurance State:** {top_insurance_state} has the
            highest insurance amount of ₹{top_insurance_amount:,.0f}.

            • **Leading Insurance Type:** {top_insurance_type}
            has the highest insurance amount among the available
            insurance categories.

            • **Business Value:** This analysis helps identify
            high-performing insurance markets and understand
            insurance adoption across different regions.
            """
        )

    else:

        st.warning(
            "No insurance data available for the selected Year & Quarter."
        )

# Case 4
elif page == "Case 4 - Market Expansion":

    st.title("📈 Case 4 - Market Expansion")

    # =========================
    # Get Data from SQL Server
    # =========================

    query = """
    SELECT *
    FROM map_transaction
    """

    df = pd.read_sql(query, conn)
        # =========================
    # Filters
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(df["Years"].unique()),
            key="case4_year"
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(df["Quarter"].unique()),
            key="case4_quarter"
        )

    df = df[
        (df["Years"] == selected_year) &
        (df["Quarter"] == selected_quarter)
    ]

    # =========================
    # Top 10 States
    # =========================

    st.subheader("🗺️ Top 10 States by Transaction Amount")

    market_states = (
        df.groupby("States")["Transaction_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_amount": "Total_Amount"
        })
        .sort_values(
            "Total_Amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=market_states,
        x="Total_Amount",
        y="States",
        ax=ax1
    )

    ax1.set_title("Top 10 States by Transaction Amount")
    ax1.set_xlabel("Transaction Amount")
    ax1.set_ylabel("State")

    st.pyplot(fig1)

    # =========================
    # Top 10 Districts
    # =========================

    st.subheader("🏙️ Top 10 Districts by Transaction Amount")

    market_districts = (
        df.groupby("District")["Transaction_amount"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_amount": "Total_Amount"
        })
        .sort_values(
            "Total_Amount",
            ascending=False
        )
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=market_districts,
        x="Total_Amount",
        y="District",
        ax=ax2
    )

    ax2.set_title("Top 10 Districts by Transaction Amount")
    ax2.set_xlabel("Transaction Amount")
    ax2.set_ylabel("District")

    st.pyplot(fig2)
        # =========================
    # Business Insights
    # =========================

    st.markdown("---")

    st.subheader("💡 Business Insights")

    if not market_states.empty and not market_districts.empty:

        top_market_state = market_states.iloc[0]["States"]
        top_market_state_amount = market_states.iloc[0]["Total_Amount"]

        top_market_district = market_districts.iloc[0]["District"]
        top_market_district_amount = market_districts.iloc[0]["Total_Amount"]

        st.info(
            f"""
            • **Top Performing State:** {top_market_state} recorded
            the highest transaction amount of
            ₹{top_market_state_amount:,.0f}.

            • **Top Performing District:** {top_market_district}
            recorded the highest transaction amount of
            ₹{top_market_district_amount:,.0f}.

            • **Business Value:** State and district-level analysis
            helps identify strong markets and potential regions
            for further business expansion.
            """
        )

    else:

        st.warning(
            "No market data available for the selected Year & Quarter."
        )

# =========================
# CASE 5 - USER GROWTH
# =========================

elif page == "Case 5 - User Growth":

    st.title("🚀 Case 5 - User Growth")

    # =========================
    # Get Data
    # =========================

    query = """
    SELECT *
    FROM aggregated_user
    """

    df = pd.read_sql(query, conn)

    # =========================
    # Filters
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            sorted(df["Years"].unique()),
            key="case5_year"
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(df["Quarter"].unique()),
            key="case5_quarter"
        )

    filtered_df = df[
        (df["Years"] == selected_year) &
        (df["Quarter"] == selected_quarter)
    ]

    # =========================
    # Total User Activity
    # =========================

    total_users = filtered_df["Transaction_count"].sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "👥 User Activity",
        f"{total_users:,.0f}"
    )

    col2.metric(
        "📅 Selected Year",
        selected_year
    )

    # =========================
    # Year-wise User Growth
    # =========================

    st.subheader("📈 Year-wise User Growth")

    yearly_users = (
        df.groupby("Years")["Transaction_count"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_count": "Total_Users"
        })
        .sort_values("Years")
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(
        yearly_users["Years"],
        yearly_users["Total_Users"],
        marker="o"
    )

    ax1.set_title("Year-wise User Growth")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("User Activity")
    ax1.grid(True)

    st.pyplot(fig1)

    # =========================
    # Quarter-wise User Growth
    # =========================

    st.subheader("📊 Quarter-wise User Growth")

    quarterly_users = (
        df.groupby(["Years", "Quarter"])["Transaction_count"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_count": "Total_Users"
        })
        .sort_values(["Years", "Quarter"])
    )

    quarterly_users["Period"] = (
        quarterly_users["Years"].astype(str)
        + "-Q"
        + quarterly_users["Quarter"].astype(str)
    )

    fig2, ax2 = plt.subplots(figsize=(12, 5))

    ax2.plot(
        quarterly_users["Period"],
        quarterly_users["Total_Users"],
        marker="o"
    )

    ax2.set_title("Quarter-wise User Growth")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("User Activity")

    plt.xticks(rotation=45)

    st.pyplot(fig2)

    # =========================
    # Top 10 States
    # =========================

    st.subheader("🗺️ Top 10 States by User Activity")

    state_users = (
        df.groupby("States")["Transaction_count"]
        .sum()
        .reset_index()
        .rename(columns={
            "Transaction_count": "Total_Users"
        })
        .sort_values(
            "Total_Users",
            ascending=False
        )
        .head(10)
    )

    fig3, ax3 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=state_users,
        x="Total_Users",
        y="States",
        ax=ax3
    )

    ax3.set_title("Top 10 States by User Activity")
    ax3.set_xlabel("User Activity")
    ax3.set_ylabel("State")

    st.pyplot(fig3)

    # =========================
    # Business Insights
    # =========================

    st.markdown("---")

    st.subheader("💡 Business Insights")

    if not yearly_users.empty and not state_users.empty:

        first_year = yearly_users.iloc[0]["Years"]
        first_year_users = yearly_users.iloc[0]["Total_Users"]

        latest_year = yearly_users.iloc[-1]["Years"]
        latest_year_users = yearly_users.iloc[-1]["Total_Users"]

        top_growth_state = state_users.iloc[0]["States"]
        top_growth_state_users = state_users.iloc[0]["Total_Users"]

        if first_year_users > 0:

            growth_percentage = (
                (latest_year_users - first_year_users)
                / first_year_users
            ) * 100

        else:

            growth_percentage = 0

        st.info(
            f"""
            • **User Growth:** User activity changed from
            {first_year_users:,.0f} in {first_year} to
            {latest_year_users:,.0f} in {latest_year}.

            • **Growth Rate:** User activity changed by
            approximately **{growth_percentage:.1f}%**
            during the analyzed period.

            • **Top State:** {top_growth_state} recorded the
            highest user activity with
            {top_growth_state_users:,.0f} users.

            • **Business Value:** User growth analysis helps
            identify growing markets and high-engagement regions
            for future customer acquisition and expansion.
            """
        )

    else:

        st.warning(
            "No user growth data available."
        )