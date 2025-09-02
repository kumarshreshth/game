from sqlalchemy.orm import Session, aliased, joinedload
from sqlalchemy import func
from typing import List, Optional, Dict, Any, Union
from fastapi import UploadFile, HTTPException
from datetime import datetime
import json
from codebase.genai.llm_call import get_chat_completion


from codebase.model.request_model import (
    Game, Franchise, Player, Match, MatchPlayer, Gallery, Team, TeamPlayer
)
from codebase.service.request_payload import (
    GameCreate, FranchiseCreate, PlayerCreate, MatchCreate,
    MatchPlayerCreate, MatchPlayerUpdate, GalleryCreate,
    TeamCreate, TeamPlayerCreate, GameScore, FixtureDetail
)
from codebase.utils.image_storage import (
    upload_image_to_storage, list_images_from_storage, delete_image_from_storage
)

# Game services
async def create_game(db: Session, game: GameCreate, image: Optional[UploadFile] = None) -> Game:
    """Create a new game in the championship"""
    image_path = None
    if image:
        image_path = await upload_image_to_storage(image, "games")
    
    # Create game object with image path if available
    db_game = Game(
        name=game.name,
        description=game.description,
        winning_points=game.winning_points,
        image_path=image_path,
        game_type=game.game_type,
        extra_data=game.extra_data
    )
    
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_games(db: Session, skip: int = 0, limit: int = 100) -> List[Game]:
    """Get all games in the championship"""
    return db.query(Game).offset(skip).limit(limit).all()

def get_game(db: Session, game_id: int) -> Optional[Game]:
    """Get a game by ID"""
    return db.query(Game).filter(Game.id == game_id).first()

def update_game(db: Session, game_id: int, game_data: Union[GameCreate, Dict[str, Any]]) -> Optional[Game]:
    """Update a game's information"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        return None
        
    # Handle both Pydantic models and dictionaries
    if hasattr(game_data, 'model_dump'):
        # It's a Pydantic model
        update_data = game_data.model_dump(exclude_unset=True)
    else:
        # It's already a dictionary
        update_data = game_data
    
    # Update game fields
    for field, value in update_data.items():
        if hasattr(db_game, field) and value is not None:
            setattr(db_game, field, value)
    

    db.commit()
    db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_id: int) -> bool:
    """Delete a game"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        return False
        
    db.delete(db_game)
    db.commit()
    return True

# Franchise services
async def create_franchise(db: Session, franchise: FranchiseCreate, logo: Optional[UploadFile] = None) -> Franchise:
    """Create a new franchise"""
    logo_path = None
    if logo:
        logo_path = await upload_image_to_storage(logo, "franchises")
    
    db_franchise = Franchise(
        name=franchise.name,
        logo_path=logo_path,
        extra_data=franchise.extra_data
    )
    
    db.add(db_franchise)
    db.commit()
    db.refresh(db_franchise)
    return db_franchise

def get_franchises(db: Session, skip: int = 0, limit: int = 100) -> List[Franchise]:
    """Get all franchises"""
    return db.query(Franchise).offset(skip).limit(limit).all()

def get_franchise(db: Session, franchise_id: int) -> Optional[Franchise]:
    """Get a franchise by ID"""
    return db.query(Franchise).filter(Franchise.id == franchise_id).first()

def update_franchise(db: Session, franchise_id: int, franchise_data: Union[FranchiseCreate, Dict[str, Any]]) -> Optional[Franchise]:
    """Update a franchise's information"""
    db_franchise = db.query(Franchise).filter(Franchise.id == franchise_id).first()
    if not db_franchise:
        return None
        
    # Handle both Pydantic models and dictionaries
    if hasattr(franchise_data, 'model_dump'):
        # It's a Pydantic model
        update_data = franchise_data.model_dump(exclude_unset=True)
    else:
        # It's already a dictionary
        update_data = franchise_data
    
    # Update franchise fields
    for field, value in update_data.items():
        if hasattr(db_franchise, field) and value is not None:
            setattr(db_franchise, field, value)
    

    db.commit()
    db.refresh(db_franchise)
    return db_franchise

