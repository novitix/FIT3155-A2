import unittest
from unittest import TestCase
from st2sa import build_suffix_tree, c2i


class Test(TestCase):
    def test_babcbd(self):
        root = build_suffix_tree('babcbd')
        self.assertEqual(set(map(str, root.atestchildren)), set(['abcbd', 'b', 'cbd', 'd']))
        self.assertEqual(set(map(str, root.children[c2i('b')].atestchildren)), set(['d', 'cbd', 'abcbd']))
        

if __name__ == '__main__':
    unittest.main()