"""
Sample data generator for AMC Champion League application
"""
import os
import sys
import json
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models and database utilities
from codebase.model.request_model import Base, Game, Franchise, Player, Match, MatchPlayer, Gallery
from codebase.utils.database import engine, SessionLocal
from codebase.utils.config_manager import config

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def get_db_session() -> Session:
    """Get database session"""
    return SessionLocal()

def create_games(db: Session):
    """Create sample games"""
    games = [
        {
            "name": "Badminton",
            "description": "Racquet sport played with a shuttlecock",
            "winning_points": 15,
            "game_type": "badminton",
            "extra_data": {
                "scoring_system": "rally point",
                "sets": 3,
                "points_per_set": 21
            }
        },
        {
            "name": "Table Tennis",
            "description": "Played on a table with paddles and a lightweight ball",
            "winning_points": 12,
            "game_type": "table_tennis",
            "extra_data": {
                "scoring_system": "rally point",
                "sets": 5,
                "points_per_set": 11
            }
        },
        {
            "name": "Pool",
            "description": "Cue sport played on a table with pockets",
            "winning_points": 10,
            "game_type": "pool",
            "extra_data": {
                "game_variant": "8-ball",
                "frames_per_match": 3
            }
        },
        {
            "name": "Carom",
            "description": "Strike and pocket board game",
            "winning_points": 8,
            "game_type": "carom",
            "extra_data": {
                "points_to_win": 29,
                "rounds_per_match": 3
            }
        },
        {
            "name": "Pickle ball",
            "description": "Paddle sport combining elements of tennis, badminton and table tennis",
            "winning_points": 13,
            "game_type": "pickleball",
            "extra_data": {
                "scoring_system": "rally point",
                "sets": 3,
                "points_per_set": 11
            }
        },
        {
            "name": "Chess",
            "description": "Strategic board game played on a checkered gameboard",
            "winning_points": 10,
            "game_type": "chess",
            "extra_data": {
                "time_control": "15+10",
                "scoring": {"win": 1, "draw": 0.5, "loss": 0}
            }
        },
        {
            "name": "Box Cricket",
            "description": "Modified version of cricket played in a confined space",
            "winning_points": 20,
            "game_type": "box_cricket",
            "extra_data": {
                "overs_per_side": 5,
                "players_per_team": 6
            }
        },
        {
            "name": "Foosball",
            "description": "Table game based on football/soccer",
            "winning_points": 10,
            "game_type": "foosball",
            "extra_data": {
                "goals_to_win": 10,
                "max_time": 15  # minutes
            }
        }
    ]
    
    for game_data in games:
        game = Game(
            name=game_data["name"],
            description=game_data["description"],
            winning_points=game_data["winning_points"],
            game_type=game_data["game_type"],
            image_path=f"/images/games/{game_data['name'].lower().replace(' ', '_')}.jpg",
            extra_data=game_data["extra_data"]
        )
        db.add(game)
    
    db.commit()
    print("Sample games created")

def create_franchises(db: Session):
    """Create sample franchises"""
    franchises = [
        {
            "name": "AM&C WARRIORS",
            "extra_data": {
                "primary_color": "blue",
                "team_slogan": "Brave Hearts, Bold Victories"
            }
        },
        {
            "name": "S&S SUPER KINGS",
            "extra_data": {
                "primary_color": "yellow",
                "team_slogan": "Rule the Game, Reign Supreme"
            }
        },
        {
            "name": "DFO&I TITANS",
            "extra_data": {
                "primary_color": "red",
                "team_slogan": "Strength in Unity, Glory in Victory"
            }
        },
        {
            "name": "CD&D DAREDEVILS",
            "extra_data": {
                "primary_color": "purple",
                "team_slogan": "Fearless in Play, Relentless in Spirit"
            }
        }
    ]
    
    for franchise_data in franchises:
        franchise = Franchise(
            name=franchise_data["name"],
            logo_path=f"/images/franchises/{franchise_data['name'].lower().replace('&', '').replace(' ', '_')}.png",
            extra_data=franchise_data["extra_data"]
        )
        db.add(franchise)
    
    db.commit()
    print("Sample franchises created")

def create_players(db: Session):
    """Create sample players"""
    # Get franchise IDs
    franchises = db.query(Franchise).all()
    franchise_ids = [f.id for f in franchises]
    
    # Generate random names
    first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Lisa", 
                  "William", "Jessica", "Richard", "Olivia", "Thomas", "Emma", "Daniel", "Sophia",
                  "James", "Ava", "Matthew", "Mia", "Andrew", "Amelia", "Charles", "Isabella"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
                 "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee"]
    
    # Create 10 players per franchise (40 total)
    players = []
    for franchise_id in franchise_ids:
        for i in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            
            # Create player
            player = Player(
                name=name,
                franchise_id=franchise_id,
                email=f"{first_name.lower()}.{last_name.lower()}@example.com",
                profile_image_path=f"/images/players/player_{franchise_id}_{i+1}.jpg",
                total_points=random.randint(0, 100),
                extra_data={
                    "age": random.randint(22, 45),
                    "years_in_company": random.randint(1, 15),
                    "favorite_games": random.sample(["Badminton", "Table Tennis", "Pool", "Carom", 
                                                    "Pickle ball", "Chess", "Box Cricket", "Foosball"], 
                                                    k=random.randint(1, 3))
                }
            )
            players.append(player)
    
    db.add_all(players)
    db.commit()
    print("Sample players created")