def delete_franchise(db: Session, franchise_id: int) -> bool:
    """Delete a franchise"""
    db_franchise = db.query(Franchise).filter(Franchise.id == franchise_id).first()
    if not db_franchise:
        return False
        
    db.delete(db_franchise)
    db.commit()
    return True

# Player services
async def create_player(db: Session, player: PlayerCreate, profile_image: Optional[UploadFile] = None) -> Player:
    """Create a new player"""
    profile_image_path = None
    if profile_image:
        profile_image_path = await upload_image_to_storage(profile_image, "players")
    
    db_player = Player(
        name=player.name,
        franchise_id=player.franchise_id,
        email=player.email,
        profile_image_path=profile_image_path,
        extra_data=player.extra_data
    )
    
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players(db: Session, skip: int = 0, limit: int = 100, franchise_id: Optional[int] = None) -> List[Player]:
    """Get all players, optionally filtered by franchise"""
    query = db.query(Player)
    if franchise_id:
        query = query.filter(Player.franchise_id == franchise_id)
    return query.offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int) -> Optional[Player]:
    """Get a player by ID"""
    return db.query(Player).filter(Player.id == player_id).first()

def update_player(db: Session, player_id: int, player_data: Union[PlayerCreate, Dict[str, Any]]) -> Optional[Player]:
    """Update a player's information"""
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if not db_player:
        return None
        
    # Handle both Pydantic models and dictionaries
    if hasattr(player_data, 'model_dump'):
        # It's a Pydantic model
        update_data = player_data.model_dump(exclude_unset=True)
    else:
        # It's already a dictionary
        update_data = player_data
    
    # Update player fields
    for field, value in update_data.items():
        if hasattr(db_player, field) and value is not None:
            setattr(db_player, field, value)
    

    db.commit()
    db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int) -> bool:
    """Delete a player"""
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if not db_player:
        return False
        
    db.delete(db_player)
    db.commit()
    return True

# Match services
def create_match(db: Session, match: MatchCreate) -> Match:
    """Create a new match"""
    db_match = Match(
        game_id=match.game_id,
        home_franchise_id=match.home_franchise_id,
        away_franchise_id=match.away_franchise_id,
        home_team_id=match.home_team_id,
        away_team_id=match.away_team_id,
        match_date=match.match_date or datetime.utcnow(),
        status=match.status,
        location=match.location,
        score_summary=match.score_summary,
        winner_id=match.winner_id,
        extra_data=match.extra_data
    )
    
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session, skip: int = 0, limit: int = 100, game_id: Optional[int] = None,
               status: Optional[str] = None, round: Optional[str] = None) -> List[Match]:
    """Get all matches, optionally filtered by game, status, and round"""
    query = db.query(Match)
    if game_id:
        query = query.filter(Match.game_id == game_id)
    if status:
        query = query.filter(Match.status == status)
    if round:
        query = query.filter(Match.round == round)
    return query.offset(skip).limit(limit).all()

def get_match(db: Session, match_id: int) -> Optional[Match]:
    """Get a match by ID"""
    return db.query(Match).filter(Match.id == match_id).first()

