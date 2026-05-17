from search.search import get_data_from_id, get_id_from_name, update_json_entry
from utils import (
    GameData,
    append_to_json,
    clear_screen,
    get_data_from_json,
    get_data_from_jsonid,
    print_game_info,
    should_update_cache,
    update_timestamp,
)

if __name__ == "__main__":
    clear_screen()
    game_name: str = input("Qual jogo deseja procurar?\n> ").strip()

    cached_games: list[GameData] = get_data_from_json()

    pid: str = get_id_from_name(game_name)
    query_game, _ = get_data_from_jsonid(pid, cached_games)

    cache_updated: bool = not should_update_cache()

    if query_game:
        if cache_updated:
            print("Jogo presente no cache...")
        else:
            print("Atualizando cache...")
            query_game = update_json_entry(pid)

        print_game_info(query_game)
        exit()

    data: GameData = get_data_from_id(pid)
    print_game_info(data)
    append_to_json(data)

    update_timestamp()
