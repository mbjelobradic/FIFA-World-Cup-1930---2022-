import pandas as pd
import os

# Load dataset
file_path = 'C:/Users/Matija/Desktop/portfolio/projekti/world cup/world_cup_matches.csv'
df = pd.read_csv(file_path)

# Create a new DataFrame to store team and total goals
team_goals = pd.DataFrame()

# Concatenate home and away goals for each team
team_goals['Total Goals'] = df.groupby('Home Team')['Home Goals'].sum() + df.groupby('Away Team')['Away Goals'].sum()

# Reset the index and rename the team column
team_goals = team_goals.reset_index()
team_goals = team_goals.rename(columns={'index': 'Team'})

# Calculate summarized points, wins, ties, and losses
points = []
wins = []
ties = []
losses = []
total_goals_conceded = []
played_games = []

for team in team_goals['Team']:
    team_points = 0
    team_wins = 0
    team_ties = 0
    team_losses = 0
    goals_conceded = 0
    games_played = 0
    
    for idx, row in df.iterrows():
        if row['Home Team'] == team:
            goals_scored = row['Home Goals']
            goals_conceded += row['Away Goals']
            games_played += 1
            
            if goals_scored > row['Away Goals']:
                team_points += 3
                team_wins += 1
            elif goals_scored == row['Away Goals']:
                team_points += 1
                team_ties += 1
            else:
                team_losses += 1
                
        elif row['Away Team'] == team:
            goals_scored = row['Away Goals']
            goals_conceded += row['Home Goals']
            games_played += 1
            
            if goals_scored > row['Home Goals']:
                team_points += 3
                team_wins += 1
            elif goals_scored == row['Home Goals']:
                team_points += 1
                team_ties += 1
            else:
                team_losses += 1
                
        if team in [row['Home Team'], row['Away Team']] and row['Penalties'] == team:
            team_points += 2  # Add 2 points for penalties

    points.append(team_points)
    wins.append(team_wins)
    ties.append(team_ties)
    losses.append(team_losses)
    total_goals_conceded.append(goals_conceded)
    played_games.append(games_played)

# Add columns to team_goals DataFrame
team_goals['Points'] = points
team_goals['Wins'] = wins
team_goals['Ties'] = ties
team_goals['Losses'] = losses
team_goals['Goals Conceded'] = total_goals_conceded
team_goals['Games Played'] = played_games

# Display the summarized results
print("Total Goals, Goals Conceded, Played Games, Points, Wins, Ties, and Losses by Team:")
print(team_goals)

# Export DataFrame to CSV
export_path = 'transformed_world_cup_data.csv'
team_goals.to_csv(export_path, index=False)

