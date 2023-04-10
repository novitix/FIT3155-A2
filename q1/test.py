import unittest
from unittest import TestCase
from st2sa import build_suffix_tree, c2i


class Test(TestCase):
    def test_babcbd(self):
        TEST_STRING = 'babcbd'
        root = build_suffix_tree(TEST_STRING)
        self.assertEqual(set(map(str, root.atestchildren)), set(['abcbd', 'b', 'cbd', 'd']))
        self.assertEqual(set(map(str, root.children[c2i('b')].atestchildren)), set(['d', 'cbd', 'abcbd']))
        
    def test_babcbca_suf_links(self):
        TEST_STRING = 'babcbca'
        root = build_suffix_tree(TEST_STRING)
        self.assertEqual(set(map(str, root.atestchildren)), set(['c', 'abcbca', 'b']))
        self.assertEqual(set(map(str, root.children[c2i('c')].atestchildren)), set(['a', 'bca']))
        self.assertEqual(set(map(str, root.children[c2i('b')].atestchildren)), set(['abcbca', 'c']))
        self.assertEqual(set(map(str, root.children[c2i('b')].children[c2i('c')].atestchildren)), set(['a', 'bca']))

if __name__ == '__main__':
    unittest.main()