def get_match_with_details(db: Session, match_id: int) -> Optional[Dict]:
    """Get a match with all related details"""
    # Create aliases for joins
    home_franchise = aliased(Franchise)
    away_franchise = aliased(Franchise)
    home_team = aliased(Team)
    away_team = aliased(Team)
    
    result = db.query(
        Match,
        Game.name.label("game_name"),
        home_franchise.name.label("home_franchise_name"),
        away_franchise.name.label("away_franchise_name"),
        home_team.name.label("home_team_name"),
        away_team.name.label("away_team_name")
    ).join(
        Game, Match.game_id == Game.id
    ).outerjoin(
        home_franchise, Match.home_franchise_id == home_franchise.id
    ).outerjoin(
        away_franchise, Match.away_franchise_id == away_franchise.id
    ).outerjoin(
        home_team, Match.home_team_id == home_team.id
    ).outerjoin(
        away_team, Match.away_team_id == away_team.id
    ).filter(Match.id == match_id).first()
    
    if not result:
        return None
    
    match, game_name, home_name, away_name, home_team_name, away_team_name = result
    
    # Get winner name if available
    winner_name = None
    if match.winner_id:
        # Check if winner is a franchise
        franchise_winner = db.query(Franchise).filter(Franchise.id == match.winner_id).first()
        if franchise_winner:
            winner_name = franchise_winner.name
        else:
            # Check if winner is a team
            team_winner = db.query(Team).filter(Team.id == match.winner_id).first()
            if team_winner:
                winner_name = team_winner.name
    
    return {
        "id": match.id,
        "game_id": match.game_id,
        "game_name": game_name,
        "home_franchise_id": match.home_franchise_id,
        "away_franchise_id": match.away_franchise_id,
        "home_franchise_name": home_name,
        "away_franchise_name": away_name,
        "home_team_id": match.home_team_id,
        "away_team_id": match.away_team_id,
        "home_team_name": home_team_name,
        "away_team_name": away_team_name,
        "match_date": match.match_date,
        "status": match.status,
        "location": match.location,
        "round": match.round,
        "score_summary": match.score_summary,
        "winner_id": match.winner_id,
        "winner_name": winner_name,
        "extra_data": match.extra_data
    }

def update_match(db: Session, match_id: int, match_data: Union[MatchCreate, Dict[str, Any]]) -> Optional[Match]:
    """Update a match's information"""
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        return None
        
    # Handle both Pydantic models and dictionaries
    if hasattr(match_data, 'model_dump'):
        # It's a Pydantic model
        update_data = match_data.model_dump(exclude_unset=True)
    else:
        # It's already a dictionary
        update_data = match_data
    
    # Generate AI summary if notes are provided in extra_data
    if update_data.get('extra_data') and isinstance(update_data['extra_data'], dict):
        extra_data = update_data['extra_data']
        
        # Check if notes exist and ai_summary is empty or not provided
        if extra_data.get('notes') and not extra_data.get('ai_summary'):
            try:
                # Create a prompt for match summary
                notes = extra_data['notes']
                prompt = f"Summarize this match report in 2-3 concise sentences focusing on key highlights and outcome: {notes}"
                
                # Get AI summary
                ai_summary = get_chat_completion(prompt)
                if ai_summary:
                    extra_data['ai_summary'] = ai_summary
                    update_data['extra_data'] = extra_data
                    
            except Exception as e:
                # Log the error but don't fail the update
                print(f"Failed to generate AI summary: {e}")
                # Set a fallback message
                extra_data['ai_summary'] = "AI summary generation failed"
    
    # Update match fields
    for field, value in update_data.items():
        if hasattr(db_match, field) and value is not None:
            setattr(db_match, field, value)
    
    
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, match_id: int) -> bool:
    """Delete a match"""
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        return False
        
    db.delete(db_match)
    db.commit()
    return True

# Match Player services
def add_player_to_match(db: Session, match_player: MatchPlayerCreate) -> MatchPlayer:
    """Add a player to a match"""
    db_match_player = MatchPlayer(
        match_id=match_player.match_id,
        player_id=match_player.player_id,
        franchise_id=match_player.franchise_id,
        points_earned=match_player.points_earned,
        is_winner=match_player.is_winner,
        extra_data=match_player.extra_data
    )
    
    db.add(db_match_player)
    db.commit()
    db.refresh(db_match_player)
    return db_match_player

def update_match_result(db: Session, match_player_id: int, update_data: MatchPlayerUpdate) -> Optional[MatchPlayer]:
    """Update match results for a player"""
    db_match_player = db.query(MatchPlayer).filter(MatchPlayer.id == match_player_id).first()
    if not db_match_player:
        return None
        
    # Update fields
    if update_data.points_earned is not None:
        db_match_player.points_earned = update_data.points_earned
    
    if update_data.is_winner is not None:
        db_match_player.is_winner = update_data.is_winner
    
    if update_data.extra_data:
        # Update extra_data without overwriting existing data
        if not db_match_player.extra_data:
            db_match_player.extra_data = {}
        db_match_player.extra_data.update(update_data.extra_data)
    

    db.commit()
    
    # Update player total points if this was a win
    if db_match_player.is_winner and db_match_player.points_earned > 0:
        player = db.query(Player).filter(Player.id == db_match_player.player_id).first()
        if player:
            player.total_points += db_match_player.points_earned
            db.commit()
    
    db.refresh(db_match_player)
    return db_match_player

