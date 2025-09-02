import sys
import os
import random
from datetime import datetime, timedelta
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from codebase.database import SessionLocal
from codebase.model.request_model_updated import (
    Game, Franchise, Player, Team, TeamPlayer, Match, MatchPlayer
)

# Game types
GAME_TYPES = ["Individual", "Team", "Mixed"]

# Sample game data
GAMES = [
    {"name": "Table Tennis", "description": "Indoor table tennis competition", "winning_points": 11, "game_type": "Individual"},
    {"name": "Chess", "description": "Strategic board game", "winning_points": 1, "game_type": "Individual"},
    {"name": "Carrom", "description": "Indoor board game", "winning_points": 29, "game_type": "Individual"},
    {"name": "Cricket", "description": "Team sport with bat and ball", "winning_points": 2, "game_type": "Team"},
    {"name": "Football", "description": "Team sport with a ball", "winning_points": 3, "game_type": "Team"},
    {"name": "Badminton", "description": "Racquet sport", "winning_points": 21, "game_type": "Mixed"}
]

# Sample franchise data
FRANCHISES = [
    {"name": "AM&C Warriors", "extra_data": {"color": "blue", "motto": "Strength in Unity"}},
    {"name": "DFO&I Titans", "extra_data": {"color": "red", "motto": "Rise Above All"}},
    {"name": "IT Services Wolves", "extra_data": {"color": "green", "motto": "Technology Hunters"}},
    {"name": "HR Hurricanes", "extra_data": {"color": "yellow", "motto": "Force of Nature"}},
    {"name": "Finance Falcons", "extra_data": {"color": "purple", "motto": "Soaring High"}}
]

# Sample player data - names and franchise assignment
PLAYERS = [
    # AM&C Warriors
    {"name": "Alex Johnson", "email": "alex.j@example.com", "franchise_id": 1},
    {"name": "Maria Rodriguez", "email": "maria.r@example.com", "franchise_id": 1},
    {"name": "David Chen", "email": "david.c@example.com", "franchise_id": 1},
    {"name": "Sarah Kim", "email": "sarah.k@example.com", "franchise_id": 1},
    {"name": "James Wilson", "email": "james.w@example.com", "franchise_id": 1},
    # DFO&I Titans
    {"name": "Emma Brown", "email": "emma.b@example.com", "franchise_id": 2},
    {"name": "Michael Davis", "email": "michael.d@example.com", "franchise_id": 2},
    {"name": "Sophia Martinez", "email": "sophia.m@example.com", "franchise_id": 2},
    {"name": "Daniel Taylor", "email": "daniel.t@example.com", "franchise_id": 2},
    {"name": "Olivia Anderson", "email": "olivia.a@example.com", "franchise_id": 2},
    # IT Services Wolves
    {"name": "William Thomas", "email": "william.t@example.com", "franchise_id": 3},
    {"name": "Isabella Jackson", "email": "isabella.j@example.com", "franchise_id": 3},
    {"name": "Ethan White", "email": "ethan.w@example.com", "franchise_id": 3},
    {"name": "Charlotte Harris", "email": "charlotte.h@example.com", "franchise_id": 3},
    {"name": "Liam Martin", "email": "liam.m@example.com", "franchise_id": 3},
    # HR Hurricanes
    {"name": "Ava Thompson", "email": "ava.t@example.com", "franchise_id": 4},
    {"name": "Noah Garcia", "email": "noah.g@example.com", "franchise_id": 4},
    {"name": "Mia Robinson", "email": "mia.r@example.com", "franchise_id": 4},
    {"name": "Jacob Lewis", "email": "jacob.l@example.com", "franchise_id": 4},
    {"name": "Amelia Walker", "email": "amelia.w@example.com", "franchise_id": 4},
    # Finance Falcons
    {"name": "Benjamin Hall", "email": "benjamin.h@example.com", "franchise_id": 5},
    {"name": "Emily Young", "email": "emily.y@example.com", "franchise_id": 5},
    {"name": "Lucas King", "email": "lucas.k@example.com", "franchise_id": 5},
    {"name": "Abigail Wright", "email": "abigail.w@example.com", "franchise_id": 5},
    {"name": "Henry Scott", "email": "henry.s@example.com", "franchise_id": 5}
]

# Define team roles
TEAM_ROLES = ["Captain", "Vice Captain", "Player", "Substitute"]

