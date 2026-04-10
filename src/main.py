from search import get_data_from_id, get_id_from_name
from utils import (
    GameData,
    append_to_json,
    get_data_from_json,
    get_data_from_jsonid,
)

if __name__ == "__main__":
    game_name: str = input("Qual jogo deseja procurar?\n> ").strip()

    current_games: list[GameData] = get_data_from_json()

    pid: str = get_id_from_name(game_name)
    query_game: GameData = get_data_from_jsonid(pid, current_games)

    if query_game:
        print("Jogo encontrado: ", query_game["name"])
        exit()

    data: GameData = get_data_from_id(pid)
    append_to_json(data)
