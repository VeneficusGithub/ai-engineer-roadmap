"""The theme button switches between light and dark with a single click."""

import json
from typing import Literal

import pytest
from playwright.sync_api import Browser, Page, expect

LIGHT, DARK = "default", "slate"
TOGGLE = 'form[data-md-component="palette"] label:not([hidden])'
Scheme = Literal["light", "dark"]


def scheme_of(page: Page) -> str | None:
    return page.locator("body").get_attribute("data-md-color-scheme")


def settled(page: Page) -> None:
    """Wait until the theme script has applied the stored or default palette."""
    page.wait_for_load_state("load")
    page.wait_for_timeout(500)


def new_page(browser: Browser, base_url: str, os_scheme: Scheme) -> Page:
    context = browser.new_context(base_url=base_url, color_scheme=os_scheme)
    return context.new_page()


def test_toggle_has_two_settings(page: Page) -> None:
    page.goto("")
    expect(page.locator('form[data-md-component="palette"] input')).to_have_count(2)


@pytest.mark.parametrize(("os_scheme", "start"), [("light", LIGHT), ("dark", DARK)])
def test_first_visit_follows_the_computer_setting(
    browser: Browser, base_url: str, os_scheme: Scheme, start: str
) -> None:
    page = new_page(browser, base_url, os_scheme)
    page.goto("")
    settled(page)
    assert scheme_of(page) == start


def test_one_click_switches_theme_and_the_choice_is_kept(
    browser: Browser, base_url: str
) -> None:
    page = new_page(browser, base_url, "light")
    page.goto("")
    settled(page)
    page.locator(TOGGLE).click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", DARK)
    page.reload()
    settled(page)
    assert scheme_of(page) == DARK
    page.locator(TOGGLE).click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", LIGHT)


def stored(index: int, media: str, scheme: str) -> str:
    color = {"media": media, "scheme": scheme, "primary": "custom", "accent": "custom"}
    return json.dumps({"index": index, "color": color})


# Choices saved by the old three-setting button: 0 = system, 1 = light, 2 = dark.
OLD_CHOICES = [
    (
        "old light choice",
        stored(1, "(prefers-color-scheme: light)", LIGHT),
        "dark",
        LIGHT,
    ),
    ("old dark choice", stored(2, "(prefers-color-scheme: dark)", DARK), "light", DARK),
    ("old system choice", stored(0, "(prefers-color-scheme)", LIGHT), "dark", DARK),
]


@pytest.mark.parametrize(
    ("value", "os_scheme", "expected"),
    [case[1:] for case in OLD_CHOICES],
    ids=[case[0] for case in OLD_CHOICES],
)
def test_choice_saved_by_the_old_button_is_kept(
    browser: Browser, base_url: str, value: str, os_scheme: Scheme, expected: str
) -> None:
    page = new_page(browser, base_url, os_scheme)
    page.goto("")
    key = page.evaluate("__md_scope.pathname") + ".__palette"
    page.evaluate("([key, value]) => localStorage.setItem(key, value)", [key, value])
    page.reload()
    settled(page)
    assert scheme_of(page) == expected
