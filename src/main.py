import requests
from requests import Response
from bs4 import BeautifulSoup, Tag, exceptions
from typing import Any

from utils import GameData, append_to_json

name: str = "Stardew Valley"
root_search_url: str = "https://store.steampowered.com/search/?term="
headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Cookie": "birthtime=283996801; lastagecheckage=1-0-1979; wants_mature_content=1",
    "Referer": "https://store.steampowered.com/",
}


def get_id_from_name(name: str) -> str:
    response: Response = requests.get(root_search_url + name, headers=headers)

    try:
        if response.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

            first_result: Tag | None = soup.find("a", class_="search_result_row")

            if first_result:
                raw_id: str | list[str] | None = first_result.get("data-ds-appid")
                # Forces to str
                app_id: str = (
                    ",".join(raw_id) if isinstance(raw_id, list) else (raw_id or "")
                )

                game_element: Tag | None = first_result.find("span", class_="title")
                game_title: str = ""
                if game_element:
                    game_title = game_element.text

                print(f"Found Match: {game_title}")
                print(f"AppID: {app_id}")
                return app_id

        elif response.status_code == 429:
            print("Rate limit!!!")

    except Exception as e:
        print(f"Não foi possível encontrar o jogo {name}")
        print(f"Error: {e}")

    return ""


def get_search_url(id: str) -> str:
    return f"https://store.steampowered.com/api/appdetails?appids={id}&cc=br&l=pt"


def get_data_from_id(id: str) -> GameData:
    try:
        # Get game data
        json_url: str = get_search_url(id)

        response: Response = requests.get(json_url, headers=headers)

        if response.status_code == 200:
            data: dict[str, Any] = response.json()

            if data and data.get(id, {}).get("success"):
                game_info: GameData = data[id]["data"]
                price: str = game_info.get("price_overview", {}).get(
                    "final_formatted", "Free"
                )

                return {
                    "name": game_info.get("name"),
                    "appid": id,
                    "price": game_info.get("price_overview", {}).get(
                        "final_formatted", "Free"
                    ),
                    "developers": ", ".join(game_info.get("developers", [])),
                    "genres": ", ".join(
                        [g["description"] for g in game_info.get("genres", [])]
                    ),
                }

        elif response.status_code == 429:
            print("Rate limit!!!")

    except Exception as e:
        print(f"Não foi possível encontrar o jogo {name}")
        print(f"Error: {e}")

    return {}


if __name__ == "__main__":
    pid: str = get_id_from_name(name)
    data: GameData = get_data_from_id(pid)
    append_to_json(data)

