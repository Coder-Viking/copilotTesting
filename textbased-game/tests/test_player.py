import unittest
from src.player import Player
from src.map import GameMap

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.game_map = GameMap()
        self.player = Player(self.game_map)

    def test_initial_position(self):
        self.assertEqual(self.player.position, (0, 0))

    def test_move_up(self):
        self.player.move("up")
        self.assertEqual(self.player.position, (0, -1))

    def test_move_down(self):
        self.player.move("down")
        self.assertEqual(self.player.position, (0, 1))

    def test_move_left(self):
        self.player.move("left")
        self.assertEqual(self.player.position, (-1, 0))

    def test_move_right(self):
        self.player.move("right")
        self.assertEqual(self.player.position, (1, 0))

    def test_move_into_wall(self):
        self.game_map.set_wall(0, -1)  # Set a wall above the player
        self.player.move("up")
        self.assertEqual(self.player.position, (0, 0))  # Should not move

    def test_collect_item(self):
        self.game_map.set_item(1, 0, "+")  # Set an item to the right
        self.player.move("right")
        self.assertIn("+", self.player.inventory)  # Player should collect the item

if __name__ == '__main__':
    unittest.main()