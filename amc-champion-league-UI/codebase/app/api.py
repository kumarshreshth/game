from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import os
import uvicorn

# Import services
from codebase.service.game_service import (
    # Game
    create_game, get_games, get_game, update_game, delete_game,
    # Franchise
    create_franchise, get_franchises, get_franchise, update_franchise, delete_franchise,
    # Player
    create_player, get_players, get_player, update_player, delete_player,
    # Match
    create_match, get_matches, get_match, update_match, delete_match, get_match_with_details,
    # Match Player
    add_player_to_match, update_match_player_result, get_match_players,
    # Gallery
    add_gallery_image, get_gallery_images, delete_gallery_image, list_s3_gallery_images,
    # Team
    create_team, get_teams, get_team, update_team, delete_team,
    get_teams_by_franchise, get_teams_by_game,
    # Team Player
    add_player_to_team, get_team_players, get_player_teams, remove_player_from_team,
    # Fixtures
    get_fixtures,
    # Leaderboard
    get_leaderboard, get_player_leaderboard, get_franchise_leaderboard, get_team_leaderboard
)

# Import from team_service
from codebase.service.team_service import get_teams_with_details

# Import models and schemas
from codebase.service.request_payload import (
    Game, GameCreate,
    Franchise, FranchiseCreate,
    Player, PlayerCreate, AddPlayerRequest,
    Match, MatchCreate,
    MatchPlayer, MatchPlayerCreate, MatchPlayerUpdate,
    Gallery, GalleryCreate,
    TeamCreate, Team, TeamPlayer, TeamPlayerCreate, TeamWithDetails,
    FixtureDetail,
    Leaderboard
)

# Import database utils
from codebase.utils.database import get_db, create_db_tables

# Create FastAPI app
app = FastAPI(
    title="AMC Champion League API",
    description="API for managing office championship games and leagues",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount static files directory for local image storage
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "AMC Champion League API is running"}

# Game endpoints
@app.post("/api/v1/games/", response_model=Game, tags=["games"])
def create_game_endpoint(game: GameCreate, db: Session = Depends(get_db)):
    return create_game(db=db, game=game)

@app.get("/api/v1/games/", response_model=List[Game], tags=["games"])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = get_games(db, skip=skip, limit=limit)
    return games

@app.get("/api/v1/games/{game_id}", response_model=Game, tags=["games"])
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = get_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@app.put("/api/v1/games/{game_id}", response_model=Game, tags=["games"])
def update_game_endpoint(game_id: int, game_data: Dict[str, Any], db: Session = Depends(get_db)):
    db_game = update_game(db=db, game_id=game_id, game_data=game_data)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@app.delete("/api/v1/games/{game_id}", tags=["games"])
