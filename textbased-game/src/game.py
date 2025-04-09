import os
import sys
import termios
import tty
import random
import time

class GameMap:
    def __init__(self, width, height, room_count=5):
        self.width = width
        self.height = height
        self.room_count = room_count
        self.enemies = {}  # Dictionary zur Verwaltung der Gegner
        self.rooms = self.create_rooms()  # Räume erstellen
        self.current_room = 0

    def create_rooms(self):
        rooms = []
        for i in range(self.room_count):
            room = [[" " for _ in range(self.width)] for _ in range(self.height)]
            # Wände hinzufügendc
            for y in range(self.height):
                for x in range(self.width):
                    if x == 0 or x == self.width - 1:
                        room[y][x] = "I"  # Vertikale Wände
                    if y == 0 or y == self.height - 1:
                        room[y][x] = "---"  # Horizontale Wände
            # Türen hinzufügen
            if i > 0:  # Eingangstür für alle Räume außer dem ersten
                room[self.height // 2][0] = " "  # Linke Tür
            if i < self.room_count - 1:  # Ausgangstür für alle Räume außer dem letzten
                room[self.height // 2][self.width - 1] = " "  # Rechte Tür

            # Gegner platzieren
            for _ in range(3):  # Platziere 3 Gegner pro Raum
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                while room[y][x] != " ":  # Stelle sicher, dass der Platz leer ist
                    x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                room[y][x] = "X"  # Gegner auf der Karte als "X" markieren
                enemy_hp = 30 + i * 10  # HP steigt mit der Raumanzahl
                enemy_weapon = Weapon("Keule", (4 + i, 9 + i), 1.5, crit_chance=0.05 + i * 0.01, crit_multiplier=1.5)
                enemy_xp = 50 + i * 20  # XP-Belohnung steigt mit der Raumanzahl
                self.enemies[(x, y)] = Enemy(name=f"Gegner {i + 1}", hp=enemy_hp, weapon=enemy_weapon, xp_reward=enemy_xp)

            # Items platzieren
            for _ in range(2):  # Platziere 2 Items pro Raum
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                while room[y][x] != " ":  # Stelle sicher, dass der Platz leer ist
                    x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                room[y][x] = "+"  # Item platzieren

            rooms.append(room)
        return rooms

    def display_map(self, player_position, player_hp, player_xp, player_xp_to_next_level):
        os.system('clear')  # Konsole leeren
        print(f"HP: {player_hp} | XP: {player_xp}/{player_xp_to_next_level} | Raum: {self.current_room + 1}/{self.room_count}")
        room = self.rooms[self.current_room]
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == player_position:
                    print("#", end="")  # Spieler
                else:
                    print(room[y][x], end="")  # Zeige das aktuelle Symbol (z. B. Wände, Gegner, Items)
            print()  # Neue Zeile nach jeder Zeile der Karte

    def is_collision(self, position):
        x, y = position
        room = self.rooms[self.current_room]
        if 0 <= y < self.height and 0 <= x < self.width:  # Überprüfe, ob die Position innerhalb der Grenzen liegt
            return room[y][x] in ["I", "---"]
        return True  # Wenn außerhalb der Grenzen, behandle es als Kollision

    def check_door(self, position):
        x, y = position
        if x == 0 and self.current_room > 0:  # Linke Tür
            self.current_room -= 1
            return True
        elif x == self.width - 1 and self.current_room < self.room_count - 1:  # Rechte Tür
            self.current_room += 1
            return True
        return False


class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  # Funktion, die den Effekt des Gegenstands definiert


class Player:
    def __init__(self, start_position):
        self.position = start_position
        self.hp = 100
        self.max_hp = 100
        self.strength = 10  # Stärke beeinflusst den Basisschaden
        self.dexterity = 5  # Geschicklichkeit beeinflusst kritische Trefferchance
        self.crit_chance = 0.1  # Kritische Trefferchance (10%)
        self.crit_multiplier = 2.0  # Kritischer Schadensmultiplikator
        self.weapon = Weapon("Schwert", (5, 10), 1.0, crit_chance=0.15, crit_multiplier=1.5)  # Standardwaffe
        self.inventory = [Item("Heiltrank", self.heal)]  # Startinventar mit einem Heiltrank
        self.special_cooldown = 0  # Cooldown für Spezialangriff
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

    def heal(self):
        self.hp = min(self.max_hp, self.hp + 50)  # Heilt 50 HP, aber nicht über max_hp hinaus

    def move(self, direction, game_map):
        new_position = self.position
        if direction == "w":  # Up
            new_position = (self.position[0], self.position[1] - 1)
        elif direction == "s":  # Down
            new_position = (self.position[0], self.position[1] + 1)
        elif direction == "a":  # Left
            new_position = (self.position[0] - 1, self.position[1])
        elif direction == "d":  # Right
            new_position = (self.position[0] + 1, self.position[1])

        if not game_map.is_collision(new_position):
            self.position = new_position
            room = game_map.rooms[game_map.current_room]
            if room[new_position[1]][new_position[0]] == "+":
                room[new_position[1]][new_position[0]] = " "  # Entferne das Item von der Karte
                self.add_random_item()
            elif room[new_position[1]][new_position[0]] == "X":
                enemy = game_map.enemies.get(new_position)
                if enemy:
                    battle = Battle(self, enemy)
                    result = battle.start()
                    if result == "sieg":
                        room[new_position[1]][new_position[0]] = " "  # Entferne den Gegner von der Karte
                        del game_map.enemies[new_position]
                    elif result == "niederlage":
                        print("Du wurdest besiegt!")
                        self.hp = 0  # Setze HP auf 0, um das Spiel zu beenden

    def add_random_item(self):
        items = [
            Item("Heiltrank", self.heal),
            Weapon("Dolch", (3, 6), 0.8),
            Weapon("Axt", (7, 12), 1.5)
        ]
        new_item = random.choice(items)
        self.inventory.append(new_item)
        print(f"Du hast ein neues Item gefunden: {new_item.name}!")
        input("Drücke eine Taste, um fortzufahren...")

    def gain_xp(self, amount):
        self.xp += amount
        print(f"Du hast {amount} XP erhalten! (XP: {self.xp}/{self.xp_to_next_level})")
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.8)  # Erhöhe die XP-Anforderung stärker
        self.max_hp += 20  # Erhöhe maximale HP
        self.hp = self.max_hp  # Fülle HP vollständig auf
        self.strength += 3  # Erhöhe Stärke
        self.dexterity += 1  # Erhöhe Geschicklichkeit
        self.crit_chance += 0.01  # Erhöhe kritische Trefferchance
        print(f"Level-Up! Du bist jetzt Level {self.level}. Deine HP wurden vollständig aufgefüllt!")
        print(f"Neue maximale HP: {self.max_hp}, Stärke: {self.strength}, Geschicklichkeit: {self.dexterity}, Kritische Trefferchance: {self.crit_chance:.2f}")

    def open_menu(self):
        options = ["Items", "Ausrüstung"]
        selected_option = 0

        while True:
            os.system('clear')
            print("=== Menü ===")
            for i, option in enumerate(options):
                if i == selected_option:
                    print(f"> {option}")
                else:
                    print(f"  {option}")
            print("\nWähle eine Option mit W/S und bestätige mit Leertaste.")

            key = get_key()
            if key == "w":  # Nach oben
                selected_option = (selected_option - 1) % len(options)
            elif key == "s":  # Nach unten
                selected_option = (selected_option + 1) % len(options)
            elif key == " ":  # Auswahl bestätigen
                if options[selected_option] == "Items":
                    self.show_items()
                elif options[selected_option] == "Ausrüstung":
                    self.equip_weapon()
            elif key == "q":  # Menü verlassen
                return

    def show_items(self):
        os.system('clear')
        print("=== Items ===")
        if not self.inventory:
            print("Dein Inventar ist leer!")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i + 1}. {item.name}")
        input("Drücke eine Taste, um zurückzukehren...")

    def equip_weapon(self):
        os.system('clear')
        print("=== Ausrüstung ===")
        weapons = [item for item in self.inventory if isinstance(item, Weapon)]
        if not weapons:
            print("Keine Waffen im Inventar!")
            input("Drücke eine Taste, um zurückzukehren...")
            return

        for i, weapon in enumerate(weapons):
            print(f"{i + 1}. {weapon.name} (Schaden: {weapon.damage_range}, Geschwindigkeit: {weapon.attack_speed}s, "
                  f"Kritische Trefferchance: {weapon.crit_chance * 100:.1f}%, Kritischer Schaden: {weapon.crit_multiplier}x)")
        print("\nWähle eine Waffe (1-9) oder drücke 'q', um zurückzukehren.")

        while True:
            choice = get_key()
            if choice == "q":  # Zurück zum Menü
                return
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(weapons):
                    self.weapon = weapons[index]
                    print(f"Du hast {self.weapon.name} ausgerüstet!")
                    input("Drücke eine Taste, um fortzufahren...")
                    return
            print("Ungültige Eingabe. Bitte wähle eine gültige Waffe oder drücke 'q'.")

    def calculate_damage(self):
        """Berechnet den Gesamtschaden basierend auf Spielerwerten und Waffe."""
        base_damage = random.randint(*self.weapon.damage_range) + self.strength
        if random.random() < (self.crit_chance + self.weapon.crit_chance):  # Kritischer Treffer
            print("Kritischer Treffer!")
            return int(base_damage * (self.crit_multiplier + self.weapon.crit_multiplier))
        return base_damage


