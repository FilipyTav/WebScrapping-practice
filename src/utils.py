import json
import os
from typing import TypeAlias, Any, TypedDict, cast


class GameData(TypedDict):
    name: str
    appid: str
    price: str
    developers: list[str]
    genres: list[str]
    website: str
    metacritic_score: int
    release_date: str


json_file_name: str = "game_data.json"


def save_to_json(
    data: GameData | list[GameData], filename: str = json_file_name
) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {filename}")


def append_to_json(new_data: GameData, filename: str = json_file_name) -> None:
    data_list: GameData | list[GameData] = get_data_from_json()
    if not data_list:
        data_list = []
    elif not isinstance(data_list, list):
        data_list = [data_list]

    data_list.append(new_data)
    save_to_json(data_list, filename)

    print(f"Data successfully appended to {filename}")


def id_in_json(id: str, data: GameData | list[GameData]) -> bool:
    if isinstance(data, list):
        for d in data:
            if d["appid"] == id:
                return True
    else:
        return data["appid"] == id

    return False


def get_data_from_json(filename: str = json_file_name) -> GameData | list[GameData]:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print("Error: ", e)
    return cast(GameData, {})


# In cents
def format_price(value: int) -> str:
    return f"R$ {value / 100:.2f}".replace(".", ",")
