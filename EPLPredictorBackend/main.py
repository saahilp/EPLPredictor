import asyncio
import aiohttp
import xlrd
import numpy
import flask
import json

from understat import Understat
from teamClass import Team
from result import Result
from json import JSONEncoder
from table import TableEntry, Table

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/results', methods=['GET'])
def get_results():
    book_results = xlrd.open_workbook('PLResults.xlsx')
    sheet_results = book_results.sheet_by_index(0)

    teams = []

    for i in range(1, sheet_results.nrows):
        home_team_name = sheet_results.cell(i, 0).value
        away_team_name = sheet_results.cell(i, 1).value
        home_team_xg = sheet_results.cell(i, 2).value
        away_team_xg = sheet_results.cell(i, 3).value
        home_team_poss = sheet_results.cell(i, 4).value
        away_team_poss = sheet_results.cell(i, 5).value

        if not any(team.name == home_team_name for team in teams):
            teams.append(Team(home_team_name))
        if not any(team.name == away_team_name for team in teams):
            teams.append(Team(away_team_name))

        for team in teams:
            if team.name == home_team_name:
                team.add_result(Result(float(home_team_xg), float(away_team_xg), float(home_team_poss), True))
            if team.name == away_team_name:
                team.add_result(Result(float(away_team_xg), float(home_team_xg), float(away_team_poss), False))

    book_fixtures = xlrd.open_workbook('PLFixtures.xlsx')
    sheet_fixtures = book_fixtures.sheet_by_index(0)
    resultsList = []

    for i in range(1, sheet_fixtures.nrows):
        home_team_name = sheet_fixtures.cell(i, 0).value
        away_team_name = sheet_fixtures.cell(i, 1).value
        fixture_date = sheet_fixtures.cell(i, 2).value

        homeTeam = [team for team in teams if team.name == home_team_name]
        awayTeam = [team for team in teams if team.name == away_team_name]

        homeTeam[0].calculate_metrics()
        homeStats = homeTeam[0].get_avg_stats()
        homeRatio = homeTeam[0].diffInRation()
        homeTeam[0].create_curves()

        awayTeam[0].calculate_metrics()
        awayStats = awayTeam[0].get_avg_stats()
        awayRatio = awayTeam[0].diffInRation()
        awayTeam[0].create_curves()

        homePossRaw = homeStats[0] * homeRatio[2]
        awayPossRaw = awayStats[0] * awayRatio[5]

        homePoss = (homePossRaw / (homePossRaw + awayPossRaw)) * 100
        awayPoss = 100 - homePoss

        homeScoreArr = homeTeam[0].predict(homePoss)
        homeScores = [homeScoreArr[0] * homeRatio[0], homeScoreArr[1] * homeRatio[1]]

        awayScoreArr = awayTeam[0].predict(awayPoss)
        awayScores = [awayScoreArr[0] * awayRatio[3], awayScoreArr[1] * awayRatio[4]]

        homeScore = (homeScores[0] + awayScores[1]) / 2
        awayScore = (homeScores[1] + awayScores[0]) / 2

        homeTeam[0].add_result(Result(float(homeScore), float(awayScore), float(homePoss), True))
        awayTeam[0].add_result(Result(float(awayScore), float(homeScore), float(awayPoss), False))

        # print(home_team_name, numpy.round(homeScore), away_team_name, numpy.round(awayScore))
        resultsList.append([home_team_name, numpy.round(homeScore), away_team_name, numpy.round(awayScore)])

    return json.dumps({"results": resultsList}, cls=NumpyArrayEncoder)


@app.route('/api/table', methods=['GET'])
def get_table():
    table = Table()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    league_table = loop.run_until_complete(load_table())

    for i in range(1, len(league_table)):
        curr_team = league_table[i]
        table.add_team(curr_team[0], curr_team[2], curr_team[3], curr_team[4], curr_team[5], curr_team[6], curr_team[7])

    league_results = json.loads(get_results())

    for result in league_results['results']:
        if result[1][0] > result[3][0]:
            table.add_result(result[0], 'W', result[1][0], result[3][0])
            table.add_result(result[2], 'L', result[3][0], result[1][0])

        elif result[1][0] == result[3][0]:
            table.add_result(result[0], 'D', result[1][0], result[3][0])
            table.add_result(result[2], 'D', result[3][0], result[1][0])

        else:
            table.add_result(result[0], 'L', result[1][0], result[3][0])
            table.add_result(result[2], 'W', result[3][0], result[1][0])

    return json.dumps({'table': table.get_table()}, default=lambda o: o.__dict__, indent=4)


async def load_table():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        # call to get results for 20/21
        table = await understat.get_league_table(
            "epl", 2020,
        )
        return table


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


get_table()
app.run()