def get_match_players(db: Session, match_id: int) -> List[Dict[str, Any]]:
    """Get all players in a match with details"""
    match_players = db.query(MatchPlayer).filter(MatchPlayer.match_id == match_id).all()
    
    result = []
    for mp in match_players:
        # Get player details
        player = db.query(Player).filter(Player.id == mp.player_id).first()
        franchise = db.query(Franchise).filter(Franchise.id == mp.franchise_id).first()
        
        result.append({
            "id": mp.id,
            "match_id": mp.match_id,
            "player_id": mp.player_id,
            "player_name": player.name if player else None,
            "franchise_id": mp.franchise_id,
            "franchise_name": franchise.name if franchise else None,
            "points_earned": mp.points_earned,
            "is_winner": mp.is_winner,
    
    
            "extra_data": mp.extra_data
        })
    
    return result

def update_match_player_result(db: Session, match_player_id: int, update_data: MatchPlayerUpdate) -> Optional[MatchPlayer]:
    """Update match results for a player"""
    db_match_player = db.query(MatchPlayer).filter(MatchPlayer.id == match_player_id).first()
    if not db_match_player:
        return None
        
    # Update fields
    if update_data.points_earned is not None:
        db_match_player.points_earned = update_data.points_earned
    
    if update_data.is_winner is not None:
        db_match_player.is_winner = update_data.is_winner
    
    if update_data.extra_data:
        # Update extra_data without overwriting existing data
        if not db_match_player.extra_data:
            db_match_player.extra_data = {}
        db_match_player.extra_data.update(update_data.extra_data)
    

    db.commit()
    
    # Update player total points if this was a win
    if db_match_player.is_winner and db_match_player.points_earned > 0:
        player = db.query(Player).filter(Player.id == db_match_player.player_id).first()
        if player:
            player.total_points += db_match_player.points_earned
            db.commit()
    
    db.refresh(db_match_player)
    return db_match_player

# Gallery services
async def add_gallery_image(db: Session, gallery_data: GalleryCreate, image: UploadFile) -> Gallery:
    """Add an image to the gallery"""
    image_path = await upload_image_to_storage(image, "gallery")
    
    db_gallery = Gallery(
        title=gallery_data.title,
        description=gallery_data.description,
        image_path=image_path,
        match_id=gallery_data.match_id,
        extra_data=gallery_data.extra_data
    )
    
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery

def get_gallery_images(db: Session, skip: int = 0, limit: int = 100, match_id: Optional[int] = None) -> List[Gallery]:
    """Get gallery images, optionally filtered by match"""
    query = db.query(Gallery)
    if match_id:
        query = query.filter(Gallery.match_id == match_id)
    return query.offset(skip).limit(limit).all()

def delete_gallery_image(db: Session, image_id: int) -> bool:
    """Delete an image from the gallery"""
    db_image = db.query(Gallery).filter(Gallery.id == image_id).first()
    if not db_image:
        return False
        
    # Delete from storage
    if db_image.image_path:
        delete_image_from_storage(db_image.image_path)
    
    db.delete(db_image)
    db.commit()
    return True

def list_s3_gallery_images() -> List[str]:
    """List all images from the S3 gallery folder (or local folder)"""
    return list_images_from_storage("gallery")

