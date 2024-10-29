import pytest
from py.xml import html


@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    """modifying the title  of html report,
    using the hook https://github.com/pytest-dev/pytest-html/blob/master/src/pytest_html/hooks.py"""
    report.title = "Delivery Regression Tests"


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    """Add the case to the header grid descriptions added by pytest_runtest_makereport to the html report,
    using the hook https://github.com/pytest-dev/pytest-html/blob/master/src/pytest_html/hooks.py"""
    cells.insert(2, html.th("Description"))


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    """Add the case descriptions added by pytest_runtest_makereport to the html report,
    using the hook https://github.com/pytest-dev/pytest-html/blob/master/src/pytest_html/hooks.py"""
    custom_description = getattr(report, "custom_description", "")
    cells.insert(2, html.td(custom_description))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """For each test case, we add a description. Description can come from a decorator or test case comment"""

    # We need to yield, to allow to run first the implementation of
    # https://github.com/pytest-dev/pytest-html/blob/master/src/pytest_html/plugin.py
    outcome = yield
    # this is the output that is seen end of test case
    report = outcome.get_result()

    # finding if we have the decorator(annotation) of the function
    meta_description = getattr(item.function, "meta_description", None)
    if meta_description is not None:
        description = meta_description.get("description")
    else:
        # if we don't have the annotation, we try to use the documentation of the function
        description = item.function.__doc__
    report.custom_description = description
