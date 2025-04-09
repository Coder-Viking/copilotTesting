class Player:
    def __init__(self, start_x, start_y):
        self.position = (start_x, start_y)

    def move(self, direction):
        if direction == "up":
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == "left":
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + 1, self.position[1])

    def get_position(self):
        return self.position