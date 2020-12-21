class TableEntry:
    def __init__(self, name, wins, draws, losses, goals_for, goals_conceded, points):
        self.name = name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_for = goals_for
        self.goals_conceded = goals_conceded
        self.goal_difference = goals_for - goals_conceded
        self.points = points


class Table:
    def __init__(self):
        self.leagueTable = []

    def add_result(self, name, result, goals_scored, goals_conceded):
        curr_team = [team for team in self.leagueTable if team.name == name]
        curr_team[0].goals_for += int(goals_scored)
        curr_team[0].goals_conceded += int(goals_conceded)
        curr_team[0].goal_difference += int(goals_scored) - int(goals_conceded)
        if result == 'W':
            curr_team[0].wins += 1
            curr_team[0].points += 3
        if result == 'D':
            curr_team[0].draws += 1
            curr_team[0].points += 1
        if result == 'L':
            curr_team[0].losses += 1

    def add_team(self, name, wins, draws, losses, goals_scored, goals_conceded, points):
        self.leagueTable.append(TableEntry(name, wins, draws, losses, goals_scored, goals_conceded, points))

    def get_table(self):
        return sorted(self.leagueTable, key=lambda e: (e.points, e.goal_difference), reverse=True)
