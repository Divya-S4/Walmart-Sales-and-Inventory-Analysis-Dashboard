import streamlit as st
from PIL import Image

from sales_analysis import sales_analysis

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="Walmart Sales and Inventory Analysis Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ------------------------------------
# Load Image
# ------------------------------------
image = Image.open("Walmart.png")
# ------------------------------------
# Home Page
# ------------------------------------
def home():

    col1, col2 = st.columns([1, 2])

    with col1:
        
        st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)   # Moves image down
        st.image(image, use_container_width=True)

    with col2:
        st.title("🛒 Welcome to the Walmart Sales Analysis Dashboard")

        st.write(
            "Your one-stop platform for exploring Walmart sales performance, "
            "identifying business trends, and forecasting future sales."
        )

        st.markdown("---")

        st.subheader("What will you explore?")

        st.markdown("""
1. Detailed Sales Analysis
2. Store Performance Analysis
3. Department Performance
4. Monthly Sales Trends
5. Holiday Impact Analysis
6. Inventory & Stock Analysis
7. Business Insights
        """)

# ------------------------------------
# Sidebar Navigation
# ------------------------------------
st.sidebar.title("🛒 Walmart Dashboard")

page = st.sidebar.radio(
    
    [
        "🏠 Home",
        "📊 Sales Analysis",
        "📦 Stock Analysis",
        "ℹ️ About"
    ]
)

# ------------------------------------
# Page Routing
# ------------------------------------
if page == "🏠 Home":
    home()

elif page == "📊 Sales Analysis":
    sales_analysis()

elif page == "📦 Stock Analysis":
    from stock_analysis import stock_analysis
    stock_analysis()

elif page == "ℹ️ About":
    from About import about
    about()
