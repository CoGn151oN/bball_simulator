import random

# Home and away effectiveness percentages
HOME_EFFECTIVENESS = 0.7
AWAY_EFFECTIVENESS = 0.3


# Define a class for a basketball player
class Player:
    def __init__(self, name, team, gp, minutes_played, efg, ts, oreb, dreb, reb, ast_to, ast_r, to_r, twopta_r,
                 threepta_r, ft_rt):
        self.name = name
        self.team = team
        self.gp = gp
        self.minutes_played = minutes_played
        self.efg = efg
        self.ts = ts
        self.oreb = oreb
        self.dreb = dreb
        self.reb = reb
        self.ast_to = ast_to
        self.ast_r = ast_r
        self.to_r = to_r
        self.twopta_r = twopta_r
        self.threepta_r = threepta_r
        self.ft_rt = ft_rt

    # Calculate the player's effectiveness in a home or away game
    def get_effectiveness(self, is_home_game):
        if is_home_game:
            return self.efg * HOME_EFFECTIVENESS + self.ts * (1 - HOME_EFFECTIVENESS)
        else:
            return self.efg * AWAY_EFFECTIVENESS + self.ts * (1 - AWAY_EFFECTIVENESS)


# Define a class for a basketball team
class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    # Calculate the team's effectiveness in a home or away game
    def get_effectiveness(self, is_home_game):
        return sum([player.get_effectiveness(is_home_game) for player in self.players]) / len(self.players)


# Define a function to simulate a possession
def simulate_possession(offense, defense):
    # Calculate the total effectiveness of the offense and defense
    off_effectiveness = offense.get_effectiveness(is_home_game)
    def_effectiveness = defense.get_effectiveness(not is_home_game)

    # Calculate the probability that the offense scores on this possession
    probability = off_effectiveness / (off_effectiveness + def_effectiveness)

    # Simulate the possession
    if random.random() < probability:
        return True  # Offense scored
    else:
        return False  # Offense missed or turned the ball over


# Define a function to simulate a full game
def simulate_game(home_team, away_team):
    home_score = 0
    away_score = 0

    # Determine which team is the home team
    is_home_game = random.choice([True, False])

    # Simulate 100 possessions for each team
    for i in range(100):
        if is_home_game:
            home_possession = simulate_possession(home_team, away_team)
            if home_possession:
                home_score += 1
            else:
                away_possession = simulate_possession(away_team, home_team)
                if away_possession:
                    away_score += 1
        else:
            away_possession = simulate_possession(away_team, home_team)
            if away_possession:
                away_score += 1
            else:
                home_possession = simulate_possession(home_team, away_team)
                if home_possession:
                    home_score += 1

        # Flip possession for the next round
        is_home_game = not is_home_game

    return home_score, away
