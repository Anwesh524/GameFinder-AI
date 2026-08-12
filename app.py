from flask import Flask, render_template, request
import json
import os
import re

app = Flask(__name__)


# =========================================================
# LOAD GAME LIBRARY
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_FILE = os.path.join(BASE_DIR, "games.json")


def load_games():
    try:
        with open(GAMES_FILE, "r", encoding="utf-8") as file:
            games = json.load(file)

        if isinstance(games, dict):
            games = games.get("games", [])

        return games

    except Exception as error:
        print("Error loading games.json:", error)
        return []


# =========================================================
# GAME COVER IMAGES
# =========================================================

GAME_IMAGES = {

    "Overwatch 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/2357570/header.jpg",

    "Apex Legends":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1172470/header.jpg",

    "Counter-Strike 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",

    "PUBG: Battlegrounds":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/578080/header.jpg",

    "Halo Infinite":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1240440/header.jpg",

    "Destiny 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1085660/header.jpg",

    "Left 4 Dead 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/550/header.jpg",

    "Minecraft":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1928870/header.jpg",

    "Grand Theft Auto V":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/271590/header.jpg",

    "Red Dead Redemption 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg",

    "The Witcher 3: Wild Hunt":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg",

    "Elden Ring":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg",

    "Dark Souls III":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/374320/header.jpg",

    "Rocket League":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/252950/header.jpg",

    "Fall Guys":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1097150/header.jpg",

    "Among Us":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/945360/header.jpg",

    "Terraria":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/105600/header.jpg",

    "Stardew Valley":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg",

    "Hades":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg",

    "Hollow Knight":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg",

    "Celeste":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/header.jpg",

    "Cuphead":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/268910/header.jpg",

    "It Takes Two":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1426210/header.jpg",

    "Portal 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/620/header.jpg",

    "Portal":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/400/header.jpg",

    "Resident Evil 4":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/2050650/header.jpg",

    "Dying Light":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/239140/header.jpg",

    "Dead by Daylight":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/381210/header.jpg",

    "Phasmophobia":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/739630/header.jpg",

    "Subnautica":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/264710/header.jpg",

    "No Man's Sky":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/275850/header.jpg",

    "Sea of Thieves":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1172620/header.jpg",

    "Monster Hunter: World":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/582010/header.jpg",

    "Warframe":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/230410/header.jpg",

    "Rainbow Six Siege":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/359550/header.jpg",

    "Team Fortress 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg",

    "Paladins":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/444090/header.jpg",

    "Plants vs. Zombies":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/3590/header.jpg",

    "Civilization VI":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/289070/header.jpg",

    "Age of Empires IV":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1466860/header.jpg",

    "Dota 2":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg",

    "Need for Speed Heat":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1222680/header.jpg",

    "Forza Horizon 5":
        "https://cdn.cloudflare.steamstatic.com/steam/apps/1551360/header.jpg",
}


# =========================================================
# SEARCH ALIASES
# =========================================================

ALIASES = {

    "fps": [
        "shooter",
        "fps",
        "first person",
        "shooting"
    ],

    "shooting": [
        "shooter",
        "fps",
        "action"
    ],

    "multiplayer": [
        "multiplayer",
        "online",
        "cooperative",
        "competitive"
    ],

    "coop": [
        "cooperative",
        "multiplayer",
        "online",
        "co-op"
    ],

    "co-op": [
        "cooperative",
        "multiplayer",
        "online"
    ],

    "rpg": [
        "rpg",
        "role playing"
    ],

    "racing": [
        "racing",
        "cars",
        "driving"
    ],

    "scary": [
        "horror",
        "scary",
        "dark",
        "survival horror"
    ],

    "horror": [
        "horror",
        "scary",
        "dark",
        "survival horror"
    ],

    "zombie": [
        "zombies",
        "zombie",
        "horror",
        "survival"
    ],

    "open world": [
        "open world",
        "exploration",
        "adventure"
    ],

    "colorful": [
        "colorful",
        "cartoon",
        "funny"
    ],

    "relaxing": [
        "relaxing",
        "casual",
        "farming"
    ],

    "puzzle": [
        "puzzle",
        "logic"
    ],

    "2d": [
        "2d",
        "platformer",
        "indie"
    ],

    "platformer": [
        "platformer",
        "2d",
        "3d"
    ],

    "competitive": [
        "competitive",
        "team based",
        "multiplayer",
        "online"
    ],

    "story": [
        "story",
        "single player",
        "adventure"
    ],

    "space": [
        "space",
        "sci-fi",
        "futuristic"
    ],

    "fantasy": [
        "fantasy",
        "magic",
        "medieval"
    ],

    "anime": [
        "anime",
        "fantasy",
        "colorful"
    ],

    "sports": [
        "sports",
        "racing",
        "football"
    ],

    "football": [
        "football",
        "sports",
        "soccer"
    ],

    "free": [
        "free to play"
    ],

    "free to play": [
        "free to play"
    ],

    "survival": [
        "survival",
        "crafting",
        "exploration"
    ],

    "sandbox": [
        "sandbox",
        "building",
        "creative",
        "crafting"
    ]
}


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize(text):
    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# GET ALL SEARCHABLE GAME TEXT
