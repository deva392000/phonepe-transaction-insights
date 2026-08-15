import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📱",
    layout="wide"
)


# ============================================================
# 2. SQL SERVER CONNECTION
# ============================================================

@st.cache_resource
def get_connection():

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-55JNORK\\SQLEXPRESS;"
        "DATABASE=phonepe;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return conn


conn = get_connection()


# ============================================================
# 3. INDIA GEOJSON
# ============================================================

INDIA_GEOJSON = (
    "https://gist.githubusercontent.com/jbrobst/"
    "56c13bbbf9d97d187fea01ca62ea5112/raw/"
    "e388c4cae20aa53cb5090210a42ebb9b765c0a36/"
    "india_states.geojson"
)


# ============================================================
# 4. STATE NAME CONVERSION
# ============================================================

STATE_MAPPING = {

    "andaman-&-nicobar-islands":
        "Andaman and Nicobar Islands",

    "andaman-and-nicobar-islands":
        "Andaman and Nicobar Islands",

    "andhra-pradesh":
        "Andhra Pradesh",

    "arunachal-pradesh":
        "Arunachal Pradesh",

    "assam":
        "Assam",

    "bihar":
        "Bihar",

    "chhattisgarh":
        "Chhattisgarh",

    "goa":
        "Goa",

    "gujarat":
        "Gujarat",

    "haryana":
        "Haryana",

    "himachal-pradesh":
        "Himachal Pradesh",

    "jammu-&-kashmir":
        "Jammu and Kashmir",

    "jammu-and-kashmir":
        "Jammu and Kashmir",

    "jharkhand":
        "Jharkhand",

    "karnataka":
        "Karnataka",

    "kerala":
        "Kerala",

    "madhya-pradesh":
        "Madhya Pradesh",

    "maharashtra":
        "Maharashtra",

    "manipur":
        "Manipur",

    "meghalaya":
        "Meghalaya",

    "mizoram":
        "Mizoram",

    "nagaland":
        "Nagaland",

    "odisha":
        "Odisha",

    "orissa":
        "Odisha",

    "punjab":
        "Punjab",

    "rajasthan":
        "Rajasthan",

    "sikkim":
        "Sikkim",

    "tamil-nadu":
        "Tamil Nadu",

    "telangana":
        "Telangana",

    "tripura":
        "Tripura",

    "uttar-pradesh":
        "Uttar Pradesh",

    "uttarakhand":
        "Uttarakhand",

    "west-bengal":
        "West Bengal",

    "delhi":
        "NCT of Delhi"
}


# ============================================================
# 5. PREPARE STATE NAME FOR MAP
# ============================================================

def prepare_map_data(df):

    df = df.copy()

    df["States"] = (
        df["States"]
        .astype(str)
        .str.strip()
    )

    df["Map_State"] = (
        df["States"]
        .str.lower()
        .str.replace(" ", "-", regex=False)
        .replace(STATE_MAPPING)
    )

    return df


# ============================================================
# 6. INDIA MAP FUNCTION
# ============================================================

def create_india_map(
    df,
    value_column,
    title,
    color_scale,
    hover_columns=None
):

    map_df = prepare_map_data(df)

    if map_df.empty:

        st.warning(
            "No data available for the selected filters."
        )

        return

    # --------------------------------------------------------
    # Hover data
    # --------------------------------------------------------

    hover_data = {}

    if hover_columns:

        for column in hover_columns:

            if column in map_df.columns:

                hover_data[column] = ":,.0f"

    # --------------------------------------------------------
    # Create map
    # --------------------------------------------------------

    fig = px.choropleth(

        map_df,

        geojson=INDIA_GEOJSON,

        featureidkey="properties.ST_NM",

        locations="Map_State",

        color=value_column,

        color_continuous_scale=color_scale,

        hover_name="States",

        hover_data=hover_data
    )

    # --------------------------------------------------------
    # Map layout
    # --------------------------------------------------------

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(

        title=title,

        height=600,

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        )
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 7. SIDEBAR
# ============================================================

