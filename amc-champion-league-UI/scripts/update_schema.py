"""
Migration script to update the database schema for match opponents and team structure
"""
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
from datetime import datetime

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import both old and new models
from codebase.model.request_model_updated import Base as NewBase
from codebase.utils.database import DATABASE_URL, engine, SessionLocal

def upgrade():
    """
    Apply the migration to update the database schema
    """
    print("Starting database schema migration...")
    
    # Create a connection to the database
    engine = create_engine(DATABASE_URL)
    
    # Create a session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Create the new tables
        print("Creating new tables...")
        NewBase.metadata.create_all(bind=engine)
        
        # Migrate data from old tables to new tables if needed
        print("Migrating data to new schema...")
        
        # Execute raw SQL to add columns to match table
        connection = engine.connect()
        
        # Check if columns already exist before adding them
        result = connection.execute(text("PRAGMA table_info(match)"))
        columns = [column[1] for column in result.fetchall()]
        
        if "home_franchise_id" not in columns:
            print("Adding home_franchise_id column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN home_franchise_id INTEGER REFERENCES franchise(id)"))
        
        if "away_franchise_id" not in columns:
            print("Adding away_franchise_id column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN away_franchise_id INTEGER REFERENCES franchise(id)"))
        
        if "home_team_id" not in columns:
            print("Adding home_team_id column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN home_team_id INTEGER REFERENCES team(id)"))
        
        if "away_team_id" not in columns:
            print("Adding away_team_id column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN away_team_id INTEGER REFERENCES team(id)"))
        
        if "score_summary" not in columns:
            print("Adding score_summary column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN score_summary TEXT"))
        
        if "winner_id" not in columns:
            print("Adding winner_id column to match table...")
            connection.execute(text("ALTER TABLE match ADD COLUMN winner_id INTEGER"))
        
        # Check if match_player table has team_id column
        result = connection.execute(text("PRAGMA table_info(match_player)"))
        columns = [column[1] for column in result.fetchall()]
        
        if "team_id" not in columns:
            print("Adding team_id column to match_player table...")
            connection.execute(text("ALTER TABLE match_player ADD COLUMN team_id INTEGER REFERENCES team(id)"))
        
        connection.close()
        
        print("Schema migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

def create_example_teams():
    """
    Create example teams for each franchise and game
    """
    print("Creating example teams for each franchise and game...")
    
    # Create a session
    session = SessionLocal()
    
    try:
        from codebase.model.request_model_updated import Franchise, Game, Team
        
        # Get all franchises and games
        franchises = session.query(Franchise).all()
        games = session.query(Game).all()
        
        teams_created = 0
        
        # Create a team for each franchise-game combination
        for franchise in franchises:
            for game in games:
                # Check if team already exists
                team_exists = session.query(Team).filter(
                    Team.franchise_id == franchise.id,
                    Team.game_id == game.id
                ).first()
                
                if not team_exists:
                    # Create team name: e.g., "AM&C Warriors Tennis Team"
                    team_name = f"{franchise.name} {game.name} Team"
                    
                    # Create the team
                    new_team = Team(
                        name=team_name,
                        franchise_id=franchise.id,
                        game_id=game.id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    
                    session.add(new_team)
                    teams_created += 1
        
        session.commit()
        print(f"Created {teams_created} new teams")
        
    except Exception as e:
        print(f"Error creating teams: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    upgrade()
    create_example_teams()
