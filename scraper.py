from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from typing import *
# from pymongo import *  # Uncomment if you're using MongoDB

# URL to scrape
url = 'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

# Fetch main page
page = urlopen(request)
page_html = page.read().decode("utf-8")
soup = BeautifulSoup(page_html, "html.parser")

# Find all Pokémon rows
pokemon_rows = soup.find("table", id="pokedex").find("tbody").find_all("tr")

for pokemon in pokemon_rows:
    pokemon_data = pokemon.find_all("td")

    try:
        id = pokemon_data[0].find("span").getText()
        avatar = pokemon_data[0].find("picture").find("source")["srcset"]
        name_tag = pokemon_data[1].find("a")
        name = name_tag.getText()
        details_uri = name_tag["href"]  # Fixed href access

        types = [ptype.getText() for ptype in pokemon_data[2].find_all("a")]

        total = pokemon_data[3].getText()
        hp = pokemon_data[4].getText()
        attack = pokemon_data[5].getText()
        defense = pokemon_data[6].getText()
        special_attack = pokemon_data[7].getText()
        special_defense = pokemon_data[8].getText()  # Fixed from "special_speed"
        speed = pokemon_data[9].getText()

        print(id, name, avatar, types)
        print(total, hp, attack, defense, special_attack, special_defense, speed)

        # Build entry page URL safely
        entry_url = f'https://pokemondb.net{details_uri}'
        print(f"Fetching entry for {name}: {entry_url}")

        # Request individual Pokémon page
        try:
            entry_request = Request(
                entry_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            entry_html = urlopen(entry_request).read().decode("utf-8")
            entry_soup = BeautifulSoup(entry_html, "html.parser")
            entry_text = ""

            # Look for Pokédex entry
            h2 = entry_soup.find("h2", string="Pokédex entries")
            if h2:
                table = h2.find_next("table")
                if table:
                    entry_text = table.find("tr").find("td").get_text(strip=True)
                else:
                    print(f"No table found under Pokédex entries for {name}")
            else:
                print(f"No Pokédex entries section found for {name}")

        except HTTPError as e:
            print(f"HTTP error {e.code} for {name} at {entry_url}")
            entry_text = ""
        except Exception as e:
            print(f"Error while fetching entry for {name}: {e}")
            entry_text = ""

        print(f"Entry: {entry_text}")
        print("-" * 40)

    except Exception as e:
        print(f"Error parsing data for a Pokémon: {e}")
        continue