st.sidebar.title(
    "📱 PhonePe Analytics"
)

st.sidebar.write(
    "Navigate through the analysis"
)

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
    "Python • SQL Server • Pandas • "
    "Plotly • Matplotlib • Streamlit"
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.title(
        "📱 PhonePe Transaction Insights"
    )

    st.subheader(
        "Digital Payment Analytics Dashboard"
    )

    st.write(
        "This project analyzes PhonePe transaction, "
        "user, insurance and market data using "
        "Python and SQL Server."
    )

    st.success(
        "SQL Server Connected Successfully! ✅"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader(
        "📊 Project Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Transactions",
        "941B+"
    )

    col2.metric(
        "💵 Transaction Value",
        "₹1,382T+"
    )

    col3.metric(
        "📈 Analysis Cases",
        "5"
    )

    col4.metric(
        "🗄️ Database",
        "SQL Server"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # PROJECT OBJECTIVE
    # --------------------------------------------------------

    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        """
        The objective of this project is to analyze PhonePe
        digital payment data and identify transaction trends,
        user engagement, insurance adoption, market expansion
        opportunities and user growth patterns.
        """
    )

    # --------------------------------------------------------
    # CASES
    # --------------------------------------------------------

    st.subheader(
        "🔍 Business Case Studies"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 💰 Case 1
            **Transaction Dynamics**

            Analyze transaction amount, transaction count,
            transaction types and state-wise performance.
            """
        )

        st.markdown(
            """
            ### 👥 Case 2
            **User Engagement**

            Analyze device brands, user activity and
            state-wise user engagement.
            """
        )

        st.markdown(
            """
            ### 🛡️ Case 3
            **Insurance Analysis**

            Analyze insurance amount, insurance types
            and state-wise insurance adoption.
            """
        )

    with col2:

        st.markdown(
            """
            ### 📈 Case 4
            **Market Expansion**

            Identify strong states and districts and
            potential markets for expansion.
            """
        )

        st.markdown(
            """
            ### 🚀 Case 5
            **User Growth**

            Analyze yearly, quarterly and state-wise
            user growth.
            """
        )

    st.markdown("---")

    st.info(
        "👈 Select a case from the sidebar to begin analysis."
    )


# ============================================================
# CASE 1
# TRANSACTION DYNAMICS
# ============================================================

elif page == "Case 1 - Transaction Dynamics":

    st.title(
        "💰 Case 1 - Transaction Dynamics"
    )

    # --------------------------------------------------------
    # SQL
    # --------------------------------------------------------

    query = """
    SELECT *
    FROM aggregated_transaction
    """

    df = pd.read_sql(
        query,
        conn
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.subheader(
        "🔎 Filters"
    )

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "Select Year",

            sorted(
                df["Years"].unique()
            ),

            key="case1_year"
        )

    with col2:

        selected_quarter = st.selectbox(
            "Select Quarter",

            sorted(
                df["Quarter"].unique()
            ),

            key="case1_quarter"
        )

    df = df[
        (df["Years"] == selected_year)
        &
        (df["Quarter"] == selected_quarter)
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_amount = (
        df["Transaction_amount"].sum()
    )

    total_transactions = (
        df["Transaction_count"].sum()
    )

    average_transaction = (
        total_amount / total_transactions
        if total_transactions > 0
        else 0
    )

    number_states = (
        df["States"].nunique()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Transaction Amount",
        f"₹{total_amount:,.0f}"
    )

    col2.metric(
        "🔢 Transactions",
        f"{total_transactions:,.0f}"
    )

    col3.metric(
        "💵 Avg Transaction",
        f"₹{average_transaction:,.2f}"
    )

    col4.metric(
        "🗺️ States",
        number_states
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP DATA
    # --------------------------------------------------------

    st.subheader(
        "🗺️ Transaction Amount by State"
    )

    map_data = (
        df.groupby("States")
        .agg(
            Transaction_Amount=(
                "Transaction_amount",
                "sum"
            ),

            Transaction_Count=(
                "Transaction_count",
                "sum"
            )
        )
        .reset_index()
    )

    map_data["Average_Transaction"] = (
        map_data["Transaction_Amount"]
        /
        map_data["Transaction_Count"]
    )

    create_india_map(

        map_data,

        "Transaction_Amount",

        "PhonePe Transaction Amount by State",

        "Reds",

        [
            "Transaction_Amount",
            "Transaction_Count",
            "Average_Transaction"
        ]
    )

    # --------------------------------------------------------
    # TOP 10 STATES
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top 10 States by Transaction Amount"
    )

    transaction_states = (
        df.groupby("States")
        ["Transaction_amount"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_amount":
                "Total_Amount"
            }
        )
        .sort_values(
            "Total_Amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=transaction_states,
        x="Total_Amount",
        y="States",
        ax=ax1
    )

    ax1.set_title(
        "Top 10 States by Transaction Amount"
    )

    ax1.set_xlabel(
        "Transaction Amount"
    )

    ax1.set_ylabel(
        "State"
    )

    st.pyplot(fig1)

    # --------------------------------------------------------
    # TRANSACTION TYPE
    # --------------------------------------------------------

    st.subheader(
        "🥧 Transaction Amount by Type"
    )

    transaction_type = (
        df.groupby("Transaction_type")
        ["Transaction_amount"]
        .sum()
        .reset_index()
    )

    if not transaction_type.empty:

        fig2, ax2 = plt.subplots(
            figsize=(7, 7)
        )

        ax2.pie(
            transaction_type[
                "Transaction_amount"
            ],

            labels=transaction_type[
                "Transaction_type"
            ],

            autopct="%1.1f%%"
        )

        ax2.set_title(
            "Transaction Amount Distribution"
        )

        st.pyplot(fig2)

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "💡 Business Insights"
    )

    top_state = (
        transaction_states.iloc[0]["States"]
    )

    top_amount = (
        transaction_states.iloc[0]
        ["Total_Amount"]
    )

    top_type = (
        transaction_type
        .sort_values(
            "Transaction_amount",
            ascending=False
        )
        .iloc[0]
        ["Transaction_type"]
    )

    st.info(
        f"""
        **Top State:** {top_state}

        **Transaction Amount:** ₹{top_amount:,.0f}

        **Leading Transaction Type:** {top_type}

        **Business Value:** Identifies high-performing
        markets and customer transaction preferences.
        """
    )


# ============================================================
# CASE 2
# USER ENGAGEMENT
# ============================================================

elif page == "Case 2 - User Engagement":

    st.title(
        "👥 Case 2 - User Engagement"
    )

    query = """
    SELECT *
    FROM aggregated_user
    """

    df = pd.read_sql(
        query,
        conn
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                df["Years"].unique()
            ),
            key="case2_year"
        )

    with col2:

        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(
                df["Quarter"].unique()
            ),
            key="case2_quarter"
        )

    df = df[
        (df["Years"] == selected_year)
        &
        (df["Quarter"] == selected_quarter)
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_activity = (
        df["Transaction_count"].sum()
    )

    brands = df["Brands"].nunique()

    states = df["States"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 User Activity",
        f"{total_activity:,.0f}"
    )

    col2.metric(
        "📱 Device Brands",
        brands
    )

    col3.metric(
        "🗺️ States",
        states
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.subheader(
        "🗺️ User Activity by State"
    )

    map_data = (
        df.groupby("States")
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "User_Activity"
            }
        )
    )

    create_india_map(

        map_data,

        "User_Activity",

        "PhonePe User Activity by State",

        "Blues",

        ["User_Activity"]
    )

    # --------------------------------------------------------
    # DEVICE BRAND
    # --------------------------------------------------------

    st.subheader(
        "📱 Device Brand Distribution"
    )

    brand_users = (
        df.groupby("Brands")
        ["Transaction_count"]
        .sum()
        .reset_index()
    )

    fig1, ax1 = plt.subplots(
        figsize=(7, 7)
    )

    ax1.pie(
        brand_users[
            "Transaction_count"
        ],

        labels=brand_users[
            "Brands"
        ],

        autopct="%1.1f%%"
    )

    ax1.set_title(
        "User Activity by Device Brand"
    )

    st.pyplot(fig1)

    # --------------------------------------------------------
    # STATES
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top 10 States by User Activity"
    )

    user_states = (
        df.groupby("States")
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "Total_Users"
            }
        )
        .sort_values(
            "Total_Users",
            ascending=False
        )
        .head(10)
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=user_states,
        x="Total_Users",
        y="States",
        ax=ax2
    )

    ax2.set_title(
        "Top 10 States by User Activity"
    )

    st.pyplot(fig2)

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "💡 Business Insights"
    )

    top_brand = (
        brand_users
        .sort_values(
            "Transaction_count",
            ascending=False
        )
        .iloc[0]["Brands"]
    )

    top_state = (
        user_states.iloc[0]["States"]
    )

    st.info(
        f"""
        **Top Device Brand:** {top_brand}

        **Top State:** {top_state}

        **Business Value:** Helps understand device
        preferences and regional PhonePe adoption.
        """
    )


# ============================================================
# CASE 3
# INSURANCE ANALYSIS
# ============================================================

elif page == "Case 3 - Insurance Analysis":

    st.title(
        "🛡️ Case 3 - Insurance Analysis"
    )

    query = """
    SELECT *
    FROM aggregated_insurance
    """

    df = pd.read_sql(
        query,
        conn
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                df["Years"].unique()
            ),
            key="case3_year"
        )

    with col2:

        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(
                df["Quarter"].unique()
            ),
            key="case3_quarter"
        )

    df = df[
        (df["Years"] == selected_year)
        &
        (df["Quarter"] == selected_quarter)
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    insurance_amount = (
        df["Insurance_amount"].sum()
    )

    states = df["States"].nunique()

    if "Insurance_count" in df.columns:

        insurance_count = (
            df["Insurance_count"].sum()
        )

    else:

        insurance_count = 0

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🛡️ Insurance Amount",
        f"₹{insurance_amount:,.0f}"
    )

    col2.metric(
        "📄 Insurance Count",
        f"{insurance_count:,.0f}"
    )

    col3.metric(
        "🗺️ States",
        states
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.subheader(
        "🗺️ Insurance Amount by State"
    )

    map_data = (
        df.groupby("States")
        ["Insurance_amount"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Insurance_amount":
                "Insurance_Amount"
            }
        )
    )

    create_india_map(

        map_data,

        "Insurance_Amount",

        "PhonePe Insurance Amount by State",

        "Greens",

        ["Insurance_Amount"]
    )

    # --------------------------------------------------------
    # TOP STATES
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top 10 States by Insurance Amount"
    )

    insurance_states = (
        df.groupby("States")
        ["Insurance_amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Insurance_amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=insurance_states,
        x="Insurance_amount",
        y="States",
        ax=ax1
    )

    ax1.set_title(
        "Top 10 States by Insurance Amount"
    )

    st.pyplot(fig1)

    # --------------------------------------------------------
    # INSURANCE TYPE
    # --------------------------------------------------------

    st.subheader(
        "🥧 Insurance Type Distribution"
    )

    insurance_type = (
        df.groupby("Insurance_type")
        ["Insurance_amount"]
        .sum()
        .reset_index()
    )

    if (
        not insurance_type.empty
        and insurance_type[
            "Insurance_amount"
        ].sum() > 0
    ):

        fig2, ax2 = plt.subplots(
            figsize=(7, 7)
        )

        ax2.pie(
            insurance_type[
                "Insurance_amount"
            ],

            labels=insurance_type[
                "Insurance_type"
            ],

            autopct="%1.1f%%"
        )

        ax2.set_title(
            "Insurance Amount Distribution"
        )

        st.pyplot(fig2)

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "💡 Business Insights"
    )

    if not insurance_states.empty:

        top_state = (
            insurance_states.iloc[0]["States"]
        )

        top_amount = (
            insurance_states.iloc[0]
            ["Insurance_amount"]
        )

        st.info(
            f"""
            **Top Insurance State:** {top_state}

            **Insurance Amount:** ₹{top_amount:,.0f}

            **Business Value:** Helps identify states
            with stronger insurance adoption and
            potential insurance markets.
            """
        )


# ============================================================
# CASE 4
# MARKET EXPANSION
# ============================================================

elif page == "Case 4 - Market Expansion":

    st.title(
        "📈 Case 4 - Market Expansion"
    )

    query = """
    SELECT *
    FROM map_transaction
    """

    df = pd.read_sql(
        query,
        conn
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                df["Years"].unique()
            ),
            key="case4_year"
        )

    with col2:

        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(
                df["Quarter"].unique()
            ),
            key="case4_quarter"
        )

    df = df[
        (df["Years"] == selected_year)
        &
        (df["Quarter"] == selected_quarter)
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_amount = (
        df["Transaction_amount"].sum()
    )

    total_transactions = (
        df["Transaction_count"].sum()
    )

    states = df["States"].nunique()

    districts = df["District"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Transaction Amount",
        f"₹{total_amount:,.0f}"
    )

    col2.metric(
        "🔢 Transactions",
        f"{total_transactions:,.0f}"
    )

    col3.metric(
        "🗺️ States",
        states
    )

    col4.metric(
        "🏙️ Districts",
        districts
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.subheader(
        "🗺️ Market Activity by State"
    )

    map_data = (
        df.groupby("States")
        .agg(
            Transaction_Amount=(
                "Transaction_amount",
                "sum"
            ),

            Transaction_Count=(
                "Transaction_count",
                "sum"
            )
        )
        .reset_index()
    )

    create_india_map(

        map_data,

        "Transaction_Amount",

        "PhonePe Market Activity by State",

        "Oranges",

        [
            "Transaction_Amount",
            "Transaction_Count"
        ]
    )

    # --------------------------------------------------------
    # TOP STATES
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top 10 States"
    )

    market_states = (
        df.groupby("States")
        ["Transaction_amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Transaction_amount",
            ascending=False
        )
        .head(10)
    )

    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=market_states,
        x="Transaction_amount",
        y="States",
        ax=ax1
    )

    ax1.set_title(
        "Top 10 States by Transaction Amount"
    )

    st.pyplot(fig1)

    # --------------------------------------------------------
    # TOP DISTRICTS
    # --------------------------------------------------------

    st.subheader(
        "🏙️ Top 10 Districts"
    )

    market_districts = (
        df.groupby("District")
        ["Transaction_amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Transaction_amount",
            ascending=False
        )
        .head(10)
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=market_districts,
        x="Transaction_amount",
        y="District",
        ax=ax2
    )

    ax2.set_title(
        "Top 10 Districts by Transaction Amount"
    )

    st.pyplot(fig2)

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "💡 Business Insights"
    )

    top_state = (
        market_states.iloc[0]["States"]
    )

    top_district = (
        market_districts.iloc[0]["District"]
    )

    st.info(
        f"""
        **Top State:** {top_state}

        **Top District:** {top_district}

        **Business Value:** State and district-level
        analysis helps identify strong markets and
        potential expansion opportunities.
        """
    )


# ============================================================
# CASE 5
# USER GROWTH
# ============================================================

elif page == "Case 5 - User Growth":

    st.title(
        "🚀 Case 5 - User Growth"
    )

    query = """
    SELECT *
    FROM aggregated_user
    """

    df = pd.read_sql(
        query,
        conn
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                df["Years"].unique()
            ),
            key="case5_year"
        )

    with col2:

        selected_quarter = st.selectbox(
            "Select Quarter",
            sorted(
                df["Quarter"].unique()
            ),
            key="case5_quarter"
        )

    filtered_df = df[
        (df["Years"] == selected_year)
        &
        (df["Quarter"] == selected_quarter)
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    user_activity = (
        filtered_df["Transaction_count"].sum()
    )

    states = filtered_df["States"].nunique()

    brands = filtered_df["Brands"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 User Activity",
        f"{user_activity:,.0f}"
    )

    col2.metric(
        "🗺️ States",
        states
    )

    col3.metric(
        "📱 Brands",
        brands
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.subheader(
        "🗺️ User Activity by State"
    )

    map_data = (
        df.groupby("States")
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "User_Activity"
            }
        )
    )

    create_india_map(

        map_data,

        "User_Activity",

        "PhonePe User Activity by State",

        "Purples",

        ["User_Activity"]
    )

    # --------------------------------------------------------
    # YEARLY GROWTH
    # --------------------------------------------------------

    st.subheader(
        "📈 Year-wise User Growth"
    )

    yearly_users = (
        df.groupby("Years")
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "Total_Users"
            }
        )
        .sort_values(
            "Years"
        )
    )

    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )

    ax1.plot(
        yearly_users["Years"],
        yearly_users["Total_Users"],
        marker="o"
    )

    ax1.set_title(
        "Year-wise User Growth"
    )

    ax1.set_xlabel(
        "Year"
    )

    ax1.set_ylabel(
        "User Activity"
    )

    ax1.grid(True)

    st.pyplot(fig1)

    # --------------------------------------------------------
    # QUARTERLY GROWTH
    # --------------------------------------------------------

    st.subheader(
        "📊 Quarter-wise User Growth"
    )

    quarterly_users = (
        df.groupby(
            ["Years", "Quarter"]
        )
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "Total_Users"
            }
        )
        .sort_values(
            ["Years", "Quarter"]
        )
    )

    quarterly_users["Period"] = (
        quarterly_users["Years"]
        .astype(str)
        +
        "-Q"
        +
        quarterly_users["Quarter"]
        .astype(str)
    )

    fig2, ax2 = plt.subplots(
        figsize=(12, 5)
    )

    ax2.plot(
        quarterly_users["Period"],
        quarterly_users["Total_Users"],
        marker="o"
    )

    ax2.set_title(
        "Quarter-wise User Growth"
    )

    ax2.set_xlabel(
        "Quarter"
    )

    ax2.set_ylabel(
        "User Activity"
    )

    plt.xticks(
        rotation=45
    )

    st.pyplot(fig2)

    # --------------------------------------------------------
    # TOP STATES
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top 10 States by User Activity"
    )

    state_users = (
        df.groupby("States")
        ["Transaction_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Transaction_count":
                "Total_Users"
            }
        )
        .sort_values(
            "Total_Users",
            ascending=False
        )
        .head(10)
    )

    fig3, ax3 = plt.subplots(
        figsize=(10, 5)
    )

    sns.barplot(
        data=state_users,
        x="Total_Users",
        y="States",
        ax=ax3
    )

    ax3.set_title(
        "Top 10 States by User Activity"
    )

    st.pyplot(fig3)

    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "💡 Business Insights"
    )

    first_year_users = (
        yearly_users.iloc[0]["Total_Users"]
    )

    latest_year_users = (
        yearly_users.iloc[-1]["Total_Users"]
    )

    first_year = (
        yearly_users.iloc[0]["Years"]
    )

    latest_year = (
        yearly_users.iloc[-1]["Years"]
    )

    if first_year_users > 0:

        growth = (
            (
                latest_year_users
                -
                first_year_users
            )
            /
            first_year_users
        ) * 100

    else:

        growth = 0

    top_state = (
        state_users.iloc[0]["States"]
    )

    st.info(
        f"""
        **User Growth:** Activity changed from
        {first_year_users:,.0f} in {first_year}
        to {latest_year_users:,.0f} in {latest_year}.

        **Growth Rate:** {growth:.1f}%

        **Top State:** {top_state}

        **Business Value:** Helps identify growing
        markets and high-engagement regions.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "PhonePe Transaction Insights | "
    "Python + SQL Server + Streamlit"
)