import requests

HEROES_URL = "https://api.opendota.com/api/heroes"


_heroes = None
heroes_map = {}
name_to_id = {}

def load_heroes():
    global _heroes, heroes_map, name_to_id

    if _heroes is not None:
        return

    response = requests.get(HEROES_URL, timeout=10)
    response.raise_for_status()  

    _heroes = response.json()

    heroes_map = {}
    for hero in _heroes:
        hero_id = hero["id"]
        hero_name = hero["localized_name"]
        heroes_map[hero_id] = hero_name

    name_to_id = {}
    for hero in _heroes:
        hero_name = hero["localized_name"].lower()
        hero_id = hero["id"]
        name_to_id[hero_name] = hero_id


def smoothed_winrate(wins, games, prior=0.5, weight=100):
    return (wins + prior * weight) / (games + weight)

MIN_GAMES = 50

def get_clean_matchups(hero_id, limit = 5):
    matchups = requests.get(
        f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    ).json()

    clean = []
    for m in matchups:
        if m["games_played"] < MIN_GAMES:
            continue

        wr = smoothed_winrate(
            m["wins"],
            m["games_played"]
        )

        clean.append({
            "hero_id": m["hero_id"],
            "winrate": wr,
            "games": m["games_played"]
        })
    clean = sorted(
        clean,
        key=lambda x: x["winrate"]
    )
    return clean[:limit]

