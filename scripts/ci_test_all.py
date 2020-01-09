#! /usr/bin/env python3

"""
This script handled executing \'compile_and_test_for_board\' for multiple
boards generating results.

It inherits the documentation for \'compile_and_test_for_board\' arguments
replacing `board` positional argument by an optional --boards argument which
replaces \'board\' positional argument by every BOARD in boards.

Example
-------

By default it should be run as

    ./ci_test_all.py path_to_riot_directory [results]


Usage
-----


```
usage: compile_and_test_for_board.py [-h] [--applications APPLICATIONS]
                                     [--applications-exclude APPLICATIONS_EXCLUDE]
                                     [--no-test] [--with-test-only]
                                     [--loglevel {debug,info,warning,error,fatal,critical}]
                                     [--incremental] [--clean-after]
                                     [--compile-targets COMPILE_TARGETS]
                                     [--flash-targets FLASH_TARGETS]
                                     [--test-targets TEST_TARGETS]
                                     [--test-available-targets TEST_AVAILABLE_TARGETS]
                                     [--jobs JOBS]
                                     riot_directory board [result_directory]

positional arguments:
  riot_directory        RIOT directory to test
  result_directory      Result directory (default: results)

optional arguments:
  -h, --help            show this help message and exit
  --boards              List of boards to test.
  --applications APPLICATIONS
                        List of applications to test, overwrites default
                        configuration of testing all applications (default:
                        None)
  --applications-exclude APPLICATIONS_EXCLUDE
                        List of applications to exclude from tested
                        applications. Also applied after "--applications".
                        (default: None)
  --no-test             Disable executing tests (default: False)
  --with-test-only      Only compile applications that have a test (default:
                        False)
  --loglevel {debug,info,warning,error,fatal,critical}
                        Python logger log level (default: info)
  --incremental         Do not rerun successful compilation and tests
                        (default: False)
  --clean-after         Clean after running each test (default: False)
  --compile-targets COMPILE_TARGETS
                        List of make targets to compile (default: clean all)
  --flash-targets FLASH_TARGETS
                        List of make targets to flash (default: flash-only)
  --test-targets TEST_TARGETS
                        List of make targets to run test (default: test)
  --test-available-targets TEST_AVAILABLE_TARGETS
                        List of make targets to know if a test is present
                        (default: test/available)
  --jobs JOBS, -j JOBS  Parallel building (0 means not limit, like '--jobs')
                        (default: None)
```
"""

import os
import sys
import argparse
import subprocess
import logging
import compile_and_test_for_board
import ci_aggregate


def _ci_connected_boards(riot_directory):
    """Get list of boards currently connected to the ci"""
    if os.environ['USER'] == 'ci':
        cwd_dir = '/builds/boards'
    else:
        cwd_dir = os.path.join(riot_directory, 'examples/hello-wolrd')
    cmd = [
        'make',
        'list-boards',
        '--no-print-directory',
    ]
    boards = subprocess.check_output(cmd, cwd=cwd_dir)
    boards = boards.decode('utf-8', errors='replace')
    return boards.split()


def _get_boards(args):
    """Returns boards list"""
    boards = args.boards
    if args.boards == ['ci-connected-boards']:
        boards = _ci_connected_boards(args.riot_directory)
    else:
        boards = args.boards
    del args.boards
    return boards


def exec_compile_and_test_for_board(board, args):
    """Execute \'compile_and_test_for_board\' for one BOARD"""
    setattr(args, 'board', board)
    try:
        compile_and_test_for_board.main(args)
    except SystemExit:
        logging.info("Ignoring \'compile_and_test_for_board\' system exit")


PARSER = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[compile_and_test_for_board.PARSER],
    conflict_handler='resolve')
PARSER.add_argument('--boards',
                    type=compile_and_test_for_board.list_from_string,
                    default='ci-connected-boards',
                    help='List of board to test')
# Remove Parent board positional argument
PARSER._actions[2].container._remove_action(PARSER._actions[2])


def test_boards():
    """For one board, compile all examples and tests and run test on board."""
    args = PARSER.parse_args()
    boards = _get_boards(args)

    for board in boards:
        exec_compile_and_test_for_board(board, args)
    ci_aggregate.aggregate_results(args.result_directory, boards)


if __name__ == '__main__':
    test_boards()
