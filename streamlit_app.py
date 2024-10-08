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

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# Option to upload your Excel data
uploaded_file = st.sidebar.file_uploader("Upload your Excel file (GDP per Capita data)", type=["xlsx"])

# Define a function to load Excel data
def load_excel(file):
    try:
        # Load the data from the first sheet
        df = pd.read_excel(file, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None

# If an Excel file is uploaded, load the data
if uploaded_file is not None:
    df_gdp = load_excel(uploaded_file)
    
    # Check if the necessary columns are in the Excel file
    if df_gdp is not None:
        st.success("GDP per Capita data successfully loaded!")
        st.write("Here's a preview of your data:")
        st.dataframe(df_gdp.head())

        # You can now perform further operations on df_gdp, such as filtering and joining with IQ data
    else:
        st.error("Please upload a valid Excel file with 'Country' and 'GDP per Capita' columns.")

# Sample IQ data (to be replaced with real IQ data)
sample_iq_data = {
    'Country': ['United States', 'China', 'Japan', 'Germany', 'United Kingdom',
                'Canada', 'France', 'India', 'Brazil', 'South Korea'],
    'Average_IQ': [98, 105, 105, 102, 100, 99, 98, 82, 87, 106]
}

# Convert the sample IQ data into a DataFrame
df_iq = pd.DataFrame(sample_iq_data)

# If the GDP data has been uploaded, we try to merge it with the IQ data
if uploaded_file is not None and df_gdp is not None:
    try:
        # Ensure both datasets have the 'Country' column to merge on
        merged_df = pd.merge(df_gdp, df_iq, on='Country', how='inner')
        st.subheader("Merged Data (GDP per Capita and Average IQ)")
        st.dataframe(merged_df)

        # Create the scatter plot
        fig = px.scatter(
            merged_df, 
            x="GDP_per_Capita", 
            y="Average_IQ",
            hover_name="Country",
            title="GDP per Capita vs. Average IQ",
            labels={
                "GDP_per_Capita": "GDP per Capita (USD)",
                "Average_IQ": "Average IQ"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error merging data: {e}")

# Footer
st.markdown("""
---
*Data Source: IMF's World Economic Outlook Database.*
""")
