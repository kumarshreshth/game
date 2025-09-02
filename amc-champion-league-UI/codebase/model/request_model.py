from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Game(Base):
    __tablename__ = "game"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    winning_points = Column(Integer, default=10)  # Default points for winning
    image_path = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)  # For storing game-specific scoring rules and other data
    
    # Relationships
    matches = relationship("Match", back_populates="game")
    teams = relationship("Team", back_populates="game")

class Franchise(Base):
    __tablename__ = "franchise"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    franchise_code = Column(String, nullable=True, unique=True)  # Unique franchise code
    logo_path = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)  # For storing any additional franchise data
    
    # Relationships
    players = relationship("Player", back_populates="franchise")
    match_players = relationship("MatchPlayer", back_populates="franchise")
    teams = relationship("Team", back_populates="franchise")
    # New relationships for matches
    home_matches = relationship("Match", foreign_keys="[Match.home_franchise_id]", back_populates="home_franchise")
    away_matches = relationship("Match", foreign_keys="[Match.away_franchise_id]", back_populates="away_franchise")

class Player(Base):
    __tablename__ = "player"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    franchise_id = Column(Integer, ForeignKey("franchise.id"), nullable=True)  # Optional franchise
    email = Column(String, nullable=True)
    profile_image_path = Column(String, nullable=True)
    total_points = Column(Integer, default=0)
    extra_data = Column(JSON, nullable=True)  # For storing any additional player data
    
    # Relationships
    franchise = relationship("Franchise", back_populates="players")
    match_participations = relationship("MatchPlayer", back_populates="player")
    team_memberships = relationship("TeamPlayer", back_populates="player")

class Match(Base):
    __tablename__ = "match"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    # New fields to identify both franchises in the match
    home_franchise_id = Column(Integer, ForeignKey("franchise.id"), nullable=True)
    away_franchise_id = Column(Integer, ForeignKey("franchise.id"), nullable=True)
    # New fields to identify specific teams in the match
    home_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    away_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    match_date = Column(String, nullable=True)  # Date in YYYY-MM-DD format
    match_time = Column(String, nullable=True)  # Time in HH:MM format
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    location = Column(String, nullable=True)
    score_summary = Column(String, nullable=True)  # Brief score like "21-19, 19-21, 21-18"
    winner_id = Column(Integer, nullable=True)  # ID of the winning franchise or team
    round = Column(String, nullable=True)  # Tournament round like "Semi Final", "Final", etc.
    extra_data = Column(JSON, nullable=True)  # For storing match-specific data and scoring
    
    # Relationships
    game = relationship("Game", back_populates="matches")
    # New relationships for opponent franchises
    home_franchise = relationship("Franchise", foreign_keys=[home_franchise_id], back_populates="home_matches")
    away_franchise = relationship("Franchise", foreign_keys=[away_franchise_id], back_populates="away_matches")
    # New relationships for opponent teams
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    players = relationship("MatchPlayer", back_populates="match")
    gallery_images = relationship("Gallery", back_populates="match")

class MatchPlayer(Base):
    __tablename__ = "match_player"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    franchise_id = Column(Integer, ForeignKey("franchise.id"), nullable=True)  # Optional franchise
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)  # Optional team
    points_earned = Column(Integer, default=0)
    is_winner = Column(Boolean, default=False)
    extra_data = Column(JSON, nullable=True)  # For storing game-specific scores and stats
    
    # Relationships
    match = relationship("Match", back_populates="players")
    player = relationship("Player", back_populates="match_participations")
    franchise = relationship("Franchise", back_populates="match_players")
    team = relationship("Team", foreign_keys=[team_id])

class Gallery(Base):
    __tablename__ = "gallery"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)  # Made optional
    description = Column(Text, nullable=True)
    image_path = Column(String, nullable=False)  # S3 bucket path or local path
    match_id = Column(Integer, ForeignKey("match.id"), nullable=True)  # Optional match relation
    extra_data = Column(JSON, nullable=True)  # For storing image metadata
    
    # Relationships
    match = relationship("Match", back_populates="gallery_images")

class Team(Base):
    __tablename__ = "team"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    franchise_id = Column(Integer, ForeignKey("franchise.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    logo_path = Column(String, nullable=True)
    extra_data = Column(JSON, nullable=True)  # For storing any additional team data
    
    # Relationships
    franchise = relationship("Franchise", back_populates="teams")
    game = relationship("Game", back_populates="teams")
    team_players = relationship("TeamPlayer", back_populates="team")
    # Team match relationships
    home_matches = relationship("Match", foreign_keys="[Match.home_team_id]", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="[Match.away_team_id]", back_populates="away_team")

class TeamPlayer(Base):
    __tablename__ = "team_player"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    is_captain = Column(Boolean, default=False)
    extra_data = Column(JSON, nullable=True)  # For storing any additional player-team data
    
    # Relationships
    team = relationship("Team", back_populates="team_players")
    player = relationship("Player", back_populates="team_memberships")
