from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from codebase.model.request_model import (
    Game, Franchise, Player, Match, MatchPlayer, Gallery, Team, TeamPlayer
)
from codebase.service.request_payload import (
    GameCreate, FranchiseCreate, PlayerCreate, MatchCreate, 
    MatchPlayerCreate, GalleryCreate, TeamCreate, TeamPlayerCreate,
    FixtureDetail
)

from codebase.utils.image_storage import (
    upload_image_to_storage, list_images_from_storage, delete_image_from_storage
)

# Team CRUD Operations
def create_team(db: Session, team: TeamCreate) -> Team:
    """Create a new team"""
    db_team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db: Session, team_id: int) -> Optional[Team]:
    """Get a team by ID"""
    return db.query(Team).filter(Team.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100, 
             franchise_id: Optional[int] = None, game_id: Optional[int] = None) -> List[Team]:
    """Get all teams with pagination and optional filters"""
    query = db.query(Team)
    
    if franchise_id:
        query = query.filter(Team.franchise_id == franchise_id)
    
    if game_id:
        query = query.filter(Team.game_id == game_id)
        
    return query.offset(skip).limit(limit).all()

def get_teams_by_franchise(db: Session, franchise_id: int) -> List[Dict[str, Any]]:
    """Get all teams for a specific franchise with game info"""
    teams = db.query(
        Team, 
        Game.name.label("game_name"),
        Game.game_type.label("game_type")
    ).join(
        Game, Team.game_id == Game.id
    ).filter(
        Team.franchise_id == franchise_id
    ).all()
    
    result = []
    for team, game_name, game_type in teams:
        # Count players in each team
        player_count = db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).count()
        
        result.append({
            "id": team.id,
            "name": team.name,
            "game_id": team.game_id,
            "game_name": game_name,
            "game_type": game_type,
            "player_count": player_count,
            "logo_path": team.logo_path,
    

        })
        
    return result

def get_teams_by_game(db: Session, game_id: int) -> List[Dict[str, Any]]:
    """Get all teams for a specific game with franchise info"""
    teams = db.query(
        Team, 
        Franchise.name.label("franchise_name")
    ).join(
        Franchise, Team.franchise_id == Franchise.id
    ).filter(
        Team.game_id == game_id
    ).all()
    
    result = []
    for team, franchise_name in teams:
        # Count players in each team
        player_count = db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).count()
        
        result.append({
            "id": team.id,
            "name": team.name,
            "franchise_id": team.franchise_id,
            "franchise_name": franchise_name,
            "player_count": player_count,
            "logo_path": team.logo_path,
    
        })
        
    return result

def get_teams_with_details(db: Session, skip: int = 0, limit: int = 100) -> List[Dict]:
    """Get teams with franchise and game names"""
    teams = db.query(
        Team,
        Franchise.name.label("franchise_name"),
        Game.name.label("game_name")
    ).join(
        Franchise, Team.franchise_id == Franchise.id
    ).join(
        Game, Team.game_id == Game.id
    ).offset(skip).limit(limit).all()
    
    result = []
    for team, franchise_name, game_name in teams:
        # Create a team object with additional attributes
        team_with_details = {
            "id": team.id,
            "name": team.name,
            "franchise_id": team.franchise_id,
            "franchise_name": franchise_name,
            "game_id": team.game_id,
            "game_name": game_name,
            "logo_path": team.logo_path,
            "extra_data": team.extra_data
        }
        result.append(team_with_details)
    
    return result

def update_team(db: Session, team_id: int, team_data: Dict[str, Any]) -> Optional[Team]:
    """Update a team"""
    db_team = get_team(db, team_id)
    if db_team:
        for key, value in team_data.items():
            setattr(db_team, key, value)
    
        db.commit()
        db.refresh(db_team)
    return db_team

# Team Player Operations
def add_player_to_team(db: Session, team_player: TeamPlayerCreate) -> TeamPlayer:
    """Add a player to a team"""
    db_team_player = TeamPlayer(**team_player.model_dump())
    db.add(db_team_player)
    db.commit()
    db.refresh(db_team_player)
    return db_team_player

def get_team_players(db: Session, team_id: int) -> List[TeamPlayer]:
    """Get all players in a team"""
    return db.query(TeamPlayer).filter(TeamPlayer.team_id == team_id).all()

def get_player_teams(db: Session, player_id: int) -> List[TeamPlayer]:
    """Get all teams a player belongs to"""
    return db.query(TeamPlayer).filter(TeamPlayer.player_id == player_id).all()

def remove_player_from_team(db: Session, team_id: int, player_id: int) -> bool:
    """Remove a player from a team"""
    db_team_player = db.query(TeamPlayer).filter(
        TeamPlayer.team_id == team_id,
        TeamPlayer.player_id == player_id
    ).first()
    if db_team_player:
        db.delete(db_team_player)
        db.commit()
        return True
    return False

# Enhanced Match Operations
def create_match_with_opponents(db: Session, match: MatchCreate) -> Match:
    """Create a new match with opponents"""
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

