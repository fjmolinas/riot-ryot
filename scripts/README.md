
## [`ci_test_all.py`](ci_test_all.py)

This script handles executing `compile_and_test_for_board.py` for multiple
boards.

By default it will run on all BOARDs connected to the ci, unless `--boards` is
specified.

## [`ci_aggregate.py`](ci_aggregate.py)

Helper script to aggregate results generate by running `compile_and_test_for_board.py` in a loop.
