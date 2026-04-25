from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from uuid import uuid4
import json

app = FastAPI()

# ----------- ROOT -----------

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is running"}

# ----------- МОДЕЛЬ -----------

class Movie(BaseModel):
    title: str
    year: int
    rating: float

class MovieResponse(Movie):
    id: str

# ----------- ГОТОВАЯ "БАЗА" -----------

movies_db = [
    {"id": str(uuid4()), "title": "Inception", "year": 2010, "rating": 8.8},
    {"id": str(uuid4()), "title": "Interstellar", "year": 2014, "rating": 8.6},
    {"id": str(uuid4()), "title": "The Dark Knight", "year": 2008, "rating": 9.0},
    {"id": str(uuid4()), "title": "Fight Club", "year": 1999, "rating": 8.8},
    {"id": str(uuid4()), "title": "Forrest Gump", "year": 1994, "rating": 8.8},
]

# ----------- СПЕЦИАЛЬНЫЕ ПУТИ (СНАЧАЛА!) -----------

@app.get("/movies/pretty")
def get_movies_pretty(min_rating: float = Query(0, ge=0, le=10)):
    filtered_movies = [m for m in movies_db if m["rating"] >= min_rating]
    json_data = json.dumps(filtered_movies, indent=4)
    return JSONResponse(content=json.loads(json_data))





@app.get("/movies/html", response_class=HTMLResponse)
def get_movies_html(min_rating: float = Query(0, ge=0, le=10)):
    filtered_movies = [m for m in movies_db if m["rating"] >= min_rating]

    html_content = """
    <html>
    <head>
        <title>Movie List</title>x
        <style>
            table {border-collapse: collapse; width: 70%; margin: 20px auto;}
            th, td {border: 1px dashed #333; padding: 25px; text-align: center;}
            th {background-color: hotpink; color: white;}
            tr:nth-child(even) {background-color: #f2f2f2;}
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">Movie Catalog</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Title</th>
                <th>Year</th>
                <th>Rating</th>
            </tr>
    """
    for idx, movie in enumerate(filtered_movies, start=1):
        html_content += f"""
            <tr>
                <td>{idx}</td>
                <td>{movie['title']}</td>
                <td>{movie['year']}</td>
                <td>{movie['rating']}</td>
            </tr>
        """
    html_content += """
        </table>
    </body>
    </html>
    """
    return html_content

# ----------- CRUD -----------

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(min_rating: float = Query(0, ge=0, le=10)):
    return [m for m in movies_db if m["rating"] >= min_rating]

@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: str):
    for movie in movies_db:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.post("/movies", response_model=MovieResponse)
def create_movie(movie: Movie):
    new_movie = movie.dict()
    new_movie["id"] = str(uuid4())
    movies_db.append(new_movie)
    return new_movie



@app.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: str, updated: Movie):
    for movie in movies_db:
        if movie["id"] == movie_id:
            movie.update(updated.dict())
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: str):
    for i, movie in enumerate(movies_db):
        if movie["id"] == movie_id:
            movies_db.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")

#LAB4
#1
from fastapi import FastAPI

app = FastAPI()

class Player:
    def __init__(self, player_id: int, name: str, hp: int):
        self._id = player_id
        self._name = name.strip().title()
        self._hp = hp if hp >= 0 else 0

    def __str__(self):
        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"

    def __del__(self):
        print(f"Player {self._name} удалён")


@app.get("/player1")
def get_one():
    p = Player(1, " john ", 120)
    return str(p)



#2
class Player:
    def __init__(self, id: int, name: str, hp: int):
        self._id = id
        self._name = name.strip().title()
        self._hp = hp if hp >= 0 else 0

    @classmethod
    def from_string(cls, data: str):
        parts = data.split(",")
        if len(parts) != 3:
            raise ValueError("Неверный формат строки")
        return cls(int(parts[0]), parts[1].strip(), int(parts[2]))

    def __str__(self):
        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"


@app.get("/player2")
def get_two():
    data = "2, alice , 90"
    p = Player.from_string(data)
    return str(p)


