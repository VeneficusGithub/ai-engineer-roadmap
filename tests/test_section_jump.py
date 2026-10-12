"""Jumping to a section keeps its heading and first item clear of the sticky bars."""

import pytest
from playwright.sync_api import Locator, Page, expect

SECTIONS = {
    "leren": "ul a.rm-item",
    "interviewvragen": "details.interview > summary",
}


def wait_until_scrolled(page: Page) -> None:
    page.wait_for_function(
        """() => new Promise(resolve => {
            let last = scrollY;
            setTimeout(() => resolve(scrollY === last), 300);
        })""",
        polling=350,
    )


def top(locator: Locator) -> float:
    box = locator.bounding_box()
    assert box is not None
    return box["y"]


def bottom(locator: Locator) -> float:
    box = locator.bounding_box()
    assert box is not None
    return box["y"] + box["height"]


def text_top(page: Page, section: str) -> float:
    """Where the heading's visible text starts (its box may hold extra space)."""
    value = page.evaluate(
        """id => {
            const range = document.createRange();
            range.selectNodeContents(document.getElementById(id).firstChild);
            return range.getBoundingClientRect().top;
        }""",
        section,
    )
    assert isinstance(value, (int, float))
    return float(value)


def assert_clear_of_toolbar(page: Page, section: str) -> None:
    wait_until_scrolled(page)
    toolbar_bottom = bottom(page.locator(".rm-toolbar"))
    heading = text_top(page, section)
    first_item = page.locator(f"h2#{section} ~ {SECTIONS[section]}").first
    assert heading >= toolbar_bottom
    assert top(first_item) >= toolbar_bottom
    assert heading - toolbar_bottom < 80, "jumped too far: big gap above heading"


@pytest.mark.parametrize("section", SECTIONS)
def test_contents_link_shows_section_heading_and_first_item(
    page: Page, section: str
) -> None:
    page.set_viewport_size({"width": 1440, "height": 700})
    page.goto("stages/llm-foundations/")
    page.locator(f'.md-sidebar--secondary a[href="#{section}"]').click()
    assert_clear_of_toolbar(page, section)
    active = page.locator(".md-sidebar--secondary a.md-nav__link--active")
    expect(active).to_have_attribute("href", f"#{section}")


def test_last_item_before_a_section_stays_clickable(page: Page) -> None:
    page.set_viewport_size({"width": 1440, "height": 700})
    page.goto("stages/llm-foundations/")
    checkbox = page.locator(".rm-check").last
    checkbox.scroll_into_view_if_needed()
    checkbox.click()
    expect(checkbox).to_be_checked()


@pytest.mark.parametrize("section", SECTIONS)
def test_section_address_shows_heading_on_a_phone(page: Page, section: str) -> None:
    page.set_viewport_size({"width": 390, "height": 700})
    page.goto("stages/mcp-skills/")
    page.goto(f"stages/mcp-skills/#{section}")
    assert_clear_of_toolbar(page, section)
