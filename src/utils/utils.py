import json
import time
import os
from typing import TypedDict, cast
from pathlib import Path


class GameData(TypedDict):
    name: str
    appid: str
    price: str
    developers: list[str]
    genres: list[str]
    website: str
    metacritic_score: int
    release_date: str


BASE_DIR: Path = Path(__file__).resolve().parent.parent

CACHE_DIR: Path = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_FILE: Path = CACHE_DIR / "game_data.json"
METADATA_FILE: Path = CACHE_DIR / "cache_metadata.json"
MD_FILE = CACHE_DIR / "game_info.md"
SECONDS_IN_DAY: int = 60 * 60 * 24


def save_to_json(data: GameData | list[GameData], filename: Path = CACHE_FILE) -> None:
    """Saves GameData to CACHE_FILE"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Cache salvo em {filename}")


def append_to_json(new_data: GameData, filename: Path = CACHE_FILE) -> None:
    """Appends GameData to CACHE_FILE"""
    if not new_data:
        return

    data_list: GameData | list[GameData] = get_data_from_json()
    if not data_list:
        data_list = []
    elif not isinstance(data_list, list):
        data_list = [data_list]

    data_list.append(new_data)
    save_to_json(data_list, filename)


def id_in_json(id: str, data: GameData | list[GameData]) -> bool:
    """Returns if game ID in cache"""
    if isinstance(data, list):
        for d in data:
            if d["appid"] == id:
                return True
    else:
        return data["appid"] == id

    return False


def get_data_from_jsonid(id: str, data: list[GameData]) -> tuple[GameData, int]:
    """Returns game info and its index from data"""
    for i, d in enumerate(data):
        if not d:
            continue

        if d["appid"] == id:
            return d, i

    return cast(GameData, {}), -1


def get_data_from_json(filename: Path = CACHE_FILE) -> list[GameData]:
    """Returs full cache info as dict"""
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


def print_game_info(game: GameData) -> None:
    if not game:
        return

    clear_screen()
    separator = "-" * 40

    devs: str = ", ".join(game["developers"])
    genres: str = ", ".join(game["genres"])

    raw_score: int = game["metacritic_score"]
    score: str = f"{raw_score}/100" if raw_score >= 0 else "--------"

    website: str = game["website"] or "--------"

    print()
    print(separator)
    print(f"NOME: {game['name'].upper()}")
    print(separator)

    print(
        f"ID:           {game['appid']}\n"
        f"Preço:        {game['price']}\n"
        f"Lançamento:   {game['release_date']}\n"
        f"Devs:         {devs}\n"
        f"Gêneros:      {genres}\n"
        f"Score:        {score}\n"
        f"Website:      {website}"
    )

    print(separator + "\n")

    save_to_markdown(game)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def save_to_markdown(data: GameData, filename: Path = MD_FILE) -> None:
    devs: str = ", ".join(data["developers"])
    genres: str = ", ".join(data["genres"])

    lines = [
        f"## {data['name']}",
        f"- **ID:** `{data['appid']}`",
        f"- **Preço:** {data['price']}",
        f"- **Lançamento:** {data['release_date']}",
    ]

    if data["metacritic_score"] >= 0:
        lines.append(f"- **Metacritic:** {data['metacritic_score']}/100")

    lines.extend(
        [
            f"- **Devs:** {devs}",
            f"- **Gêneros:** {genres}",
            f"- **Website:** [{data['website']}]({data['website']})",
            "\n---\n",  # Separator
        ]
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Jogo '{data['name']}' salvo em: {filename}")
