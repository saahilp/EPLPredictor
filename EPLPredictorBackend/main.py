import csv
import asyncio
import aiohttp


from understat import Understat
from teamClass import Team
from result import Result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('PLResultsFormat.csv') as fp:
        reader = csv.reader(fp, delimiter=",")
        dfs = [row for row in reader]

    teams = []

    for i in range(1, len(dfs)):
        if not any(team.name == dfs[i][0] for team in teams):
            teams.append(Team(dfs[i][0]))
        if not any(team.name == dfs[i][1] for team in teams):
            teams.append(Team(dfs[i][1]))

        for team in teams:
            if team.name == dfs[i][0]:
                team.add_result(Result(float(dfs[i][2]), float(dfs[i][3]), float(dfs[i][4]), True))
            if team.name == dfs[i][1]:
                awayTeam = team.add_result(Result(float(dfs[i][3]), float(dfs[i][2]), float(dfs[i][5]), False))
    homeTeam = [team for team in teams if team.name == 'Liverpool']
    awayTeam = [team for team in teams if team.name == 'Newcastle United']

    homeTeam[0].calculate_metrics()
    homeStats = homeTeam[0].get_avg_stats()
    homeRatio = homeTeam[0].diffInRation()
    homeTeam[0].create_curves()

    awayTeam[0].calculate_metrics()
    awayStats = awayTeam[0].get_avg_stats()
    awayRatio = awayTeam[0].diffInRation()
    awayTeam[0].create_curves()

    homePossRaw = homeStats[0] * homeRatio[2]
    awayPossRaw = 45.17  # awayStats[0] * awayRatio[5]

    homePoss = (homePossRaw / (homePossRaw + awayPossRaw)) * 100
    awayPoss = 100 - homePoss

    homeScore = homeTeam[0].predict(homePoss)
    homeScore1 = [homeScore[0] * homeRatio[0], homeScore[1] * homeRatio[1]]

    awayScore = awayTeam[0].predict(awayPoss)
    awayScore1 = [awayScore[0] * awayRatio[3], awayScore[1] * awayRatio[4]]

    print(homeScore1, awayScore1)

    print("Done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