#3
class Item:
    def __init__(self, item_id: int, name: str, power: int):
        self.id = item_id
        self.name = name.strip().title()
        self.power = power

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.id == other.id and self.name == other.name

    def __hash__(self):
        return hash((self.id, self.name))

    def __str__(self):
        return f"Item(id={self.id}, name='{self.name}', power={self.power})"


@app.get("/items")
def get_items():
    i = Item(1, " Sword ", 50)
    return str(i)


#4
class Item:
    def __init__(self, item_id: int, name: str, power: int):
        self.id = item_id
        self.name = name.strip().title()
        self.power = power

    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Item(id={self.id}, name='{self.name}', power={self.power})"


class Inventory:
    def __init__(self):
        self._items: dict[int, Item] = {}

    def add_item(self, item: Item):
        self._items[item.id] = item

    def remove_item(self, item_id: int):
        if item_id in self._items:
            del self._items[item_id]

    def get_items(self) -> list[Item]:
        return list(self._items.values())

    def unique_items(self) -> set[Item]:
        return set(self._items.values())

    def to_dict(self) -> dict[int, Item]:
        return self._items


@app.get("/inventory")
def test_inventory():
    inv = Inventory()

    i1 = Item(1, " Margo ", 50)
    i2 = Item(1, " Maral ", 100)
    i3 = Item(2, " Aiym ", 30)

    inv.add_item(i1)
    inv.add_item(i2)
    inv.add_item(i3)

    return {
        "all_items": [str(x) for x in inv.get_items()],
        "as_dict": {k: str(v) for k, v in inv.to_dict().items()},
        "unique_count": len(inv.unique_items())
    }



#5
class Item:
    def __init__(self, item_id: int, name: str, power: int):
        self.id = item_id
        self.name = name.strip().title()
        self.power = power

    def __str__(self):
        return f"Item(id={self.id}, name='{self.name}', power={self.power})"


class Inventory:
    def __init__(self):
        self._items: dict[int, Item] = {}

    def add_item(self, item: Item):
        self._items[item.id] = item

    def get_strong_items(self, min_power: int) -> list[Item]:
        check = lambda item: item.power >= min_power
        return [item for item in self._items.values() if check(item)]


@app.get("/strong")
def filter_items(min_p: int = 40):
    inv = Inventory()

    inv.add_item(Item(1, "Zere", 15))
    inv.add_item(Item(2, "Margo", 50))
    inv.add_item(Item(3, "Aiym", 80))

    strong_ones = inv.get_strong_items(min_p)

    return {
        "min_power_threshold": min_p,
        "items": [str(x) for x in strong_ones]
    }


#6
from datetime import datetime
class Event:
    def __init__(self, event_type: str, data: dict):
        self.type = event_type
        self.data = data
        self.timestamp = datetime.now()

    def __str__(self):
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Event(type='{self.type}', data={self.data}, timestamp='{time_str}')"


@app.get("/event")
def get_event():
    e = Event("ATTACK", {"damage": 20})
    return str(e)


#7
class Item:
    def __init__(self, name, power):
        self.name = name.strip().title()
        self.power = power


class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data


class Player:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.inventory = []

    def handle_event(self, event):
        if event.type == "ATTACK":
            self.hp -= event.data.get("damage", 0)
        elif event.type == "LOOT":
            item = event.data.get("item")
            self.inventory.append(item)


class Warrior(Player):
    def handle_event(self, event):
        if event.type == "ATTACK":
            event.data["damage"] *= 0.9
        super().handle_event(event)


class Mage(Player):
    def handle_event(self, event):
        if event.type == "LOOT":
            item = event.data.get("item")
            item.power = int(item.power * 1.1)
        super().handle_event(event)


@app.get("/battle")
def battle():
    warrior = Warrior("Maral", 100)
    mage = Mage("Daiana", 100)

    warrior.handle_event(Event("ATTACK", {"damage": 20}))

    mage.handle_event(Event("LOOT", {"item": Item("Staff", 50)}))

    return {
        "warrior_hp": warrior.hp,
        "mage_item_power": mage.inventory[0].power
    }


#8
from datetime import datetime
class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data


class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name