class Weapon:
    def __init__(self, name, damage_range, attack_speed, crit_chance=0.0, crit_multiplier=1.0):
        self.name = name
        self.damage_range = damage_range  # Schaden von-bis
        self.attack_speed = attack_speed  # Angriffsgeschwindigkeit in Sekunden
        self.crit_chance = crit_chance  # Kritische Trefferchance
        self.crit_multiplier = crit_multiplier  # Kritischer Schadensmultiplikator


class Enemy:
    def __init__(self, name="Monster", hp=50, weapon=None, xp_reward=50):
        self.name = name
        self.hp = hp
        self.weapon = weapon if weapon else Weapon("Klauen", (3, 8), 1.2)  # Standardwaffe
        self.xp_reward = xp_reward  # XP-Belohnung für das Besiegen


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def display_battle(self):
        os.system('clear')
        print("=== Kampf ===")
        print(f"Spieler: {self.player.hp}/{self.player.max_hp} HP | Gegner: {self.enemy.hp} HP")
        print(f"Spieler-Waffe: {self.player.weapon.name} (Schaden: {self.player.weapon.damage_range}, Geschwindigkeit: {self.player.weapon.attack_speed}s)")
        print(f"Gegner-Waffe: {self.enemy.weapon.name} (Schaden: {self.enemy.weapon.damage_range}, Geschwindigkeit: {self.enemy.weapon.attack_speed}s)")
        print("\nSpieler:")
        print(" O ")
        print("/|\\")
        print("/ \\")
        print("\nGegner:")
        print(" M ")
        print("/|\\")
        print("/ \\")
        print("\nDer Kampf läuft automatisch...")

    def player_attack(self):
        damage = self.player.calculate_damage()
        self.enemy.hp -= damage
        print(f"Du hast {damage} Schaden verursacht!")

    def enemy_attack(self):
        damage = random.randint(*self.enemy.weapon.damage_range)
        self.player.hp -= damage
        print(f"Der Gegner hat {damage} Schaden verursacht!")

    def start(self):
        while self.player.hp > 0 and self.enemy.hp > 0:
            self.display_battle()

            # Spieleraktion
            self.player_attack()
            if self.enemy.hp <= 0:
                print(f"Du hast {self.enemy.name} besiegt!")
                self.player.gain_xp(self.enemy.xp_reward)
                return "sieg"

            time.sleep(self.player.weapon.attack_speed)  # Wartezeit basierend auf Spielerwaffe

            # Gegneraktion
            self.enemy_attack()
            if self.player.hp <= 0:
                print("Du wurdest besiegt!")
                return "niederlage"

            time.sleep(self.enemy.weapon.attack_speed)  # Wartezeit basierend auf Gegnerwaffe


