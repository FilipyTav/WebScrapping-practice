from search import get_data_from_id, get_id_from_name, name
from utils import GameData, append_to_json

if __name__ == "__main__":
    pid: str = get_id_from_name(name)
    data: GameData = get_data_from_id(pid)
    append_to_json(data)

