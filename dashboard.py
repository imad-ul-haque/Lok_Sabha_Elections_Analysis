import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
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
df1 = pd.read_sql(query, engine)



query = "select * FROM candidates"
# df2 = pd.read_sql(query, engine)
df2 = pd.read_csv('Candidates.csv')


query = "SELECT * FROM election"
df3 = pd.read_sql(query, engine)

gender_ratio = pd.read_csv('gender_rat.csv')


# Sidebar filters
st.sidebar.title("Filters")
years = st.sidebar.multiselect("Select Year(s)", df3['election_year'].unique(), default=[1980,2014, 2019, 2024])
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
st.title("Election Dashboard")

# Election Metrics in a Single Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Votes", formatted_total_votes)
col2.metric("Total Turnout", formatted_total_turnout)
col3.metric("Total Constituencies", formatted_total_constituencies)
col4.metric("Total Candidates", formatted_total_candidates)


# Election Dashboard
st.subheader("Election Overview")
st.markdown("### Graphs")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Party-wise Votes")

    # Group by party and count occurrences
    party_votes = filtered_df3['party'].value_counts()

    # Sort by votes in descending order
    sorted_party_votes = party_votes.sort_values(ascending=False)

    # Get the top 5 parties
    top_parties = sorted_party_votes.head(8)

    # Calculate the votes for 'Others'
    other_votes = sorted_party_votes.iloc[8:].sum()  # Start from index 5 for 'Others'

    # Create a Series for 'Others'
    others_series = pd.Series({'Others': other_votes})

    # Concatenate top parties and 'Others'
    final_party_votes = pd.concat([top_parties, others_series])

    # Ensure final_party_votes is sorted in descending order
    final_party_votes = final_party_votes.sort_values(ascending=False)

    # Convert the index to a categorical type to preserve the order
    final_party_votes.index = pd.CategoricalIndex(final_party_votes.index, categories=final_party_votes.index, ordered=True)

    # Plot the bar chart
    st.bar_chart(final_party_votes)
  

with col2:
    st.write("Gender Distribution")
    # state_turnout = df3.groupby('state')['turnout'].mean()
    # st.line_chart(state_turnout)

    # Get the top 5 type categories
    top_type_category = filtered_df3["type_category"].value_counts().head(3).reset_index()
    top_type_category.columns = ['Type Category', 'Count']

    # To use st.bar_chart, the DataFrame needs to be in a specific format
    # Transpose the DataFrame so that 'Type Category' becomes index and 'Count' is used for plotting
    top_type_category.set_index('Type Category', inplace=True)

    # Create the bar chart
    st.bar_chart(top_type_category)

