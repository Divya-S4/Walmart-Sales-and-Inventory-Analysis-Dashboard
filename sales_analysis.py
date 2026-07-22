import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data


def sales_analysis():

    # -----------------------------
    # Load Data
    # -----------------------------
    df = load_data()

    # -----------------------------
    # Page Title
    # -----------------------------
    st.markdown(
        """
        <h2 style='text-align:center;'>
            📊 Walmart Sales Analysis Dashboard
        </h2>
        """,
        unsafe_allow_html=True
    )

    # ==========================================================
    # SIDEBAR FILTERS
    # ==========================================================

    st.sidebar.header("Filters")
    st.sidebar.markdown("---")

    years = sorted(df["Year"].unique())
    selected_year = st.sidebar.selectbox(
        "📅 Select Year",
        ["All"] + years
    )

    st.sidebar.markdown("---")

    stores = sorted(df["Store"].unique())
    selected_store = st.sidebar.selectbox(
        "🏬 Select Store",
        ["All"] + stores
    )

    st.sidebar.markdown("---")

    types = sorted(df["Type"].unique())
    selected_types = st.sidebar.multiselect(
        "🏪 Store Type",
        types,
        default=types
    )

    st.sidebar.markdown("---")

    departments = sorted(df["Dept"].unique())
    selected_department = st.sidebar.selectbox(
        "📦 Department",
        ["All"] + departments
    )

    st.sidebar.markdown("---")

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    selected_month = st.sidebar.selectbox(
        "📅 Select Month",
        ["All"] + month_order
    )

    st.sidebar.markdown("---")

    holiday = st.sidebar.selectbox(
        "🎄 Holiday",
        ["All", "Holiday", "Non-Holiday"]
    )

    # ==========================================================
    # APPLY FILTERS
    # ==========================================================

    filtered = df.copy()

    if selected_year != "All":
        filtered = filtered[filtered["Year"] == selected_year]

    if selected_store != "All":
        filtered = filtered[filtered["Store"] == selected_store]

    filtered = filtered[filtered["Type"].isin(selected_types)]

    if selected_department != "All":
        filtered = filtered[filtered["Dept"] == selected_department]

    if selected_month != "All":
        filtered = filtered[filtered["Month"] == selected_month]

    if holiday == "Holiday":
        filtered = filtered[filtered["IsHoliday"] == True]

    elif holiday == "Non-Holiday":
        filtered = filtered[filtered["IsHoliday"] == False]

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    st.markdown(
        """
        <h2 style='text-align:center;'>
            Sales Overview
        </h2>
        """,
        unsafe_allow_html=True
    )

    total_sales = filtered["Weekly_Sales"].sum()
    avg_sales = filtered["Weekly_Sales"].mean()
    total_stores = filtered["Store"].nunique()
    total_departments = filtered["Dept"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    c2.metric("📊 Avg Weekly Sales", f"${avg_sales:,.0f}")
    c3.metric("🏬 Stores", total_stores)
    c4.metric("📦 Departments", total_departments)

    st.markdown("---")

    # ==========================================================
    # STORE PERFORMANCE
    # ==========================================================

    st.markdown(
        """
        <h2 style='text-align:center;'>
            Store Performance
        </h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------
    # Top 10 Stores
    # -----------------------------
    # ==========================================================
# Top 10 Departments (Vertical Bar Chart)
# ==========================================================

    with col1:

     top_departments = (
        filtered.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

     fig = px.bar(
        top_departments,
        x="Dept",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Top 10 Performing Departments"
    )

     fig.update_traces(
        width=0.6,
        textposition="outside"
    )

     fig.update_layout(
        height=450,
        title_x=0.15,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Department",
        yaxis_title="Weekly Sales",
        xaxis=dict(type="category"),
        yaxis_tickformat="~s"
    )

     st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Store Type Sales
    # -----------------------------
    with col2:

        type_sales = (
            filtered.groupby("Type")["Weekly_Sales"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            type_sales,
            names="Type",
            values="Weekly_Sales",
            hole=0.55,
            title="Sales Contribution by Store Type"
        )

        fig.update_layout(
        height=450,
        title_x=0.25,
        title_font=dict(size=15)
)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

# ==========================================================
# DEPARTMENT PERFORMANCE
# ==========================================================

    st.markdown(
     """
     <h2 style='text-align:center;'>
        Department Performance
     </h2>
    """,
    unsafe_allow_html=True
)

# Create two equal columns
    col1, col2 = st.columns([1, 1], gap="large")

# ==========================================================
# Top 10 Departments
# ==========================================================

    with col1:

     top_departments = (
        filtered.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

     fig = px.bar(
        top_departments,
        x="Dept",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Top 10 Performing Departments"
    )

     fig.update_traces(width=0.7)

     fig.update_layout(
        height=400,
        title_x=0.12,
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

     st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Bottom 10 Departments (Vertical Bar Chart)
# ==========================================================

    with col2:

     bottom_departments = (
        filtered.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
    )

     fig = px.bar(
        bottom_departments,
        x="Dept",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Bottom 10 Performing Departments"
    )

     fig.update_traces(
        width=0.6,
        textposition="outside"
    )

     fig.update_layout(
        height=450,
        title_x=0.15,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Department",
        yaxis_title="Weekly Sales",
        xaxis=dict(type="category"),
        yaxis_tickformat="~s"
    )

     st.plotly_chart(fig, use_container_width=True)
  
# ----------------------------------------------------------
# Monthly Sales Trend
# ----------------------------------------------------------

    with col1:

     month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

     monthly_sales = (
        filtered.groupby("Month")["Weekly_Sales"]
        .sum()
        .reset_index()
    )

     monthly_sales["Month"] = pd.Categorical(
        monthly_sales["Month"],
        categories=month_order,
        ordered=True
    )

     monthly_sales = monthly_sales.sort_values("Month")

     fig = px.line(
        monthly_sales,
        x="Month",
        y="Weekly_Sales",
        markers=True,
        title="Overall Monthly Sales"
    )

     fig.update_traces(
        line=dict(width=4),
        marker=dict(size=9)
    )

     fig.update_layout(
        height=450,
        title_x=0.15
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Monthly Sales by Store Type
# ----------------------------------------------------------

    with col2:

     monthly_type = (
        filtered.groupby(["Month", "Type"])["Weekly_Sales"]
        .sum()
        .reset_index()
    )

     monthly_type["Month"] = pd.Categorical(
        monthly_type["Month"],
        categories=month_order,
        ordered=True
    )

     monthly_type = monthly_type.sort_values("Month")

     fig = px.line(
        monthly_type,
        x="Month",
        y="Weekly_Sales",
        color="Type",
        markers=True,
        title="Monthly Sales by Store Type"
    )

     fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

     fig.update_layout(
        height=450,
        title_x=0.12
    )

     st.plotly_chart(fig, use_container_width=True)

    

# ==========================================================
# HOLIDAY SALES ANALYSIS
# ==========================================================

    st.markdown(
    """
     <h2 style='text-align:center;'>
        Holiday Sales Analysis
     </h2>
    """,
     unsafe_allow_html=True
)

    col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Holiday vs Non-Holiday Sales
# ----------------------------------------------------------

    with col1:

     holiday_sales = (
        filtered.groupby("IsHoliday")["Weekly_Sales"]
        .sum()
        .reset_index()
    )

     holiday_sales["IsHoliday"] = holiday_sales["IsHoliday"].replace({
        True: "Holiday",
        False: "Non-Holiday"
    })

     fig = px.pie(
        holiday_sales,
        names="IsHoliday",
        values="Weekly_Sales",
        hole=0.55,
        title="Holiday vs Non-Holiday Sales"
    )

     fig.update_layout(
        height=450,
        title_x=0.18
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Average Weekly Sales
# ----------------------------------------------------------

    with col2:

     avg_sales = (
        filtered.groupby("IsHoliday")["Weekly_Sales"]
        .mean()
        .reset_index()
    )

     avg_sales["IsHoliday"] = avg_sales["IsHoliday"].replace({
        True: "Holiday",
        False: "Non-Holiday"
    })

     fig = px.bar(
        avg_sales,
        x="IsHoliday",
        y="Weekly_Sales",
        color="IsHoliday",
        text_auto=".2s",
        title="Average Weekly Sales"
    )

     fig.update_layout(
        height=450,
        title_x=0.20,
        xaxis_title="",
        yaxis_title="Average Weekly Sales",
        coloraxis_showscale=False
    )

     st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

# ==========================================================
# EXTERNAL FACTORS AFFECTING SALES
# ==========================================================

    st.markdown(
    """
     <h2 style='text-align:center;'>
        External Factors Affecting Sales
     </h2>
    """,
     unsafe_allow_html=True
)

    col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Temperature vs Weekly Sales
# ----------------------------------------------------------

    with col1:

     fig = px.scatter(
        filtered,
        x="Temperature",
        y="Weekly_Sales",
        color="Type",
        opacity=0.7,
        title="Temperature vs Weekly Sales"
    )

     fig.update_layout(
        height=420,
        title_x=0.15,
        coloraxis_showscale=False
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Fuel Price vs Weekly Sales
# ----------------------------------------------------------

    with col2:

     fig = px.scatter(
        filtered,
        x="Fuel_Price",
        y="Weekly_Sales",
        color="Type",
        opacity=0.7,
        title="Fuel Price vs Weekly Sales"
    )

     fig.update_layout(
        height=420,
        title_x=0.15,
        coloraxis_showscale=False
    )

     st.plotly_chart(fig, use_container_width=True)


    col3, col4 = st.columns(2)


# ==============================
# Business Recommendations
# ==============================
    st.markdown("---")
    

    st.markdown("""
## Logic to Increase Purchases

**Segmented Campaigns** : Develop segmented marketing campaigns that address specific regional needs and customer preferences.

**Customer Feedback** : Collect and analyze customer feedback from different regions to improve products, pricing, and services.

**Strategic Investment** : Invest in regions showing strong growth potential or underserved markets to increase sales opportunities.

**Store Performance** : Focus on improving underperforming stores through better inventory management, local promotions, and operational improvements.

**Discount Optimization** : Optimize discount strategies by reducing excessive discounts on low-margin products and offering targeted promotions.

**Inventory Planning** : Maintain optimal inventory levels for high-demand products to prevent stockouts and improve customer satisfaction.

**Seasonal Planning** : Use historical sales trends and holiday patterns to plan inventory, staffing, and promotional campaigns effectively.
""")