# Leaderboard services
def get_player_leaderboard(db: Session, limit: int = 10, game_id: Optional[int] = None) -> List[Dict]:
    """Get player leaderboard based on total points"""
    query = db.query(Player)
    if game_id:
        # Filter players who have played matches in the specific game
        query = query.join(MatchPlayer).join(Match).filter(Match.game_id == game_id).distinct()
    
    players = query.order_by(Player.total_points.desc()).limit(limit).all()
    
    result = []
    for player in players:
        # Count matches played, won, and lost, optionally filtered by game
        match_player_query = db.query(MatchPlayer).filter(MatchPlayer.player_id == player.id)
        if game_id:
            match_player_query = match_player_query.join(Match).filter(Match.game_id == game_id)
        
        matches_played = match_player_query.count()
        matches_won = match_player_query.filter(MatchPlayer.is_winner == True).count()
        matches_lost = matches_played - matches_won
        
        # Get franchise name if available
        franchise_name = None
        if player.franchise_id:
            franchise = db.query(Franchise).filter(Franchise.id == player.franchise_id).first()
            if franchise:
                franchise_name = franchise.name
                
        result.append({
            "id": player.id,
            "name": player.name,
            "franchise_id": player.franchise_id,
            "franchise_name": franchise_name,
            "total_points": player.total_points,
            "matches_played": matches_played,
            "matches_won": matches_won,
            "matches_lost": matches_lost
        })
    
    return result

def get_franchise_leaderboard(db: Session, limit: int = 10, game_id: Optional[int] = None) -> List[Dict]:
    """Get franchise leaderboard based on total points of players"""
    franchises = db.query(Franchise).all()
    
    franchise_stats = []
    for franchise in franchises:
        # Get all players in this franchise
        players_query = db.query(Player).filter(Player.franchise_id == franchise.id)
        if game_id:
            # Filter players who have played matches in the specific game
            players_query = players_query.join(MatchPlayer).join(Match).filter(Match.game_id == game_id).distinct()
        
        players = players_query.all()
        
        # Calculate total points from matches, optionally filtered by game
        total_points = 0
        matches_won = 0
        total_matches_played = 0
        
        for player in players:
            match_query = db.query(MatchPlayer).filter(MatchPlayer.player_id == player.id)
            if game_id:
                match_query = match_query.join(Match).filter(Match.game_id == game_id)
            
            player_points = match_query.with_entities(
                func.sum(MatchPlayer.points_earned)
            ).scalar() or 0
            total_points += player_points
            
            player_matches_played = match_query.count()
            total_matches_played += player_matches_played
            
            player_wins = match_query.filter(MatchPlayer.is_winner == True).count()
            matches_won += player_wins
        
        matches_lost = total_matches_played - matches_won
        
        # Count teams in franchise
        teams_query = db.query(Team).filter(Team.franchise_id == franchise.id)
        if game_id:
            teams_query = teams_query.filter(Team.game_id == game_id)
        teams_count = teams_query.count()
        
        franchise_stats.append({
            "id": franchise.id,
            "name": franchise.name,
            "total_points": total_points,
            "players_count": len(players),
            "teams_count": teams_count,
            "matches_played": total_matches_played,
            "matches_won": matches_won,
            "matches_lost": matches_lost
        })
    
    # Sort by total points
    franchise_stats.sort(key=lambda x: x["total_points"], reverse=True)
    return franchise_stats[:limit]

# Team services
def create_team(db: Session, team: TeamCreate) -> Team:
    """Create a new team under a franchise for a specific game"""
    db_team = Team(
        name=team.name,
        franchise_id=team.franchise_id,
        game_id=team.game_id,
        extra_data=team.extra_data
    )
    
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, skip: int = 0, limit: int = 100, franchise_id: Optional[int] = None, 
             game_id: Optional[int] = None) -> List[Team]:
    """Get all teams, optionally filtered by franchise and/or game"""
    query = db.query(Team)
    if franchise_id:
        query = query.filter(Team.franchise_id == franchise_id)
    if game_id:
        query = query.filter(Team.game_id == game_id)
    return query.offset(skip).limit(limit).all()

def get_team(db: Session, team_id: int) -> Optional[Team]:
    """Get a team by ID"""
    return db.query(Team).filter(Team.id == team_id).first()

def update_team(db: Session, team_id: int, team_data: Union[TeamCreate, Dict[str, Any]]) -> Optional[Team]:
    """Update a team's information"""
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        return None
        
    # Handle both Pydantic models and dictionaries
    if hasattr(team_data, 'model_dump'):
        # It's a Pydantic model
        update_data = team_data.model_dump(exclude_unset=True)
    else:
        # It's already a dictionary
        update_data = team_data
    
    # Update team fields
    for field, value in update_data.items():
        if hasattr(db_team, field) and value is not None:
            setattr(db_team, field, value)
    
    
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int) -> bool:
    """Delete a team"""
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        return False
        
    db.delete(db_team)
    db.commit()
    return True

