import asyncio
import aiohttp
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

STATUS_ORDER = [
    "CURRENT",
    "COMPLETED",
    "PLANNING",
    "PAUSED",
    "DROPPED",
    "REPEATING"
]

async def fetch_entries(session, url, username, media_type):
    query = """
        query($username: String) {
        MediaListCollection(userName: $username, type: %s) {
            lists {
            entries {
                id
                media {
                title {
                    romaji
                    english
                }
                format
                episodes
                chapters
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
        """ % (media_type)
    variables = {"username": username}

    async with session.post(url, json={'query': query, 'variables': variables}) as response:
        if response.status != 200:
            print(f"Error: API request failed with status code {response.status}")
            print("Response text:", await response.text())
            return []

        data = await response.json()
        collection = (data.get("data") or {}).get("MediaListCollection") or {}

        entries = {}
        for media_list in collection.get("lists") or []:
            for entry in media_list.get("entries") or []:
                entries.setdefault(entry["id"], entry)

        return sorted(
            entries.values(),
            key=lambda e: STATUS_ORDER.index(e["status"]) if e["status"] in STATUS_ORDER else len(STATUS_ORDER)
        )

def fill_sheet(ws, media_type, entries):
    total_key = "episodes" if media_type == "ANIME" else "chapters"
    ws.append(["Romaji", "Format", "Status", f"Progress/{total_key.capitalize()}", "Genres", "Score"])

    for entry in entries:
        genres = ", ".join(entry["media"]["genres"])
        ws.append([
            entry["media"]["title"]["romaji"],
            entry["media"]["format"],
            entry["status"],
            f"{entry['progress']}/{entry['media'][total_key] or '?'}",
            genres,
            entry["score"],
        ])
        last_row = ws.max_row
        title_cell = ws.cell(row=last_row, column=1)
        title_cell.hyperlink = entry["media"]["siteUrl"]
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

async def export_xlsx():
    url = "https://graphql.anilist.co"
    username = input("Enter your Anilist username: ")
    if username == "":
        print("Username not provided!")
        return
    output = input("Enter output path [anilist.xlsx]: ") or "anilist.xlsx"
    media_types = ["ANIME", "MANGA"]

    wb = Workbook()
    if wb.active is not None:
        wb.remove(wb.active)

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch_entries(session, url, username, t) for t in media_types])
        for media_type, entries in zip(media_types, results):
            fill_sheet(wb.create_sheet(media_type.capitalize()), media_type, entries)

    wb.save(output)

def main():
    asyncio.run(export_xlsx())

if __name__ == "__main__":
    main()
