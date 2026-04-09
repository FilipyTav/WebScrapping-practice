import json
import os

def save_to_json(data: dict[str, Any], filename: str = "game_data.json") -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {filename}")

def append_to_json(new_data: dict[str, Any], filename: str = "game_data.json") -> None:
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

# In cents
def format_price(value: int) -> str:
    return f"R$ {value / 100:.2f}".replace('.', ',')