#! /bin/bash

# TODO: shellcheck

readonly RIOT="$1"; shift
readonly RESULTS="${RIOT}/results"
readonly SCRIPT=${RIOT}/dist/tools/compile_and_test_for_board/compile_and_test_for_board.py
# Handle as array
readonly CI_CONNECTED_BOARDS=$(make --no-print-directory -C /builds/boards/ list-boards)
# Handle as array
readonly BOARDS=${@:-${CI_CONNECTED_BOARDS}}

test_board() {
  local board="$1"
  ${SCRIPT} "${RIOT}" "${board}" "${RESULTS}" -j0 --clean-after --with-test-only
}

print_results() {
  cd "${RESULTS}" || exit
  for summary in */failuresummary.md; do
    printf "#### %s\n\n" "${summary}"
    cat "${summary}"; printf '\n'
  done > failuresummay.md
  cat failuresummary.md
  cd - || exit
}

main() {
  local results=0
  for board in ${BOARDS}; do
    test_board "${board}" || results=1
  done
  print_results
  exit "${results}"
}

main "$@"
