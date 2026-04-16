"""Basic UI tests for the Soul Foods Dash app."""
from typing import Generator

import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def app_runner() -> Generator:
    """Provide a Dash app instance for the test browser."""
    app = import_app("app").app
    yield app


def test_header_is_present(dash_duo, app_runner) -> None:
    dash_duo.start_server(app_runner)
    header = dash_duo.find_element("h1")
    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


def test_visualisation_graph_is_present(dash_duo, app_runner) -> None:
    dash_duo.start_server(app_runner)
    graph = dash_duo.find_element("#sales-chart")
    assert graph is not None


def test_region_picker_is_present(dash_duo, app_runner) -> None:
    dash_duo.start_server(app_runner)
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None

