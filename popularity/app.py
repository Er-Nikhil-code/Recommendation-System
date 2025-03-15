# importing necessary libraries
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Popularity based Recommendation",  # Appears on the browser tab
    page_icon="🚀",               
    layout="centered",                
)

# Title of the webpage
st.title("Popularity based Recommendation")
st.write("This app is designed to provide top 50 books to the user.")

# creating dataframes from .csv files
books = pd.read_csv("Dataset/Books.csv")
ratings = pd.read_csv("Dataset/Ratings.csv")
users = pd.read_csv("Dataset/Users.csv")

# getting ratings and book details together in a dataframe
ratings_with_name = ratings.merge(books,on='ISBN')

# counting number of ratings on books
num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df = num_rating_df.rename(columns={'Book-Rating':'num_ratings'})

# calculating average rating
avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].agg(lambda x: x.astype(float).mean()).reset_index()
avg_rating_df = avg_rating_df.rename(columns = {'Book-Rating' : 'avg_rating'})

# popular books based on average user-rating
popular_df = num_rating_df.merge(avg_rating_df,on='Book-Title')

# extracting top 50  popular books based on avg user rating and books having number of ratings more than 250
popular_df = popular_df[popular_df['num_ratings'] > 250].sort_values('avg_rating', ascending = False).head(50)

# dropping duplicates based on book-title if any
popular_df = popular_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-S','num_ratings','avg_rating']]

# displaying top 50 books in streamlit
for idx, row in enumerate(popular_df.iterrows(), start=1):
    cols = st.columns([1, 2, 6])  # Adjust column widths for layout

    # Rank number
    with cols[0]:
        st.markdown(f"**#{idx}**")  # Displaying 1, 2, 3, 4, ...

    # Book cover image
    with cols[1]:
        st.image(row[1]['Image-URL-S'], width=100)

    # Book details
    with cols[2]:
        st.markdown(f"### {row[1]['Book-Title']}")
        st.markdown(f"**Author:** {row[1]['Book-Author']}")
        st.markdown(f"**Average Rating:** {row[1]['avg_rating']:.3f} ⭐")
        st.markdown(f"**Number of Ratings:** {row[1]['num_ratings']}")

    st.markdown("---")  # Separator line
