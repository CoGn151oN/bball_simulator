import pandas as pd
import numpy as np
import random

# set home and away effectiveness
home_effectiveness = 0.7
away_effectiveness = 0.3

# read in the player stats data
player_stats = pd.read_csv('player_stats.csv')

# add row numbers
player_stats.insert(0, 'Row', range(1, 1 + len(player_stats)))


# simulate a possession
def simulate_possession(offense, defense):
    # calculate the offense's expected effective field goal percentage
    off_efg = (offense['eFG%'] + defense['DREB%']) / 2
    # adjust for home/away
    if offense['Team'] == 'Home':
        off_efg *= home_effectiveness
    else:
        off_efg *= away_effectiveness
    # calculate the defense's expected defensive rebound percentage
    def_drb = (defense['DREB%'] + offense['OREB%']) / 2
    # calculate the expected number of offensive rebounds by the offense
    off_orb = (offense['OREB%'] / 100) * (1 - off_efg) * (offense['2PTA-R'] + offense['3PTA-R'])
    # calculate the expected number of turnovers by the offense
    off_to = (offense['TO-R'] / 100) * (offense['2PTA-R'] + offense['3PTA-R'])
    # calculate the expected number of shots by the offense
    off_fga = offense['2PTA-R'] + offense['3PTA-R'] + off_orb - off_to
    # calculate the expected number of made shots by the offense
    off_fgm = off_fga * off_efg
    # adjust for home/away
    if defense['Team'] == 'Home':
        off_fgm *= away_effectiveness
    else:
        off_fgm *= home_effectiveness
    # calculate the expected number of missed shots by the offense
    off_miss = off_fga - off_fgm
    # calculate the expected number of defensive rebounds by the defense
    def_drbn = (defense['DREB%'] / 100) * off_miss
    # calculate the expected number of possessions
    poss = off_fga + off_to - off_orb + def_drbn
    # calculate the expected number of points scored by the offense
    off_pts = 2 * off_fgm + 3 * (off_fga - off_fgm)
    # adjust for home/away
    if offense['Team'] == 'Home':
        off_pts *= home_effectiveness
    else:
        off_pts *= away_effectiveness
    # calculate the expected number of points scored by the defense
    def_pts = 2 * def_drbn + 3 * (def_drb - def_drbn)
    # adjust for home/away
    if defense['Team'] == 'Home':
        def_pts *= away_effectiveness
    else:
        def_pts *= home_effectiveness
    return {'poss': poss, 'off_pts': off_pts, 'def_pts': def_pts}


# simulate the game
def simulate_game(home_players, away_players):
    # initialize the score
    home_score = 0
    away_score = 0
    # simulate 100 possessions
    for i in range(100):
        # randomly choose an offense and a defense
        if i % 2 == 0:
            offense_players = home_players
            defense_players = away_players
            home_team = True
        else:
            offense_players = away_players
            defense_players = home_players
            home_team = False
        # calculate the possession outcome
        outcome = simulate_possession(offense_players, defense_players, home_team)
        # update the score
        if home_team:
            home_score += outcome
        else:
            away_score += outcome
    # return the final score
    return home_score, away_score


# simulate 10,000 games
home_wins = 0
away_wins = 0
for i in range(10000):
    # randomly choose 5 home players and 5 away players
    home_players = random.sample(list(player_data[player_data['Team'] == 'Home'].index), 5)
    away_players = random.sample(list(player_data[player_data['Team'] == 'Away'].index), 5)
    # simulate the game
    home_score, away_score = simulate_game(home_players, away_players)
    # update the win counts
    if home_score > away_score:
        home_wins += 1
    else:
        away_wins += 1

# print the win probabilities
print('Home win probability:', home_wins / (home_wins + away_wins))
print('Away win probability:', away_wins / (home_wins + away_wins))
