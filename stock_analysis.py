import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data


def stock_analysis():

    # ======================================
    # Load Data
    # ======================================

    df = load_data()

    st.markdown("""
    <h2 style='text-align:center;'>
        📦 Walmart Inventory & Stock Analysis
    </h2>
    """, unsafe_allow_html=True)
    # ======================================
    # SIDEBAR FILTERS
    # ======================================
    st.sidebar.header("📌 Stock Filters")
    st.sidebar.markdown("---")

    years = sorted(df["Year"].unique())
    selected_year = st.sidebar.selectbox(
        "📅 Select Year",
        ["All"] + years,
        key="stock_year"
    )

    stores = sorted(df["Store"].unique())
    selected_store = st.sidebar.selectbox(
        "🏬 Select Store",
        ["All"] + stores,
        key="stock_store"
    )

    types = sorted(df["Type"].unique())
    selected_types = st.sidebar.multiselect(
        "🏪 Store Type",
        types,
        default=types,
        key="stock_type"
    )

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    selected_month = st.sidebar.selectbox(
        "📅 Month",
        ["All"] + month_order,
        key="stock_month"
    )
    # ======================================
    # Apply Filters
    # ======================================
    filtered = df.copy()

    if selected_year != "All":
        filtered = filtered[
            filtered["Year"] == selected_year
        ]

    if selected_store != "All":
        filtered = filtered[
            filtered["Store"] == selected_store
        ]

    filtered = filtered[
        filtered["Type"].isin(selected_types)
    ]

    if selected_month != "All":
        filtered = filtered[
            filtered["Month"] == selected_month
        ]

   
    

    department_sales = (
     filtered.groupby("Dept")["Weekly_Sales"]
     .sum()
)

    high_demand = (
     department_sales >= department_sales.quantile(0.75)
) .sum()

    overstock = (
     department_sales <= department_sales.quantile(0.25)
).sum()

    highest_store = (
     filtered.groupby("Store")["Weekly_Sales"]
     .sum()
     .idxmax()
)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("📦 Departments", filtered["Dept"].nunique())
    c2.metric("🔴 Restock Required", high_demand)
    c3.metric("🟢 Overstock Risk", overstock)
    c4.metric("🏬 Highest Demand Store", highest_store)
    st.markdown("---")
    
