
import unittest
from clyent import add_subparser_modules
from argparse import ArgumentParser

import mock

def add_hello_parser(subparsers):
    subparser = subparsers.add_parser('hello')
    subparser.add_argument('world')
    subparser.set_defaults(main=mock.Mock())

class Test(unittest.TestCase):

    def test_add_subparser_modules(self):


        parser = ArgumentParser()

        with mock.patch('clyent.iter_entry_points') as iter_entry_points:

            ep = mock.Mock()
            ep.load.return_value = add_hello_parser
            iter_entry_points.return_value = [ep]
            add_subparser_modules(parser, None, 'entry_point_name')

        args = parser.parse_args(['hello', 'world'])
        self.assertEqual(args.world, 'world')

if __name__ == '__main__':
    unittest.main()
