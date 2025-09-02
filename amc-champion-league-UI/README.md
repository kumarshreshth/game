# AMC Champion League API

A FastAPI-based application for managing an office championship league with multiple games, franchises, players, and matches.

## Features

- Manage games, franchises, players, teams, and matches
- Track match results and scores with flexible JSON schemas for different game types
- **Tournament round management with Quarter Finals, Semi Finals, and Finals**
- **Advanced filtering by tournament rounds for matches and fixtures**
- **Tournament bracket visualization and comprehensive match data**
- Image gallery for storing and retrieving match photos
- Leaderboards for players, franchises, and teams
- Support for both local and S3-based image storage
- Comprehensive fixture management with detailed match information

## Supported Games

- Badminton
- Table Tennis
- Pool
- Carom
- Pickle Ball
- Chess
- Box Cricket
- Foosball

## Franchise Teams

- AM&C WARRIORS
- S&S SUPER KINGS
- DFO&I TITANS
- CD&D DAREDEVILS

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Deloitte-US-Consulting/amc-champion-league.git
cd amc-champion-league
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the application:

```bash
python run.py
```

This will start the FastAPI application at http://localhost:8000.

2. Access the API documentation at http://localhost:8000/docs to interact with the API endpoints.

## Sample Data Generation

The application comes with comprehensive sample data already populated:

- **8 game types** (Badminton, Table Tennis, Pool, Carom, Pickle Ball, Chess, Box Cricket, Foosball)
- **4 franchises** with complete team rosters
- **320+ players** (80 per franchise across all games)
- **320+ matches** with complete tournament structure including Quarter Finals, Semi Finals, and Finals
- **1600+ match player records** with detailed performance data
- **Gallery images** for tournament matches

The data includes a full tournament structure for each game with proper round progression and realistic match results.

## Testing with Postman

1. Import the Postman collection file:
   - Open Postman
   - Click on "Import" button
   - Select the file: `amc_champion_league_postman_collection.json`

2. Configure the base URL variable:
   - Click on the collection name "AMC Champion League API"
   - Go to the "Variables" tab
   - Update the "baseUrl" value to match your server (default: http://localhost:8000)

3. Start testing the endpoints:
   - Begin with the "Health Check" request to verify the API is running
   - Explore other endpoint folders (Games, Franchises, Players, etc.)
   - Use the pre-configured request bodies to create and update resources

## Project Structure

```
codebase/
  ├── app/
  │   └── api.py                # Main API entry point with all endpoints
  ├── model/
  │   └── request_model.py      # SQLAlchemy ORM models
  ├── service/
  │   ├── game_service.py       # Business logic
  │   └── request_payload.py    # Pydantic models for request/response
  ├── config/
  │   └── config.ini            # Application configuration
  └── utils/
      ├── database.py           # Database utilities
      ├── image_storage.py      # Image storage utilities (local/S3)
      ├── config_manager.py     # Configuration manager
      └── logging_config.py     # Logging configuration

scripts/
  └── create_sample_data.py     # Script to generate sample data

requirements.txt                # Project dependencies
run.py                          # Application startup script
```

## API Endpoints

### Health Check
- GET `/health` - Check API health

### Games
- GET `/games` - Get all games
- GET `/games/{game_id}` - Get a game by ID
- POST `/games` - Create a new game
- PUT `/games/{game_id}` - Update a game
- DELETE `/games/{game_id}` - Delete a game

### Franchises
- GET `/franchises` - Get all franchises
- GET `/franchises/{franchise_id}` - Get a franchise by ID
- POST `/franchises` - Create a new franchise
- PUT `/franchises/{franchise_id}` - Update a franchise
- DELETE `/franchises/{franchise_id}` - Delete a franchise

### Teams
- GET `/teams` - Get all teams
- GET `/teams?franchise_id={id}` - Get teams by franchise
- GET `/teams?game_id={id}` - Get teams by game
- GET `/teams/{team_id}` - Get a team by ID
- POST `/teams` - Create a new team
- PUT `/teams/{team_id}` - Update a team
- DELETE `/teams/{team_id}` - Delete a team

### Players
- GET `/players` - Get all players
- GET `/players?franchise_id={id}` - Get players by franchise
- GET `/players/{player_id}` - Get a player by ID
- POST `/players` - Create a new player
- POST `/players/legacy` - Create a player (legacy format)
- PUT `/players/{player_id}` - Update a player
- DELETE `/players/{player_id}` - Delete a player

### Matches
- GET `/matches` - Get all matches
- GET `/matches?game_id={id}` - Get matches by game
- GET `/matches?status={status}` - Get matches by status
- **GET `/matches?round={round}` - Get matches by tournament round (Quarter Finals, Semi Finals, Finals)**
- **GET `/matches?round={round}&game_id={id}` - Get matches by round and game**
- GET `/matches/{match_id}` - Get a match by ID
- POST `/matches` - Create a new match
- PUT `/matches/{match_id}` - Update a match
- DELETE `/matches/{match_id}` - Delete a match

### Fixtures
- GET `/fixtures` - Get all match fixtures with detailed information
- GET `/fixtures?game_id={id}` - Get fixtures by game
- GET `/fixtures?status={status}` - Get fixtures by status
- **GET `/fixtures?round={round}` - Get fixtures by tournament round (Quarter Finals, Semi Finals, Finals)**
- **GET `/fixtures/bracket?game_id={id}&status={status}` - Get tournament bracket view**
- GET `/fixtures?franchise_id={id}` - Get fixtures by franchise

### Match Players
- GET `/matches/{match_id}/players` - Get all players in a match
- POST `/match-players` - Add a player to a match
- PUT `/match-players/{match_player_id}` - Update match results

### Gallery
- GET `/gallery` - Get all gallery images
- GET `/gallery?match_id={id}` - Get gallery images for a match
- POST `/gallery` - Add an image to the gallery
- DELETE `/gallery/{image_id}` - Delete a gallery image
- GET `/gallery/s3` - List S3/local gallery images

### Leaderboard
- GET `/leaderboard` - Get combined player, franchise, and team leaderboard
- GET `/leaderboard/players` - Get player leaderboard
- GET `/leaderboard/franchises` - Get franchise leaderboard
- GET `/leaderboard/teams` - Get team leaderboard

## Configuration

The application can be configured via the `codebase/config/config.ini` file or environment variables:

- **Database**: Configure database connection details
- **Storage**: Configure S3 or local storage for images
- **Application**: Configure host, port, and debug mode
- **Games**: List of supported games
- **Scoring**: Default points for winning matches

## Deployment

To deploy using Docker:

1. Build the Docker image:

```bash
docker build -t amc-champion-league .
```

2. Run the container:

```bash
docker run -p 8000:8000 amc-champion-league
```

## Future Extensions

- Authentication and authorization
- Game-specific statistics and visualizations
- Tournament scheduling and bracket generation
- Mobile app integration
