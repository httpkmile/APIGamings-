import requests
import streamlit as st


def search_games(genre, game_id):
    endpoint = f"https://www.freetogame.com/api/games?genre={genre}&id={game_id}"
    response = requests.get(endpoint)
    games_data = response.json() if response.status_code == 200 else None
    return games_data


def get_all_genres():
    endpoint = "https://www.freetogame.com/api/games"
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        return []
    
    games_data = response.json()
    genres = set()
    for game in games_data:
        genres.add(game['genre'])
    return sorted(list(genres))


def filter_games_by_genre(genre):
    endpoint = "https://www.freetogame.com/api/games"
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        return []

    games_data = response.json()
    
    game_filters = [
        game for game in games_data 
        if genre.lower() in game['genre'].lower()
    ]
    return game_filters


st.image("assets/header.jpg", width=None, use_container_width=True)
st.title("Gamings")

def run_search():
    st.session_state.search_triggered = True
    st.rerun()

genres = get_all_genres()
if genres:
    genre = st.selectbox("Select a genre:", [""] + genres)
    st.caption("Or type a custom genre below:")
    custom_genre = st.text_input("Enter custom genre", on_change=run_search)
else:
    st.caption("Input a genre like: Shooter, horror, battle royale, etc...")
    genre = st.text_input("Enter a genre", on_change=run_search)
    custom_genre = ""

game_id = st.text_input("Enter a name", on_change=run_search)
search = st.button("Search")

if search or st.session_state.get("search_triggered", False):
    st.session_state.search_triggered = False
    selected_genre = genre if genre else custom_genre
    if selected_genre:
        games = filter_games_by_genre(selected_genre)
    else:
        games = search_games(selected_genre, game_id)
    if games:
        for game in games:
            st.write(f"**{game.get('title', 'No title')}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.badge(game.get('genre', 'Unknown'), color="blue")
            with col2:
                st.badge(game.get('platform', 'Unknown'), color="green")
            with col3:
                st.badge(game.get('release_date', 'Unknown'), color="orange")
            
            st.write(f"**Description:** {game.get('short_description', 'No description')}")
            
            col4, col5 = st.columns(2)
            with col4:
                if game.get('publisher'):
                    st.badge(f"Publisher: {game.get('publisher')}", color="purple")
            with col5:
                if game.get('developer'):
                    st.badge(f"Developer: {game.get('developer')}", color="cyan")
            
            with st.expander("View complete game data", expanded=False):
                st.json(game)
              
    else:
        st.write("No games found")
