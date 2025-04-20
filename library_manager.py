import streamlit as st
import json
import os

# Data file
LIBRARY_FILE = "library_data.json"

# Load data from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save data to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Book formatter
def format_book(book):
    status = "Read" if book["Read"] else "Unread"
    return f"{book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}"

# App logic
st.set_page_config(page_title="📚 Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

# Session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

menu = st.sidebar.radio("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"])

# Add a book
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter the book title")
    author = st.text_input("Enter the author")
    year = st.number_input("Enter the publication year", min_value=0, step=1)
    genre = st.text_input("Enter the genre")
    read = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"

    if st.button("Add Book"):
        if title and author and genre:
            st.session_state.library.append({
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Read": read
            })
            st.success("Book added successfully!")
            save_library(st.session_state.library)
        else:
            st.warning("Please fill out all fields.")

# Remove a book
elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["Title"] for book in st.session_state.library]
    if titles:
        selected_title = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            st.session_state.library = [book for book in st.session_state.library if book["Title"] != selected_title]
            save_library(st.session_state.library)
            st.success("Book removed successfully!")
    else:
        st.info("Library is empty.")

# Search for a book
elif menu == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    search_type = st.radio("Search by", ["Title", "Author"])
    query = st.text_input(f"Enter the {search_type.lower()}")

    if query:
        results = [
            book for book in st.session_state.library
            if query.lower() in book[search_type].lower()
        ]
        if results:
            st.markdown("### 📘 Matching Books:")
            for book in results:
                st.write(format_book(book))
        else:
            st.warning("No matching books found.")

# Display all books
elif menu == "Display All Books":
    st.subheader("📖 Your Library")
    if st.session_state.library:
        for i, book in enumerate(st.session_state.library, 1):
            st.write(f"{i}. {format_book(book)}")
    else:
        st.info("Your library is empty.")

# Display statistics
elif menu == "Display Statistics":
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
    if total == 0:
        st.info("No books to show statistics.")
    else:
        read_count = sum(1 for book in st.session_state.library if book["Read"])
        percent_read = (read_count / total) * 100
        st.write(f"**Total books:** {total}")
        st.write(f"**Percentage read:** {percent_read:.1f}%")

# Exit (for Streamlit it's just a visual)
elif menu == "Exit":
    st.subheader("👋 Thanks for using Library Manager!")
    st.write("Your data has been saved automatically.")

