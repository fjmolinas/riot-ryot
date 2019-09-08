#! /bin/bash

# TODO: use getopt instead of getops

readonly RIOT="$1"; shift
readonly RESULTS="${RIOT}/results"
readonly SCRIPT=${RIOT}/dist/tools/compile_and_test_for_board/compile_and_test_for_board.py
readonly CI_CONNECTED_BOARDS=$(make --no-print-directory -C /builds/boards/ list-boards)

# Parse arguments
while getopts "a:b:" name; do
  case $name in
    a)  a="$OPTARG";;
    b)  b="$OPTARG";;
    ?)  printf "Usage: %s [-a applications] [-b boards] \n" "$0"
        exit 2;;
  esac
done

# Default Boards
if [ -z "$b" ]; then
    readonly BOARDS=${CI_CONNECTED_BOARDS}
else
    readonly BOARDS=$b
fi

test_board_apps() {
  local board="$1"
  local apps="$2"
  ${SCRIPT} "${RIOT}" "${board}" "${RESULTS}" -j0 --clean-after --with-test-only --applications="${apps}"
}

print_results() {
  cd "${RESULTS}" || exit
  for summary in */failuresummary.md; do
    printf "#### %s\n\n" "${summary}"
    cat "${summary}"; printf '\n'
  done > failuresummary.md
  cat failuresummary.md
  cd - || exit
}

main() {
  local results=0
  for board in ${BOARDS}; do
    test_board_apps "${board}" "${a}" || results=1
  done
  print_results
  exit "${results}"
}

main "$@"