def create_matches(db: Session):
    """Create sample matches"""
    # Get game IDs
    games = db.query(Game).all()
    game_ids = [(g.id, g.name) for g in games]
    
    # Get players grouped by franchise
    franchises = db.query(Franchise).all()
    franchise_players = {}
    for franchise in franchises:
        players = db.query(Player).filter(Player.franchise_id == franchise.id).all()
        franchise_players[franchise.id] = players
    
    # Create 5 matches per game (40 total)
    matches = []
    match_players = []
    
    # Start date for matches (2 weeks ago)
    start_date = datetime.now() - timedelta(days=14)
    
    for game_id, game_name in game_ids:
        for i in range(5):
            # Randomly select match date between start_date and now
            days_offset = random.randint(0, 13)
            match_date = start_date + timedelta(days=days_offset)
            
            # Randomly select status
            status = random.choice(["scheduled", "in_progress", "completed"])
            if match_date > datetime.now():
                status = "scheduled"
            elif match_date.date() == datetime.now().date():
                status = random.choice(["scheduled", "in_progress"])
            else:
                status = "completed"
            
            # Create match
            match = Match(
                game_id=game_id,
                match_date=match_date,
                status=status,
                location=f"Conference Room {random.choice('ABCDE')}",
                extra_data={
                    "referee": f"Referee {random.randint(1, 5)}",
                    "notes": f"Sample match {i+1} for {game_name}"
                }
            )
            matches.append(match)
    
    db.add_all(matches)
    db.commit()
    print("Sample matches created")
    
    # Now add players to matches
    matches = db.query(Match).all()
    for match in matches:
        # Get game to determine player count
        game = db.query(Game).filter(Game.id == match.game_id).first()
        
        # Determine number of players per side based on game type
        if game.name == "Box Cricket":
            players_per_team = 6
        elif game.name in ["Badminton", "Table Tennis", "Pool", "Chess", "Foosball"]:
            players_per_team = 2
        else:
            players_per_team = 1
        
        # Randomly select two franchises for the match
        match_franchises = random.sample(list(franchise_players.keys()), 2)
        
        # Add players from each franchise
        for franchise_id in match_franchises:
            # Randomly select players from the franchise
            selected_players = random.sample(franchise_players[franchise_id], 
                                           min(players_per_team, len(franchise_players[franchise_id])))
            
            # Determine winner (if match is completed)
            is_winner = False
            points_earned = 0
            
            if match.status == "completed":
                # First franchise has 60% chance of winning
                if franchise_id == match_franchises[0] and random.random() < 0.6:
                    is_winner = True
                    points_earned = game.winning_points
                # Second franchise has 40% chance of winning
                elif franchise_id == match_franchises[1] and random.random() < 0.4:
                    is_winner = True
                    points_earned = game.winning_points
            
            # Create match players
            for player in selected_players:
                # Generate game-specific score data
                score_data = generate_game_score(game.game_type, is_winner)
                
                match_player = MatchPlayer(
                    match_id=match.id,
                    player_id=player.id,
                    franchise_id=franchise_id,
                    points_earned=points_earned if is_winner else 0,
                    is_winner=is_winner,
                    extra_data={
                        "position": f"Player {random.randint(1, players_per_team)}",
                        "score_data": score_data
                    }
                )
                match_players.append(match_player)
                
                # Update player's total points if they won
                if is_winner:
                    player.total_points += points_earned
    
    db.add_all(match_players)
    db.commit()
    print("Players added to matches")

