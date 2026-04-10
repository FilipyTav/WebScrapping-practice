import json
import time
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


CACHE_FILE: str = "game_data.json"
METADATA_FILE: str = "cache_metadata.json"
SECONDS_IN_DAY: int = 60 * 60 * 24


def save_to_json(data: GameData | list[GameData], filename: str = CACHE_FILE) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {filename}")


def append_to_json(new_data: GameData, filename: str = CACHE_FILE) -> None:
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


def get_data_from_json(filename: str = CACHE_FILE) -> list[GameData]:
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


def should_update_cache() -> bool:
    """>24 hours elapsed since last update"""
    if not os.path.exists(METADATA_FILE):
        return True

    with open(METADATA_FILE, "r") as f:
        try:
            metadata: dict[str, int] = json.load(f)
            last_update: int = metadata.get("last_update", 0)
        except json.JSONDecodeError:
            return True

    current_time: float = time.time()
    return (current_time - last_update) >= SECONDS_IN_DAY


def update_timestamp() -> None:
    """Saves the current time to the metadata file."""
    with open(METADATA_FILE, "w") as f:
        json.dump({"last_update": time.time()}, f)
