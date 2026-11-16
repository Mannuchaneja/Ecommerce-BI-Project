
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="🛒",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent.parent / "reports"

st.title("🛒 E-Commerce Business Intelligence")
st.write("Interactive Data Analysis Dashboard")
st.divider()

# Load CSV files
@st.cache_data
def load_data():
    products = pd.read_csv(DATA_DIR / "Product.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    return products, customers, orders

try:
    products, customers, orders = load_data()

    st.success("All datasets loaded successfully!")

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(products))
    col2.metric("Total Customers", len(customers))
    col3.metric("Total Orders", len(orders))

    st.divider()

    # Dataset selection
    st.subheader("📊 Explore Your Data")

    choice = st.selectbox(
        "Select Dataset",
        ["Orders", "Products", "Customers"]
    )

    if choice == "Orders":
        df = orders
    elif choice == "Products":
        df = products
    else:
        df = customers

    st.write("### Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.write("### Dataset Information")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    # Numeric analysis
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        st.divider()
        st.subheader("📈 Numerical Analysis")

        selected_column = st.selectbox(
            "Choose a numeric column",
            numeric_columns
        )

        fig, ax = plt.subplots()
        df[selected_column].dropna().hist(
            bins=15, ax=ax
        )
        ax.set_title("Distribution of " + selected_column)
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")

        st.pyplot(fig)
        plt.close(fig)

    # Categorical analysis
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical_columns:
        st.divider()
        st.subheader("📊 Category Analysis")

        category = st.selectbox(
            "Choose a category",
            categorical_columns
        )

        counts = df[category].value_counts().head(10)

        st.bar_chart(counts)

    # Download data
    st.divider()
    st.subheader("⬇️ Download Data")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Selected Dataset",
        data=csv_data,
        file_name="ecommerce_report.csv",
        mime="text/csv"
    )

except FileNotFoundError as error:
    st.error("CSV file not found: " + str(error))
    st.info("Check that all three CSV files are inside the reports folder.")

except Exception as error:
    st.error("Error: " + str(error))
