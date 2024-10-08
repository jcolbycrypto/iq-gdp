import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the app
st.title("Relationship Between GDP per Capita and Average IQ by Country")

# Add a brief description
st.markdown("""
This app visualizes the relationship between a country's GDP per capita (for a specific year or an average over years) and its average IQ.
Use the sidebar to filter data and explore the correlation.
""")

# Sidebar for file uploads
st.sidebar.header("Upload Data Files")

# Upload GDP data file
gdp_file = st.sidebar.file_uploader("Upload GDP per Capita CSV", type=["csv"])
# Upload IQ data file
iq_file = st.sidebar.file_uploader("Upload Average IQ CSV", type=["csv"])

if gdp_file is not None and iq_file is not None:
    try:
        # Read the uploaded GDP and IQ CSV files
        gdp_data = pd.read_csv(gdp_file)
        iq_data = pd.read_csv(iq_file)
        st.success("Data successfully loaded!")
        
        # Display a preview of the GDP data
        st.subheader("GDP Data Preview")
        st.dataframe(gdp_data.head())
        
        # Display a preview of the IQ data
        st.subheader("IQ Data Preview")
        st.dataframe(iq_data.head())

        # Extract year columns from GDP data
        year_columns = [col for col in gdp_data.columns if col.isdigit()]
        st.sidebar.subheader("Select Year or Aggregate")

        # Option to select a specific year or take an average
        selected_year = st.sidebar.selectbox("Select a Year", year_columns)
        aggregate = st.sidebar.checkbox("Use Average GDP over all years", value=False)

        if aggregate:
            gdp_data['GDP_per_Capita'] = gdp_data[year_columns].mean(axis=1)  # Calculate average GDP across years
        else:
            gdp_data['GDP_per_Capita'] = gdp_data[selected_year]  # Select GDP for the specific year

        # Merge GDP and IQ data on Country
        merged_data = pd.merge(gdp_data[['Country', 'GDP_per_Capita']], iq_data, on='Country')

        # Check if necessary columns exist
        if 'GDP_per_Capita' in merged_data.columns and 'Average_IQ' in merged_data.columns:
            # Slider to filter GDP per capita
            min_gdp = int(merged_data['GDP_per_Capita'].min())
            max_gdp = int(merged_data['GDP_per_Capita'].max())
            selected_gdp = st.sidebar.slider("GDP per Capita Range", min_gdp, max_gdp, (min_gdp, max_gdp))
            filtered_data = merged_data[(merged_data['GDP_per_Capita'] >= selected_gdp[0]) & (merged_data['GDP_per_Capita'] <= selected_gdp[1])]
        
            # Slider to filter Average IQ
            min_iq = int(filtered_data['Average_IQ'].min())
            max_iq = int(filtered_data['Average_IQ'].max())
            selected_iq = st.sidebar.slider("Average IQ Range", min_iq, max_iq, (min_iq, max_iq))
            filtered_data = filtered_data[(filtered_data['Average_IQ'] >= selected_iq[0]) & (filtered_data['Average_IQ'] <= selected_iq[1])]

            # Display the filtered data
            st.subheader("Filtered Data")
            st.dataframe(filtered_data)

            # Create a scatter plot
            fig = px.scatter(
                filtered_data, 
                x="GDP_per_Capita", 
                y="Average_IQ",
                size="GDP_per_Capita",
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
            if filtered_data.shape[0] > 1:
                correlation = filtered_data['GDP_per_Capita'].corr(filtered_data['Average_IQ'])
                st.markdown(f"**Correlation between GDP per Capita and Average IQ:** {correlation:.2f}")
            else:
                st.markdown("Not enough data points to calculate correlation.")

        else:
            st.error("Merged data is missing required columns.")
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.info("Please upload both GDP and IQ CSV files to begin.")

# Footer
st.markdown("""
---
*Data Source: Custom CSV Upload*
""")