# =========================================================

def game_text(game):

    values = []

    values.append(game.get("name", ""))

    for field in [
        "genres",
        "themes",
        "modes",
        "platforms",
        "tags"
    ]:

        data = game.get(field, [])

        if isinstance(data, list):
            values.extend(data)

        else:
            values.append(str(data))

    return normalize(" ".join(values))


# =========================================================
# EXPAND USER QUERY
# =========================================================

def get_search_terms(query):

    normalized_query = normalize(query)

    words = normalized_query.split()

    terms = set(words)

    # Add the complete query
    terms.add(normalized_query)

    # Add aliases
    for alias, replacements in ALIASES.items():

        if alias in normalized_query:

            terms.add(alias)

            for replacement in replacements:
                terms.add(normalize(replacement))

    # Special combinations

    if "multiplayer" in normalized_query and "shooter" in normalized_query:

        terms.update([
            "multiplayer",
            "shooter",
            "fps",
            "online",
            "competitive",
            "team based"
        ])

    if "colorful" in normalized_query and "shooter" in normalized_query:

        terms.update([
            "colorful",
            "shooter",
            "cartoon",
            "fps"
        ])

    if "open" in words and "world" in words:

        terms.update([
            "open world",
            "exploration"
        ])

    if "horror" in normalized_query:

        terms.update([
            "horror",
            "scary",
            "dark"
        ])

    if "racing" in normalized_query:

        terms.update([
            "racing",
            "cars",
            "driving"
        ])

    return list(terms)


# =========================================================
# CALCULATE GAME MATCH
# =========================================================

def calculate_match(game, query):

    if not query:
        return 0

    searchable = game_text(game)

    terms = get_search_terms(query)

    if not terms:
        return 0

    score = 0
    max_score = 0

    name = normalize(game.get("name", ""))

    genres = [
        normalize(x)
        for x in game.get("genres", [])
    ]

    themes = [
        normalize(x)
        for x in game.get("themes", [])
    ]

    modes = [
        normalize(x)
        for x in game.get("modes", [])
    ]

    platforms = [
        normalize(x)
        for x in game.get("platforms", [])
    ]

    tags = [
        normalize(x)
        for x in game.get("tags", [])
    ]

    for term in terms:

        if not term:
            continue

        max_score += 1

        # Exact name match
        if term == name:

            score += 5
            max_score += 4

        # Name contains term
        elif term in name:

            score += 4
            max_score += 3

        # Genre match
        if term in genres:

            score += 3
            max_score += 2

        # Theme match
        if term in themes:

            score += 2
            max_score += 1

        # Mode match
        if term in modes:

            score += 3
            max_score += 2

        # Platform match
        if term in platforms:

            score += 1

        # Tag match
        if term in tags:

            score += 3
            max_score += 2

        # General searchable match
        elif term in searchable:

            score += 1

    if max_score <= 0:
        return 0

    percentage = int(
        (score / max_score) * 100
    )

    # Keep the percentage visually reasonable
    percentage = max(
        0,
        min(99, percentage)
    )

    return percentage


# =========================================================
# FIND BEST GAMES
# =========================================================

def find_games(query):

    games = load_games()

    if not query.strip():
        return [], []

    scored_games = []

    for original_game in games:

        # Make a copy so we don't modify games.json data
        game = dict(original_game)

        match = calculate_match(
            game,
            query
        )

        if match > 0:

            game["match"] = match

            game["image"] = GAME_IMAGES.get(
                game.get("name")
            )

            scored_games.append(game)

    # Highest match first
    scored_games.sort(
        key=lambda item: item.get("match", 0),
        reverse=True
    )

    # Return up to 12 results
    results = scored_games[:12]

    # Get keywords for display
    keywords = get_search_terms(query)

    # Remove tiny/common single words from display
    display_keywords = []

    ignored = {
        "i",
        "want",
        "a",
        "an",
        "the",
        "game",
        "games",
        "to",
        "play",
        "with",
        "for",
        "and",
        "of"
    }

    for keyword in keywords:

        if keyword not in ignored:

            if keyword not in display_keywords:

                display_keywords.append(
                    keyword
                )

    display_keywords = display_keywords[:12]

    return results, display_keywords


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return render_template(
        "index.html",
        results=[],
        query="",
        keywords=[]
    )


# =========================================================
# SEARCH
# =========================================================

@app.route("/search", methods=["POST"])
def search():

    query = request.form.get(
        "query",
        ""
    ).strip()

    results, keywords = find_games(
        query
    )

    return render_template(
        "index.html",
        results=results,
        query=query,
        keywords=keywords
    )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("        GAMEFINDER AI")
    print("======================================")
    print()
    print("Game library:", len(load_games()), "games")
    print()
    print("Server starting...")
    print()
    print("Open:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )