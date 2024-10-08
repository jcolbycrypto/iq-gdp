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

# Sidebar for file upload
st.sidebar.header("Upload Data Files")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload your CSV with GDP per Capita and Average IQ data", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)
        st.success("Data successfully loaded!")
        
        # Display a preview of the uploaded data
        st.write("Here's a preview of your data:")
        st.dataframe(data.head())

        # Extract year columns (assuming they are numerical)
        year_columns = [col for col in data.columns if col.isdigit()]
        st.sidebar.subheader("Select Year or Aggregate")

        # Option to select a specific year or take an average
        selected_year = st.sidebar.selectbox("Select a Year", year_columns)
        aggregate = st.sidebar.checkbox("Use Average GDP over all years", value=False)

        if aggregate:
            data['GDP_per_Capita'] = data[year_columns].mean(axis=1)  # Calculate average GDP across years
        else:
            data['GDP_per_Capita'] = data[selected_year]  # Select GDP for the specific year

        # Check if necessary columns exist
        if 'Country' in data.columns and 'GDP_per_Capita' in data.columns and 'Average_IQ' in data.columns and 'Region' in data.columns:
            # Slider to filter GDP per capita
            min_gdp = int(data['GDP_per_Capita'].min())
            max_gdp = int(data['GDP_per_Capita'].max())
            selected_gdp = st.sidebar.slider("GDP per Capita Range", min_gdp, max_gdp, (min_gdp, max_gdp))
            filtered_data = data[(data['GDP_per_Capita'] >= selected_gdp[0]) & (data['GDP_per_Capita'] <= selected_gdp[1])]
        
            # Slider to filter Average IQ
            min_iq = int(filtered_data['Average_IQ'].min())
            max_iq = int(filtered_data['Average_IQ'].max())
            selected_iq = st.sidebar.slider("Average IQ Range", min_iq, max_iq, (min_iq, max_iq))
            filtered_data = filtered_data[(filtered_data['Average_IQ'] >= selected_iq[0]) & (filtered_data['Average_IQ'] <= selected_iq[1])]

            # Filter by region
            regions = filtered_data['Region'].unique().tolist()
            selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
            filtered_data = filtered_data[filtered_data['Region'].isin(selected_regions)]
        
            # Display the filtered data
            st.subheader("Filtered Data")
            st.dataframe(filtered_data)

            # Create a scatter plot
            fig = px.scatter(
                filtered_data, 
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
            if filtered_data.shape[0] > 1:
                correlation = filtered_data['GDP_per_Capita'].corr(filtered_data['Average_IQ'])
                st.markdown(f"**Correlation between GDP per Capita and Average IQ:** {correlation:.2f}")
            else:
                st.markdown("Not enough data points to calculate correlation.")

        else:
            st.error("Please make sure your CSV contains the columns: 'Country', 'GDP_per_Capita', 'Average_IQ', and 'Region'.")
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.info("Please upload a CSV file to begin.")
    
# Footer
st.markdown("""
---
*Data Source: Custom CSV Upload*
""")
