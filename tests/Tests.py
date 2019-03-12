import unittest
from main.DraftSimulator import *


class GetPlayersTests(unittest.TestCase):

    def test_http_response_200(self):
        self.assertEqual(str(request), '<Response [200]>')

    def test_player_names_valid(self):
        for player in top300List:
            self.assertTrue(player.isalpha() or any(x in player for x in [' ', '.', "'", 'D/ST']))

    def test_pos_names_valid(self):
        for pos in top300List:
            if not pos != 'D/ST':
                self.assertTrue(pos.isalpha())
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_position_count(self):
        test_list = ['Saquon Barkley', 'Odell Beckham Jr', 'Julio Jones', 'Travis Kelce', 'Zach Ertz', 'George Kittle',
                     'Packers D/ST', 'Ravens D/ST', 'Jaguars D/ST', 'Seahawks D/ST', 'Justin Tucker', 'Robbie Gould',
                     'Harrison Butker', 'Matt Prater', 'Matt Bryant']
        pos_list = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']
        expected_counts = []
        actual_counts = []
        for pos in pos_list:
            n = pos_list.index(pos)
            expected_count = n
            actual_count = position_count(test_list, pos)
            expected_counts.append(expected_count)
            actual_counts.append(actual_count)
        self.assertEqual(expected_counts, actual_counts)

    def test_valid_choice(self):
        test_team = ['Saquon Barkley', 'Odell Beckham Jr', 'Julio Jones', 'Travis Kelce', 'Packers D/ST']
        self.assertTrue(valid_choice('Aaron Rodgers', test_team))
        self.assertTrue(valid_choice('Adam Thielen', test_team))
        self.assertFalse(valid_choice('Jaguars D/ST', test_team))
        self.assertFalse(valid_choice(None, test_team))
