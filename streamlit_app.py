import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the app
st.title("Relationship Between GDP per Capita and Average IQ by Country")

# Add a brief description
st.markdown("""
This app visualizes the relationship between a country's GDP per capita and its average IQ. 
Use the sidebar to filter data and explore the correlation.
""")

# Sample data
# In a real-world scenario, you should replace this with actual data.
# You can load data from a CSV file or an API.
sample_data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom',
                'Canada', 'France', 'India', 'Brazil', 'South Korea'],
    'GDP_per_Capita': [63000, 10000, 40000, 45000, 42000, 46000, 39000, 2000, 9000, 35000],
    'Average_IQ': [98, 105, 105, 102, 100, 99, 98, 82, 87, 106],
    'Region': ['North America', 'Asia', 'Asia', 'Europe', 'Europe',
               'North America', 'Europe', 'Asia', 'South America', 'Asia']
}

# Convert the sample data into a DataFrame
df = pd.DataFrame(sample_data)

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# Option to upload your own data
uploaded_file = st.sidebar.file_uploader("Upload your CSV data", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        user_df = pd.read_csv(uploaded_file)
        # Check if necessary columns exist
        if {'Country', 'GDP_per_Capita', 'Average_IQ'}.issubset(user_df.columns):
            df = user_df
            st.success("Data successfully loaded!")
        else:
            st.error("CSV file must contain 'Country', 'GDP_per_Capita', and 'Average_IQ' columns.")
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Filter by region if the 'Region' column exists
if 'Region' in df.columns:
    regions = df['Region'].unique().tolist()
    selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
    df = df[df['Region'].isin(selected_regions)]

# Slider to filter GDP per capita
min_gdp = int(df['GDP_per_Capita'].min())
max_gdp = int(df['GDP_per_Capita'].max())
selected_gdp = st.sidebar.slider("GDP per Capita Range", min_gdp, max_gdp, (min_gdp, max_gdp))
df = df[(df['GDP_per_Capita'] >= selected_gdp[0]) & (df['GDP_per_Capita'] <= selected_gdp[1])]

# Slider to filter Average IQ
min_iq = int(df['Average_IQ'].min())
max_iq = int(df['Average_IQ'].max())
selected_iq = st.sidebar.slider("Average IQ Range", min_iq, max_iq, (min_iq, max_iq))
df = df[(df['Average_IQ'] >= selected_iq[0]) & (df['Average_IQ'] <= selected_iq[1])]

# Display the filtered data
st.subheader("Filtered Data")
st.dataframe(df)

# Create a scatter plot
fig = px.scatter(
    df, 
    x="GDP_per_Capita", 
    y="Average_IQ",
    size="GDP_per_Capita",
    color="Region" if 'Region' in df.columns else None,
    hover_name="Country",
    trendline="ols",
    title="GDP per Capita vs. Average IQ",
    labels={
        "GDP_per_Capita": "GDP per Capita (USD)",
        "Average_IQ": "Average IQ"
    }
)

st.plotly_chart(fig, use_container_width=True)

# Display correlation coefficient
if df.shape[0] > 1:
    correlation = df['GDP_per_Capita'].corr(df['Average_IQ'])
    st.markdown(f"**Correlation between GDP per Capita and Average IQ:** {correlation:.2f}")
else:
    st.markdown("Not enough data points to calculate correlation.")

# Footer
st.markdown("""
---
*Data Source: Replace with your actual data source.*
""")