with col3:
    st.write("Male vs Female Turnout Ratio Over the Years")

    # Sort the DataFrame by Year
    gender_ratio = gender_ratio.sort_values('Year')

    # Create Plotly figure
    fig = go.Figure()

    # Add Female Turnout line
    fig.add_trace(go.Scatter(
        x=gender_ratio['Year'],
        y=gender_ratio['Female_Turnout'],
        mode='lines+markers',
        name='Female Turnout',
        line=dict(color='blue'),
        marker=dict(symbol='circle')
    ))

    # Add Male Turnout line
    fig.add_trace(go.Scatter(
        x=gender_ratio['Year'],
        y=gender_ratio['Male_Turnout'],
        mode='lines+markers',
        name='Male Turnout',
        line=dict(color='red'),
        marker=dict(symbol='square')
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Turnout (%)',
        legend_title='Legend',
        legend=dict(
            orientation="h",  # Horizontal orientation for the legend
            yanchor="top",    # Anchor the legend to the top
            y=-0.2,           # Position the legend below the plot
            xanchor="center", # Center the legend horizontally
            x=0.5            # Center the legend horizontally
        ),
        margin=dict(t=50, b=100, l=50, r=50),  # Adjust margins to provide space for the legend
        template='plotly_white'
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)
    


# Constituency Overview Metrics
st.subheader("Constituency Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

# Total votes polled
total_votes_polled = filtered_df1['votes_polled'].sum()
col1.metric("Total Votes Polled", format_number(total_votes_polled))

# Number of constituencies
total_constituencies = filtered_df1['pc_name'].nunique()
col2.metric("Total Constituencies", format_number(total_constituencies))

# Total male electors
total_male_electors = filtered_df1['male_electors'].sum()
col3.metric("Total Male Electors", format_number(total_male_electors))

# Total female electors
total_female_electors = filtered_df1['female_electors'].sum()
col4.metric("Total Female Electors", format_number(total_female_electors))

# Constituency Overview Graphs and Map
st.subheader("Constituency Overview")

# Layout with two columns
col1, col2 = st.columns([1, 1])

with col1:
    # st.write("Votes Polled by PC Name")
    if not filtered_df1.empty:
        grouped_df1 = filtered_df1.groupby('pc_name')['votes_polled'].sum().reset_index()
        fig1 = px.bar(grouped_df1, x='pc_name', y='votes_polled', title='Votes Polled by PC Name',height=500)
        st.plotly_chart(fig1)
    
    # st.write("Votes Polled by Constituency")
    # if not filtered_df1.empty:
    #     fig2 = px.line(filtered_df1.groupby('pc_name')['votes_polled'].sum(), title='Votes Polled by Constituency')
    #     st.plotly_chart(fig2)


    # Sidebar selection for pc_name

    pc_trend = df1[df1['pc_name'].isin(pc_names)]
    pc_names =pc_trend['pc_name'].unique()
    selected_pc_names = st.multiselect("Select PC Names", options=pc_names, default=pc_names[:2])

    # Filter the DataFrame based on selected pc_name
    filtered_df = pc_trend[pc_trend['pc_name'].isin(selected_pc_names)]

    # Create the line plot
    fig = px.line(filtered_df, 
                x='election_year', 
                y='votes_polled_percentage', 
                color='pc_name', 
                markers=True, 
                title='Trend in Votes Polled Percentage by PC Name Over the Years',
                height=500)

    # Update layout to make it look more appealing in Streamlit
    fig.update_layout(legend_title_text='PC Name',
                    xaxis_title='Election Year',
                    yaxis_title='Votes Polled Percentage (%)',
                    plot_bgcolor='rgba(0,0,0,0)')  # Set transparent background

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

    agg_data = filtered_df3.groupby('state').size().reset_index(name='seats')


    # Apply the mapping to the 'state' column
    agg_data['state'] = agg_data['state'].map(state_mapping)

    # Handle any states that might not match by dropping null values
    agg_data = agg_data.dropna(subset=['state'])



    # Load GeoJSON data from a URL
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)
    geojson_data = response.json()


    # Extract and print the state names from the GeoJSON
    state_names_geojson = [feature['properties']['ST_NM'] for feature in geojson_data['features']]
    # print("States in GeoJSON:", state_names_geojson)

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
        bgcolor='rgba(0,0,0,0.6)',  # Dark background for the color bar
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
        projection=dict(
            type='mercator'
        ),
        lonaxis={'range': [68, 98]},  # Longitude range for India
        lataxis={'range': [6, 38]}    # Latitude range for India
    )

    fig.update_layout(
        title=dict(
            text="Seats by State in India",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=1000,
        width=750,  # Adjust width as needed
        template='plotly_dark'  # Apply dark theme
    )

    # Display the map in Streamlit
    st.plotly_chart(fig, use_container_width=True)





# Candidates Dashboard
st.subheader("Candidates Overview")
st.markdown("### Graphs")
col1, col2 = st.columns(2)

with col1:
#     st.dataframe(filtered_df2)

        
    # Group by 'Party' and calculate the average 'Votes_Percentage'
    party_votes_pct = filtered_df2.groupby('Party')['Votes_Percentage'].mean().reset_index()

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

    # Create a pie chart
    fig_pie = px.pie(
        final_data, 
        names='Party', 
        values='Votes_Percentage', 
        title='Votes Percentage by Party',
        labels={'Party': 'Party', 'Votes_Percentage': 'Votes Percentage'}
    )

    # Update layout for better readability and display labels below
    fig_pie.update_layout(
        title='Votes Percentage by Party',
        legend_title='Party',
        margin=dict(t=50, b=0, l=0, r=0),  # Adjust margins for better fit
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)  # Place legend below
    )

    # Display the pie chart in Streamlit
    st.plotly_chart(fig_pie)


with col2:
    constituency = st.selectbox('Select Constituency:', filtered_df2['pc_name'].unique())

    # Filter the dataframe based on the selected constituency
    df = filtered_df2[filtered_df2['pc_name'] == constituency]

        # Create a treemap with a peach color palette
    fig = px.treemap(
        df,
        path=['position', 'Candidate_Name'],
        values='Votes',
        color='Votes',
        color_continuous_scale=[[0, '#FFE5B4'], [1, '#FF6347']],  # Peach to tomato gradient
        hover_data={'Votes': True},
        title=f'Votes Distribution by Position for {constituency}'
    )

    # Customize the treemap layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        title_font=dict(size=28, color='white', family="Arial"),  # Bigger title font, white color
        font=dict(color='black', size=22, family="Arial"),  # Bigger font, black color
        margin=dict(l=10, r=10, t=70, b=150),  # Adjust margins to give more space to the treemap
        coloraxis_colorbar=dict(
            orientation="h",  # Horizontal color bar (legend)
            yanchor="top",
            y=-0.3,  # Position below the treemap
            xanchor="center",
            x=0.5,
            tickfont=dict(color='white', size=16),  # Font size and color for ticks
            title=dict(text="Votes", side="bottom", font=dict(size=18, color="black"))  # Title below the color bar
        )
    )

    # Show labels inside the blocks with a better size
    fig.update_traces(
        textinfo="label+value",  # Show labels and values inside the blocks
        textfont=dict(size=20, color='black'),  # Larger font size for labels, black color
        marker=dict(
            line=dict(color='rgba(0,0,0,0)', width=0),  # Ensure no border color
            pad=dict(t=0, l=0, r=0, b=0)  # Increase padding for wider space
        )
    )

    # Display the treemap in Streamlit
    st.plotly_chart(fig)

# Display the complete dashboard
st.markdown("---")

# Provide additional information and credits
st.sidebar.info("Data sourced from provided datasets.")


