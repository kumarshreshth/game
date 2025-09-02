"""Create Teams and Update Match Structure

Revision ID: 20230501_teams_match_update
Revises: 20230401_initial_migration
Create Date: 2023-05-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '20230501_teams_match_update'
down_revision = '20230401_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Create teams table
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('franchise_id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('logo_path', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('extra_data', JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['franchise_id'], ['franchises.id'], ),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create team_players table
    op.create_table(
        'team_players',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('extra_data', JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('team_id', 'player_id', name='uq_team_player')
    )
    
    # Add opponent columns to matches table
    op.add_column('matches', sa.Column('home_franchise_id', sa.Integer(), nullable=True))
    op.add_column('matches', sa.Column('away_franchise_id', sa.Integer(), nullable=True))
    op.add_column('matches', sa.Column('home_team_id', sa.Integer(), nullable=True))
    op.add_column('matches', sa.Column('away_team_id', sa.Integer(), nullable=True))
    op.add_column('matches', sa.Column('winner_id', sa.Integer(), nullable=True))
    op.add_column('matches', sa.Column('score_summary', sa.String(length=255), nullable=True))
    
    # Add foreign key constraints for matches
    op.create_foreign_key('fk_match_home_franchise', 'matches', 'franchises', ['home_franchise_id'], ['id'])
    op.create_foreign_key('fk_match_away_franchise', 'matches', 'franchises', ['away_franchise_id'], ['id'])
    op.create_foreign_key('fk_match_home_team', 'matches', 'teams', ['home_team_id'], ['id'])
    op.create_foreign_key('fk_match_away_team', 'matches', 'teams', ['away_team_id'], ['id'])
    
    # Add team_id to match_players table
    op.add_column('match_players', sa.Column('team_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_match_player_team', 'match_players', 'teams', ['team_id'], ['id'])


def downgrade():
    # Remove foreign key constraints
    op.drop_constraint('fk_match_player_team', 'match_players', type_='foreignkey')
    op.drop_column('match_players', 'team_id')
    
    op.drop_constraint('fk_match_home_franchise', 'matches', type_='foreignkey')
    op.drop_constraint('fk_match_away_franchise', 'matches', type_='foreignkey')
    op.drop_constraint('fk_match_home_team', 'matches', type_='foreignkey')
    op.drop_constraint('fk_match_away_team', 'matches', type_='foreignkey')
    
    # Remove columns from matches table
    op.drop_column('matches', 'score_summary')
    op.drop_column('matches', 'winner_id')
    op.drop_column('matches', 'away_team_id')
    op.drop_column('matches', 'home_team_id')
    op.drop_column('matches', 'away_franchise_id')
    op.drop_column('matches', 'home_franchise_id')
    
    # Drop team_players table
    op.drop_table('team_players')
    
    # Drop teams table
    op.drop_table('teams')
