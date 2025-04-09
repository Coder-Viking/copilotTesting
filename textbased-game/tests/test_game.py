import unittest
from src.game import Game
from src.player import Player
from src.map import GameMap

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player()
        self.game_map = GameMap()

    def test_initial_player_position(self):
        self.assertEqual(self.player.position, (0, 0))

    def test_player_movement(self):
        self.player.move("down")
        self.assertEqual(self.player.position, (1, 0))
        self.player.move("right")
        self.assertEqual(self.player.position, (1, 1))

    def test_collision_with_wall(self):
        self.game_map.create_map()
        self.player.position = (1, 0)  # Position next to a wall
        self.player.move("up")  # Attempt to move into a wall
        self.assertEqual(self.player.position, (1, 0))  # Should not move

    def test_collect_item(self):
        self.game_map.create_map()
        self.player.position = (2, 2)  # Position on an item
        item_collected = self.game.collect_item(self.player.position)
        self.assertTrue(item_collected)

if __name__ == '__main__':
    unittest.main()