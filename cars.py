import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="🚗 Car Price Visualizer", layout="wide")

# Custom CSS styling for cleaner visuals
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown("<h1 class='title'>🚘 Car Price Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Use the sidebar to explore cars by brand and see average pricing distributions.")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("CARS.csv")
    df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')
    df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('int64')
    df.dropna(subset=["Make", "DriveTrain", "MSRP", "Invoice"], inplace=True)
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

# Sidebar options
st.sidebar.header("🔧 Filters")
brand = st.sidebar.selectbox("Select a Car Brand", sorted(df.Make.unique()))

# Filtered data
brd = df[df.Make == brand]

# Section: Brand Table
st.markdown(f"### 🔍 Data for Brand: `{brand}`")
st.dataframe(brd, use_container_width=True)

# Section: Invoice by Category
st.markdown("### 💵 Average Invoice Price by Car Category")
fig1, ax1 = plt.subplots(figsize=(8, 5))
sb.barplot(data=df, x="category", y="Invoice", ax=ax1, palette="Blues_d")
ax1.set_title("Invoice by Price Category")
ax1.set_xlabel("Price Category")
ax1.set_ylabel("Average Invoice")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)

# Section: MSRP by DriveTrain
st.markdown("### ⚙️ Average MSRP by Drive Train")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sb.barplot(data=df, x="DriveTrain", y="MSRP", ax=ax2, palette="Greens_d")
ax2.set_title("MSRP by Drive Train")
ax2.set_xlabel("Drive Train")
ax2.set_ylabel("Average MSRP")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# Bonus: Brand-specific plot (optional)
st.markdown(f"### 📊 {brand} — Invoice by Category")
fig3, ax3 = plt.subplots(figsize=(8, 5))
sb.barplot(data=brd, x="category", y="Invoice", ax=ax3, palette="Purples_d")
ax3.set_title(f"{brand} - Invoice Price by Category")
ax3.set_xlabel("Category")
ax3.set_ylabel("Average Invoice")
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
st.pyplot(fig3)

# Download filtered brand data
st.markdown("### 📥 Download Selected Brand Data")
st.download_button(
    label="Download Brand Data as CSV",
    data=brd.to_csv(index=False),
    file_name=f"{brand}_cars.csv",
    mime="text/csv",
)
