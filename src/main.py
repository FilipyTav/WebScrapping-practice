import requests
from bs4 import BeautifulSoup

from utils import save_to_json

name: str = "Stardew Valley"
root_search_url: str = "https://store.steampowered.com/search/?term="
headers: dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    
    'Cookie': 'birthtime=283996801; lastagecheckage=1-0-1979; wants_mature_content=1',
    
    'Referer': 'https://store.steampowered.com/',
}

if __name__ == '__main__':
    try:
        response: Response = requests.get(root_search_url + name, headers=headers)
        
        if response.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
            
            first_result: Tag | None = soup.find('a', class_='search_result_row')
            
            if first_result:
                app_id: str | list[str] | None = first_result.get('data-ds-appid')
                game_title: str = first_result.find('span', class_='title').text
                
                print(f"Found Match: {game_title}")
                print(f"AppID: {app_id}")
                
                json_url: str = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=br&l=pt"
                api_response: requests.Response = requests.get(json_url, headers=headers)
                data: dict[str, Any] = api_response.json()

                if data and data.get(app_id, {}).get('success'):
                    game_info: dict[str, Any] = data[app_id]['data']
                    price: str = game_info.get('price_overview', {}).get('final_formatted', 'Free')
                    relevant_data: dict[str, any] = {
                        "name": game_info.get("name"),
                        "appid": app_id,
                        "price": game_info.get("price_overview", {}).get("final_formatted", "Free"),
                        "developers": ", ".join(game_info.get("developers", [])),
                        "genres": ", ".join([g["description"] for g in game_info.get("genres", [])])
                    }
                    save_to_json(relevant_data)
        elif response.status_code == 429:
            print("Rate limit!!!")
            pass
            
    except Exception as e:
        print(f"An error occurred: {e}")