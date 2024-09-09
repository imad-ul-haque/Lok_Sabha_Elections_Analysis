
import matplotlib.pyplot as plt
import plotly.express as px
import sqlalchemy
import plotly.graph_objects as go
import seaborn as sns
import geopandas as gpd
import json
import folium
from folium import Choropleth, GeoJson  # Import GeoJson here
from streamlit_folium import st_folium
import requests
import plotly.graph_objects as go


import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
from PIL import Image
import base64 


# # Set Streamlit to wide mode by default
# st.set_page_config(layout="wide")

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Your other Streamlit code starts here
st.markdown(
    """
    <style>
    .gradient-text {
        font-size: 3em;  /* Adjust this to make the text bigger */
        background: -webkit-linear-gradient(left, #FF9933, #FFFFFF, #138808);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='gradient-text'>Lok Sabha Election Analysis</h1><br><br>", unsafe_allow_html=True)






gemini_api = "AIzaSyAlzvQ_9dUdj5z-AUjsYOM5uHP-XPUvKAQ"  # Replace this with your actual key

# Configure the Gemini model with the API key
genai.configure(api_key=gemini_api)



# Initialize Streamlit sidebar and input field


# Initialize the Generative Model
model = genai.GenerativeModel('gemini-1.5-pro')


if not gemini_api:
    st.sidebar.error("API key is not set. Please configure the GEMINI_API_KEY environment variable.")

# Initialize the Generative Model if API key is available
if gemini_api:
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.sidebar.error(f"Failed to initialize the model: {e}")
else:
    st.sidebar.error("API key is not set.")

# Use the sidebar for both input and output
with st.sidebar:
    st.title("Ask Anything Related to Indian Election")

    # Input box
    input_query = st.text_input("",placeholder="Write your query here:")

    # Display the response in the sidebar
    if input_query and gemini_api:
        try:
            # Prepare the full prompt for the model
            full_prompt = (
                f"Role: Act as a Conversational Assistant\n"
                f"Task: Answer the question '{input_query}' in a clear and concise manner. The response should be informative and include a relevant general assumption and minimal embellishment. Aim for a conversational tone, avoiding robotic language. Keep the response under 50 words.\n"
                f"Break down the response into points:\n"
                f"1. Start with a straightforward and accurate answer to the question.\n"
                f"2. Add a relevant general assumption or context if needed.\n"
                f"3. Include a touch of embellishment to make the response engaging, but avoid unnecessary details.\n"
                f"4. Ensure the response is natural and conversational, avoiding any robotic or overly formal language."
            )
            
             # Generate content using the model
            response = model.generate_content(full_prompt)
            
            # Display the response in the sidebar
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

# uploaded_file = st.file_uploader("Upload your dataset here (CSV)",type="csv")
# if uploaded_file is not None:
#         # Read the CSV file
#         df = pd.read_csv(uploaded_file)

#         # Display the data
#         with st.expander("Preview"):
#             st.write(df.head())

#         # Plot the data
#         user_input = st.text_input("Type your message here",placeholder="Ask me about your data")
#         if user_input:
#                 answer = generateResponse(dataFrame=df,prompt=user_input)
#                 st.write(answer)





# Database connection parameters
username = 'root'
password = 'test'
host = '127.0.0.1'
port = '3306'
database = 'Loksabha'

# Create the SQLAlchemy engine
engine = sqlalchemy.create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')



# Assuming 'engine' is your SQLAlchemy engine


query = "SELECT * FROM constituency"
# df1 = pd.read_sql(query, engine)
df1 = pd.read_csv('constituency.csv')



query = "select * FROM candidates"
# df2 = pd.read_sql(query, engine)
df2 = pd.read_csv('Candidates.csv')


query = "SELECT * FROM election"
# df3 = pd.read_sql(query, engine)
df3 = pd.read_csv('Election.csv')

gender_ratio = pd.read_csv('gender_rat.csv')





# Sidebar filters
st.sidebar.title("Filters")
years = st.sidebar.multiselect("Select Year(s)", df3['election_year'].unique(), default=[2019])
states = st.sidebar.multiselect("Select State(s)", df3['state'].unique(), default=['Gujarat'])

# Filter `pc_names` based on selected `states`
if states:
    filtered_df3 = df3[df3['state'].isin(states) & df3['election_year'].isin(years)]
    pc_names_options = filtered_df3['pc_name'].unique()
else:
    # If no state is selected, show all pc_names
    pc_names_options = df3['pc_name'].unique()

# Default to the last 10 `pc_names` if none are selected
default_pc_names = pc_names_options[-554:] if len(pc_names_options) > 10 else pc_names_options

# Sidebar multiselect for `pc_names`
pc_names = st.sidebar.multiselect("Select Constituency(ies)", pc_names_options, default=default_pc_names)



# Apply filters
filtered_df1 = df1[df1['election_year'].isin(years) & df1['pc_name'].isin(pc_names)]


filtered_df2 = df2[df2['election_year'].isin(years) & df2['pc_name'].isin(pc_names)]


# filtered_df3 = df3[df3['election_year'].isin(years) & df3['pc_name'].isin(pc_names) & df3['state'].isin(states)]
filtered_df3 = df3[df3['election_year'].isin(years)]


with st.sidebar:
        st.title("AI Data Analyst")
        st.write("Engage in insightful conversations with your data through powerful visualizations, empowering you to uncover valuable insights and make informed decisions effortlessly!")
        # Added a divider
        st.divider()
        # Add content to the sidebar/drawer
        with st.expander("Data Visualization"):
            st.write("Made with Gemini pro ")


        # st.write("<div>Developed by - <span style=\"color: cyan; font-size: 24px; font-weight: 600;\">Jaishree Yadav</span></div>",unsafe_allow_html=True)


# Define a function to format numbers
def format_number(num):
    """Format numbers into human-readable formats (K, M, B, L)."""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f} B"  # Billions
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f} M"  # Millions
    elif num >= 100_000:
        return f"{num / 100_000:.1f} L"  # Lakhs
    elif num >= 1_000:
        return f"{num / 1_000:.1f} K"  # Thousands
    else:
        return str(num)  # No formatting needed

# Calculate metrics
total_votes = round(filtered_df3['votes'].sum(), 2)
total_turnout = round(filtered_df3['turnout'].mean(), 2)
total_constituencies = filtered_df3['pc_name'].nunique()
total_candidates = filtered_df3['winning_candidate'].nunique()

# Format metrics
formatted_total_votes = format_number(total_votes)
formatted_total_turnout = format_number(total_turnout)
formatted_total_turnout = formatted_total_turnout + "%"
formatted_total_constituencies = format_number(total_constituencies)
formatted_total_candidates = format_number(total_candidates)

# Dashboard Layout


# st.markdown("<h1 style='text-align: center;'>Lok Sabha Election Analysis</h1><br><br>", unsafe_allow_html=True)
st.subheader("Election Metrics 🗳️")

# Election Metrics in a Single Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Votes", formatted_total_votes)
col2.metric("Total Turnout", formatted_total_turnout)
if 2019 in years or 2024 in years:
    col3.metric("Total Constituencies", "543")
else:
    col3.metric("Total Constituencies", formatted_total_constituencies)
    
col4.metric("Total Candidates", formatted_total_candidates)


# Election Dashboard
# st.markdown("<h1 style='text-align: center;'>Election Dashboard</h1>", unsafe_allow_html=True)
# st.subheader("Lok Sabha Election Analysis")

# Election Dashboard


st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("Election Analysis")

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Top Parties with Seats Won")


    # Group by party and count occurrences
    party_votes = filtered_df3['party'].value_counts()

    # Sort by votes in descending order
    sorted_party_votes = party_votes.sort_values(ascending=False)

    # Get the top 6 parties
    top_parties = sorted_party_votes.head(6)

    # Convert the index to a categorical type to preserve the order
    top_parties.index = pd.CategoricalIndex(top_parties.index, categories=top_parties.index, ordered=True)

    # Convert to DataFrame for Plotly
    top_parties_df = top_parties.reset_index()
    top_parties_df.columns = ['Party', 'Votes']

    # Create the bar chart using Plotly Express
    fig = px.bar(top_parties_df, x='Party', y='Votes', text='Votes')

    # Rotate the x-tick labels by -45 degrees
    fig.update_layout(
        xaxis_title='Party',
        yaxis_title='Seats Count',
        xaxis_tickangle=-45,        # Rotate the x-ticks
        height=550,                  
        yaxis=dict(range=[0, top_parties.max() * 1.2]),  # Set y-axis range slightly above the max value
        template='plotly_white'
    )

    # Automatically position data labels outside the bars
    fig.update_traces(textposition='outside')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

with col2:
    st.write("Candidates by Category")

    # Get the top 3 type categories
    top_type_category = filtered_df3["type_category"].value_counts().head(3).reset_index()
    top_type_category.columns = ['Type Category', 'Count']

    # Create the bar chart using Plotly Express
    fig_category = px.bar(top_type_category, x='Type Category', y='Count', text='Count')

    # Adjust layout to rotate x-ticks and increase the bar height
    fig_category.update_layout(
        xaxis_title='Type Category',
        yaxis_title='Number of Candidates',
        xaxis_tickangle=-45,         # Rotate the x-ticks by -45 degrees
        yaxis=dict(range=[0, top_type_category['Count'].max() * 1.1]),  # Slightly above max value
        height=480,                  # Set a custom height for the chart
        template='plotly_white'
    )

    # Position data labels outside the bars
    fig_category.update_traces(textposition='outside')

    # Display the plot in Streamlit
    st.plotly_chart(fig_category)

# Plotting the Male vs Female Turnout Ratio Over the Years
with col3:
    st.write("Genderwise Voter Turnout")

    # Sort the DataFrame by Year
    gender_ratio = gender_ratio.sort_values('Year')

    # Create Plotly figure
    fig_turnout = go.Figure()

    # Add Female Turnout line (labels below the line)
    fig_turnout.add_trace(go.Scatter(
        x=gender_ratio['Year'],
        y=gender_ratio['Female_Turnout'],
        mode='lines+markers+text',
        name='Female Turnout',
        line=dict(color='red'),
        marker=dict(symbol='circle'),
        text=gender_ratio['Female_Turnout'],   # Add data labels
        textposition="bottom center"           # Position labels below the markers
    ))

    # Add Male Turnout line (labels above the line)
    fig_turnout.add_trace(go.Scatter(
        x=gender_ratio['Year'],
        y=gender_ratio['Male_Turnout'],
        mode='lines+markers+text',
        name='Male Turnout',
        line=dict(color='blue'),
        marker=dict(symbol='square'),
        text=gender_ratio['Male_Turnout'],    # Add data labels
        textposition="top center"             # Position labels above the markers
    ))

    # Calculate min and max values
    min_y = min(gender_ratio[['Female_Turnout', 'Male_Turnout']].min() -2)
    max_y = max(gender_ratio[['Female_Turnout', 'Male_Turnout']].max())

    # Update layout
    fig_turnout.update_layout(
        xaxis_title='Year',
        yaxis_title='Turnout (%)',
        yaxis=dict(
            range=[min_y, max_y + (max_y - min_y) * 0.1]  # Set lower limit to min_y and upper limit slightly beyond max_y
        ),
        legend_title='Legend',
        legend=dict(
            orientation="h",  # Horizontal orientation for the legend
            yanchor="top",    # Anchor the legend to the top
            y=-0.2,           # Position the legend below the plot
            xanchor="center", # Center the legend horizontally
            x=0.5             # Center the legend horizontally
        ),
        margin=dict(t=50, b=100, l=50, r=50),  # Adjust margins to provide space for the legend
        template='plotly_white',
        height=500
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig_turnout)


st.markdown("<br><br>", unsafe_allow_html=True)






# Function to generate a dataframe-related response using Gemini
def generateDataframeResponse(dataFrame, prompt):
    df_summary = dataFrame.to_string()
    model = genai.GenerativeModel('gemini-1.5-pro')
    full_prompt = (
        f"Role: Act as PANDAS AI Model.\n"
        f"Task: Given the question '{prompt}', provide a clear ,concise response based on the data below ,in 70 words and write for further details click on analyze button\n"
        f"Dataframe summary: {df_summary}\n"
        f"Dont write these things - PANDAS AI model here"
    )
    response = model.generate_content(full_prompt)
    return response.text

# Function to generate a detailed analysis including general assumptions using Gemini
def generateDetailedAnalysis(dataFrame, prompt):
    df_summary = dataFrame.to_string()
    model = genai.GenerativeModel('gemini-1.5-pro')
    full_prompt = (
        f"Role: Act as an informed analyst.\n"
        f"Task: Given the question '{prompt}', provide a detailed analysis based on the data below and include general assumptions.respond in 150 words or less\n"
        f"Dataframe summary: {df_summary}\n"
        f"Break down the response into:\n"
        f"- State-wise analysis\n"
        f"- Party-wise analysis\n"
        f"- General context and assumptions related to the data\n"
        f"Avoid including irrelevant technical details and focus on what would be meaningful and understandable to a general audience."
    )
    response = model.generate_content(full_prompt)
    return response.text

# Function to generate a response using Gemini
def generateResponse(dataFrame, prompt):
    df_summary = dataFrame.to_string()
    model = genai.GenerativeModel('gemini-1.5-pro')
    full_prompt = (
        f"Role: Act as PANDAS AI Model.\n"
        f"Task: Given the question '{prompt}', provide a response based on the data below.clear ,concise response based on the data below ,in 70 words and write for further details click on analyze button\n"
        f"Dataframe summary: {df_summary}\n"
        f"Don't include irrelevant technical details."
    )
    response = model.generate_content(full_prompt)
    return response.text

# Function to analyze trends using Gemini
def analyzeTrends(dataFrame, input_query):
    try:
        summary = dataFrame.describe().to_string()
        model = genai.GenerativeModel('gemini-1.5-pro')
        full_prompt = (
            f"Role: Act as Analyst and social women.\n"
            f"Task: Analyze the trend in the following data and explain the possible real-world reasons behind these trends based on Indian election history:\n\n"
            f"{summary}\n\n"
            f"Question from user: {input_query}\n\n"
            f"Provide insights that consider typical patterns and historical context. Break down your explanation into:\n"
            f"- Analyze the dataframe and explain the trends\n"
            f"- Provide real-life scenarios related to India\n"
            f"Avoid including irrelevant technical details and focus on practical explanations that are understandable to a general audience."
        )
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"I can't answer that question. Error: {e}"


# Load and encode the image (teacher2.png) as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

teacher_image_base64 = get_image_as_base64("teacher2.png")

# Streamlit input boxes and image buttons
st.title("Ask Gyan")

# Create columns for inputs and buttons
col1, col2 = st.columns(2)


with col1:
    input1 = st.text_input("Ask Queries related to Top Parties with Seats Won ✨", placeholder="Ask me about your data")
    # Display the teacher image as a clickable button
    # st.markdown(
    #     f"""
    #     <style>
    #     .teacher-button {{
    #         cursor: pointer;
    #         display: inline-block;
    #         margin: 0px;
    #         position: relative;
    #         left: -25px;  /* Move the button 5px to the right */
    #     }}
    #     .teacher-image {{
    #         width: 150px;
    #         height: 150px;
    #         object-fit: contain;
    #     }}
    #     </style>
    #     <div class="teacher-button" onclick="document.getElementById('analyze-button-1').click()">
    #         <img src="data:image/png;base64,{teacher_image_base64}" class="teacher-image" alt="Click to analyze trends">
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    # Handle Enter key press for generating responses
    if input1:
        initial_response = generateDataframeResponse(dataFrame=top_parties_df, prompt=input1)
        st.write(initial_response)
    
    # Hidden button to be triggered by the image click
    if st.button("Analyze", key="analyze-button-1", help="Click the teacher image to analyze trends"):
        if input1:
            detailed_response = generateDetailedAnalysis(dataFrame=top_parties_df, prompt=input1)
            st.write(detailed_response)
        else:
            st.write("Please ask a query related to the data.")

with col2:
    input2 = st.text_input("Ask Queries related to Genderwise Voter Turnout ✨", placeholder="Write question here")
    # Display the teacher image as a clickable button
    # st.markdown(
    #     f"""
    #     <style>
    #     .teacher-button {{
    #         cursor: pointer;
    #         display: inline-block;
    #         margin: 0px;
    #         position: relative;
    #         left: -25px;  /* Move the button 5px to the right */
    #     }}
    #     .teacher-image {{
    #         width: 150px;
    #         height: 150px;
    #         object-fit: contain;
    #     }}
    #     </style>
    #     <div class="teacher-button" onclick="document.getElementById('analyze-button-2').click()">
    #         <img src="data:image/png;base64,{teacher_image_base64}" class="teacher-image" alt="Click to analyze trends">
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    if input2:
        answer = generateResponse(dataFrame=gender_ratio, prompt=input2)
        st.write(answer)

    # Hidden button to be triggered by the image click
    if st.button("Analyze", key="analyze-button-2", help="Click the teacher image to analyze trends"):
        if input2:
            trend_analysis = analyzeTrends(dataFrame=gender_ratio, input_query=input2)
            st.write(trend_analysis)
        else:
            st.write("Please ask a query related to the data.")


# Constituency Overview Metrics
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("Constituency Metrics")
col1, col2, col3, col4 = st.columns(4)

# Total votes polled
total_votes_polled = filtered_df1['votes_polled'].sum()
col1.metric("Total Votes Polled 📦", format_number(total_votes_polled))

# Number of constituencies
total_constituencies = filtered_df1['pc_name'].nunique()
col2.metric("Total Constituencies", format_number(total_constituencies))

# Total male electors
total_male_electors = filtered_df1['male_electors'].sum()
col3.metric("Total Male Electors", format_number(total_male_electors))

# Total female electors
total_female_electors = filtered_df1['female_electors'].sum()
col4.metric("Total Female Electors 🙎‍♀️", format_number(total_female_electors)," ")

# Constituency Overview Graphs and Map
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("Constituency Analysis")

# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    # st.write("Votes Polled by constituency")
    if not filtered_df1.empty:
        grouped_df1 = filtered_df1.groupby('pc_name')['votes_polled'].sum().reset_index()
        fig1 = px.bar(grouped_df1, x='pc_name', y='votes_polled', title='Votes Polled by constituency',height=500)
        fig1.update_xaxes(title_text='Constituency')
        st.plotly_chart(fig1)
    
    # st.write("Votes Polled by Constituency")
    # if not filtered_df1.empty:
    #     fig2 = px.line(filtered_df1.groupby('pc_name')['votes_polled'].sum(), title='Votes Polled by Constituency')
    #     st.plotly_chart(fig2)


    # Sidebar selection for pc_name

    pc_trend = df1[df1['pc_name'].isin(pc_names)]
    pc_names =pc_trend['pc_name'].unique()
    selected_pc_names = st.multiselect("Select constituency", options=pc_names, default=pc_names[:2])

    # Filter the DataFrame based on selected pc_name
    filtered_df = pc_trend[pc_trend['pc_name'].isin(selected_pc_names)]

    # Create the line plot
    fig = px.line(filtered_df, 
                x='election_year', 
                y='votes_polled_percentage', 
                color='pc_name', 
                markers=True, 
                title='Trend in Votes Polled by constituency',
                text='votes_polled_percentage',
                height=500)

    # Update layout to make it look more appealing in Streamlit
    fig.update_layout(legend_title_text='constituency',
                    xaxis_title='Election Year',
                    yaxis_title='Votes Polled Percentage (%)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title_font=dict(size=18)  # Increase the font size of the x-axis title
                    ),
                    yaxis=dict(
                        title_font=dict(size=18)  # Increase the font size of the y-axis title
                    ))  # Set transparent background
    
    # Update the text position to show labels above the markers
    fig.update_traces(textposition='top center')  # Position labels above the line

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