def generate_game_score(game_type, is_winner):
    """Generate random score data for a game"""
    if game_type == "badminton":
        # Generate sets scores
        if is_winner:
            sets = [
                {"player1": 21, "player2": random.randint(10, 19)},
                {"player1": random.randint(10, 19), "player2": 21},
                {"player1": 21, "player2": random.randint(10, 19)}
            ]
            final_result = {"player1": 2, "player2": 1}
        else:
            sets = [
                {"player1": random.randint(10, 19), "player2": 21},
                {"player1": 21, "player2": random.randint(10, 19)},
                {"player1": random.randint(10, 19), "player2": 21}
            ]
            final_result = {"player1": 1, "player2": 2}
        return {"sets": sets, "final_result": final_result}
    
    elif game_type == "table_tennis":
        # Generate sets scores
        if is_winner:
            sets = [
                {"player1": 11, "player2": random.randint(5, 9)},
                {"player1": 11, "player2": random.randint(5, 9)},
                {"player1": random.randint(5, 9), "player2": 11},
                {"player1": 11, "player2": random.randint(5, 9)}
            ]
            final_result = {"player1": 3, "player2": 1}
        else:
            sets = [
                {"player1": random.randint(5, 9), "player2": 11},
                {"player1": random.randint(5, 9), "player2": 11},
                {"player1": 11, "player2": random.randint(5, 9)},
                {"player1": random.randint(5, 9), "player2": 11}
            ]
            final_result = {"player1": 1, "player2": 3}
        return {"sets": sets, "final_result": final_result}
    
    elif game_type == "chess":
        if is_winner:
            return {
                "result": "win",
                "moves": random.randint(20, 60),
                "time_remaining": f"{random.randint(1, 10)}:{random.randint(0, 59):02d}"
            }
        else:
            result = random.choice(["loss", "resignation"])
            return {
                "result": result,
                "moves": random.randint(15, 40),
                "time_remaining": f"{random.randint(0, 5)}:{random.randint(0, 59):02d}"
            }
    
    elif game_type == "pool":
        if is_winner:
            frames = [
                {"player1": 1, "player2": 0},
                {"player1": 0, "player2": 1},
                {"player1": 1, "player2": 0}
            ]
            final_result = {"player1": 2, "player2": 1}
        else:
            frames = [
                {"player1": 0, "player2": 1},
                {"player1": 1, "player2": 0},
                {"player1": 0, "player2": 1}
            ]
            final_result = {"player1": 1, "player2": 2}
        return {"frames": frames, "final_result": final_result}
    
    elif game_type == "carom":
        if is_winner:
            rounds = [
                {"player1": random.randint(20, 29), "player2": random.randint(15, 25)},
                {"player1": random.randint(20, 29), "player2": random.randint(15, 25)},
            ]
            final_result = {"player1": 2, "player2": 0}
        else:
            rounds = [
                {"player1": random.randint(15, 25), "player2": random.randint(20, 29)},
                {"player1": random.randint(15, 25), "player2": random.randint(20, 29)},
            ]
            final_result = {"player1": 0, "player2": 2}
        return {"rounds": rounds, "final_result": final_result}
    
    elif game_type == "box_cricket":
        if is_winner:
            innings = [
                {"team1": random.randint(50, 90), "team1_wickets": random.randint(2, 5), "team1_overs": "5.0"},
                {"team2": random.randint(30, 49), "team2_wickets": random.randint(3, 6), "team2_overs": "5.0"}
            ]
            final_result = {"winner": "team1", "margin": f"{random.randint(10, 40)} runs"}
        else:
            innings = [
                {"team1": random.randint(40, 60), "team1_wickets": random.randint(3, 6), "team1_overs": "5.0"},
                {"team2": random.randint(61, 90), "team2_wickets": random.randint(1, 4), "team2_overs": "4.3"}
            ]
            final_result = {"winner": "team2", "margin": f"{6 - random.randint(1, 5)} wickets"}
        return {"innings": innings, "final_result": final_result}
    
    elif game_type == "foosball":
        if is_winner:
            return {
                "goals": {"team1": 10, "team2": random.randint(4, 8)},
                "final_result": f"10-{random.randint(4, 8)}"
            }
        else:
            return {
                "goals": {"team1": random.randint(4, 8), "team2": 10},
                "final_result": f"{random.randint(4, 8)}-10"
            }
    
    elif game_type == "pickleball":
        if is_winner:
            sets = [
                {"player1": 11, "player2": random.randint(5, 9)},
                {"player1": 11, "player2": random.randint(5, 9)}
            ]
            final_result = {"player1": 2, "player2": 0}
        else:
            sets = [
                {"player1": random.randint(5, 9), "player2": 11},
                {"player1": random.randint(5, 9), "player2": 11}
            ]
            final_result = {"player1": 0, "player2": 2}
        return {"sets": sets, "final_result": final_result}
    
    # Default generic score data
    return {"notes": "Generic game score"}

def create_gallery_images(db: Session):
    """Create sample gallery entries"""
    # Get match IDs
    matches = db.query(Match).all()
    
    gallery_entries = []
    for i, match in enumerate(matches):
        if i % 3 == 0:  # Only create gallery for every third match
            # Get game name
            game = db.query(Game).filter(Game.id == match.game_id).first()
            
            # Create 2-3 gallery entries for the match
            num_images = random.randint(2, 3)
            for j in range(num_images):
                title = f"{game.name} Match Highlight {j+1}"
                description = f"Action shot from {game.name} match on {match.match_date.strftime('%Y-%m-%d')}"
                
                gallery = Gallery(
                    title=title,
                    description=description,
                    image_path=f"/images/gallery/match_{match.id}_image_{j+1}.jpg",
                    match_id=match.id,
                    extra_data={
                        "photographer": f"Photographer {random.randint(1, 3)}",
                        "tags": [game.name.lower(), "action", "highlights"]
                    }
                )
                gallery_entries.append(gallery)
    
    db.add_all(gallery_entries)
    db.commit()
    print("Sample gallery entries created")

def create_sample_data():
    """Create all sample data"""
    db = get_db_session()
    
    try:
        create_tables()
        create_games(db)
        create_franchises(db)
        create_players(db)
        create_matches(db)
        create_gallery_images(db)
        
        print("All sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
