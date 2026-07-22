import streamlit as st

def about():

    st.markdown(
        """
        <h1 style='text-align:center;'>
            ℹ️ About the Project
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # =====================================================
    # ABOUT DEVELOPER
    # =====================================================

    st.markdown("## 👩‍💻 About the Developer")

    st.info("""
**Name:** Divya S

**Academic Qualification:** Master of Computer Applications (MCA)

**College:** Acharya Institute of Technology, Bengaluru

**Project Type:** Academic Major Project

**Project Completion Date:** 12-07-2025
""")

    st.markdown("---")

    # =====================================================
    # PROJECT OVERVIEW
    # =====================================================

    st.markdown("## 🛒 Project Overview")

    st.write("""
The **Walmart Sales and Inventory Analysis Dashboard** is an interactive business intelligence application developed using **Python** and **Streamlit**.

The dashboard transforms raw Walmart sales data into meaningful business insights through interactive visualizations, KPI metrics, filtering options, and inventory recommendations.

The project helps business users understand sales performance, inventory demand, department performance, seasonal trends, and inventory planning without requiring technical knowledge.
""")

    st.markdown("---")

    # =====================================================
    # OBJECTIVES
    # =====================================================

    st.markdown("## 🎯 Project Objectives")

    st.markdown("""
- Analyze Walmart sales performance across multiple stores.
- Identify high-performing and low-performing departments.
- Monitor inventory demand across stores.
- Detect departments requiring immediate restocking.
- Identify overstock risks.
- Analyze holiday demand patterns.
- Support inventory planning using business insights.
- Help management make data-driven inventory decisions.
""")

    st.markdown("---")

    # =====================================================
    # FEATURES
    # =====================================================

    st.markdown("## 🚀 Dashboard Features")

    st.markdown("""
### 📊 Sales Analysis

- Sales Overview KPIs
- Store Performance Analysis
- Department Performance
- Monthly Sales Trends
- Holiday Sales Analysis
- Business Insights
- Sales Improvement Recommendations

### 📦 Inventory Analysis

- Stores Requiring Highest Inventory
- Departments Requiring Immediate Restocking
- Overstock Risk Analysis
- Monthly Inventory Demand
- Holiday Stock Planning
- Inventory Priority Matrix
- Inventory Recommendations

### 🎛 Interactive Dashboard

- Dynamic Sidebar Filters
- Store Filter
- Department Filter
- Store Type Filter
- Year Filter
- Month Filter
- Holiday Filter
""")

    st.markdown("---")

    # =====================================================
    # BUSINESS PROBLEMS
    # =====================================================

    st.markdown("## 💼 Business Problems Addressed")

    st.markdown("""
The dashboard addresses several real-world retail challenges including:

- Declining sales performance
- Stock shortages
- Overstock situations
- Seasonal demand fluctuations
- Inefficient inventory allocation
- Poor inventory visibility
- Holiday stock planning
- Department-wise inventory optimization
""")

    st.markdown("---")

    # =====================================================
    # TECHNOLOGIES
    # =====================================================

    st.markdown("## 🛠 Technologies Used")

    st.markdown("""
**Programming Language** : Python

**Framework** : Streamlit

**Libraries**

- Pandas
- NumPy
- Plotly Express
- Plotly Graph Objects

**Development Tools**

- VS Code
- GitHub

**Dataset**

- Walmart Sales Dataset From Kaggle (https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)
""")

    st.markdown("---")

    # =====================================================
    # BUSINESS VALUE
    # =====================================================

    st.markdown("## 📈 Business Value")

    st.markdown("""
The dashboard enables management to:

- Improve inventory planning
- Reduce stockouts
- Minimize overstock costs
- Increase customer satisfaction
- Optimize department performance
- Improve sales through better inventory allocation
- Support strategic business decisions using data
""")

    st.markdown("---")

    # =====================================================
    # FUTURE ENHANCEMENTS
    # =====================================================

    st.markdown("## 🔮 Future Enhancements")

    st.markdown("""
- AI-based demand prediction
- Real-time inventory monitoring
- Supplier performance analysis
- Automated inventory alerts
- Product-level inventory tracking
- Warehouse optimization
- Customer purchasing pattern analysis
- Mobile dashboard support
""")

    st.markdown("---")

    st.success("✅ Developed by Divya S as an MCA Academic Major Project at Acharya Institute of Technology (2025).")