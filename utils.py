import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    # Load datasets
    pd.read_csv("train.csv")
    pd.read_csv("stores.csv")
    pd.read_csv("features.csv")

    # Convert dates
    train["Date"] = pd.to_datetime(train["Date"])
    features["Date"] = pd.to_datetime(features["Date"])

    # Merge datasets
    df = train.merge(stores, on="Store", how="left")

    df = df.merge(
        features,
        on=["Store", "Date", "IsHoliday"],
        how="left"
    )

    # Handle missing values
    markdown_cols = [
        "MarkDown1",
        "MarkDown2",
        "MarkDown3",
        "MarkDown4",
        "MarkDown5"
    ]

    for col in markdown_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    if "CPI" in df.columns:
        df["CPI"] = df["CPI"].fillna(df["CPI"].median())

    if "Unemployment" in df.columns:
        df["Unemployment"] = df["Unemployment"].fillna(df["Unemployment"].median())

    if "Fuel_Price" in df.columns:
        df["Fuel_Price"] = df["Fuel_Price"].fillna(df["Fuel_Price"].median())

    if "Temperature" in df.columns:
        df["Temperature"] = df["Temperature"].fillna(df["Temperature"].median())

    # Remove duplicates
    df = df.drop_duplicates()

    # Create useful columns
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    df["Quarter"] = df["Date"].dt.quarter
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Day"] = df["Date"].dt.day_name()

    return df
