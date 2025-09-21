from bs4 import *
from urllib.request import *
from typing import *
from pymongo import *

url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers = {'Users-agent': 'Mozilla/5.0'}
)

page = urlopen(request)
page_context_bytes = page.read()
page_html = page_context_bytes.decode("utf-8")
soup = BeautifulSoup(page_html, "html.parser")

pokemon_rows = soup.find_all("table", id = "pokedex")[0].find_all("tbody")[0].find_all("tr")

#print(pokemon_rows)

for pokemon in pokemon_rows:
    pokemon_data = pokemon.find_all("td")
    
    id = pokemon_data[0].find_all("span")[0].getText()
    avatar = pokemon_data[0].find_all("picture")[0].find_all("source")[0]["srcset"]
    detail_uri = pokemon_data[1].find_all("a")[0].getText("href")
    name = pokemon_data[1].find_all("a")[0].getText()
    types = []

    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append(pokemon_type.getText())
    
    total = pokemon_data[3].getText()
    hp = pokemon_data[4].getText()
    attack = pokemon_data[5].getText()
    defense = pokemon_data[6].getText()
    special_attack = pokemon_data[7].getText()
    special_speed = pokemon_data[8].getText()
    speed = pokemon_data[9].getText()

    print(id, name, avatar, types)
    print(total, hp, attack, defense, special_attack, special_speed, speed)