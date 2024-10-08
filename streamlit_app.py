import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Set the title of the app
st.title("Relationship Between GDP per Capita and Average IQ by Country")

# Add a brief description
st.markdown("""
This app visualizes the relationship between a country's GDP per capita and its average IQ. 
Use the sidebar to filter data and explore the correlation.
""")

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# API call to get real GDP per capita data from IMF DataMapper
@st.cache_data
def get_gdp_data():
    # URL for GDP per capita data from the IMF API
    url = "https://api.imf.org/datamapper/NGDPDPC@WEO/OEMDC/ADVEC/WEOWORLD"
    
    # Make the request to the IMF API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant data from the JSON
        gdp_data = []
        for country, gdp in data['data'].items():
            gdp_data.append({
                'Country': country,
                'GDP_per_Capita': gdp['value']
            })
        
        return pd.DataFrame(gdp_data)
    else:
        st.error(f"Error fetching GDP data: {response.status_code}")
        return pd.DataFrame()

# Call the function to get GDP data
gdp_df = get_gdp_data()

# Sample IQ data (replace with real data as needed)
sample_iq_data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom',
                'Canada', 'France', 'India', 'Brazil', 'South Korea'],
    'Average_IQ': [98, 105, 105, 102, 100, 99, 98, 82, 87, 106],
    'Region': ['North America', 'Asia', 'Asia', 'Europe', 'Europe',
               'North America', 'Europe', 'Asia', 'South America', 'Asia']
}

# Convert the IQ data into a DataFrame
iq_df = pd.DataFrame(sample_iq_data)

# Merge GDP data and IQ data
merged_df = pd.merge(iq_df, gdp_df, on='Country', how='inner')

# Filter by region if the 'Region' column exists
regions = merged_df['Region'].unique().tolist()
selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
filtered_df = merged_df[merged_df['Region'].isin(selected_regions)]

# Slider to filter GDP per capita
min_gdp = int(filtered_df['GDP_per_Capita'].min())
max_gdp = int(filtered_df['GDP_per_Capita'].max())
selected_gdp = st.sidebar.slider("GDP per Capita Range", min_gdp, max_gdp, (min_gdp, max_gdp))
filtered_df = filtered_df[(filtered_df['GDP_per_Capita'] >= selected_gdp[0]) & (filtered_df['GDP_per_Capita'] <= selected_gdp[1])]

# Slider to filter Average IQ
min_iq = int(filtered_df['Average_IQ'].min())
max_iq = int(filtered_df['Average_IQ'].max())
selected_iq = st.sidebar.slider("Average IQ Range", min_iq, max_iq, (min_iq, max_iq))
filtered_df = filtered_df[(filtered_df['Average_IQ'] >= selected_iq[0]) & (filtered_df['Average_IQ'] <= selected_iq[1])]

# Display the filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Create a scatter plot
fig = px.scatter(
    filtered_df, 
    x="GDP_per_Capita", 
    y="Average_IQ",
    size="GDP_per_Capita",
    color="Region",
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
if filtered_df.shape[0] > 1:
    correlation = filtered_df['GDP_per_Capita'].corr(filtered_df['Average_IQ'])
    st.markdown(f"**Correlation between GDP per Capita and Average IQ:** {correlation:.2f}")
else:
    st.markdown("Not enough data points to calculate correlation.")

# Footer
st.markdown("""
---
*Data Source: IMF DataMapper and custom Average IQ dataset.*
""")