class Logger:
    @staticmethod
    def log(event: Event, player: Player, filename: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"{timestamp};{player.id};{event.type};{event.data}\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_entry)


@app.get("/log")
def test_log():
    p = Player(1, "John")
    e = Event("ATTACK", {"damage": 20})

    Logger.log(e, p, "logs.txt")

    return {"status": "success", "message": "Событие записано в logs.txt"}


#9
import ast
class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data

    def __repr__(self):
        return f"Event(type='{self.type}', data={self.data})"


class Logger:
    @staticmethod
    def read_logs(filename: str) -> list[Event]:
        events = []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(";")

                    if len(parts) == 4:
                        event_type = parts[2]
                        event_data = ast.literal_eval(parts[3])

                        events.append(Event(event_type, event_data))
        except FileNotFoundError:
            return []

        return events




@app.get("/read_logs")
def get_logs():
    filename = "logs.txt"
    logs = Logger.read_logs(filename)

    return {"count": len(logs), "events": [repr(e) for e in logs]}


#10
class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data

    def __repr__(self):
        return f"Event({self.type})"


class EventIterator:
    def __init__(self, events: list[Event]):
        self._events = events
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._events):
            event = self._events[self._index]
            self._index += 1
            return event
        raise StopIteration


@app.get("/iterate")
def test_iterator():
    event_list = [
        Event("ATTACK", {"dmg": 10}),
        Event("HEAL", {"hp": 5}),
        Event("LOOT", {"id": 1})
    ]

    iterator = EventIterator(event_list)

    result = [str(event) for event in iterator]

    return {"iterated_events": result}


#11
from typing import Iterator

class Event:
    def __init__(self, e_type: str, data: dict):
        self.type = e_type
        self.data = data

def damage_stream(events: list[Event]) -> Iterator[int]:
    for event in events:
        if event.type == "ATTACK":
            damage = event.data.get("damage", 0)
            yield damage


@app.get("/stream")
def get_stream():
    events = [
        Event("ATTACK", {"damage": 10}),
        Event("HEAL", {"amount": 5}),
        Event("ATTACK", {"damage": 25}),
        Event("LOOT", {"id": 1}),
        Event("ATTACK", {"damage": 7})
    ]

    stream = damage_stream(events)

    result = list(stream)

    return {
        "filtered_damage": result,
        "total_hits": len(result)
    }


#12
import random

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Item:
    def __init__(self, name, power):
        self.name = name
        self.power = power


class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data

    def __repr__(self):
        return f"Event({self.type}, {self.data})"


def generate_events(players: list[Player], items: list[Item], n: int) -> list[Event]:
    all_events = []

    types = ["ATTACK", "HEAL", "LOOT"]

    get_random_type = lambda: random.choice(types)

    for player in players:
        for _ in range(n):
            e_type = get_random_type()

            if e_type == "ATTACK":
                data = {"damage": random.randint(10, 50)}
            elif e_type == "HEAL":
                data = {"amount": random.randint(5, 20)}
            else:
                random_item = random.choice(items)
                data = {"item_name": random_item.name, "power": random_item.power}

            all_events.append(Event(e_type, data))

    return all_events


@app.get("/generate")
def run_generation():
    players = [Player(1, "Maral"), Player(2, "Daiana")]
    items = [Item("Axe", 40), Item("Bow", 45), Item("Potion", 0)]

    events = generate_events(players, items, n=2)

    return {"generated_count": len(events), "events": [repr(e) for e in events]}


#13
from collections import Counter

class Event:
    def __init__(self, e_type, data, player_id):
        self.type = e_type
        self.data = data
        self.player_id = player_id

def analyze_logs(events: list[Event]) -> dict:
    if not events:
        return {"error": "No events to analyze"}

    player_damage = {}
    total_damage = 0

    event_types = [e.type for e in events]

    for e in events:
        if e.type == "ATTACK":
            dmg = e.data.get("damage", 0)
            total_damage += dmg
            player_damage[e.player_id] = player_damage.get(e.player_id, 0) + dmg

    top_player = max(player_damage, key=player_damage.get) if player_damage else None


    most_common_event = Counter(event_types).most_common(1)[0][0]

    return {
        "total_damage": total_damage,
        "top_player": top_player,
        "most_common_event": most_common_event
    }