def delete_game_endpoint(game_id: int, db: Session = Depends(get_db)):
    success = delete_game(db=db, game_id=game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game deleted successfully"}

# Franchise endpoints
@app.post("/api/v1/franchises/", response_model=Franchise, tags=["franchises"])
def create_franchise_endpoint(franchise: FranchiseCreate, db: Session = Depends(get_db)):
    return create_franchise(db=db, franchise=franchise)

@app.get("/api/v1/franchises/", response_model=List[Franchise], tags=["franchises"])
def read_franchises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    franchises = get_franchises(db, skip=skip, limit=limit)
    return franchises

@app.get("/api/v1/franchises/{franchise_id}", response_model=Franchise, tags=["franchises"])
def read_franchise(franchise_id: int, db: Session = Depends(get_db)):
    db_franchise = get_franchise(db, franchise_id=franchise_id)
    if db_franchise is None:
        raise HTTPException(status_code=404, detail="Franchise not found")
    return db_franchise

@app.put("/api/v1/franchises/{franchise_id}", response_model=Franchise, tags=["franchises"])
def update_franchise_endpoint(franchise_id: int, franchise_data: Dict[str, Any], db: Session = Depends(get_db)):
    db_franchise = update_franchise(db=db, franchise_id=franchise_id, franchise_data=franchise_data)
    if db_franchise is None:
        raise HTTPException(status_code=404, detail="Franchise not found")
    return db_franchise

@app.delete("/api/v1/franchises/{franchise_id}", tags=["franchises"])
def delete_franchise_endpoint(franchise_id: int, db: Session = Depends(get_db)):
    success = delete_franchise(db=db, franchise_id=franchise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Franchise not found")
    return {"message": "Franchise deleted successfully"}

# Player endpoints
@app.post("/api/v1/players/", response_model=Player, tags=["players"])
async def create_player_endpoint(player: PlayerCreate, db: Session = Depends(get_db)):
    return await create_player(db=db, player=player)

@app.get("/api/v1/players/", response_model=List[Player], tags=["players"])
def read_players(
    skip: int = 0, 
    limit: int = 100, 
    franchise_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    players = get_players(db, skip=skip, limit=limit, franchise_id=franchise_id)
    return players

@app.get("/api/v1/players/{player_id}", response_model=Player, tags=["players"])
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.put("/api/v1/players/{player_id}", response_model=Player, tags=["players"])
def update_player_endpoint(player_id: int, player_data: Dict[str, Any], db: Session = Depends(get_db)):
    db_player = update_player(db=db, player_id=player_id, player_data=player_data)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.delete("/api/v1/players/{player_id}", tags=["players"])
def delete_player_endpoint(player_id: int, db: Session = Depends(get_db)):
    success = delete_player(db=db, player_id=player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player deleted successfully"}

# Legacy player endpoint for compatibility
@app.post("/api/v1/add-player", tags=["players"])
def add_player_legacy(player: AddPlayerRequest, db: Session = Depends(get_db)):
    # Convert legacy request to new format
    new_player = PlayerCreate(
        name=player.player_name,
        email=player.player_email,
        # Note: player_team is handled differently now with franchises
    )
    return create_player(db=db, player=new_player)

# Team endpoints
@app.post("/api/v1/teams/", response_model=Team, tags=["teams"])
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team"""
    return create_team(db=db, team=team)

@app.get("/api/v1/teams/{team_id}", response_model=Team, tags=["teams"])
def get_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    """Get a team by ID"""
    db_team = get_team(db=db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.get("/api/v1/teams/", response_model=List[Team], tags=["teams"])
def get_teams_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    franchise_id: Optional[int] = None, 
    game_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get teams with optional filtering"""
    if franchise_id:
        return get_teams_by_franchise(db=db, franchise_id=franchise_id)
    elif game_id:
        return get_teams_by_game(db=db, game_id=game_id)
    return get_teams(db=db, skip=skip, limit=limit)

@app.get("/api/v1/teams-with-details/", response_model=List[TeamWithDetails], tags=["teams"])
def get_teams_details_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get teams with franchise and game details"""
    return get_teams_with_details(db=db, skip=skip, limit=limit)

@app.put("/api/v1/teams/{team_id}", response_model=Team, tags=["teams"])
def update_team_endpoint(team_id: int, team_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Update a team"""
    db_team = update_team(db=db, team_id=team_id, team_data=team_data)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.delete("/api/v1/teams/{team_id}", tags=["teams"])
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    """Delete a team"""
    success = delete_team(db=db, team_id=team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted successfully"}

# Team Player endpoints
@app.post("/api/v1/team-players/", response_model=TeamPlayer, tags=["team-players"])
def add_player_to_team_endpoint(team_player: TeamPlayerCreate, db: Session = Depends(get_db)):
    """Add a player to a team"""
    return add_player_to_team(db=db, team_player=team_player)

@app.get("/api/v1/teams/{team_id}/players", response_model=List[Dict], tags=["team-players"])
def get_team_players_endpoint(team_id: int, db: Session = Depends(get_db)):
    """Get all players in a team"""
    return get_team_players(db=db, team_id=team_id)

@app.get("/api/v1/players/{player_id}/teams", response_model=List[Dict], tags=["team-players"])
def get_player_teams_endpoint(player_id: int, db: Session = Depends(get_db)):
    """Get all teams a player belongs to"""
    return get_player_teams(db=db, player_id=player_id)

@app.delete("/api/v1/teams/{team_id}/players/{player_id}", tags=["team-players"])
def remove_player_from_team_endpoint(team_id: int, player_id: int, db: Session = Depends(get_db)):
    """Remove a player from a team"""
    success = remove_player_from_team(db=db, team_id=team_id, player_id=player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found in team")
    return {"message": "Player removed from team successfully"}

# Match endpoints
@app.post("/api/v1/matches/", response_model=Match, tags=["matches"])
def create_match_endpoint(match: MatchCreate, db: Session = Depends(get_db)):
    return create_match(db=db, match=match)

@app.get("/api/v1/matches/", response_model=List[Match], tags=["matches"])
def read_matches(
    skip: int = 0, 
    limit: int = 100,
    game_id: Optional[int] = None,
    status: Optional[str] = None,
    franchise_id: Optional[int] = None,
    round: Optional[str] = None,
    db: Session = Depends(get_db)
):
    matches = get_matches(db, skip=skip, limit=limit, game_id=game_id, status=status, round=round)
    return matches

@app.get("/api/v1/matches/{match_id}", response_model=Match, tags=["matches"])
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@app.get("/api/v1/matches/{match_id}/details", response_model=Dict, tags=["matches"])
def get_match_details_endpoint(match_id: int, db: Session = Depends(get_db)):
    """Get detailed match information including opponents"""
    match_details = get_match_with_details(db=db, match_id=match_id)
    if not match_details:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_details

@app.put("/api/v1/matches/{match_id}", response_model=Match, tags=["matches"])
def update_match_endpoint(match_id: int, match_data: Dict[str, Any], db: Session = Depends(get_db)):
    db_match = update_match(db=db, match_id=match_id, match_data=match_data)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@app.delete("/api/v1/matches/{match_id}", tags=["matches"])
def delete_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    success = delete_match(db=db, match_id=match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"message": "Match deleted successfully"}

# Fixtures endpoints
@app.get("/api/v1/fixtures/", response_model=List[FixtureDetail], tags=["fixtures"])
def get_fixtures_endpoint(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    game_id: Optional[int] = None,
    franchise_id: Optional[int] = None,
    round: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get fixtures/matches with opponent details
    
    Optional filters:
    - status: scheduled, in_progress, completed, cancelled
    - game_id: Filter by specific game
    - franchise_id: Filter by franchise (home or away)
    - round: Filter by tournament round (Semi Final, Final, etc.)
    """
    return get_fixtures(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        game_id=game_id,
        franchise_id=franchise_id,
        round=round
    )

# Match Players endpoints
@app.post("/api/v1/match-players/", response_model=MatchPlayer, tags=["match-players"])
def add_player_to_match_endpoint(match_player: MatchPlayerCreate, db: Session = Depends(get_db)):
    return add_player_to_match(db=db, match_player=match_player)

@app.get("/api/v1/matches/{match_id}/players", response_model=List[Dict], tags=["match-players"])
def get_match_players_endpoint(match_id: int, db: Session = Depends(get_db)):
    return get_match_players(db=db, match_id=match_id)

@app.put("/api/v1/match-players/{match_player_id}", response_model=MatchPlayer, tags=["match-players"])
def update_match_player_result_endpoint(
    match_player_id: int, 
    match_player_update: MatchPlayerUpdate, 
    db: Session = Depends(get_db)
):
    db_match_player = update_match_player_result(
        db=db, 
        match_player_id=match_player_id, 
        update_data=match_player_update
    )
    
    if db_match_player is None:
        raise HTTPException(status_code=404, detail="Match player not found")
    
    return db_match_player

# Gallery endpoints
@app.post("/api/v1/gallery/", response_model=Gallery, tags=["gallery"])
async def create_gallery_item(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    match_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    gallery_data = GalleryCreate(
        title=title,
        description=description,
        match_id=match_id
    )
    return await add_gallery_image(db=db, gallery_data=gallery_data, image=file)

@app.get("/api/v1/gallery/", response_model=List[Gallery], tags=["gallery"])
def read_gallery(skip: int = 0, limit: int = 100, match_id: Optional[int] = None, db: Session = Depends(get_db)):
    gallery_items = get_gallery_images(db=db, skip=skip, limit=limit, match_id=match_id)
    return gallery_items

@app.get("/api/v1/s3-gallery/", response_model=List[str], tags=["gallery"])
def list_s3_images():
    return list_s3_gallery_images()

@app.delete("/api/v1/gallery/{gallery_id}", tags=["gallery"])
def delete_gallery_item(gallery_id: int, db: Session = Depends(get_db)):
    success = delete_gallery_image(db=db, image_id=gallery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    return {"message": "Gallery item deleted successfully"}

# Leaderboard endpoints
@app.get("/api/v1/leaderboard/", response_model=Dict, tags=["leaderboard"])
def get_leaderboard_endpoint(game_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_leaderboard(db=db, game_id=game_id)

@app.get("/api/v1/leaderboard/players", tags=["leaderboard"])
def get_player_leaderboard_endpoint(
    limit: int = 10,
    game_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    return get_player_leaderboard(db=db, limit=limit, game_id=game_id)

@app.get("/api/v1/leaderboard/franchises", tags=["leaderboard"])
def get_franchise_leaderboard_endpoint(
    limit: int = 10,
    game_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_franchise_leaderboard(db=db, limit=limit, game_id=game_id)

@app.get("/api/v1/leaderboard/teams", tags=["leaderboard"])
def get_team_leaderboard_endpoint(
    limit: int = 10,
    game_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_team_leaderboard(db=db, limit=limit, game_id=game_id)

# Run the application
if __name__ == "__main__":
    # Ensure database tables exist
    create_db_tables()
    
    # Run the FastAPI app with Uvicorn
    uvicorn.run(
        "codebase.app.api:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
