import unittest
from main.GetPlayers import *


class GetPlayersTests(unittest.TestCase):

    def http_response_200(self):
        self.assertEqual(str(request), '<Response [200]>')

    def player_names_valid(self):
        for player in top300List:
            self.assertTrue(player.isalpha() or any(x in player for x in [' ', '.', "'", 'D/ST']))

    def pos_names_valid(self):
        for pos in top300List:
            if not pos != 'D/ST':
                self.assertTrue(pos.isalpha())
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
