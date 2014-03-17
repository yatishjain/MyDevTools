__author__ = 'ShayWeiss'

import os
import string
import random
import unittest

import string_utils

class TestFileParsers(unittest.TestCase):
    # is_palindrome tests
    def test_one_letter_is_a_palindrom(self):
        random_char = random.choice([c for c in string.ascii_lowercase])
        self.assertTrue(string_utils.is_palindrome(random_char))

    def test_a_palindrome_is_a_palindrome_regardless_of_spaces_and_case(self):
        s = 'Rats live on no evil sta r'
        self.assertTrue(string_utils.is_palindrome(s))

    def test_unless_we_care_about_case(self):
        s = 'Rats live on no evil sta r'
        self.assertFalse(string_utils.is_palindrome(s, ignore_case=False))

    def test_or_spaces(self):
        s = 'Rats live on no evil sta r'
        self.assertFalse(string_utils.is_palindrome(s, ignore_spaces=False))

    def test_not_a_palindrome_is_not_a_palindrome(self):
        s = 'Rats live on no evil sta G'
        self.assertFalse(string_utils.is_palindrome(s, ignore_spaces=False))


    def test_all_substrings(self):
        s = 'abc'
        substrings = set(['a', 'b', 'c', 'ab', 'bc', 'abc'])
        self.assertEqual(substrings, string_utils.all_substrings(s))


    def test_count_occurrences_with_overlap(self):
        # the usual count method for string counts without overlaps:
        self.assertEqual(1, 'aaa'.count('aa'))

        # and sometimes we need with overlaps:
        self.assertEqual(2, string_utils.count_occurrences_with_overlap('aaa', 'aa'))


    def test_find_subsequence_returns_true_is_subsequence_exist(self):
        self.assertTrue(string_utils.find_subsequance('f11o22 3 4 o 32590', 'foo'))

    def test_find_subsequence_returns_false_is_subsequence_doesnt_exist(self):
        self.assertFalse(string_utils.find_subsequance('f11o22 3 4 o 32590', 'bar'))


    def test_find_subsequence_efficient_returns_true_is_subsequence_exist(self):
        self.assertTrue(string_utils.find_subsequance_efficient('f11o22 3 4 o 32590', 'foo'))

    def test_find_subsequence_efficient_returns_false_is_subsequence_doesnt_exist(self):
        self.assertFalse(string_utils.find_subsequance_efficient('f11o22 3 4 o 32590', 'bar'))


    def test_camelcase(self):
        self.assertEqual('A Game Of Thrones', string_utils.camelcase('a game of thrones'))

    def test_camelcase_with_exceptions(self):
        self.assertEqual('A Game of Thrones', string_utils.camelcase('a game of thrones', exceptions=['of']))

    def test_camelcase_with_exceptions_first_word_is_still_capitalized(self):
        self.assertEqual('A Game of a Thrones', string_utils.camelcase('a game of a thrones', exceptions=['a', 'of']))


    def test_turn_to_valid_filename(self):
        non_valid_filename = 'this_is-a n!@#$%^&*on() valid filename.ext'
        self.assertEqual('this_is-a non valid filename.ext', string_utils.turn_to_valid_filename(non_valid_filename))

    def test_turn_to_valid_filename_can_accept_exceptions(self):
        non_valid_filename = 'this_is-a n!@#$%^&*on() valid filename.ext'
        self.assertEqual('this_is-a non() valid filename.ext', string_utils.turn_to_valid_filename(non_valid_filename, accept_as_valid='()'))

if __name__ == '__main__':
    unittest.main()
