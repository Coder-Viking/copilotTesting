class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self.create_map()

    def create_map(self):
        game_map = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append("I")  # Wall
                else:
                    row.append(" ")  # Empty space
            game_map.append(row)
        return game_map

    def display_map(self, player_position):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == player_position:
                    print("#", end="")  # Player
                else:
                    print(self.map[y][x], end="")
            print()  # New line after each row

    def check_collision(self, position):
        x, y = position
        if self.map[y][x] == "I":
            return True  # Collision with wall
        return False  # No collision