import asyncio
import xlsxwriter

import aiohttp

from understat import Understat
from datetime import datetime


# get fixtures from Understat

async def get_fixtures():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        # call to get fixtures for 20/21
        fixtures = await understat.get_league_fixtures(
            "epl", 2020,
        )
        return fixtures


if __name__ == '__main__':

    # running async function defined above
    loop = asyncio.get_event_loop()
    league_fixtures = loop.run_until_complete(get_fixtures())

    # create excel file to write into
    workbook = xlsxwriter.Workbook('PLFixtures.xlsx')
    worksheet = workbook.add_worksheet()

    # add column headers
    worksheet.write(0, 0, 'Home Team')
    worksheet.write(0, 1, 'Away Team')
    worksheet.write(0, 2, 'Date')

    # define starting cells to write into
    row = 1
    col = 0

    for fixture in league_fixtures:
        # add home and away teams to row
        worksheet.write(row, col, fixture['h']['title'])
        worksheet.write(row, col + 1, fixture['a']['title'])
        # format date to a more readable format and write to cell
        d = datetime.strptime(fixture['datetime'], "%Y-%m-%d %H:%M:%S")
        worksheet.write(row, col + 2, d.strftime("%b %d %Y"))
        # move to the next row
        row += 1

    workbook.close()
