import asyncio
import aiohttp
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

async def fetch_status(session, url, username, status_type):
    query = """
        query($username: String) {
        MediaListCollection(userName: $username, type: ANIME, status: %s) {
            lists {
            entries {
                media {
                title {
                    romaji
                    english
                }
                format
                episodes
                genres
                siteUrl
                }
                status
                progress
                score
            }
            }
        }
        }
        """ % (status_type)
    variables = {"username": username}

    async with session.post(url, json={'query': query, 'variables': variables}) as response:
        if response.status != 200:
            print(f"Error: API request failed with status code {response.status}")
            print("Response text:", await response.text())
            return []

        data = await response.json()
        lists = data.get("data", {}).get("MediaListCollection", {}).get("lists", [{}])
        if len(lists) == 0:
            return []
        return lists[0].get("entries", [])

async def export_xlsx():
    wb = Workbook()
    ws = wb.active
    if ws is None:
        ws = wb.create_sheet()
    ws.append(["Romaji", "Format", "Status", "Progress/Episodes", "Genres", "Score"])

    url = "https://graphql.anilist.co"
    username = input("Enter your Anilist username: ")
    if username == "":
        print("Username not provided!")
        return
    output = input("Enter output path [anime_list.xlsx]: ") or "anime_list.xlsx"
    status = [
        "CURRENT",
        "COMPLETED",
        "PLANNING",
        "PAUSED",
        "DROPPED",
        "REPEATING"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, url, username, status_type) for status_type in status]
        results = await asyncio.gather(*tasks)

        for data in results:
            for anime in data:
                anime["media"]["genres"] = str(anime["media"]["genres"]).replace("[", "").replace("]", "").replace("'", "")
                ws.append([
                    anime["media"]["title"]["romaji"],
                    anime["media"]["format"],
                    anime["status"],
                    f"{anime['progress']}/{anime['media']['episodes']}",
                    anime["media"]["genres"],
                    anime["score"],
                ])
                last_row = ws.max_row
                title_cell = ws.cell(row=last_row, column=1)
                title_cell.hyperlink = anime["media"]["siteUrl"]
                title_cell.style = "Hyperlink"
                title_cell.font = Font(name='Noto Sans')

    for col_num in range(1, ws.max_column + 1):
        max_length = 0
        col_letter = get_column_letter(col_num)

        for row_num in range(1, ws.max_row + 1):
            cell_value = ws.cell(row=row_num, column=col_num).value
            if cell_value:
                max_length = max(max_length, len(str(cell_value)))
        ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(output)

def main():
    asyncio.run(export_xlsx())

if __name__ == "__main__":
    main()
