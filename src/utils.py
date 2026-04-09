import json
import os

json_file_name: str = "game_data.json"

def save_to_json(data: dict[str, Any], filename: str = json_file_name) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {filename}")

def append_to_json(new_data: dict[str, Any], filename: str = json_file_name) -> None:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    data_list = [data_list]
            except json.JSONDecodeError:
                data_list = []
    else:
        data_list = []

    data_list.append(new_data)

    save_to_json(data_list, filename)
        
    print(f"Data successfully appended to {filename}")

def key_in_json() -> bool:
    return True

def dict_from_json(filename: str = json_file_name) -> dict[str, any]:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print("Error: ", e)
                return {}
    return {}

# In cents
def format_price(value: int) -> str:
    return f"R$ {value / 100:.2f}".replace('.', ',')