def create_sample_data(db: Session):
    print("Creating sample data...")

    # Create games
    games = []
    for game_data in GAMES:
        game = Game(
            name=game_data["name"],
            description=game_data["description"],
            winning_points=game_data["winning_points"],
            game_type=game_data["game_type"]
        )
        db.add(game)
        games.append(game)
    
    db.commit()
    print(f"Created {len(games)} games")

    # Create franchises
    franchises = []
    for franchise_data in FRANCHISES:
        franchise = Franchise(
            name=franchise_data["name"],
            extra_data=franchise_data["extra_data"]
        )
        db.add(franchise)
        franchises.append(franchise)
    
    db.commit()
    print(f"Created {len(franchises)} franchises")

    # Create players
    players = []
    for player_data in PLAYERS:
        player = Player(
            name=player_data["name"],
            email=player_data["email"],
            franchise_id=player_data["franchise_id"]
        )
        db.add(player)
        players.append(player)
    
    db.commit()
    print(f"Created {len(players)} players")

    # Create teams for team-based games
    teams = []
    for game in games:
        if game.game_type in ["Team", "Mixed"]:
            for franchise in franchises:
                team_name = f"{franchise.name} {game.name}"
                team = Team(
                    name=team_name,
                    franchise_id=franchise.id,
                    game_id=game.id
                )
                db.add(team)
                teams.append(team)
    
    db.commit()
    print(f"Created {len(teams)} teams")

    # Assign players to teams
    team_players = []
    for team in teams:
        # Get players from the team's franchise
        franchise_players = [p for p in players if p.franchise_id == team.franchise_id]
        
        # Select 4-6 random players for the team
        num_players = random.randint(4, min(6, len(franchise_players)))
        selected_players = random.sample(franchise_players, num_players)
        
        # Assign roles
        captain = selected_players[0]
        vice_captain = selected_players[1]
        
        # Create team player assignments
        for i, player in enumerate(selected_players):
            role = "Captain" if player == captain else "Vice Captain" if player == vice_captain else "Player"
            team_player = TeamPlayer(
                team_id=team.id,
                player_id=player.id,
                role=role
            )
            db.add(team_player)
            team_players.append(team_player)
    
    db.commit()
    print(f"Assigned players to teams with {len(team_players)} team player entries")

    # Create matches
    matches = []
    
    # Team matches
    team_games = [g for g in games if g.game_type in ["Team", "Mixed"]]
    for game in team_games:
        game_teams = [t for t in teams if t.game_id == game.id]
        
        # Group teams by franchise
        teams_by_franchise = {}
        for team in game_teams:
            if team.franchise_id not in teams_by_franchise:
                teams_by_franchise[team.franchise_id] = []
            teams_by_franchise[team.franchise_id].append(team)
        
        # Create matches between different franchises
        franchise_ids = list(teams_by_franchise.keys())
        for i in range(len(franchise_ids)):
            for j in range(i+1, len(franchise_ids)):
                home_franchise_id = franchise_ids[i]
                away_franchise_id = franchise_ids[j]
                
                home_team = teams_by_franchise[home_franchise_id][0]
                away_team = teams_by_franchise[away_franchise_id][0]
                
                # Create future and past matches
                # Past match (completed)
                past_date = datetime.now() - timedelta(days=random.randint(1, 30))
                past_match = Match(
                    game_id=game.id,
                    home_franchise_id=home_franchise_id,
                    away_franchise_id=away_franchise_id,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    match_date=past_date,
                    status="completed",
                    location=f"Field {random.randint(1, 5)}",
                    score_summary=f"{random.randint(0, 5)}-{random.randint(0, 5)}"
                )
                
                # Determine winner
                if random.choice([True, False]):
                    past_match.winner_id = home_team.id
                else:
                    past_match.winner_id = away_team.id
                
                db.add(past_match)
                matches.append(past_match)
                
                # Future match (scheduled)
                future_date = datetime.now() + timedelta(days=random.randint(1, 30))
                future_match = Match(
                    game_id=game.id,
                    home_franchise_id=away_franchise_id,  # Swap home and away
                    away_franchise_id=home_franchise_id,
                    home_team_id=away_team.id,
                    away_team_id=home_team.id,
                    match_date=future_date,
                    status="scheduled",
                    location=f"Field {random.randint(1, 5)}"
                )
                db.add(future_match)
                matches.append(future_match)
    
    # Individual matches
    individual_games = [g for g in games if g.game_type == "Individual"]
    for game in individual_games:
        # Create matches between players from different franchises
        for i in range(len(franchises)):
            for j in range(i+1, len(franchises)):
                home_franchise = franchises[i]
                away_franchise = franchises[j]
                
                # Past match (completed)
                past_date = datetime.now() - timedelta(days=random.randint(1, 30))
                past_match = Match(
                    game_id=game.id,
                    home_franchise_id=home_franchise.id,
                    away_franchise_id=away_franchise.id,
                    match_date=past_date,
                    status="completed",
                    location=f"Room {random.randint(101, 110)}",
                    score_summary=f"{random.randint(0, 21)}-{random.randint(0, 21)}"
                )
                
                # Determine winner
                if random.choice([True, False]):
                    past_match.winner_id = home_franchise.id
                else:
                    past_match.winner_id = away_franchise.id
                
                db.add(past_match)
                matches.append(past_match)
                
                # Future match (scheduled)
                future_date = datetime.now() + timedelta(days=random.randint(1, 30))
                future_match = Match(
                    game_id=game.id,
                    home_franchise_id=away_franchise.id,  # Swap home and away
                    away_franchise_id=home_franchise.id,
                    match_date=future_date,
                    status="scheduled",
                    location=f"Room {random.randint(101, 110)}"
                )
                db.add(future_match)
                matches.append(future_match)
    
    db.commit()
    print(f"Created {len(matches)} matches")
    
    # Add match players for completed matches
    match_players = []
    for match in matches:
        if match.status == "completed":
            # Determine the winner franchise/team
            winner_id = match.winner_id
            
            if match.home_team_id and match.away_team_id:
                # Team match
                home_team_players = db.query(TeamPlayer).filter(TeamPlayer.team_id == match.home_team_id).all()
                away_team_players = db.query(TeamPlayer).filter(TeamPlayer.team_id == match.away_team_id).all()
                
                # Add home team players
                for tp in home_team_players[:min(5, len(home_team_players))]:
                    is_winner = match.winner_id == match.home_team_id
                    points = random.randint(1, 5) if is_winner else random.randint(0, 2)
                    
                    mp = MatchPlayer(
                        match_id=match.id,
                        player_id=tp.player_id,
                        franchise_id=match.home_franchise_id,
                        team_id=match.home_team_id,
                        points_earned=points,
                        is_winner=is_winner
                    )
                    db.add(mp)
                    match_players.append(mp)
                
                # Add away team players
                for tp in away_team_players[:min(5, len(away_team_players))]:
                    is_winner = match.winner_id == match.away_team_id
                    points = random.randint(1, 5) if is_winner else random.randint(0, 2)
                    
                    mp = MatchPlayer(
                        match_id=match.id,
                        player_id=tp.player_id,
                        franchise_id=match.away_franchise_id,
                        team_id=match.away_team_id,
                        points_earned=points,
                        is_winner=is_winner
                    )
                    db.add(mp)
                    match_players.append(mp)
            
            else:
                # Individual match - select 1-2 players from each franchise
                home_players = [p for p in players if p.franchise_id == match.home_franchise_id]
                away_players = [p for p in players if p.franchise_id == match.away_franchise_id]
                
                num_players = random.randint(1, 2)
                selected_home = random.sample(home_players, min(num_players, len(home_players)))
                selected_away = random.sample(away_players, min(num_players, len(away_players)))
                
                # Add home franchise players
                for player in selected_home:
                    is_winner = match.winner_id == match.home_franchise_id
                    points = random.randint(1, 5) if is_winner else random.randint(0, 2)
                    
                    mp = MatchPlayer(
                        match_id=match.id,
                        player_id=player.id,
                        franchise_id=match.home_franchise_id,
                        points_earned=points,
                        is_winner=is_winner
                    )
                    db.add(mp)
                    match_players.append(mp)
                
                # Add away franchise players
                for player in selected_away:
                    is_winner = match.winner_id == match.away_franchise_id
                    points = random.randint(1, 5) if is_winner else random.randint(0, 2)
                    
                    mp = MatchPlayer(
                        match_id=match.id,
                        player_id=player.id,
                        franchise_id=match.away_franchise_id,
                        points_earned=points,
                        is_winner=is_winner
                    )
                    db.add(mp)
                    match_players.append(mp)
    
    db.commit()
    
    # Update player total points based on match results
    for player in players:
        # Get all match player records for this player
        player_matches = db.query(MatchPlayer).filter(MatchPlayer.player_id == player.id).all()
        total_points = sum(mp.points_earned for mp in player_matches if mp.points_earned)
        
        player.total_points = total_points
    
    db.commit()
    print(f"Created {len(match_players)} match player entries and updated player scores")
    
    print("Sample data creation complete!")


def main():
    db = SessionLocal()
    try:
        create_sample_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
