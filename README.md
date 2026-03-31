# Gamings API

A modern web application for browsing and filtering free-to-play games using the FreeToGame API.

## Features

- **Real-time Search**: Filter games by genre with instant results
- **Genre Selection**: Interactive dropdown with all available genres
- **Custom Search**: Option to search by specific game names
- **Responsive Design**: Clean, modern interface that works on all devices
- **Game Details**: Display comprehensive information about each game
- **Complete Data View**: Expandable section with full JSON data for developers

## Technologies Used

- **Backend**: Python with Streamlit
- **API**: FreeToGame API (https://www.freetogame.com/api)
- **Frontend**: Streamlit components
- **Data**: JSON responses from FreeToGame

## Installation

1. Clone this repository:
```bash
git clone https://github.com/httpkmile/APIGamings.git
cd APIGamings
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `requirements.txt` file:
```txt
streamlit
requests
```

## Usage

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

### How to Use

1. **Select a Genre**: Use the dropdown to choose from available genres
2. **Custom Genre**: Type a specific genre name in the text field
3. **Search by Name**: Enter a game name in the "Enter a name" field
4. **Real-time Updates**: Results update automatically as you type
5. **Press Enter**: Use Enter key for quick search
6. **View Complete Data**: Click "View complete game data" to see full JSON

## API Integration

The application integrates with the FreeToGame API to fetch:

- Game titles and descriptions
- Genre information
- Platform details
- Release dates
- Publisher and developer information
- Game thumbnails
- Complete game data in JSON format

### API Endpoints Used

- `https://www.freetogame.com/api/games` - All games
- `https://www.freetogame.com/api/games?genre={genre}&id={id}` - Filtered search

## Project Structure

```
APIGamings/
├── app.py              # Main application file
├── assets/
│   └── header.jpg      # Header image
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Functions

### Core Functions

- `search_games(genre, game_id)`: Search games by genre and ID
- `get_all_genres()`: Extract all unique genres from the API
- `filter_games_by_genre(genre)`: Filter games locally by genre
- `run_search()`: Handle real-time search triggers

### UI Components

- Genre selector dropdown
- Custom genre input
- Game name search
- Game display with badges
- Expandable JSON data viewer
- Responsive layout

## Features Details

### Real-time Search
- Automatic search as you type
- Enter key support
- Instant results without button clicks

### Game Information Display
- Title with bold formatting
- Genre, platform, and release date badges
- Detailed descriptions
- Publisher and developer information
- Complete JSON data in expandable section

### Responsive Design
- Full-width header image
- Mobile-friendly layout
- Column-based information display

## Data Model

Each game object contains:
```json
{
  "id": 540,
  "title": "Game Title",
  "thumbnail": "https://...",
  "short_description": "Game description",
  "game_url": "https://...",
  "genre": "Shooter",
  "platform": "PC (Windows)",
  "publisher": "Publisher Name",
  "developer": "Developer Name",
  "release_date": "2022-10-04",
  "freetogame_profile_url": "https://..."
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the application
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- FreeToGame API for providing the game data
- Streamlit for the web framework
- All contributors and users of this application

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact the development team

---

**Note**: This application uses the FreeToGame API which provides free-to-play game information. Make sure you have an internet connection for the application to work properly.
