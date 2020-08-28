import os
import subprocess
import sys
from tests_selector.utils.common import (
    split_changes,
    tests_from_changed_srcfiles,
    tests_from_changed_testfiles,
    read_newly_added_tests,
    file_diff_dict_branch,
    run_tests_and_update_db,
    COVERAGE_CONF_FILE_NAME,
    DB_FILE_NAME,
)
from tests_selector.utils.git import changed_files_branch
from tests_selector.utils.db import save_selected_tests

PYTEST_PARAMS = sys.argv[1:] if len(sys.argv) > 1 else []


def get_tests_from_branch_changes(diff_dict_test, diff_dict_src, testfiles, srcfiles):
    (
        src_test_set,
        src_changed_lines_dict,
        src_new_line_map_dict,
    ) = tests_from_changed_srcfiles(diff_dict_src, srcfiles)

    (
        test_test_set,
        test_changed_lines_dict,
        test_new_line_map_dict,
    ) = tests_from_changed_testfiles(diff_dict_test, testfiles)

    test_set = test_test_set.union(src_test_set)

    update_tuple = (
        test_changed_lines_dict,
        test_new_line_map_dict,
        src_changed_lines_dict,
        src_new_line_map_dict,
    )
    return test_set, update_tuple


def main():
    if not os.path.isfile(COVERAGE_CONF_FILE_NAME) or not os.path.isfile(DB_FILE_NAME):
        print("Run tests_selector_init first")
        exit(1)

    changed_files = changed_files_branch()
    changed_test_files, changed_src_files = split_changes(changed_files)
    diff_dict_src = file_diff_dict_branch(changed_src_files)
    diff_dict_test = file_diff_dict_branch(changed_test_files)
    new_tests = read_newly_added_tests()
    print(f"found {len(changed_test_files)} changed test files")
    print(f"found {len(changed_src_files)} changed src files")
    print(f"found {len(new_tests)} newly added tests")

    changes_test_set, update_tuple = get_tests_from_branch_changes(
        diff_dict_test, diff_dict_src, changed_test_files, changed_src_files
    )
    final_test_set = changes_test_set.union(new_tests)
    print(f"found {len(final_test_set)} tests to execute")

    if len(final_test_set) > 0:
        save_selected_tests(final_test_set)
        run_tests_and_update_db(update_tuple, PYTEST_PARAMS)


if __name__ == "__main__":
    main()