# ==========================================================
# STORES REQUIRING HIGHEST INVENTORY
# ==========================================================

    st.markdown("""
   <h2 style='text-align:center;'>
Stores Requiring Highest Inventory
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

# ----------------------------------------------------------
# Left Column - Vertical Bar Chart
# ----------------------------------------------------------
    with col1:

     top_store = (
        filtered.groupby("Store")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

     fig = px.bar(
        top_store,
        x="Store",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Top 10 Stores Requiring Highest Inventory"
    )

     fig.update_traces(
        textposition="outside"
    )

     fig.update_layout(
      height=450,
      title_x=0.15,
      xaxis_title="Store",
      yaxis_title="Weekly Sales",
      coloraxis_showscale=False,

    # Show every store label
     xaxis=dict(
        type="category",
        tickmode="array",
        tickvals=top_store["Store"],
        ticktext=top_store["Store"]
    )
)
    

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Right Column - Business Insight
# ----------------------------------------------------------
    with col2:

     highest_store = top_store.iloc[0]["Store"]
     highest_sales = top_store.iloc[0]["Weekly_Sales"]

     st.markdown("### Inventory Insight")

     st.info(f"""
### Highest Priority Store

**Store {highest_store}** has the highest inventory demand.

**Weekly Sales:** ${highest_sales:,.0f}
### Recommended Actions

• Increase inventory allocation.
• Maintain higher safety stock.
• Monitor inventory levels daily.
• Prioritize replenishment during peak demand.
• Ensure faster warehouse restocking.
""")

   

# ==========================================================
# DEPARTMENTS REQUIRING IMMEDIATE RESTOCKING
# ==========================================================
    st.markdown("""
<h2 style='text-align:center;'>
Departments Requiring Immediate Restocking
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

# ----------------------------------------------------------
# Left Column - Chart
# ----------------------------------------------------------

    with col1:

     restock = (
        filtered.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # Convert Department to string
     restock["Dept"] = restock["Dept"].astype(str)

     fig = px.bar(
        restock,
        x="Dept",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Top Departments Requiring Immediate Restocking"
    )

     fig.update_traces(
        textposition="outside"
    )

     fig.update_layout(

        height=430,
        title_x=0.12,

        xaxis_title="Department",
        yaxis_title="Weekly Sales",

        coloraxis_showscale=False,

        xaxis=dict(
            type="category"
        ),

        yaxis=dict(
            tickformat="~s"
        )
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Right Column - Business Insight
# ----------------------------------------------------------
    with col2:

     top_dept = restock.iloc[0]["Dept"]
     top_sales = restock.iloc[0]["Weekly_Sales"]

     st.markdown("### Key Insights from the Graph")

     st.info(f"""

### Highest Priority Department

**Department {top_dept} require immediate restocking**

**Weekly Sales:** ${top_sales:,.0f}

### Strategies to Increase Inventory Efficiency

- Increase inventory allocation.
- Maintain safety stock levels.
- Monitor inventory daily.
- Coordinate with suppliers for faster replenishment.
- Review inventory during peak shopping periods.
""")

# ==========================================================
# OVERSTOCK RISK DEPARTMENTS
# ==========================================================
    st.markdown("""
<h2 style='text-align:center;'>
Departments with Overstock Risk
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

# ----------------------------------------------------------
# Left Column - Chart
# ----------------------------------------------------------

    with col1:

     overstock = (
        filtered.groupby("Dept")["Weekly_Sales"]
        .sum()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
    )

     overstock["Dept"] = overstock["Dept"].astype(str)

     fig = px.bar(
        overstock,
        x="Dept",
        y="Weekly_Sales",
        color="Weekly_Sales",
        text_auto=".2s",
        title="Departments with Highest Overstock Risk"
    )

     fig.update_traces(
        textposition="outside"
    )

     fig.update_layout(
        height=430,
        title_x=0.12,
        xaxis_title="Department",
        yaxis_title="Weekly Sales",
        coloraxis_showscale=False,
        xaxis=dict(type="category"),
        yaxis=dict(tickformat="~s")
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Right Column - Business Insight
# ----------------------------------------------------------

    with col2:

     risk_dept = overstock.iloc[0]["Dept"]
     risk_sales = overstock.iloc[0]["Weekly_Sales"]

     st.markdown("### Key Insights")

     st.warning(f"""

### Highest Overstock Risk

**Department {risk_dept} has the highest overstock risk**
 **Weekly Sales:** ${risk_sales:,.0f}
### Recommended Actions to Mitigate Overstock Risk
- Reduce future purchase quantities.
- Launch promotional offers or discounts.
- Bundle slow-moving products with fast-selling items.
- Review reorder levels regularly.
- Monitor demand before placing new orders.

""")



# ==========================================================
# MONTHLY INVENTORY DEMAND
# ==========================================================

    st.markdown("---")

    st.markdown("""
<h2 style='text-align:center;'>
Monthly Inventory Demand
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

# ----------------------------------------------------------
# Left Column - Monthly Demand Chart
# ----------------------------------------------------------

    with col1:

     month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

     monthly_inventory = (
        filtered.groupby("Month")["Weekly_Sales"]
        .sum()
        .reset_index()
    )

     monthly_inventory["Month"] = pd.Categorical(
        monthly_inventory["Month"],
        categories=month_order,
        ordered=True
    )

     monthly_inventory = monthly_inventory.sort_values("Month")

     fig = px.line(
        monthly_inventory,
        x="Month",
        y="Weekly_Sales",
        markers=True,
        title="Monthly Inventory Requirement"
    )

     fig.update_traces(
        line=dict(width=4),
        marker=dict(size=10)
    )

     fig.update_layout(
        height=430,
        title_x=0.10,
        xaxis_title="Month",
        yaxis_title="Inventory Demand",
        yaxis=dict(tickformat="~s")
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Right Column - Business Insight
# ----------------------------------------------------------

    with col2:

     highest_month = (
        monthly_inventory.loc[
            monthly_inventory["Weekly_Sales"].idxmax(),
            "Month"
        ]
    )

     highest_sales = (
        monthly_inventory["Weekly_Sales"].max()
    )

     st.markdown("### Inventory Insight")

     st.info(f"""

### Peak Inventory Month

**{highest_month}** has the highest inventory demand.

**Inventory Demand:** ${highest_sales:,.0f}
• Inventory demand reaches its highest level during **{highest_month}**.
### Strategies to Prepare for Peak Inventory Demand

- Increase purchase orders before peak demand.
- Maintain higher safety stock.
- Coordinate with suppliers in advance.
- Improve warehouse planning.
- Monitor inventory levels weekly during peak months.

""")

# ==========================================================
# HOLIDAY STOCK PLANNING
# ==========================================================

    st.markdown("---")

    st.markdown("""
<h2 style='text-align:center;'>
Holiday Stock Planning
</h2>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

# ----------------------------------------------------------
# Left Column - Chart
# ----------------------------------------------------------

    with col1:

     holiday_sales = (
        filtered.groupby("IsHoliday")["Weekly_Sales"]
        .mean()
        .reset_index()
    )

     holiday_sales["IsHoliday"] = holiday_sales["IsHoliday"].replace({
        True: "Holiday",
        False: "Non-Holiday"
    })

     fig = px.bar(
        holiday_sales,
        x="IsHoliday",
        y="Weekly_Sales",
        color="IsHoliday",
        text_auto=".2s",
        title="Holiday vs Non-Holiday Inventory Demand"
    )

     fig.update_traces(
        textposition="outside"
    )

     fig.update_layout(
        height=370,
        title_x=0.12,
        xaxis_title="Period",
        yaxis_title="Inventory Demand",
        yaxis=dict(tickformat="~s"),
        showlegend=False
    )

     st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# Right Column - Business Insight
# ----------------------------------------------------------

    with col2:

     holiday_total = holiday_sales.loc[
        holiday_sales["IsHoliday"] == "Holiday",
        "Weekly_Sales"
    ].sum()

     nonholiday_total = holiday_sales.loc[
        holiday_sales["IsHoliday"] == "Non-Holiday",
        "Weekly_Sales"
    ].mean()

     if holiday_total > nonholiday_total:
        peak_period = "Holiday"
        recommendation = "Increase inventory before holiday weeks to meet higher customer demand."
     else:
        peak_period = "Non-Holiday"
        recommendation = "Maintain balanced inventory throughout the year while preparing for seasonal peaks."


     st.info(f"""
### Peak Inventory Period

**{peak_period}**

### Sales Summary

🎄 Holiday Sales: **${holiday_total:,.0f}**

🛒 Non-Holiday Sales: **${nonholiday_total:,.0f}**
### Recommended Actions

✅ {recommendation}

- Increase warehouse capacity before major holidays.
- Coordinate with suppliers in advance.
- Monitor inventory daily during festive seasons.
- Allocate additional stock to high-performing stores.

""")

    st.markdown("---")

# ==========================================================
# INVENTORY PRIORITY MATRIX
# ==========================================================



    st.markdown("""
<h2 style='text-align:center;'>
Inventory Priority Matrix
</h2>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# Prepare Priority Table
# ----------------------------------------------------------

    priority = (
     filtered.groupby("Dept")["Weekly_Sales"]
     .sum()
     .reset_index()
)

    high_limit = priority["Weekly_Sales"].quantile(0.75)
    low_limit = priority["Weekly_Sales"].quantile(0.25)

    def assign_priority(sales):

     if sales >= high_limit:
        return "🔴 High"

     elif sales <= low_limit:
        return "🟢 Low"

     else:
        return "🟡 Medium"

    priority["Priority"] = priority["Weekly_Sales"].apply(assign_priority)

    priority = priority.sort_values(
     by="Weekly_Sales",
     ascending=False
)

    priority = priority.rename(columns={
     "Dept":"Department",
     "Weekly_Sales":"Weekly Sales"
})

    priority["Weekly Sales"] = priority["Weekly Sales"].apply(
     lambda x: f"${x:,.0f}"
)

# ----------------------------------------------------------
# Display Table
# ----------------------------------------------------------

    st.dataframe(
     priority,
     hide_index=True,
     use_container_width=True
)

    st.markdown("")

# ----------------------------------------------------------
# Priority Guidelines
# ----------------------------------------------------------

    st.markdown("""
<h3 style='text-align:center;'>
Inventory Priority Guidelines
</h3>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

# ----------------------------------------------------------
# High Priority
# ----------------------------------------------------------

    with col1:

     st.error("""
### 🔴 High Priority

**Action Required Immediately**

• Increase inventory allocation

• Maintain higher safety stock

• Daily inventory monitoring

• Fast supplier replenishment

• Prevent stockouts

""")

# ----------------------------------------------------------
# Medium Priority
# ----------------------------------------------------------

    with col2:

     st.warning("""
### 🟡 Medium Priority

**Regular Monitoring**

• Weekly inventory review

• Maintain current stock

• Observe demand trends

• Standard replenishment

• Review reorder levels

""")

# ----------------------------------------------------------
# Low Priority
# ----------------------------------------------------------

    with col3:

     st.success("""
### 🟢 Low Priority

**Overstock Risk**

• Reduce purchase orders

• Run promotional offers

• Bundle slow-moving products

• Optimize warehouse space

• Monitor inventory monthly

""")

st.markdown("---")
