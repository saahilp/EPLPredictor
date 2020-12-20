import asyncio
import aiohttp


from understat import Understat
from openpyxl import load_workbook


async def load_results():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_results(
            "epl", 2020,
        )
        return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    league_results = loop.run_until_complete(load_results())
    book = load_workbook('PLResults.xlsx')
    sheet = book.active
    for result in league_results:
        print(result['xG']['h'])
        sheet.append((result['h']['title'], result['a']['title'], result['xG']['h'], result['xG']['a']))
    book.save('PLResults.xlsx')