with col2:

    state_mapping = {
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Andhra Pradesh ": "Andhra Pradesh",  # Same in both
        "Arunachal Pradesh": "Arunachal Pradesh",  # Same in both
        "Assam": "Assam",  # Same in both
        "Bihar ": "Bihar",  # Same in both
        "Chandigarh": "Chandigarh",  # Same in both
        "Chhattisgarh": "Chhattisgarh",  # Same in both
        "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
        "Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi": "Delhi",  # Same in both
        "Goa": "Goa",  # Same in both
        "Gujarat": "Gujarat",  # Same in both
        "Haryana": "Haryana",  # Same in both
        "Himachal Pradesh": "Himachal Pradesh",  # Same in both
        "Jammu & Kashmir": "Jammu & Kashmir",  # Same in both
        "Jharkhand": "Jharkhand",  # Same in both
        "Karnataka": "Karnataka",  # Same in both
        "Kerala": "Kerala",  # Same in both
        "Ladakh": "Ladakh",  # Same in both
        "Lakshadweep": "Lakshadweep",  # Same in both
        "Madhya Pradesh ": "Madhya Pradesh",  # Same in both
        "Maharashtra": "Maharashtra",  # Same in both
        "Manipur": "Manipur",  # Same in both
        "Meghalaya": "Meghalaya",  # Same in both
        "Mizoram": "Mizoram",  # Same in both
        "Nagaland": "Nagaland",  # Same in both
        "Orissa": "Odisha",
        "Pondicherry": "Puducherry",
        "Punjab": "Punjab",  # Same in both
        "Rajasthan": "Rajasthan",  # Same in both
        "Sikkim": "Sikkim",  # Same in both
        "Tamil Nadu": "Tamil Nadu",  # Same in both
        "Telangana": "Telangana",  # Same in both
        "Tripura": "Tripura",  # Same in both
        "Uttar Pradesh ": "Uttar Pradesh",  # Same in both
        "Uttarakhand": "Uttarakhand",  # Same in both
        "West Bengal": "West Bengal"  # Same in both
    }

