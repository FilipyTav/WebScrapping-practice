import json

def save_to_json(data: dict[str, Any], filename: str = "game_data.json") -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {filename}")

# In cents
def format_price(value: int) -> str:
    return f"R$ {value / 100:.2f}".replace('.', ',')