@app.get("/analyze")
def run_analysis():
    logs = [
        Event("ATTACK", {"damage": 50}, player_id=1),
        Event("LOOT", {}, player_id=1),
        Event("ATTACK", {"damage": 30}, player_id=2),
        Event("ATTACK", {"damage": 40}, player_id=1),
        Event("HEAL", {"amount": 20}, player_id=2),
    ]

    return analyze_logs(logs)


#14
decide_action = lambda hp, inv_count: (
    "HEAL" if hp < 30 else
    "LOOT" if inv_count == 0 else
    "ATTACK"
)


@app.get("/decide")
def get_decision(hp: int, items: int):
    action = decide_action(hp, items)

    return {
        "status": {"hp": hp, "inventory_items": items},
        "recommended_action": action
    }


#15
class Item:
    def __init__(self, name, power):
        self.name = name
        self.power = power

class Event:
    def __init__(self, e_type, data):
        self.type = e_type
        self.data = data

class Player:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.inventory = []

    def handle_event(self, event):
        if event.type == "ATTACK":
            self.hp -= event.data.get("damage", 0)
        elif event.type == "LOOT":
            self.inventory.append(event.data.get("item"))

class Warrior(Player):
    def handle_event(self, event):
        if event.type == "ATTACK":
            event.data["damage"] *= 0.9
        super().handle_event(event)

class Mage(Player):
    def handle_event(self, event):
        if event.type == "LOOT":
            item = event.data.get("item")
            if item:
                item.power = int(item.power * 1.1)
        super().handle_event(event)

@app.get("/battle_test")
def battle_test():
    w = Warrior("Maral", 100)
    m = Mage("Daiana", 100)

    atk = Event("ATTACK", {"damage": 20})
    loot = Event("LOOT", {"item": Item("Staff", 50)})

    w.handle_event(atk)
    m.handle_event(loot)

    return {
        "warrior_hp": w.hp,
        "mage_item_power": m.inventory[0].power
    }



#16
class Player:
    def __init__(self, name: str, hp: int):
        self.name = name
        self._hp = hp if hp >= 0 else 0
        self._inventory = []

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = hp if hp >= 0 else 0

    @property
    def inventory(self):
        return list(self._inventory)

    def add_to_inventory(self, item: str):
        if len(self._inventory) < 10:
            self._inventory.append(item)


@app.get("/player")
def get_player():
    p = Player("Maral", 100)

    p.hp -= 20

    p.add_to_inventory("Axe")

    return {
        "name": p.name,
        "hp": p.hp,
        "items": p.inventory
    }


#17
class Player:
    def __init__(self, name: str):
        self.name = name
        print(f"Player {self.name} создан")

    def __del__(self):
        print(f"Player {self.name} удалён")


@app.get("/delete_test")
def delete_test():
    p = Player("Maral")

    player_name = p.name

    del p

    return {"message": f"Проверьте консоль: игрок {player_name} должен быть удалён."}


#18
class Item:
    def __init__(self, name: str, power: int):
        self.name = name
        self.power = power

    def __repr__(self):
        return f"{self.name}({self.power})"

class Inventory:
    def __init__(self):
        self._items = {}
        self._next_id = 1

    def add_item(self, item: Item):
        self._items[self._next_id] = item
        self._next_id += 1

    def __iter__(self):
        return iter(self._items.values())

@app.get("/inventory_filter")
def test_filter():
    inv = Inventory()
    inv.add_item(Item("Dagger", 15))
    inv.add_item(Item("Sword", 50))
    inv.add_item(Item("Axe", 80))
    inv.add_item(Item("Stick", 5))

    strong_items = [item for item in inv if item.power >= 40]

    return {
        "all_items_count": len(inv._items),
        "strong_items": [str(i) for i in strong_items]
    }


#19
class Item:
    def __init__(self, name: str, power: int):
        self.name = name
        self.power = power

    def __repr__(self):
        return f"{self.name}({self.power})"


