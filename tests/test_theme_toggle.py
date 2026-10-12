"""The theme button switches between light and dark with a single click."""

from collections.abc import Callable

import pytest
from conftest import Scheme
from playwright.sync_api import Page, expect

LIGHT, DARK = "default", "slate"
TOGGLE = 'form[data-md-component="palette"] label:not([hidden])'


def scheme_of(page: Page) -> str | None:
    return page.locator("body").get_attribute("data-md-color-scheme")


def settled(page: Page) -> None:
    """Wait until the theme script has applied the stored or default palette."""
    page.wait_for_load_state("load")
    page.wait_for_timeout(500)


def test_toggle_has_two_settings(page: Page) -> None:
    page.goto("")
    expect(page.locator('form[data-md-component="palette"] input')).to_have_count(2)


@pytest.mark.parametrize(("os_scheme", "start"), [("light", LIGHT), ("dark", DARK)])
def test_first_visit_follows_the_computer_setting(
    page_with_scheme: Callable[[Scheme], Page], os_scheme: Scheme, start: str
) -> None:
    page = page_with_scheme(os_scheme)
    page.goto("")
    settled(page)
    assert scheme_of(page) == start


def test_one_click_switches_theme_and_the_choice_is_kept(
    page_with_scheme: Callable[[Scheme], Page],
) -> None:
    page = page_with_scheme("light")
    page.goto("")
    settled(page)
    page.locator(TOGGLE).click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", DARK)
    page.reload()
    settled(page)
    assert scheme_of(page) == DARK
    page.locator(TOGGLE).click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", LIGHT)


def test_pages_load_no_extra_theme_script(page: Page) -> None:
    """The theme needs no help from our own scripts to remember a choice."""
    page.goto("")
    expect(page.locator('head script[src*="theme-choice"]')).to_have_count(0)
