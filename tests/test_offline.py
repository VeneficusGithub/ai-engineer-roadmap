"""Tests only talk to the local test server, never to the internet.

Google Fonts and YouTube thumbnails occasionally never answer; the browser then
waits for them before a page counts as loaded, and a test times out.
"""

from collections.abc import Callable
from urllib.parse import urlparse

from conftest import Scheme
from playwright.sync_api import Page, Request

VIDEO_PAGE = "stages/llm-foundations/"


def outside_requests_that_finished(page: Page, path: str) -> list[str]:
    finished: list[str] = []

    def record(request: Request) -> None:
        if urlparse(request.url).hostname != "127.0.0.1":
            finished.append(request.url)

    page.on("requestfinished", record)
    page.goto(path)
    page.wait_for_load_state("load")
    return finished


def test_test_page_reaches_only_the_local_server(page: Page) -> None:
    assert outside_requests_that_finished(page, VIDEO_PAGE) == []


def test_page_with_colour_scheme_reaches_only_the_local_server(
    page_with_scheme: Callable[[Scheme], Page],
) -> None:
    page = page_with_scheme("dark")
    assert outside_requests_that_finished(page, VIDEO_PAGE) == []
