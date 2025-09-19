import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="MovieLens Dashboard",
    layout="wide"
)

# Load the dataset
df = pd.read_csv("movie_ratings.csv")

st.title("MovieLens Dashboard")

# -------------------------
# Whats the breakdown of genres for the movies that were rated?
# -------------------------
genre_counts = df['genres'].value_counts()

# -------------------------
# Which genres have the highest viewer satisfaction?
# -------------------------
gb_genre = df.groupby('genres')
genre_mean_ratings = gb_genre['rating'].mean().sort_values(ascending=False)

# Put the two bar charts side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Breakdown of Movie Genres")
    fig, ax = plt.subplots(figsize=(4,2.5))  # smaller figure
    genre_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_xlabel("Genres", fontsize=7)
    ax.set_ylabel("Number of Ratings", fontsize=7)
    ax.set_title("Number of Ratings per Genre", fontsize=9)
    ax.set_xticklabels(genre_counts.index, rotation=45, ha='right', fontsize=7)
    ax.tick_params(axis='y', labelsize=7)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Average Rating by Genre")
    fig, ax = plt.subplots(figsize=(4,2.5))  # smaller figure
    genre_mean_ratings.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_xlabel("Genres", fontsize=7)
    ax.set_ylabel("Average Rating", fontsize=7)
    ax.set_title("Viewer Satisfaction by Genre", fontsize=9)
    ax.set_xticklabels(genre_mean_ratings.index, rotation=45, ha='right', fontsize=7)
    ax.tick_params(axis='y', labelsize=7)
    plt.ylim(3,5)
    plt.tight_layout()
    st.pyplot(fig)

# -------------------------
# How does mean rating change across movie release years?
# -------------------------
gb_year = df.groupby('year')
mean_ratings_by_year = gb_year['rating'].mean()

st.subheader("Mean Movie Rating by Release Year")
fig, ax = plt.subplots(figsize=(6,2))  # compact line plot
mean_ratings_by_year.plot(kind='line', ax=ax, marker='o', color='orange')
ax.set_xlabel("Release Year", fontsize=7)
ax.set_ylabel("Average Rating", fontsize=7)
ax.set_title("Trend of Average Ratings Over Years", fontsize=9)
ax.tick_params(axis='x', rotation=45, labelsize=7)
ax.tick_params(axis='y', labelsize=7)
plt.ylim(2,5)
plt.tight_layout()
st.pyplot(fig)

# -------------------------
# What are the 5 best-rated movies that have at least 50 ratings? At least 150 ratings?
# -------------------------
gb_movie = df.groupby('title')
ratings_count = gb_movie['rating'].count()
mean_ratings = gb_movie['rating'].mean()

# movies with at least 50 ratings
plus_50_ratings = ratings_count[ratings_count >= 50]
top_5_with_50 = mean_ratings[plus_50_ratings.index].sort_values(ascending=False).head(5)
top_5_50_df = top_5_with_50.reset_index()
top_5_50_df.columns = ['Movie Title', 'Average Rating']

# movies with at least 150 ratings
plus_150_ratings = ratings_count[ratings_count >= 150]
top_5_with_150 = mean_ratings[plus_150_ratings.index].sort_values(ascending=False).head(5)
top_5_150_df = top_5_with_150.reset_index()
top_5_150_df.columns = ['Movie Title', 'Average Rating']

st.subheader("Top Rated Movies")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Top 5 Movies (≥50 Ratings)**")
    st.table(top_5_50_df)

with col2:
    st.markdown("**Top 5 Movies (≥150 Ratings)**")
    st.table(top_5_150_df)
