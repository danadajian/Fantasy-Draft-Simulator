import unittest
from main.App import position_ignore, position_count


class GetPlayersTests(unittest.TestCase):

    def test_position_ignore(self):
        test_list = ['Aaron Rodgers', 'Saquon Barkley', 'Odell Beckham Jr', 'Travis Kelce', 'Seahawks D/ST']
        pos_list = ['QB', 'RB', 'WR', 'TE', 'DST']
        expected_lists = []
        actual_lists = []
        for pos in pos_list:
            n = pos_list.index(pos)
            expected_list = test_list[0:n] + test_list[n+1:]
            actual_list = position_ignore(test_list, pos)
            expected_lists.append(expected_list)
            actual_lists.append(actual_list)
        self.assertEqual(actual_lists, expected_lists)

    def test_position_count(self):
        list_a = ['a', 'b', 'c', 'd', 'e']
        list_b = ['b', 'd']
        self.assertEqual(position_count(list_a, list_b), 2)