def get_key():
    """
    Capture a single key press without requiring Enter.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


def main():
    width, height = 20, 10
    game_map = GameMap(width, height)
    player = Player(start_position=(1, 1))

    while True:  # Endlosschleife für Neustart nach Niederlage
        player.position = (1, 1)  # Setze Spielerposition zurück
        player.hp = player.max_hp  # Setze HP zurück
        while player.hp > 0:
            game_map.display_map(player.position, player.hp, player.xp, player.xp_to_next_level)
            move = get_key()
            if move in ["w", "a", "s", "d"]:
                player.move(move, game_map)
            elif move == "m":  # Menü öffnen
                player.open_menu()
            elif game_map.check_door(player.position):
                player.position = (1, height // 2)  # Setze Spielerposition zurück
            elif game_map.rooms[game_map.current_room][player.position[1]][player.position[0]] == "X":
                enemy = game_map.enemies.get(player.position)
                if enemy:
                    battle = Battle(player, enemy)
                    result = battle.start()
                    if result == "niederlage":
                        print("Du wurdest besiegt!")
                        break
                    elif result == "sieg":
                        # Entferne den Gegner von der Karte
                        game_map.rooms[game_map.current_room][player.position[1]][player.position[0]] = " "
                        del game_map.enemies[player.position]
        print("Spiel vorbei! Neustart...")


if __name__ == "__main__":
    main()