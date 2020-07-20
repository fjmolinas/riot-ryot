#! /usr/bin/env python3

"""
usage: ci_aggregate.py [-h] boards [result_directory]

positional arguments:
  boards            List of board to test
  result_directory  Result directory (default: None)

optional arguments:
  -h, --help        show this help message and exit
"""

import os
import re
import argparse


def list_from_string(list_str=None):
    """Get list of items from `list_str`

    >>> list_from_string(None)
    []
    >>> list_from_string("")
    []
    >>> list_from_string("  ")
    []
    >>> list_from_string("a")
    ['a']
    >>> list_from_string("a  ")
    ['a']
    >>> list_from_string("a b  c")
    ['a', 'b', 'c']
    """
    value = (list_str or '').split(' ')
    return [v for v in value if v]


def _board_results_in_dir(dir):
    return next(os.walk(os.path.abspath(dir)))[1]


def _append_board_to_test_location(text, board):
    return re.sub(r'(\[.*\])(\()(.*\))', r"\1({}/\3".format(board), text)


def aggregate_results(results_dir, boards, echo=True):
    """Aggregate all results for boards presents in results_dir"""
    if boards is None:
        boards = _board_results_in_dir(results_dir)
    failuresummary = os.path.abspath(os.path.join(results_dir,
                                                  'failuresummary.md'))
    with open(failuresummary, "w+") as failuresummary_file:
        for board in boards:
            boards_result_dir = os.path.abspath(
                                    os.path.join(
                                        results_dir,
                                        '{}/failuresummary.md'.format(board)))
            try:
                with open(boards_result_dir) as board_failuresummary:
                    separator = "\n### {}/failuresummary\n\n".format(board)
                    failuresummary_file.write(separator)
                    for line in board_failuresummary:
                        line = _append_board_to_test_location(line, board)
                        failuresummary_file.write(line)
            except FileNotFoundError:
                print("results for {} not found in results_dir {}"
                      .format(board, results_dir))
    if echo is True:
        with open(failuresummary, "r") as failuresummary_file:
            print(failuresummary_file.read())


PARSER = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('result_directory',
                    help='Result directory')
PARSER.add_argument('--boards',
                    type=list_from_string,
                    default=None,
                    help='List of board to test')


if __name__ == '__main__':
    args = PARSER.parse_args()
    aggregate_results(results_dir=args.result_directory, boards=args.boards)
