import unittest
from src.map import GameMap

class TestGameMap(unittest.TestCase):
    def setUp(self):
        self.game_map = GameMap()

    def test_map_creation(self):
        self.assertIsNotNone(self.game_map)

    def test_display_map(self):
        expected_output = (
            "IIIIIIII\n"
            "I      I\n"
            "I  +   I\n"
            "I      I\n"
            "IIIIIIII\n"
        )
        self.game_map.create_map()
        self.assertEqual(self.game_map.display_map(), expected_output)

    def test_collision_with_wall(self):
        self.game_map.create_map()
        self.assertTrue(self.game_map.check_collision(0, 0))  # Wall
        self.assertFalse(self.game_map.check_collision(1, 1))  # Empty space

    def test_collision_with_item(self):
        self.game_map.create_map()
        self.assertTrue(self.game_map.check_collision(2, 2))  # Item
        self.assertFalse(self.game_map.check_collision(1, 1))  # Empty space

if __name__ == '__main__':
    unittest.main()