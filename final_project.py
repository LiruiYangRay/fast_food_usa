"""
Name: Lirui Yang
CS230: Section 4
Data: Fast Food Restaurants in the USA
URL:

Description:

This program is a data visualization tool that explores fast food restaurants in the USA. It allows users to filter restaurants by city and category, view data summaries, and analyze trends through charts, tables, and maps. The app also includes advanced features like sorting, adding calculated columns, and combining city and province information for detailed insights.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

data_path = 'fast_food_usa.xlsx'
try:
    df = pd.read_excel(data_path, sheet_name='in', engine='openpyxl')
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

def filter_data(city="All", categories=None):
    filtered = df
    if city != "All":
        filtered = filtered[filtered['city'] == city]
    if categories:
        filtered = filtered[filtered['categories'].isin(categories)]
    return filtered

def calculate_summary(data):
    total_restaurants = len(data)
    unique_categories = data['categories'].nunique() if not data.empty else 0
    return total_restaurants, unique_categories

def province_distribution(data, top_n=10):
    province_counts = data['province'].value_counts()
    top_provinces = province_counts.head(top_n)
    others_count = province_counts[top_n:].sum()
    if others_count > 0:
        top_provinces["Others"] = others_count
    return top_provinces

st.title("Fast Food Restaurants in the USA")

st.sidebar.header("Filter Options")

cities = ["All"] + [city for city in df['city'].dropna().unique()]
selected_city = st.sidebar.selectbox("Select a City", options=cities)

categories = [cat for cat in df['categories'].dropna().unique()]
search_term = st.sidebar.text_input("Search Restaurant Category")
if search_term:
    filtered_categories = [cat for cat in categories if search_term.lower() in cat.lower()]
else:
    filtered_categories = categories
selected_category = st.sidebar.multiselect("Select Restaurant Type(s)", options=filtered_categories, default=filtered_categories)

if st.sidebar.button("Reset Filters"):
    selected_city = "All"
    selected_category = categories
    search_term = ""

filtered_df = filter_data(selected_city, selected_category)

st.header("Filtered Restaurants")
st.dataframe(filtered_df[['name', 'address', 'city', 'province', 'categories']])

st.subheader("Data Summary")
total, unique_cats = calculate_summary(filtered_df)
st.write("Total Restaurants:", total)
st.write("Unique Categories:", unique_cats)

st.subheader("Category Distribution")
if not filtered_df.empty:
    category_counts = filtered_df['categories'].value_counts().head(10)
    fig, ax = plt.subplots()
    category_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Top 10 Categories")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.write("No data available for the selected filters.")

st.subheader("Restaurants by Province")
if not filtered_df.empty:
    province_counts = province_distribution(filtered_df)
    fig, ax = plt.subplots()
    province_counts.plot.pie(autopct="%1.1f%%", figsize=(5, 5), ax=ax)
    ax.set_ylabel("")
    ax.set_title("Provinces")
    st.pyplot(fig)
else:
    st.write("No data available for the selected filters.")

st.subheader("Restaurant Locations")
if not filtered_df.empty:
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=filtered_df['latitude'].mean(),
                longitude=filtered_df['longitude'].mean(),
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=filtered_df,
                    get_position='[longitude, latitude]',
                    get_radius=200,
                    get_color='[200, 30, 0, 160]',
                    pickable=True,
                )
            ],
        )
    )
else:
    st.write("No data available for the selected filters.")

st.subheader("Top 5 Restaurants by Category")
if not filtered_df.empty:
    top_categories = filtered_df['categories'].value_counts().head(5)
    st.write(top_categories)
else:
    st.write("No data available for the selected filters.")

st.subheader("Province Distribution")
if not filtered_df.empty:
    province_dist = province_distribution(filtered_df)
    formatted_dist = [f"{key}: {value}" for key, value in province_dist.items()]
    st.write(", ".join(formatted_dist))
else:
    st.write("No data available for the selected filters.")

st.subheader("Additional Data Insights")

if not filtered_df.empty:
    sorted_df = filtered_df.sort_values(by='name', ascending=True)
    st.write("Sorted Restaurants by Name (Ascending):")
    st.dataframe(sorted_df[['name', 'city', 'province']])
else:
    st.write("No data available for sorting.")

if not filtered_df.empty:
    filtered_df['location'] = filtered_df['city'] + ", " + filtered_df['province']
    st.write("Sorted Restaurants by Location:")
    st.dataframe(filtered_df[['name', 'location', 'categories']])
else:
    st.write("No data available to add a new column.")







