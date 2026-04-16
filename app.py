import requests # Importa o módulo requests para fazer requisições HTTP
import streamlit as st # Importa o módulo da framework streamlit
import base64 # Importa o módulo base64
from urllib.parse import urlencode # Importa a função urlencode do módulo urllib.parse
import os 
from dotenv import load_dotenv # Carrega variáveis de ambiente do arquivo .env

# Lê o conteúdo do style.css
def load_css():
    with open("style.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Twitch Authentication 
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI", "http://localhost:8501")

def get_twitch_access_token():
    """Get Twitch API access token"""
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        st.error(f"Error getting Twitch access token: {e}")
        return None

def get_game_cover_url(game_name, access_token):
    """Get game cover URL from Twitch IGDB API"""
    if not access_token:
        return None
        
    url = "https://api.igdb.com/v4/covers"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    
    # First get game ID
    game_url = "https://api.igdb.com/v4/games"
    game_data = f"search \"{game_name}\"; fields name, cover;"
    
    try:
        response = requests.post(game_url, headers=headers, data=game_data)
        if response.status_code == 200 and response.json():
            game_result = response.json()[0]
            cover_id = game_result.get("cover")
            
            if cover_id:
                # Get cover URL
                cover_data = f"fields url; where id = {cover_id};"
                cover_response = requests.post(url, headers=headers, data=cover_data)
                
                if cover_response.status_code == 200 and cover_response.json():
                    cover_url = cover_response.json()[0].get("url", "")
                    # Convert to high resolution URL
                    if cover_url:
                        # Adiciona http:// se não existir
                        if not cover_url.startswith("http"):
                            cover_url = "https://" + cover_url
                        return cover_url.replace("thumb", "cover_big")
        return None
    except Exception as e:
        st.error(f"Error getting game cover: {e}")
        return None

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
def display_navbar():
    """Display navigation bar with external links"""
    navbar_html = """
    <nav class="navbar">
        <div class="navbar-links">
            <a href="https://www.freetogame.com/games" target="_blank" class="navbar-link">
                <span>API</span>
            </a>
            <a href="https://www.igdb.com/" target="_blank" class="navbar-link">
                <span>Covers</span>
            </a>
            <a href="https://github.com/httpkmile/APIGamings-" target="_blank" class="navbar-link">
                <span>GitHub</span>
            </a>
            <a href="https://icons8.com/icons/set/super-mushroom-mario" target="_blank" class="navbar-link">
                <span>Icons</span>
            </a>
        </div>
    </nav>
    """
    st.markdown(navbar_html, unsafe_allow_html=True)

def display_game_header():
    """Display app header"""
    st.image("assets/header.jpg", width=None, use_container_width=True)
    st.title("Free Games - API")


def display_game_info(game):
    """Display individual game information"""
    st.write(f"**{game.get('title', 'No title')}**")
    
    # Get and display game cover from Twitch
    access_token = get_twitch_access_token()
    cover_url = get_game_cover_url(game.get('title', ''), access_token)
    
    if cover_url:
        st.image(cover_url, width=200, caption="Game Cover")
    elif game.get('thumbnail'):
        st.image(game.get('thumbnail'), width=200, caption="Game Thumbnail")
    
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
    # Configurar Streamlit para modo dark (removendo opção light)
    st.set_page_config(
        page_title="Gamings",
        page_icon="🎮",
        initial_sidebar_state="expanded",
        menu_items=None
    )
    
    # Forçar modo dark no Streamlit via CSS
    st.markdown("""
    <style>
    /* Esconder o menu de tema */
    .stMainMenu button[aria-label="Main menu"] {
        display: none !important;
    }
    
    /* Forçar modo dark */
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    /* Componentes dark */
    .stBlockContainer {
        background-color: #1e2130 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Carregar CSS customizado ()
    load_css()
    
    # Exibir navbar
    display_navbar()
    
    display_game_header()
    
    # Genre selection
    genres = get_all_genres()
    if genres:
        genre = st.selectbox("Select a example genre:", [""] + genres)
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
