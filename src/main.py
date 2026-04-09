import requests

name: str = "Stardew Valley"
root_search_url: str = "https://store.steampowered.com/search/?term="
headers: dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    
    'Cookie': 'birthtime=283996801; lastagecheckage=1-0-1979; wants_mature_content=1',
    
    'Referer': 'https://store.steampowered.com/',
}


try:
    response: Response = requests.get(root_search_url + name, headers=headers)
    
    if response.status_code == 200:
        pass
    elif response.status_code == 429:
        # Rate limit
        pass
        
except Exception as e:
    print(f"An error occurred: {e}")