import pytest
import sys

from tests_selector.pytest.normal_phase_plugin import NormalPhasePlugin
from tests_selector.utils.db import get_selected_tests


def main():
    test_set = set(get_selected_tests())
    pytest_params = sys.argv[1:] if len(sys.argv) > 1 else []
    pytest.main(pytest_params, plugins=[NormalPhasePlugin(test_set)])


if __name__ == "__main__":
    main()
