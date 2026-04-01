import requests
import streamlit as st


# API Functions
def search_games(genre, game_id):
    """Search games by genre and ID"""
    endpoint = f"https://www.freetogame.com/api/games?genre={genre}&id={game_id}"
    response = requests.get(endpoint)
    return response.json() if response.status_code == 200 else None


def get_all_genres():
    """Get all unique genres from the API"""
    endpoint = "https://www.freetogame.com/api/games"
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        return []
    
    games_data = response.json()
    genres = {game['genre'] for game in games_data}
    return sorted(list(genres))


def filter_games_by_genre(genre):
    """Filter games by genre"""
    endpoint = "https://www.freetogame.com/api/games"
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        return []

    games_data = response.json()
    return [
        game for game in games_data 
        if genre.lower() in game['genre'].lower()
    ]


def run_search():
    """Trigger search state"""
    st.session_state.search_triggered = True
    st.rerun()


# UI Components
def display_game_header():
    """Display app header"""
    st.image("assets/header.jpg", width=None, use_container_width=True)
    st.title("Gamings")


def display_game_info(game):
    """Display individual game information"""
    st.write(f"**{game.get('title', 'No title')}**")
    
    # Game badges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.badge(game.get('genre', 'Unknown'), color="blue")
    with col2:
        st.badge(game.get('platform', 'Unknown'), color="green")
    with col3:
        st.badge(game.get('release_date', 'Unknown'), color="orange")
    
    st.write(f"**Description:** {game.get('short_description', 'No description')}")
    
    # Publisher and Developer
    col4, col5 = st.columns(2)
    with col4:
        if game.get('publisher'):
            st.badge(f"Publisher: {game.get('publisher')}")
    with col5:
        if game.get('developer'):
            st.badge(f"Developer: {game.get('developer')}")
    
    # Expandable JSON data
    with st.expander("View complete game data", expanded=False):
        st.json(game)


# Main App
def userinput(selected_genre):
    """Display games count for selected genre"""
    # Get games for selected genre
    userdata = filter_games_by_genre(selected_genre)
    total = len(userdata) if userdata else 0
    
    # Display metric
    if selected_genre:
        st.metric(f"Total games ({selected_genre})", total)
    else:
        st.metric("Total games", total)
    
    return userdata


def main():
    display_game_header()
    
    # Genre selection
    genres = get_all_genres()
    if genres:
        genre = st.selectbox("Select a genre:", [""] + genres)
        st.caption("Or type a custom genre below:")
        custom_genre = st.text_input("Enter custom genre", on_change=run_search)
    else:
        st.caption("Input a genre like: Shooter, horror, battle royale, etc...")
        genre = st.text_input("Enter a genre", on_change=run_search)
        custom_genre = ""
    
    # Game search
    game_id = st.text_input("Enter a name", on_change=run_search)
    search = st.button("Search")
    
    # Search results
    if search or st.session_state.get("search_triggered", False):
        st.session_state.search_triggered = False
        selected_genre = genre if genre else custom_genre
        
        if selected_genre:
            games = filter_games_by_genre(selected_genre)
            total = len(games) if games else 0
            st.metric(f"Total games ({selected_genre})", total)
        else:
            games = search_games(selected_genre, game_id)
        
        if games:
            for game in games:
                display_game_info(game)
        else:
            st.write("No games found")
    else:
        # Show total games on initial load
        userinput("")


if __name__ == "__main__":
    main()