class Inventory:
    def __init__(self, items: list[Item]):
        self.items = items

    def __iter__(self):
        return iter(self.items)


def analyze_inventory(inventories: list[Inventory]) -> dict:
    all_items = []

    for inv in inventories:
        all_items.extend(list(inv))

    if not all_items:
        return {"unique_items": set(), "top_power": None}

    unique_names = {item.name for item in all_items}

    best_item = max(all_items, key=lambda x: x.power)

    return {
        "unique_items": unique_names,
        "top_power": {
            "name": best_item.name,
            "power": best_item.power
        }
    }


@app.get("/analyze_inv")
def run_analysis():
    inv1 = Inventory([Item("Sword", 50), Item("Shield", 30)])
    inv2 = Inventory([Item("Sword", 50), Item("Axe", 80)])

    result = analyze_inventory([inv1, inv2])

    result["unique_items"] = list(result["unique_items"])
    return result


#20
import random
import ast
from datetime import datetime
from collections import Counter


class Item:
    def __init__(self, name, power):
        self.name = name.strip().title()
        self.power = power

    def __repr__(self):
        return f"{self.name}({self.power})"


class Event:
    def __init__(self, e_type, data, player_id=None):
        self.type = e_type
        self.data = data
        self.player_id = player_id


class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item): self._items.append(item)

    def __iter__(self): return iter(self._items)

    def __len__(self): return len(self._items)


class Player:
    def __init__(self, p_id, name, hp):
        self.id = p_id
        self.name = name
        self._hp = hp
        self.inventory = Inventory()

    @property
    def hp(self):
        return self._hp

    def handle_event(self, event):
        if event.type == "ATTACK":
            self._hp -= event.data.get("damage", 0)
        elif event.type == "LOOT":
            self.inventory.add(event.data.get("item"))


class Warrior(Player):
    def handle_event(self, event):
        if event.type == "ATTACK":
            event.data["damage"] *= 0.9  # -10% урона
        super().handle_event(event)


class Mage(Player):
    def handle_event(self, event):
        if event.type == "LOOT":
            item = event.data.get("item")
            if item: item.power = int(item.power * 1.1)  # +10% к силе
        super().handle_event(event)


class Logger:
    @staticmethod
    def log(event, player, filename="game.log"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp};{player.id};{event.type};{event.data}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line)

    @staticmethod
    def read_logs(filename="game.log"):
        events = []
        try:
            with open(filename, "r") as f:
                for line in f:
                    p = line.strip().split(";")
                    if len(p) == 4:
                        events.append(Event(p[2], ast.literal_eval(p[3]), int(p[1])))
        except FileNotFoundError:
            pass
        return events


def main():
    players = [Warrior(1, "Gimli", 100), Mage(2, "Gandalf", 80)]
    items_pool = [Item("Axe", 50), Item("Staff", 40), Item("Shield", 30)]
    log_file = "game.log"

    open(log_file, "w").close()

    types = ["ATTACK", "LOOT"]
    get_type = lambda: random.choice(types)

    for p in players:
        for _ in range(3):
            t = get_type()
            data = {"damage": random.randint(10, 30)} if t == "ATTACK" else {"item": random.choice(items_pool)}

            event = Event(t, data, p.id)
            p.handle_event(event)
            Logger.log_action(u, "view", p, log_file)


    logs = Logger.read_logs(log_file)

    stats = Counter([e.type for e in logs])

    damage_map = {}
    for e in [x for x in logs if x.type == "ATTACK"]:
        damage_map[e.player_id] = damage_map.get(e.player_id, 0) + e.data['damage']

    top_dmg_id = max(damage_map, key=damage_map.get) if damage_map else None

    top_inv_player = max(players, key=lambda p: len(p.inventory))

    print(f"Всего событий: {dict(stats)}")
    print(f"Топ-дамагер: {top_dmg_id} (Урон: {damage_map.get(top_dmg_id)})")
    print(f"Топ-собиратель: {top_inv_player.name} (Предметов: {len(top_inv_player.inventory)})")
    for p in players:
        print(f"{p.name}: HP={p.hp:.1f}, Inventory={list(p.inventory)}")