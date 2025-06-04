import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="Car Price Visualizer", layout="wide")

# Title of the app
st.title("Car Price Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')
    df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('int64')
    return df

df = load_data()

# Categorize prices
def price(x):
    if 10000 <= x <= 22000:
        return "Low Budget"
    elif 22000 < x <= 40000:
        return "Mid Budget"
    elif 40000 < x <= 60000:
        return "High Budget"
    else:
        return "Luxury"

df["category"] = df.MSRP.apply(price)

# Sidebar for brand selection
brand = st.sidebar.selectbox("Select a Car Brand", sorted(df.Make.unique()))

# Filtered DataFrame for the selected brand
brd = df[df.Make == brand]

# Display brand data
st.subheader(f"Showing data for: {brand}")
st.dataframe(brd)

# Plot 1: Category vs Invoice
st.subheader("Average Invoice by Price Category")
fig1, ax1 = plt.subplots()
sb.barplot(data=df, x="category", y="Invoice", ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)

# Plot 2: DriveTrain vs MSRP
st.subheader("Average MSRP by Drive Train")
fig2, ax2 = plt.subplots()
sb.barplot(data=df, x="DriveTrain", y="MSRP", ax=ax2)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)
