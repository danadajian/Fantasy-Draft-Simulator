import unittest
from main.App import position_ignore, position_count, valid_choice


class GetPlayersTests(unittest.TestCase):

    def test_position_ignore(self):
        test_list = ['Aaron Rodgers', 'Saquon Barkley', 'Odell Beckham Jr', 'Travis Kelce', 'Seahawks D/ST',
                     'Justin Tucker']
        pos_list = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']
        expected_lists = []
        actual_lists = []
        for pos in pos_list:
            n = pos_list.index(pos)
            expected_list = test_list[0:n] + test_list[n + 1:]
            actual_list = position_ignore(test_list, pos)
            expected_lists.append(expected_list)
            actual_lists.append(actual_list)
        self.assertEqual(actual_lists, expected_lists)

    def test_position_count(self):
        test_list = ['Saquon Barkley', 'Odell Beckham Jr', 'Julio Jones', 'Travis Kelce', 'Zach Ertz', 'George Kittle',
                     'Packers D/ST', 'Ravens D/ST', 'Jaguars D/ST', 'Seahawks D/ST', 'Justin Tucker', 'Robbie Gould',
                     'Harrison Butker', 'Jake Elliot', 'Matt Bryant']
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