# Load GeoJSON data from a URL
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # Extract the state names from the GeoJSON file
    state_names_geojson = [feature['properties']['ST_NM'] for feature in geojson_data['features']]

    # Create a dropdown for selecting a party
    selected_party = st.selectbox('Select a Party:', filtered_df3['party'].unique())

    # Filter the data for the selected party
    filtered_data = filtered_df3[filtered_df3['party'] == selected_party]

    # Group the filtered data by state and count the number of seats
    agg_data = filtered_data.groupby('state')['party'].count().reset_index(name='seats')

    # Apply the mapping to the 'state' column
    agg_data['state'] = agg_data['state'].map(state_mapping)

    # Handle any states that might not match by dropping null values
    agg_data = agg_data.dropna(subset=['state'])

    # Ensure all states from GeoJSON are present in the data
    agg_data = pd.DataFrame({
        'state': state_names_geojson,
        'seats': [agg_data[agg_data['state'] == state]['seats'].sum() if state in agg_data['state'].values else 0 for state in state_names_geojson]
    })

       
        # Create the choropleth map
    fig = go.Figure(data=go.Choropleth(
        geojson=geojson_data,
        featureidkey='properties.ST_NM',
        locationmode='geojson-id',
        locations=agg_data['state'],
        z=agg_data['seats'],
        autocolorscale=False,
        colorscale='Reds',  # Color scale for the dark theme
        marker_line_color='peachpuff',  # Outline color for states
        colorbar=dict(
            title={'text': "Seats"},
            thickness=15,
            len=0.3,
            bgcolor='#0E1117',  # Dark background for the color bar
            tick0=0,
            dtick=5,  # Adjust based on your data range
            xanchor='right',  # Anchor the colorbar to the right side
            x=1.0,  # Position colorbar at the far right
            yanchor='middle',  # Anchor the colorbar to the middle vertically
            y=0.4,  # Position colorbar in the middle vertically
            titlefont=dict(color='white'),  # Set color of the color bar title
            tickfont=dict(color='white')    # Set color of the color bar ticks
        )
    ))
    
    fig.update_geos(
        visible=False,
        projection=dict(type='mercator'),
        lonaxis={'range': [68, 98]},  # Longitude range for India
        lataxis={'range': [6, 38]},   # Latitude range for India
        showland=True,
        landcolor='white',
        showcountries=True,
        countrycolor='black',
        showocean=True,
        oceancolor='lightblue'
    )
    
    fig.update_layout(
        title=dict(
            text=f"{selected_party} Seats In Lok Sabha Election",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=900,
        width=750,  # Adjust width as needed
        template='plotly_dark',  # Apply dark theme
        paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        plot_bgcolor='rgba(0,0,0,0)',   # Make the plot background transparent
        geo=dict(
            visible=False,  # Hide the geo axes
            showcoastlines=False,
            showland=False,
            showocean=False,
            showcountries=False,
            showlakes=False
        ),
        dragmode=False,  # Disable dragging
        uirevision='constant',  # Disable user interface revisions
    )

    # Display the map in Streamlit
    st.plotly_chart(fig, use_container_width=True)






# Candidates Dashboard
st.subheader("Party by Constituency")

col1, col2 = st.columns(2)

with col1:
    constituency = st.selectbox(
        'Select Constituency:', 
        filtered_df2['pc_name'].unique(),
        index=0,  # Automatically select the first option
        key='selectbox_col1'
    )

    # Filter the dataframe based on the selected constituency
    party_wise = filtered_df2[filtered_df2['pc_name'] == constituency]

    # Group by 'Party' and calculate the average 'Votes_Percentage'
    party_votes_pct = party_wise.groupby('Party')['Votes_Percentage'].mean().reset_index()

    # Sort by Votes Percentage in descending order
    party_votes_pct = party_votes_pct.sort_values(by='Votes_Percentage', ascending=False)

    # Separate the top 3 parties and the rest
    top_parties = party_votes_pct.head(3)
    others = party_votes_pct.iloc[3:]

    # Combine others into a single row
    others_sum = pd.DataFrame({
        'Party': ['Others'],
        'Votes_Percentage': [others['Votes_Percentage'].sum()]
    })

    # Concatenate top parties with others
    final_data = pd.concat([top_parties, others_sum])

    # Define an orange color palette
        # Define a color palette with only the first color being orange
    custom_colors = ['#de7703', '#017a38', '#1ce2fc', '#c41cfc', '#DA70D6', '#87CEEB', '#32CD32', '#FFD700']

    
    # Create the pie chart with the custom color palette
    fig_pie = px.pie(
        final_data, 
        names='Party', 
        values='Votes_Percentage', 
        title='Votes Percentage by Party',
        labels={'Party': 'Party', 'Votes_Percentage': 'Votes Percentage'},
        color_discrete_sequence=custom_colors  # Apply the custom palette here
    )
    
    # Update traces to show percentage values inside the pie slices
    fig_pie.update_traces(
        textinfo='percent',
        hoverinfo='label+percent+value',
        textposition='inside',
        texttemplate='%{value:.2f}%',
        textfont=dict(color='white')  # Set text color to white
    )
    
    # Update layout for better readability
    fig_pie.update_layout(
        title='Votes Percentage by Party',
        legend_title='Party',
        margin=dict(t=50, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    
    # Display the pie chart in Streamlit
    st.plotly_chart(fig_pie)

with col2:
    constituency = st.selectbox(
        'Select Constituency:', 
        filtered_df2['pc_name'].unique(),
        index=0,  # Automatically select the first option
        key='selectbox_col2'
    )

    # Filter the dataframe based on the selected constituency
    df = filtered_df2[filtered_df2['pc_name'] == constituency]

    # Sort the dataframe in decreasing order of votes
    df = df.sort_values(by='Votes', ascending=False)

    # Create a horizontal bar graph with the 'inferno' color palette and custom data labels
    fig = px.bar(
        df,
        y='Candidate_Name',  # Use 'y' for horizontal bars
        x='Votes',
        color='Votes',
        color_continuous_scale='inferno',  # Use the inferno color palette
        title=f'Votes Distribution by Candidate for {constituency}',
        labels={'Votes': 'Number of Votes', 'Candidate_Name': 'Candidate'},
        orientation='h',
        text='Votes'  # Use the 'Votes' column for the text labels
    )
    
    # Customize the layout, including data labels and positioning outside the bars
    fig.update_traces(
        texttemplate='%{x:.2f}',  # Show 'Votes' with 2 decimal places
        textposition='outside'  # Position the text labels outside the bars
    )
    
    # Customize the overall graph layout (remove color axis and add data labels)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=24, color='white', family="Arial"),
        font=dict(color='black', size=22, family="Arial"),
        margin=dict(l=150, r=10, t=70, b=50),  # Adjust margins for better readability
        coloraxis_showscale=False,  # Remove the color legend/scale
        yaxis=dict(
            autorange='reversed'  # Ensure that larger values are at the top
        )
    )

    # Display only the top 2-3 bars initially
    top_n = 3
    top_df = df.head(top_n)  # Get the top N rows
    top_df = top_df.sort_values(by='Votes',ascending = True)

    st.write("### Top Candidates")
    st.plotly_chart(px.bar(
        top_df,
        y='Candidate_Name',  # Use 'y' for horizontal bars
        x='Votes',
        color='Votes',
        color_continuous_scale='inferno',
        title=f'Top {top_n} Candidates for {constituency}',
        labels={'Votes': 'Number of Votes', 'Candidate_Name': 'Candidate'},
        orientation='h'
    ).update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=24, color='white', family="Arial"),
        font=dict(color='black', size=22, family="Arial"),
        margin=dict(l=150, r=10, t=70, b=50)
    ))

    # Expandable section for remaining bars
    with st.expander("Show More"):
        st.plotly_chart(fig)

    # # Expandable section for remaining bars
    # with st.expander("Show More"):
    #     st.plotly_chart(fig)


# Display the complete dashboard
st.markdown("---")

# Provide additional information and credits
st.sidebar.info("Data sourced from provided datasets.")
