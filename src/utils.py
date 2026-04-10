import json
import os
from typing import TypedDict, cast


class GameData(TypedDict):
    name: str
    appid: str
    price: str
    developers: list[str]
    genres: list[str]
    website: str
    metacritic_score: int
    release_date: str


cache_file: str = "game_data.json"


def save_to_json(data: GameData | list[GameData], filename: str = cache_file) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {filename}")


def append_to_json(new_data: GameData, filename: str = cache_file) -> None:
    data_list: GameData | list[GameData] = get_data_from_json()
    if not data_list:
        data_list = []
    elif not isinstance(data_list, list):
        data_list = [data_list]

    data_list.append(new_data)
    save_to_json(data_list, filename)


def id_in_json(id: str, data: GameData | list[GameData]) -> bool:
    if isinstance(data, list):
        for d in data:
            if d["appid"] == id:
                return True
    else:
        return data["appid"] == id

    return False


def get_data_from_jsonid(id: str, data: list[GameData]) -> tuple[GameData, int]:
    for i, d in enumerate(data):
        if d["appid"] == id:
            return d, i

    return cast(GameData, {}), -1


def get_data_from_json(filename: str = cache_file) -> list[GameData]:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print("Error: ", e)
    return []


# In cents
def format_price(value: int) -> str:
    return f"R$ {value / 100:.2f}".replace(".", ",")
