"""Build the site once per test session and serve it on a local port."""

import functools
import http.server
import re
import subprocess
import threading
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Literal

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"

# Anything not served by the local test server: Google Fonts, YouTube thumbnails.
OUTSIDE = re.compile(r"^https?://(?!127\.0\.0\.1[:/])")

Scheme = Literal["light", "dark"]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    subprocess.run(["zensical", "build", "--clean", "--strict"], cwd=ROOT, check=True)
    handler = functools.partial(QuietHandler, directory=str(SITE_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


def block_outside_requests(context: BrowserContext) -> None:
    """Outside servers occasionally never answer, and a page then never finishes
    loading. No test checks them, so the browser refuses those requests."""
    context.route(OUTSIDE, lambda route: route.abort())


@pytest.fixture(autouse=True)
def _offline_context(context: BrowserContext) -> None:
    block_outside_requests(context)


@pytest.fixture
def page_with_scheme(
    browser: Browser, base_url: str
) -> Iterator[Callable[[Scheme], Page]]:
    """Open a page in a fresh browser window whose computer prefers light or dark."""
    contexts: list[BrowserContext] = []

    def open_page(color_scheme: Scheme) -> Page:
        context = browser.new_context(base_url=base_url, color_scheme=color_scheme)
        block_outside_requests(context)
        contexts.append(context)
        return context.new_page()

    yield open_page
    for context in contexts:
        context.close()
