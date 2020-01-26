"""
Pytest configuration
"""


def pytest_addoption(parser):
    """
    Add support for recording of expected test results.
    """
    parser.addoption("--record", action="store_true")


def pytest_generate_tests(metafunc):
    """
    Save the record value to tests needing it.
    """
    option_value = metafunc.config.option.record
    if "record" in metafunc.fixturenames:
        metafunc.parametrize("record", [option_value])