def get_teams_by_franchise(db: Session, franchise_id: int) -> List[Team]:
    """Get all teams for a specific franchise"""
    return db.query(Team).filter(Team.franchise_id == franchise_id).all()

def get_teams_by_game(db: Session, game_id: int) -> List[Team]:
    """Get all teams for a specific game"""
    return db.query(Team).filter(Team.game_id == game_id).all()

def get_teams_with_details(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    """Get teams with their franchise and game details"""
    return db.query(Team).options(
        joinedload(Team.franchise),
        joinedload(Team.game)
    ).offset(skip).limit(limit).all()

# Team Player services
def add_player_to_team(db: Session, team_player: TeamPlayerCreate) -> TeamPlayer:
    """Add a player to a team"""
    db_team_player = TeamPlayer(
        team_id=team_player.team_id,
        player_id=team_player.player_id,
        extra_data=team_player.extra_data
    )
    
    db.add(db_team_player)
    db.commit()
    db.refresh(db_team_player)
    return db_team_player

def get_team_players(db: Session, team_id: int) -> List[Dict[str, Any]]:
    """Get all players in a team with details"""
    team_players = db.query(TeamPlayer).filter(TeamPlayer.team_id == team_id).all()
    
    result = []
    for tp in team_players:
        # Get player details
        player = db.query(Player).filter(Player.id == tp.player_id).first()
        if player:
            result.append({
                "team_player_id": tp.id,
                "player_id": player.id,
                "player_name": player.name,
                "player_email": player.email,
                "total_points": player.total_points,
                "extra_data": tp.extra_data
            })
    
    return result

def remove_player_from_team(db: Session, team_player_id: int) -> bool:
    """Remove a player from a team"""
    db_team_player = db.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).first()
    if not db_team_player:
        return False
        
    db.delete(db_team_player)
    db.commit()
    return True

def get_player_teams(db: Session, player_id: int) -> List[Dict[str, Any]]:
    """Get all teams that a player belongs to"""
    team_players = db.query(TeamPlayer).filter(TeamPlayer.player_id == player_id).all()
    
    result = []
    for tp in team_players:
        # Get team details
        team = db.query(Team).filter(Team.id == tp.team_id).first()
        if team:
            # Get franchise and game details
            franchise = db.query(Franchise).filter(Franchise.id == team.franchise_id).first()
            game = db.query(Game).filter(Game.id == team.game_id).first()
            
            result.append({
                "team_player_id": tp.id,
                "team_id": team.id,
                "team_name": team.name,
                "franchise_name": franchise.name if franchise else None,
                "game_name": game.name if game else None,
                "extra_data": tp.extra_data
            })
    
    return result

def get_team_leaderboard(db: Session, limit: int = 10, game_id: Optional[int] = None) -> List[Dict]:
    """Get team leaderboard based on total points"""
    query = db.query(Team)
    if game_id:
        query = query.filter(Team.game_id == game_id)
    
    teams = query.all()
    team_stats = []
    
    for team in teams:
        # Get total points from team players in matches
        total_points = db.query(MatchPlayer).join(
            TeamPlayer, MatchPlayer.player_id == TeamPlayer.player_id
        ).filter(
            TeamPlayer.team_id == team.id
        ).with_entities(
            func.sum(MatchPlayer.points_earned)
        ).scalar() or 0
        
        # Get matches played and won by team players
        matches_played = db.query(MatchPlayer).join(
            TeamPlayer, MatchPlayer.player_id == TeamPlayer.player_id
        ).filter(
            TeamPlayer.team_id == team.id
        ).count()
        
        matches_won = db.query(MatchPlayer).join(
            TeamPlayer, MatchPlayer.player_id == TeamPlayer.player_id
        ).filter(
            TeamPlayer.team_id == team.id,
            MatchPlayer.is_winner == True
        ).count()
        
        matches_lost = matches_played - matches_won
        
        # Get players count
        players_count = db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).count()
        
        # Get franchise and game details
        franchise = db.query(Franchise).filter(Franchise.id == team.franchise_id).first()
        game = db.query(Game).filter(Game.id == team.game_id).first()
        
        team_stats.append({
            "id": team.id,
            "name": team.name,
            "franchise_name": franchise.name if franchise else None,
            "game_name": game.name if game else None,
            "total_points": int(total_points),
            "players_count": players_count,
            "matches_played": matches_played,
            "matches_won": matches_won,
            "matches_lost": matches_lost
        })
    
    # Sort by total points
    team_stats.sort(key=lambda x: x["total_points"], reverse=True)
    return team_stats[:limit]

