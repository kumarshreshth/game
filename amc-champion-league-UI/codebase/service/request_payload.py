from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import json

# Base schemas with optional fields where appropriate

class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    winning_points: Optional[int] = 10
    image_path: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class FranchiseBase(BaseModel):
    name: str
    franchise_code: Optional[str] = None
    logo_path: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class FranchiseCreate(FranchiseBase):
    pass

class Franchise(FranchiseBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class TeamBase(BaseModel):
    name: str
    franchise_id: int
    game_id: int
    logo_path: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class TeamWithDetails(Team):
    franchise_name: str
    game_name: str

class TeamPlayerBase(BaseModel):
    team_id: int
    player_id: int
    is_captain: Optional[bool] = False
    extra_data: Optional[Dict[str, Any]] = None

class TeamPlayerCreate(BaseModel):
    team_id: int
    player_id: int
    role: Optional[str] = "member"  # Default role is "member"
    extra_data: Optional[Dict[str, Any]] = None

class TeamPlayer(TeamPlayerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PlayerBase(BaseModel):
    name: str
    franchise_id: Optional[int] = None
    email: Optional[str] = None
    profile_image_path: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    total_points: int
    
    model_config = ConfigDict(from_attributes=True)

# Legacy model for compatibility
class AddPlayerRequest(BaseModel):
    player_name: str
    player_team: str
    player_email: str

class MatchBase(BaseModel):
    game_id: int
    home_franchise_id: Optional[int] = None
    away_franchise_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    match_date: Optional[str] = None  # Date in YYYY-MM-DD format
    match_time: Optional[str] = None  # Time in HH:MM format
    status: Optional[str] = "scheduled"
    location: Optional[str] = None
    round: Optional[str] = None  # Tournament round (Quarter Finals, Semi Finals, Finals)
    score_summary: Optional[str] = None
    winner_id: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class MatchWithOpponents(Match):
    home_franchise_name: Optional[str] = None
    away_franchise_name: Optional[str] = None
    home_team_name: Optional[str] = None
    away_team_name: Optional[str] = None
    game_name: str
    winner_name: Optional[str] = None

class MatchPlayerBase(BaseModel):
    match_id: int
    player_id: int
    franchise_id: Optional[int] = None
    team_id: Optional[int] = None
    points_earned: Optional[int] = 0
    is_winner: Optional[bool] = False
    extra_data: Optional[Dict[str, Any]] = None

class MatchPlayerCreate(MatchPlayerBase):
    pass

class MatchPlayerUpdate(BaseModel):
    points_earned: Optional[int] = None
    is_winner: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None

class MatchPlayer(MatchPlayerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class GalleryBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_path: str
    match_id: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None

class GalleryCreate(GalleryBase):
    pass

class Gallery(GalleryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Additional schemas for specific responses

class PlayerLeaderboardEntry(BaseModel):
    id: int
    name: str
    franchise_id: Optional[int] = None
    franchise_name: Optional[str] = None
    total_points: int
    matches_played: int
    matches_won: int
    
    model_config = ConfigDict(from_attributes=True)

class FranchiseLeaderboardEntry(BaseModel):
    id: int
    name: str
    total_points: int
    players_count: int
    matches_won: int
    
    model_config = ConfigDict(from_attributes=True)

class TeamLeaderboardEntry(BaseModel):
    id: int
    name: str
    franchise_id: int
    franchise_name: str
    game_id: int
    game_name: str
    total_points: int
    matches_played: int
    matches_won: int
    
    model_config = ConfigDict(from_attributes=True)

class Leaderboard(BaseModel):
    player_leaderboard: List[PlayerLeaderboardEntry]
    franchise_leaderboard: List[FranchiseLeaderboardEntry]
    team_leaderboard: Optional[List[TeamLeaderboardEntry]] = None

# Fixture schema for match display
class FixtureDetail(BaseModel):
    id: int
    game_id: int
    game_name: Optional[str] = None
    home_franchise_id: Optional[int] = None
    home_franchise_name: Optional[str] = None
    away_franchise_id: Optional[int] = None
    away_franchise_name: Optional[str] = None
    home_team_id: Optional[int] = None
    home_team_name: Optional[str] = None
    away_team_id: Optional[int] = None
    away_team_name: Optional[str] = None
    home_team: Optional[Dict[str, Any]] = None  # Make this optional
    away_team: Optional[Dict[str, Any]] = None  # Make this optional
    match_date: Optional[str] = None  # Date in YYYY-MM-DD format
    match_time: Optional[str] = None  # Time in HH:MM format
    status: Optional[str] = "scheduled"
    location: Optional[str] = None
    score_summary: Optional[str] = None
    winner_id: Optional[int] = None
    winner: Optional[Dict[str, Any]] = None  # Make this optional
    round: Optional[str] = None  # Tournament round
    extra_data: Optional[Dict[str, Any]] = None

# Game Score Schemas - Flexible structure to handle various game types

class BadmintonScore(BaseModel):
    sets: List[Dict[str, int]]  # [{player1: 21, player2: 19}, {player1: 19, player2: 21}]
    final_result: Dict[str, int]  # {player1: 1, player2: 1}

class TableTennisScore(BaseModel):
    sets: List[Dict[str, int]]  # Similar to badminton
    final_result: Dict[str, int]

class PoolScore(BaseModel):
    frames: List[Dict[str, int]]
    final_result: Dict[str, int]

class CaromScore(BaseModel):
    rounds: List[Dict[str, int]]
    final_result: Dict[str, int]

class ChessScore(BaseModel):
    result: str  # "win", "draw", "resignation"
    winner: Optional[str] = None
    moves: Optional[int] = None

class CricketScore(BaseModel):
    innings: List[Dict[str, Any]]  # More complex structure for cricket
    final_result: Dict[str, Any]

class FoosballScore(BaseModel):
    goals: Dict[str, int]
    final_result: Dict[str, str]

class PickleballScore(BaseModel):
    sets: List[Dict[str, int]]
    final_result: Dict[str, int]

# Generic score container - can hold any game type
class GameScore(BaseModel):
    game_type: str
    score_data: Dict[str, Any]  # Will contain the specific game score
    
    # Helper method to parse the score based on game type
    @classmethod
    def parse_score(cls, game_type: str, score_data: Dict[str, Any]) -> Any:
        score_types = {
            "badminton": BadmintonScore,
            "table_tennis": TableTennisScore, 
            "pool": PoolScore,
            "carom": CaromScore,
            "chess": ChessScore,
            "box_cricket": CricketScore,
            "foosball": FoosballScore,
            "pickleball": PickleballScore
        }
        
        if game_type.lower() in score_types:
            return score_types[game_type.lower()](**score_data)
        return score_data  # Return raw data if game type not recognized