def get_match_with_opponents(db: Session, match_id: int) -> Optional[Dict]:
    """Get a match with opponent details"""
    # Create aliases for joined tables to handle multiple joins to the same table
    HomeFranchise = aliased(Franchise)
    AwayFranchise = aliased(Franchise)
    HomeTeam = aliased(Team)
    AwayTeam = aliased(Team)
    
    result = db.query(
        Match,
        Game.name.label("game_name"),
        HomeFranchise.name.label("home_franchise_name"),
        AwayFranchise.name.label("away_franchise_name"),
        HomeTeam.name.label("home_team_name"),
        AwayTeam.name.label("away_team_name")
    ).join(
        Game, Match.game_id == Game.id
    ).outerjoin(
        HomeFranchise, Match.home_franchise_id == HomeFranchise.id
    ).outerjoin(
        AwayFranchise, Match.away_franchise_id == AwayFranchise.id
    ).outerjoin(
        HomeTeam, Match.home_team_id == HomeTeam.id
    ).outerjoin(
        AwayTeam, Match.away_team_id == AwayTeam.id
    ).filter(Match.id == match_id).first()
    
    if result:
        match, game_name, home_name, away_name, home_team_name, away_team_name = result
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
            "score_summary": match.score_summary,
            "winner_id": match.winner_id,
    
    
            "extra_data": match.extra_data
        }
    return None

def get_fixtures(db: Session, 
                skip: int = 0, 
                limit: int = 100, 
                status: Optional[str] = None,
                game_id: Optional[int] = None,
                franchise_id: Optional[int] = None) -> List[FixtureDetail]:
    """
    Get match fixtures with filtering options
    """
    # Create aliases for joined tables
    HomeFranchise = aliased(Franchise)
    AwayFranchise = aliased(Franchise)
    HomeTeam = aliased(Team)
    AwayTeam = aliased(Team)
    
    query = db.query(
        Match.id,
        Match.game_id,
        Match.home_franchise_id,
        Match.away_franchise_id,
        Match.home_team_id,
        Match.away_team_id,
        Match.match_date,
        Match.status,
        Match.location,
        Match.score_summary,
        Match.winner_id,
        Game.name.label("game_name"),
        Game.game_type.label("game_type"),
        HomeFranchise.name.label("home_franchise_name"),
        AwayFranchise.name.label("away_franchise_name"),
        HomeTeam.name.label("home_team_name"),
        AwayTeam.name.label("away_team_name")
    ).join(
        Game, Match.game_id == Game.id
    ).outerjoin(
        HomeFranchise, Match.home_franchise_id == HomeFranchise.id
    ).outerjoin(
        AwayFranchise, Match.away_franchise_id == AwayFranchise.id
    ).outerjoin(
        HomeTeam, Match.home_team_id == HomeTeam.id
    ).outerjoin(
        AwayTeam, Match.away_team_id == AwayTeam.id
    )
    
    # Apply filters if provided
    if status:
        query = query.filter(Match.status == status)
    
    if game_id:
        query = query.filter(Match.game_id == game_id)
    
    if franchise_id:
        query = query.filter(
            (Match.home_franchise_id == franchise_id) | 
            (Match.away_franchise_id == franchise_id)
        )
    
    # Get results with pagination
    results = query.order_by(Match.match_date).offset(skip).limit(limit).all()
    
    fixtures = []
    for r in results:
        fixture = FixtureDetail(
            id=r.id,
            game_id=r.game_id,
            game_name=r.game_name,
            game_type=r.game_type,
            home_franchise_id=r.home_franchise_id,
            home_franchise_name=r.home_franchise_name,
            away_franchise_id=r.away_franchise_id,
            away_franchise_name=r.away_franchise_name,
            home_team_id=r.home_team_id,
            home_team_name=r.home_team_name,
            away_team_id=r.away_team_id,
            away_team_name=r.away_team_name,
            match_date=r.match_date,
            status=r.status,
            location=r.location,
            score_summary=r.score_summary,
            winner_id=r.winner_id
        )
        fixtures.append(fixture)
    
    return fixtures

def get_team_stats(db: Session, team_id: int) -> Dict[str, Any]:
    """Get statistics for a team"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return None
        
    # Get franchise and game details
    franchise = db.query(Franchise).filter(Franchise.id == team.franchise_id).first()
    game = db.query(Game).filter(Game.id == team.game_id).first()
    
    # Get team players
    team_players = db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).all()
    player_count = len(team_players)
    
    # Get player details
    players = []
    for tp in team_players:
        player = db.query(Player).filter(Player.id == tp.player_id).first()
        if player:
            players.append({
                "id": player.id,
                "name": player.name,
                "email": player.email,
                "total_points": player.total_points,
                "role": tp.role
            })
    
    # Get match statistics
    matches = db.query(Match).filter(
        (Match.home_team_id == team.id) | (Match.away_team_id == team.id)
    ).all()
    
    matches_played = len(matches)
    matches_won = db.query(Match).filter(
        Match.winner_id == team.id
    ).count()
    
    # Calculate win rate
    win_rate = (matches_won / matches_played * 100) if matches_played > 0 else 0
    
    return {
        "id": team.id,
        "name": team.name,
        "franchise_id": team.franchise_id,
        "franchise_name": franchise.name if franchise else None,
        "game_id": team.game_id,
        "game_name": game.name if game else None,
        "game_type": game.game_type if game else None,
        "player_count": player_count,
        "players": players,
        "matches_played": matches_played,
        "matches_won": matches_won,
        "win_rate": win_rate,
        "extra_data": team.extra_data
    }
def update_match_result(db: Session, 
                       match_id: int, 
                       score_summary: str, 
                       winner_id: int,
                       extra_data: Optional[Dict[str, Any]] = None) -> Optional[Match]:
    """
    Update a match with results
    """
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if db_match:
        db_match.score_summary = score_summary
        db_match.winner_id = winner_id
        db_match.status = "completed"
    
        
        if extra_data:
            if not db_match.extra_data:
                db_match.extra_data = {}
            db_match.extra_data.update(extra_data)
        
        db.commit()
        db.refresh(db_match)
        return db_match
    
    return None