# Fixture services
def get_fixtures(db: Session, skip: int = 0, limit: int = 100, game_id: Optional[int] = None,
                status: Optional[str] = None, franchise_id: Optional[int] = None, round: Optional[str] = None) -> List[FixtureDetail]:
    """Get fixtures (matches with team/franchise details)"""
    # Base query for matches
    query = db.query(Match)
    
    # Apply filters
    if game_id:
        query = query.filter(Match.game_id == game_id)
    if status:
        query = query.filter(Match.status == status)
    if franchise_id:
        query = query.filter(
            (Match.home_franchise_id == franchise_id) | (Match.away_franchise_id == franchise_id)
        )
    if round:
        query = query.filter(Match.round == round)
    
    # Get matches
    matches = query.offset(skip).limit(limit).all()
    
    # Fetch related data for each match
    fixtures = []
    for match in matches:
        # Get game details
        game = db.query(Game).filter(Game.id == match.game_id).first()
        
        # Get franchise details
        home_franchise = None
        away_franchise = None
        if match.home_franchise_id:
            home_franchise = db.query(Franchise).filter(Franchise.id == match.home_franchise_id).first()
        if match.away_franchise_id:
            away_franchise = db.query(Franchise).filter(Franchise.id == match.away_franchise_id).first()
            
        # Get team details if applicable
        home_team = None
        away_team = None
        if match.home_team_id:
            home_team = db.query(Team).filter(Team.id == match.home_team_id).first()
        if match.away_team_id:
            away_team = db.query(Team).filter(Team.id == match.away_team_id).first()
        
        # Get winner details
        winner = None
        if match.winner_id:
            # Check if winner is a franchise
            winner_franchise = db.query(Franchise).filter(Franchise.id == match.winner_id).first()
            if winner_franchise:
                winner = {"type": "franchise", "id": winner_franchise.id, "name": winner_franchise.name}
            else:
                # Check if winner is a team
                winner_team = db.query(Team).filter(Team.id == match.winner_id).first()
                if winner_team:
                    winner = {"type": "team", "id": winner_team.id, "name": winner_team.name}
            
        # Create fixture detail
        fixture = FixtureDetail(
            id=match.id,
            game_id=match.game_id,
            game_name=game.name if game else None,
            home_franchise_id=match.home_franchise_id,
            home_franchise_name=home_franchise.name if home_franchise else None,
            away_franchise_id=match.away_franchise_id,
            away_franchise_name=away_franchise.name if away_franchise else None,
            home_team_id=match.home_team_id,
            home_team_name=home_team.name if home_team else None,
            away_team_id=match.away_team_id,
            away_team_name=away_team.name if away_team else None,
            home_team={"id": home_team.id, "name": home_team.name} if home_team else None,
            away_team={"id": away_team.id, "name": away_team.name} if away_team else None,
            match_date=match.match_date,
            status=match.status,
            location=match.location,
            score_summary=match.score_summary,
            winner_id=match.winner_id,
            winner=winner,
            round=match.round,
            extra_data=match.extra_data
        )
        fixtures.append(fixture)
        
    return fixtures

def get_leaderboard(db: Session, game_id: Optional[int] = None) -> Dict:
    """Get combined player and franchise leaderboard"""
    return {
        "player_leaderboard": get_player_leaderboard(db, game_id=game_id),
        "franchise_leaderboard": get_franchise_leaderboard(db, game_id=game_id),
        "team_leaderboard": get_team_leaderboard(db, game_id=game_id)
    }